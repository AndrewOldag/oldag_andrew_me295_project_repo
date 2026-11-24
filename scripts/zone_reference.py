"""Real reference set for the particle-path zone check, report-only (spec 2026-11-23_zone-check-real-reference, task c035;
docs/proposals/2026-11-23_zone-reference.md).

synthetic   c034 freeze v4 set (18 clean, 90 shifted, 9 repaired) with the residual split into common mode and shape.
            Synthetic shape threshold by the R4 rule on the clean tracks (this test only). Writes synthetic.csv, synthetic.md
sample      24 accepted c027 windows by the proposal's rule (seed 20261123). Writes sample.csv
extend      126 more (inbox 33: seed 20261124, proportional strata, at most 2 per root). Appends to sample.csv
overlays    Per sampled window: first, middle and last frame read from storage (read-only, one window at a time, raw
            frames deleted after use) with midline, midline tip, tracked chain (first point marked) and predicted
            particle positions. PNGs, index.html and labels.csv (blank rows appended for new windows, existing labels kept) in staging/c035_overlays/ (git-ignored). The
            index shows no residual value or flag. A rerun skips windows with a PNG
thresholds  Proposal step 5 on Andrew's labels: 99.5th percentile x 1.5 (2 significant figures, rounded up) of
            `pp_shape_rel` and `pp_common_rel` over the clean windows. Writes reference.csv and thresholds.md; the
            values wait for Andrew's approval and are not written to config

  python scripts/zone_reference.py synthetic --cache <freeze v4 track cache>
  python scripts/zone_reference.py sample --cache <c027 track cache>
  python scripts/zone_reference.py extend --cache <c027 track cache>
  python scripts/zone_reference.py overlays --cache <c027 track cache> --host <storage ssh alias> --data <movie root>
  python scripts/zone_reference.py thresholds --cache <c027 track cache>
"""
import argparse
import collections
import csv
import html
import json
import re
import shlex
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from checker.zone_checks import (SUBSTEPS, _profile, _velocity, particle_path, shifted_fields,  # noqa: E402
                                 tip_frame_positions)
from integrity_thresholds import LABELS, round_up_2sf, track_set  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from zone_checks import SHIFTS, WINDOWS, track_file  # noqa: E402

OUT = ROOT / "results" / "2026-11-23_zone_reference"
OVERLAYS = ROOT / "staging" / "c035_overlays"
ZOOM_PX = 120                                    # half width of the tip-region panels
MOVED_VELOCITY = np.array([0.5, 0.3]) / 90.0     # px/s, (row, col): scripts/remote/real_moved.py VELOCITY
MANIFEST = ROOT / "manifest" / "root_manifest.csv"
SEED = 20261123
SEED_EXTRA = 20261124                            # inbox 33 extension
EXTRA = 126
STRATA = {"control": 5, "control then control": 4, "mannitol": 5, "mannitol then control": 5,
          "mannitol then mannitol": 5}
SAMPLE_COLS = ["window", "root", "condition", "order", "pool", "draw"]
KEYS = ("pp_rms_px", "pp_common_px", "pp_shape_rms_px", "pp_rms_rel", "pp_common_rel", "pp_shape_rel")


def pp_values(rec, fields=None):
    return particle_path(rec, fields=fields).values


def _fmt(x):
    return "" if x is None else (f"{x:.6g}" if isinstance(x, float) else x)


def _write_csv(path, rows, cols):
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: _fmt(r.get(k)) for k in cols})


def r4(v):
    return float(round_up_2sf(1.5 * np.percentile(np.asarray(v, float), 99.5)))


def synthetic(a):
    cache = Path(a.cache)
    labels = json.loads(LABELS.read_text())["labels"]
    rows = []
    for rod, path in track_set(cache):
        lab = labels[rod]
        rec = from_tracker_npz(path)
        base = {"rod": rod, "kind": lab["kind"], "seed": lab["seed"], "track": path.name}
        rows.append(base | {"class": lab["class"], "shift_px": 0} | pp_values(rec))
        if lab["class"] == "accept_clean" and lab["kind"] != "v3_still":
            for d in SHIFTS:
                rows.append(base | {"class": "shifted", "shift_px": d} | pp_values(rec, shifted_fields(rec, d)))
    OUT.mkdir(parents=True, exist_ok=True)
    _write_csv(OUT / "synthetic.csv", rows, ["rod", "class", "kind", "seed", "shift_px", "track", *KEYS])
    clean = [r for r in rows if r["class"] == "accept_clean"]
    th = r4([r["pp_shape_rel"] for r in clean if r["pp_shape_rel"] is not None])

    def line(name, d, sub):
        comp = [r for r in sub if r["pp_shape_rel"] is not None]
        flagged = sum(r["pp_shape_rel"] > th for r in comp)
        share = [r["pp_common_px"] ** 2 / r["pp_rms_px"] ** 2 for r in sub if r["pp_rms_px"]]
        sh = [r["pp_shape_rel"] for r in comp]
        rng = f"{min(sh):.3g}-{max(sh):.3g}" if sh else "-"
        med = f"{np.median(share):.2f}" if share else "-"
        return f"| {name} | {d} | {len(sub)} | {flagged} of {len(comp)} | {rng} | {med} |", flagged, len(comp)

    lines = ["# Synthetic re-run with the residual split (freeze v4, seeds 26-28)", "",
             f"Synthetic shape threshold (R4 rule on the 18 clean tracks, this test only): `pp_shape_rel` {th:g}", "",
             "| Set | Shift px | Records | shape flags | `pp_shape_rel` range | common share of squared residual (median) |",
             "| :-- | --: | --: | --: | :-- | --: |"]
    lines.append(line("accept_clean (threshold set)", 0, clean)[0])
    caught = {}
    for d in SHIFTS:
        ln, f, n = line("shifted", f"{d:+d}", [r for r in rows if r["class"] == "shifted" and r["shift_px"] == d])
        lines.append(ln)
        caught[d] = (f, n)
    lines.append(line("accept_repaired (not in the threshold set)", 0,
                      [r for r in rows if r["class"] == "accept_repaired"])[0])
    ok = all(f == n == 15 for f, n in caught.values())
    lines += ["", f"Stop rule (proposal): shape flags 15 of 15 at every shift: {'met' if ok else 'NOT met'}", ""]
    (OUT / "synthetic.md").write_text("\n".join(lines))
    print(json.dumps({"pp_shape_rel_threshold": th, "caught": {str(k): v for k, v in caught.items()},
                      "stop_rule_met": ok}))


def _hours(window):
    a, b = window.rsplit("__w", 1)[1].split("-")
    return float(a), float(b)


def _pool(cache):
    """Proposal step 2 pool by condition: accepted, include yes, usable hours, base track with both relative values."""
    man = {r["id"]: r for r in csv.DictReader(open(MANIFEST))}
    pool = collections.defaultdict(list)
    for r in csv.DictReader(open(WINDOWS)):
        if r["integrated"] != "accepted" or r["condition"] not in STRATA:
            continue
        m = man.get(r["root"])
        h0, h1 = _hours(r["window"])
        if m is None or m["include"] != "yes" or h0 < float(m["usable_from_h"]) or h1 > float(m["usable_to_h"]):
            continue
        p = track_file(cache, r["window"], "st1")
        if p is None:
            continue
        v = pp_values(from_tracker_npz(p, root_id=r["window"]))
        if v["pp_shape_rel"] is None or v["pp_common_rel"] is None:
            continue
        pool[r["condition"]].append(r)
    return pool


def _draw(pool, quota, rng, taken, per_root):
    """Conditions in sorted order; each pool sorted by window id, permuted, taken in that order, skipping windows in
    `taken` and roots that already hold `per_root` windows, until the stratum's quota is met (or the pool runs out)."""
    count = collections.Counter(r["root"] for r in taken.values())
    rows = []
    for cond in sorted(quota):
        cands = sorted(pool[cond], key=lambda r: r["window"])
        n = 0
        for i in rng.permutation(len(cands)):
            if n == quota[cond]:
                break
            r = cands[i]
            if r["window"] in taken or count[r["root"]] >= per_root:
                continue
            count[r["root"]] += 1
            n += 1
            rows.append({"window": r["window"], "root": r["root"], "condition": cond, "order": n,
                         "pool": len(cands)})
    return rows


def allocate(total, sizes):
    """Largest-remainder allocation of `total` in proportion to `sizes`; ties to the key first in sorted order."""
    keys = sorted(sizes)
    n = sum(sizes.values())
    exact = {k: total * sizes[k] / n for k in keys}
    out = {k: int(np.floor(exact[k])) for k in keys}
    for k in sorted(keys, key=lambda k: (-(exact[k] - out[k]), keys.index(k)))[:total - sum(out.values())]:
        out[k] += 1
    return out


def sample(a):
    pool = _pool(Path(a.cache))
    rows = _draw(pool, STRATA, np.random.default_rng(SEED), {}, 1)
    for r in rows:
        r["draw"] = 1
    OUT.mkdir(parents=True, exist_ok=True)
    _write_csv(OUT / "sample.csv", rows, SAMPLE_COLS)
    print(json.dumps({c: len(pool[c]) for c in sorted(STRATA)} | {"sampled": len(rows)}))


def extend(a):
    """Inbox 33: 126 more windows (seed 20261124), proportional strata, at most 2 per root counting the first 24.
    Appends to sample.csv; a rerun once the extension is drawn does nothing."""
    first = list(csv.DictReader(open(OUT / "sample.csv")))
    if any(r.get("draw") == "2" for r in first):
        print(json.dumps({"sampled": len(first), "note": "extension already drawn"}))
        return
    assert len(first) == sum(STRATA.values()), len(first)
    pool = _pool(Path(a.cache))
    quota = allocate(EXTRA, {c: len(pool[c]) for c in STRATA})
    rows = _draw(pool, quota, np.random.default_rng(SEED_EXTRA), {r["window"]: r for r in first}, 2)
    for r in first:
        r["draw"] = 1
    for r in rows:
        r["draw"] = 2
    _write_csv(OUT / "sample.csv", first + rows, SAMPLE_COLS)
    got = collections.Counter(r["condition"] for r in rows)
    print(json.dumps({"pool": {c: len(pool[c]) for c in sorted(STRATA)}, "quota": quota,
                      "drawn": {c: got[c] for c in sorted(STRATA)}, "sampled": len(first) + len(rows)}))


def predicted_positions(rec):
    """(T, M) predicted tip-frame position of each seed (finite in the first and last frame) in every frame, by the
    particle_path integration of checker/zone_checks.py; NaN for points that are not seeds."""
    s, v, _, ok = _profile(rec.fields)
    S = tip_frame_positions(rec)
    seed = np.isfinite(S[0]) & np.isfinite(S[-1])
    vel = _velocity(s, v, ok)
    out = np.full(S.shape, np.nan)
    x = S[0, seed].copy()
    out[0, seed] = x
    for i, dt in enumerate(np.diff(np.asarray(rec.frame_times_s, float))):
        h = dt / SUBSTEPS
        for _ in range(SUBSTEPS):
            k1 = vel(x); k2 = vel(x + 0.5 * h * k1); k3 = vel(x + 0.5 * h * k2); k4 = vel(x + h * k3)
            x = x + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        out[i + 1, seed] = x
    return out


def on_midline(line, S):
    """Points at arc length S from the tip along `line` (K, 2); NaN past its ends."""
    line = line[np.isfinite(line[:, 0])]
    sl = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(line, axis=0), axis=1))])
    S = np.where((S >= 0) & (S <= sl[-1]), S, np.nan)
    return np.stack([np.interp(S, sl, line[:, 0]), np.interp(S, sl, line[:, 1])], axis=-1)


def window_frames(elapsed_s, h0, h1):
    """Movie frame indices of a window, as scripts/remote/real_midline.py selects them."""
    t_h = np.asarray(elapsed_s) / 3600.0
    return np.nonzero((t_h >= h0) & (t_h <= h1))[0]


def _elapsed_s(text):
    m = re.search(r"theElapsedTimes:\s*\[(.*?)\]", text, re.DOTALL)
    vals = [float(v) for v in m.group(1).split(",") if v.strip()]
    return np.array(vals[1:]) / 1000.0              # the first value is a count header


def append_labels(path, windows):
    """Blank rows for windows not yet in labels.csv, in sample order after the existing rows; labels kept."""
    if not path.exists():
        path.write_text("window,label\n")
    with open(path, newline="") as fh:
        have = {r["window"] for r in csv.DictReader(fh)}
    with open(path, "a", newline="") as fh:
        fh.write("".join(f"{w},\n" for w in windows if w not in have))


def overlays(a):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from measure.remote_link import Link

    cache = Path(a.cache)
    man = {r["id"]: r for r in csv.DictReader(open(MANIFEST))}
    rows = list(csv.DictReader(open(OUT / "sample.csv")))
    raw = OVERLAYS / "_raw"
    raw.mkdir(parents=True, exist_ok=True)
    link = Link(a.host)
    notes = {}
    try:
        for r in rows:
            w = r["window"]
            png = OVERLAYS / f"{w}.png"
            if png.exists():
                continue
            m = man[r["root"]]
            imgdir = f"{a.data.rstrip('/')}/{m['experiment']}/{m['montage_imgdir']}"
            tf = track_file(cache, w, "st1")
            rec = from_tracker_npz(tf, root_id=w)
            el = _elapsed_s(link.run(f"cat {shlex.quote(imgdir + '/ElapsedTimes.yaml')}").decode())
            fr = window_frames(el, *_hours(w))
            T = len(rec.frame_times_s)
            if len(fr) != T or np.max(np.abs(el[fr] - el[fr[0]] - (rec.frame_times_s - rec.frame_times_s[0]))) > 1.0:
                notes[w] = f"frame times do not match the track ({len(fr)} frames, track {T})"
                print(w, notes[w])
                continue
            pred = predicted_positions(rec)
            # a whole-pixel reference track is on the copy cropped by D at the top left (real_moved.py whole_pixel)
            tw = rec.frame_times_s - rec.frame_times_s[0]
            crop = np.rint(np.outer(tw, MOVED_VELOCITY)).astype(int).max(axis=0) if "_wp_ref" in tf.name else 0
            fig, grid = plt.subplots(2, 3, figsize=(18, 11), gridspec_kw={"height_ratios": [1, 1.4]})
            for k, i in enumerate((0, T // 2, T - 1)):
                f = raw / f"{w}_{int(fr[i])}.npy"
                f.write_bytes(link.run(f"cat {shlex.quote(f'{imgdir}/ImageData_Ch0_TP{int(fr[i]):07d}.npy')}"))
                img = np.load(f)
                f.unlink()                           # raw frame deleted after use
                img = img[0] if img.ndim == 3 else img
                off = rec.stage_px[i] - crop         # image = world - stage_px (+ crop on a reference copy)
                mid = rec.midline[i] - off
                ch = rec.centre[i] - off
                pp = on_midline(mid, pred[i])
                pts = np.concatenate([mid[np.isfinite(mid[:, 0])], ch[np.isfinite(ch[:, 0])]])
                r0, c0 = np.maximum(pts.min(0) - 80, 0).astype(int)
                r1, c1 = np.minimum(pts.max(0) + 80, img.shape).astype(int)
                lo, hi = np.percentile(img[r0:r1, c0:c1], (1, 99.5))
                tip = mid[0]
                zoom = (max(tip[0] - ZOOM_PX, 0), min(tip[0] + ZOOM_PX, img.shape[0]),
                        max(tip[1] - ZOOM_PX, 0), min(tip[1] + ZOOM_PX, img.shape[1]))
                for ax, (a0, a1, b0, b1), ms in ((grid[0, k], (r0, r1, c0, c1), 1.0),
                                                 (grid[1, k], zoom, 2.0)):
                    ax.imshow(img, cmap="gray", vmin=lo, vmax=hi)
                    ax.plot(mid[:, 1], mid[:, 0], "-", color="cyan", lw=0.8 * ms, label="midline")
                    ax.plot(tip[1], tip[0], "*", color="red", ms=10 * ms, label="midline tip")
                    ax.plot(ch[:, 1], ch[:, 0], "o", color="yellow", ms=2.5 * ms, label="tracked chain")
                    j = np.flatnonzero(np.isfinite(ch[:, 0]))
                    if len(j):
                        ax.plot(ch[j[0], 1], ch[j[0], 0], "s", mfc="none", mec="magenta", ms=8 * ms, mew=2,
                                label="first chain point")
                    ax.plot(pp[:, 1], pp[:, 0], "x", color="lime", ms=4 * ms, mew=1, label="predicted")
                    ax.set_xlim(b0, b1); ax.set_ylim(a1, a0)
                    ax.set_xticks([]); ax.set_yticks([])
                grid[0, k].set_title(f"frame {i} of {T - 1} ({rec.frame_times_s[i] / 3600:.2f} h)")
                grid[1, k].set_title(f"tip region, {2 * ZOOM_PX} px")
            grid[0, 0].legend(loc="lower left", fontsize=8, framealpha=0.7)
            fig.suptitle(w)
            fig.tight_layout()
            fig.savefig(png, dpi=110)
            plt.close(fig)
            print(w, "done", flush=True)
    finally:
        link.close()
    append_labels(OVERLAYS / "labels.csv", [r["window"] for r in rows])
    items = []
    for r in rows:
        w = html.escape(r["window"])
        body = (f'<img src="{w}.png" style="width:100%">' if (OVERLAYS / f"{r['window']}.png").exists()
                else f"<p>not made: {html.escape(notes.get(r['window'], 'see run output'))}</p>")
        items.append(f'<h2 id="{w}">{w} ({html.escape(r["condition"])})</h2>\n{body}')
    (OVERLAYS / "index.html").write_text(
        "<!doctype html><meta charset='utf-8'><title>c035 overlays</title><body style='font-family:sans-serif'>"
        "<h1>c035 reference windows: label each clean or not clean in labels.csv</h1>"
        "<p>Not clean: midline tip or first chain point visibly wrong, or the profile visibly misplaced (predicted "
        "points, green x, visibly off the tracked chain, yellow). Frames: first, middle and last of the window. "
        "Red star: midline tip. Magenta square: first chain point.</p>\n" + "\n".join(items) + "</body>")
    print(json.dumps({"windows": len(rows), "made": sum((OVERLAYS / f"{r['window']}.png").exists() for r in rows),
                      "not made": notes}))


def read_labels(path, windows):
    """labels.csv as {window: label}; every sampled window labelled `clean` or `not clean`, no other window."""
    lab = {r["window"]: r["label"].strip() for r in csv.DictReader(open(path))}
    assert set(lab) == set(windows), "labels.csv windows differ from sample.csv"
    bad = sorted(w for w, v in lab.items() if v not in ("clean", "not clean"))
    assert not bad, f"unlabelled or unknown label: {bad[:5]}"
    return lab


def reference_thresholds(rows):
    """Step 5 rule on the clean rows. Fewer than 12 clean: None (proposal: no threshold, ask Andrew)."""
    clean = [r for r in rows if r["label"] == "clean"]
    if len(clean) < 12:
        return None
    return {k: r4([r[k] for r in clean]) for k in ("pp_shape_rel", "pp_common_rel")}


def thresholds(a):
    sample_rows = list(csv.DictReader(open(OUT / "sample.csv")))
    lab = read_labels(OVERLAYS / "labels.csv", [r["window"] for r in sample_rows])
    n_clean = sum(v == "clean" for v in lab.values())
    if n_clean < 30:
        print(json.dumps({"clean": n_clean, "note": "fewer than 30 clean: say so in status before computing"}))
        return
    rows = []
    for r in sample_rows:
        v = pp_values(from_tracker_npz(track_file(Path(a.cache), r["window"], "st1"), root_id=r["window"]))
        rows.append(r | {"label": lab[r["window"]]} | v)
    th = reference_thresholds(rows)
    for r in rows:
        r["over_shape"] = "yes" if r["pp_shape_rel"] > th["pp_shape_rel"] else "no"
        r["over_common"] = "yes" if r["pp_common_rel"] > th["pp_common_rel"] else "no"
    _write_csv(OUT / "reference.csv", rows, ["window", "condition", "draw", "label", "pp_common_rel", "pp_shape_rel",
                                             "over_common", "over_shape"])
    lines = ["# Reference thresholds (proposal step 5), waiting for Andrew's approval", "",
             f"Labels: {len(rows)} windows, {n_clean} clean, {len(rows) - n_clean} not clean (Andrew).",
             "Rule: 99.5th percentile over the clean windows (numpy linear) x 1.5, rounded up to 2 significant figures.",
             "", "| Value | 99.5th pct (clean) | Threshold | clean over | not clean over | clean range | not clean range |",
             "| :-- | --: | --: | --: | --: | :-- | :-- |"]
    for k, flag in (("pp_shape_rel", "over_shape"), ("pp_common_rel", "over_common")):
        c = [r[k] for r in rows if r["label"] == "clean"]
        n = [r[k] for r in rows if r["label"] != "clean"]
        lines.append(f"| `{k}` | {np.percentile(c, 99.5):.4g} | {th[k]:g} | "
                     f"{sum(r[flag] == 'yes' for r in rows if r['label'] == 'clean')} of {len(c)} | "
                     f"{sum(r[flag] == 'yes' for r in rows if r['label'] != 'clean')} of {len(n)} | "
                     f"{min(c):.3g}-{max(c):.3g} | {min(n):.3g}-{max(n):.3g} |")
    lines += ["", "Not clean windows over either threshold: " + (", ".join(
        r["window"] for r in rows if r["label"] != "clean" and "yes" in (r["over_shape"], r["over_common"])) or "none"),
        "", "For information, synthetic set (synthetic.csv) at the shape threshold, flagged of computable:"]
    syn = [r for r in csv.DictReader(open(OUT / "synthetic.csv")) if r["pp_shape_rel"]]
    for cls, d in [("accept_clean", 0), *[("shifted", d) for d in SHIFTS], ("accept_repaired", 0)]:
        sub = [r for r in syn if r["class"] == cls and int(r["shift_px"]) == d]
        lines.append(f"- {cls} {d:+d} px: {sum(float(r['pp_shape_rel']) > th['pp_shape_rel'] for r in sub)} "
                     f"of {len(sub)}")
    lines += ["", "Not written to config until Andrew approves (then `config/zone_reference_thresholds.yaml`).", ""]
    (OUT / "thresholds.md").write_text("\n".join(lines))
    print(json.dumps({"windows": len(rows), "clean": n_clean, "thresholds": th}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("synthetic"); s.add_argument("--cache", required=True)
    s = sub.add_parser("sample"); s.add_argument("--cache", required=True)
    s = sub.add_parser("extend"); s.add_argument("--cache", required=True)
    s = sub.add_parser("overlays"); s.add_argument("--cache", required=True)
    s.add_argument("--host", required=True); s.add_argument("--data", required=True)
    s = sub.add_parser("thresholds"); s.add_argument("--cache", required=True)
    a = ap.parse_args()
    {"synthetic": synthetic, "sample": sample, "extend": extend, "overlays": overlays,
     "thresholds": thresholds}[a.cmd](a)


if __name__ == "__main__":
    main()
