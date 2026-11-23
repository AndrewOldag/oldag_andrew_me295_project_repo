"""Growth-zone placement checks, report-only (spec 2026-11-23, task c034; docs/proposals/2026-11-23_zone-checks.md).

synthetic   Freeze v4 rods (seeds 26-28) from the cached tracks: the 18 accept_clean base tracks, the 15 growing ones
            with the profile shifted by -60, -30, -15, +15, +30, +60 px, and the 9 accept_repaired tracks at their
            labelled repair. Writes results/2026-11-23_zone_checks/synthetic.csv. No tracker run
thresholds  From the clean rows of synthetic.csv: 99.5th percentile x 1.5, rounded up to 2 significant figures, per
            value. Writes config/zone_thresholds.yaml, then the detection table synthetic.md with those thresholds
real        Every window of results/2026-11-18_integrated_run/windows.csv: base track and, where a remedy was kept
            and the window accepted, the accepted track; from the c027 track cache, read-only. Per-window values go
            to --values (git-ignored; a rerun skips windows already there). Writes real_counts.md (counts only)

  python scripts/zone_checks.py synthetic --cache <freeze v4 track cache>
  python scripts/zone_checks.py thresholds
  python scripts/zone_checks.py real --cache <c027 track cache> [--values staging/zone_checks/real.jsonl]
"""
import argparse
import collections
import csv
import json
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from checker.zone_checks import ZONE_FILE, run_zone_checks, shifted_fields  # noqa: E402
from integrity_thresholds import LABELS, round_up_2sf, track_set  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402

OUT = ROOT / "results" / "2026-11-23_zone_checks"
WINDOWS = ROOT / "results" / "2026-11-18_integrated_run" / "windows.csv"
SHIFTS = (-60, -30, -15, 15, 30, 60)
KEYS = ("plateau_regr", "plateau_speed", "pp_rms_px", "pp_max_px", "pp_rms_rel", "pp_max_rel")
GATING = {"plateau": ("plateau_regr", "plateau_speed"), "particle_path": ("pp_rms_rel", "pp_max_rel")}


def row_values(rec, th=None, fields=None):
    res = run_zone_checks(rec, th, fields)
    out = {k: v for r in res for k, v in r.values.items()}
    out.update({r.check: r.passed for r in res})
    return out


def synthetic(a):
    cache = Path(a.cache)
    labels = json.loads(LABELS.read_text())["labels"]
    rows = []
    for rod, path in track_set(cache):
        lab = labels[rod]
        rec = from_tracker_npz(path)
        rows.append({"rod": rod, "class": lab["class"], "kind": lab["kind"], "seed": lab["seed"], "shift_px": 0,
                     "track": path.name} | row_values(rec))
        if lab["class"] == "accept_clean" and lab["kind"] != "v3_still":
            for d in SHIFTS:
                rows.append({"rod": rod, "class": "shifted", "kind": lab["kind"], "seed": lab["seed"], "shift_px": d,
                             "track": path.name} | row_values(rec, fields=shifted_fields(rec, d)))
    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["rod", "class", "kind", "seed", "shift_px", "track", *KEYS]
    with open(OUT / "synthetic.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else (f"{r[k]:.6g}" if isinstance(r[k], float) else r[k]))
                        for k in cols})
    print(json.dumps(collections.Counter(r["class"] for r in rows)))


def _num(x):
    return None if x in ("", None) else float(x)


def flags(r, th):
    """Per check: True = flagged, False = within, None = no gating value computable."""
    out = {}
    for check, keys in GATING.items():
        got = [(_num(r[k]), th[k]) for k in keys if _num(r[k]) is not None]
        out[check] = None if not got else any(v > t for v, t in got)
    c = [v for v in out.values() if v is not None]
    out["either"] = None if not c else any(c)
    return out


def thresholds(a):
    rows = list(csv.DictReader(open(OUT / "synthetic.csv")))
    clean = [r for r in rows if r["class"] == "accept_clean"]
    th = {}
    for k in ("plateau_regr", "plateau_speed", "pp_rms_rel", "pp_max_rel"):
        v = np.array([_num(r[k]) for r in clean if _num(r[k]) is not None])
        th[k] = float(round_up_2sf(1.5 * np.percentile(v, 99.5)))
    ZONE_FILE.write_text("# Growth-zone placement thresholds, rule of docs/proposals/2026-11-23_zone-checks.md,\n"
                         "# from scripts/zone_checks.py thresholds (18 freeze v4 accept_clean base tracks). Report-only.\n"
                         + yaml.safe_dump(th, sort_keys=False))
    lines = ["# Synthetic detection, freeze v4 rods (seeds 26-28)", "",
             f"Thresholds (`config/zone_thresholds.yaml`): " + ", ".join(f"{k} {v:g}" for k, v in th.items()), "",
             "| Set | Shift px | Records | plateau flags | particle_path flags | either |",
             "| :-- | --: | --: | --: | --: | --: |"]

    def line(name, d, sub):
        f = [flags(r, th) for r in sub]
        cnt = lambda c: f"{sum(x[c] is True for x in f)} of {sum(x[c] is not None for x in f)}"
        lines.append(f"| {name} | {d} | {len(sub)} | {cnt('plateau')} | {cnt('particle_path')} | {cnt('either')} |")
    line("accept_clean (threshold set)", 0, clean)
    for d in SHIFTS:
        line("shifted", f"{d:+d}", [r for r in rows if r["class"] == "shifted" and int(r["shift_px"]) == d])
    line("accept_repaired (not in the threshold set)", 0, [r for r in rows if r["class"] == "accept_repaired"])
    lines += ["", "- Counts read `flagged of computable`. `plateau_speed` and the relative particle-path values are not "
              "computable on `v3_still` (no growth); its `plateau_regr` is", ""]
    (OUT / "synthetic.md").write_text("\n".join(lines))
    print(json.dumps(th))


def real_tracks(r):
    """(kind, track file stem) to check for one windows.csv row."""
    base = f"{r['window']}_ft2__st1__L1000.npz"
    out = [("base", base)]
    st = r["final_settings"]
    if r["integrated"].startswith("accepted") and st and st != "st1":
        out.append(("accepted", f"{r['window']}_ft2__{st}__L1000.npz"))
    return out


def real(a):
    cache = Path(a.cache)
    vals_path = Path(a.values)
    vals_path.parent.mkdir(parents=True, exist_ok=True)
    done = {}
    if vals_path.exists():
        for ln in vals_path.read_text().splitlines():
            d = json.loads(ln)
            done[(d["window"], d["kind"])] = d
    windows = list(csv.DictReader(open(WINDOWS)))
    with open(vals_path, "a") as fh:
        for r in windows:
            for kind, name in real_tracks(r):
                if (r["window"], kind) in done:
                    continue
                p = cache / name
                d = {"window": r["window"], "kind": kind, "track": name}
                if not p.exists():
                    d["error"] = "track not cached"
                else:
                    try:
                        d |= row_values(from_tracker_npz(p, root_id=r["window"]))
                    except Exception as e:           # noqa: BLE001 - counted as not computed
                        d["error"] = f"{type(e).__name__}: {e}"
                fh.write(json.dumps(d) + "\n")
                fh.flush()
                done[(r["window"], kind)] = d
    th = yaml.safe_load(ZONE_FILE.read_text())
    real_report(windows, done, th)


def real_report(windows, done, th):
    by_class, by_cond = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    examples = collections.defaultdict(list)
    for r in windows:
        for kind, _ in real_tracks(r):
            d = done[(r["window"], kind)]
            key = (r["integrated"], kind)
            ckey = (r["condition"] or "(none)", kind)
            for agg, k in ((by_class, key), (by_cond, ckey)):
                agg[k]["windows"] += 1
                if "error" in d:
                    agg[k]["not computed"] += 1
                    continue
                f = flags({k2: ("" if d.get(k2) is None else d[k2]) for k2 in KEYS}, th)
                for c in ("plateau", "particle_path", "either"):
                    if f[c] is None:
                        agg[k][f"{c} n/a"] += 1
                    elif f[c]:
                        agg[k][f"{c} flagged"] += 1
            if "error" not in d and kind == "base":
                f = flags({k2: ("" if d.get(k2) is None else d[k2]) for k2 in KEYS}, th)
                examples[(r["integrated"], f["particle_path"], f["plateau"])].append(r["window"])
    cols = ["windows", "not computed", "plateau flagged", "plateau n/a", "particle_path flagged", "particle_path n/a",
            "either flagged"]

    def table(title, agg, head):
        out = [f"## {title}", "", f"| {head} | Track | " + " | ".join(cols) + " |",
               "| :-- | :-- | " + " | ".join("--:" for _ in cols) + " |"]
        for (k, kind), c in sorted(agg.items()):
            out.append(f"| {k} | {kind} | " + " | ".join(str(c[x]) for x in cols) + " |")
        return out + [""]
    ok = [d for d in done.values() if "error" not in d and d["kind"] == "base"]
    pct = lambda k: [d[k] for d in ok if d.get(k) is not None]
    q = lambda v: " / ".join(f"{np.percentile(v, p):.3g}" for p in (50, 90, 99)) if v else "-"
    lines = ["# Growth-zone placement checks on the c027 windows (report-only)", "",
             "Thresholds `config/zone_thresholds.yaml`: " + ", ".join(f"{k} {v:g}" for k, v in th.items()),
             "They gate nothing; no c027 outcome changes. `plateau_regr` values are not shown (basal strain rate)", ""]
    lines += table("By outcome class", by_class, "Outcome")
    lines += table("By condition", by_cond, "Condition")
    lines += ["## Residuals, base tracks (median / 90th / 99th percentile)", "",
              "| Value | Computed | Percentiles |", "| :-- | --: | :-- |"]
    for k in ("plateau_speed", "pp_rms_px", "pp_max_px", "pp_rms_rel", "pp_max_rel"):
        lines.append(f"| {k} | {len(pct(k))} | {q(pct(k))} |")
    lines += ["", "## Example windows (base track; first 3 by id per group)", "",
              "| Outcome | particle_path | plateau | Windows |", "| :-- | :-- | :-- | :-- |"]
    word = {True: "flag", False: "pass", None: "n/a"}
    for (cls, pp, pl), ws in sorted(examples.items(), key=lambda x: (x[0][0], str(x[0][1]), str(x[0][2]))):
        lines.append(f"| {cls} | {word[pp]} | {word[pl]} | {', '.join(sorted(ws)[:3])} ({len(ws)}) |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "real_counts.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"base": len([d for d in done.values() if d["kind"] == "base"]),
                      "accepted": len([d for d in done.values() if d["kind"] == "accepted"]),
                      "errors": sum("error" in d for d in done.values())}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("synthetic"); s.add_argument("--cache", required=True)
    sub.add_parser("thresholds")
    s = sub.add_parser("real"); s.add_argument("--cache", required=True)
    s.add_argument("--values", default=str(ROOT / "staging" / "zone_checks" / "real.jsonl"))
    a = ap.parse_args()
    {"synthetic": synthetic, "thresholds": thresholds, "real": real}[a.cmd](a)


if __name__ == "__main__":
    main()
