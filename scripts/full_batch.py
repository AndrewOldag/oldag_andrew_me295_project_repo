"""Full batch of real windows (real-calib inbox items 7-11; proposal docs/proposals/2026-10-25_full-batch.md).

  python scripts/full_batch.py run [--batch 1|2] [--config private/real_runner_fb<N>.yaml] [--windows W ...]
  python scripts/full_batch.py summary [--batch 1|2]

Batch 1: 11 roots; tracks made on the lab server. Batch 2: every other include-yes root; each root's segmentation,
midlines and tracks are made on the cluster (one job per root, decisions 2026-10-25) and copied to the host with md5
checks; `run` reads those tracks from the host and only checks them. The moved copy (w10-12) is made and tracked on
the host in both batches.

`run`, per window whose ft2 net midline is on the host: RealRunner at the initial settings (every frame, uncoupled,
1000 px), then the checker with the real profile: closure gates at the real threshold (19 px/h, decisions
2026-10-24); rigid invariance and plane sections reported, not gating. Moved copies for rigid invariance on one window
per root only, w10-12 (Andrew, inbox item 9). No screen, no remedy, no agent. One JSON per window in
DIR/windows/; a window with a file is skipped, so an interrupted run resumes.
`summary`: windows done and checker outcome counts by condition. Writes DIR/summary.json and DIR/table.md. No
per-window check values in the table.
"""
import argparse
import json
import math
import shlex
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from agents.dispatcher import manifest_rows, windows  # noqa: E402
from agents.executors import apply_profile, real_rigid_invariance  # noqa: E402
from checker import load_thresholds, run_checks  # noqa: E402
from measure.real_runner import TRACK_LENGTH, RealRunner, RealWindow  # noqa: E402
from real_calib import CLOSURE_DEFINITION, MIDLINE, base_info  # noqa: E402

OUTS = {1: ROOT / "results" / "2026-10-25_full_batch_1", 2: ROOT / "results" / "2026-10-25_full_batch_2"}
# Proposal, first batch: in each experiment-condition group the first include-yes root in position order that is in
# neither the calibration set nor the section C subset; every dispatcher window of each
ROOTS = ["0708_c2", "0708_m1", "0711_c3", "0711_m1", "0714_c5", "0714_m1", "0721_c2", "0721_m1",
         "0727_cc1", "0727_mc2", "0727_mm1"]
MOVED_SPAN = (10.0, 12.0)            # the one window per root with a moved copy (inbox item 9)
REAL_CLOSURE_PX_H = 19.0             # decisions 2026-10-24 (41 control windows); supersedes 18 px/h


def _position(row):
    letters = row["position"].rstrip("0123456789")
    return letters, int(row["position"][len(letters):] or 0)


def batch2_roots():
    """Every other include-yes root, one per experiment-condition group in turn (position order inside a group), so
    an early stop still covers every group. Batch 2 runs every step on the cluster, root by root (inbox item 11)."""
    groups = {}
    for r in sorted(manifest_rows(), key=lambda r: (r["experiment"], r["condition"], _position(r))):
        if r["id"] not in ROOTS:
            groups.setdefault((r["experiment"], r["condition"]), []).append(r["id"])
    out, k = [], 0
    while any(k < len(v) for v in groups.values()):
        out += [v[k] for v in groups.values() if k < len(v)]
        k += 1
    return out


def batch_windows(batch=1):
    """Batch 1: by window index across the roots (proposal: an early stop still covers every group). Batch 2: root
    by root in `batch2_roots` order, the order the cluster processes them."""
    roots = ROOTS if batch == 1 else batch2_roots()
    rows = {r["id"]: r for r in manifest_rows()}
    per = {i: windows(float(rows[i]["usable_from_h"]), float(rows[i]["usable_to_h"]), 2.0, 1.0) for i in roots}
    if batch == 2:
        return [RealWindow(i, a, b) for i in roots for a, b in per[i]]
    out = []
    for k in range(max(len(v) for v in per.values())):
        out += [RealWindow(i, *per[i][k]) for i in roots if k < len(per[i])]
    return out


def host_track(runner, w):
    """Batch 2: the cluster track copied to the host beside the window's midline (`<root>/midline/` ->
    `<root>/tracks/`)."""
    return runner.midline_path(w).replace("/midline/", "/tracks/").replace("_ft2_netmid.npz", "_ft2__st1__L1000.npz")


def thresholds():
    th = dict(load_thresholds())
    th["closure"] = REAL_CLOSURE_PX_H
    return th


def check_window(m, th):
    checks = apply_profile(run_checks(m.record, m.moved, th), "real")
    vals = {c.check: (None if not math.isfinite(c.value) else round(c.value, 4)) for c in checks}
    passed = {c.check: c.passed for c in checks}
    detail = {c.check: c.detail for c in checks}
    if m.moved is not None:
        win = real_rigid_invariance(m.record, m.moved, th)
        vals["rigid_invariance_profile_window"] = (None if win is None or not math.isfinite(win.value)
                                                   else round(win.value, 4))
    gate = passed["closure"]
    outcome = "pass" if gate is True else "fail" if gate is False else "not computable"
    return outcome, vals, passed, detail


def run(a):
    plain = RealRunner(a.config, cache=a.cache, moved=False)
    moved = RealRunner(a.config, cache=a.cache, moved=True)
    if plain.track_length != TRACK_LENGTH:
        sys.exit(f"tracked length {plain.track_length:g} px; real windows need {TRACK_LENGTH:g} px")
    plain.sync_code()
    th = thresholds()
    out = Path(a.out) / "windows"
    out.mkdir(parents=True, exist_ok=True)
    q = shlex.quote
    for w in batch_windows(a.batch):
        if a.windows and w.id() not in a.windows:
            continue
        f = out / f"{w.id()}.json"
        if f.exists():
            continue
        if w.id() not in plain.windows:
            print(f"{w.id()}: not in the runner config; skipped", flush=True)
            continue
        if plain._ssh(f"test -f {q(plain.midline_path(w))} && echo yes || echo no").decode().strip() != "yes":
            print(f"{w.id()}: midline not ready", flush=True)     # no file: retried on the next run
            continue
        runner = moved if (w.from_h, w.to_h) == MOVED_SPAN else plain
        cached = plain.cache_path(w, plain.initial_settings(w))
        if a.batch == 2 and runner is plain and not cached.exists():
            # the cluster track, md5-checked on the host; cached here so the runner starts no host step
            t = host_track(plain, w)
            if plain._ssh(f"test -f {q(t)} && echo yes || echo no").decode().strip() != "yes":
                print(f"{w.id()}: track not on the host yet", flush=True)
                continue
            cached.write_bytes(plain._ssh(f"cat {q(t)}"))
        res = {"window": w.id(), "root": w.root_id, "window_h": [w.from_h, w.to_h], "midline": MIDLINE,
               "moved_copy": runner is moved, "track_length_px": runner.track_length,
               "closure_definition": CLOSURE_DEFINITION, "closure_threshold_px_per_h": REAL_CLOSURE_PX_H}
        try:
            m = runner.measure(w, runner.initial_settings(w))
            res["outcome"], res["values"], res["passed"], res["detail"] = check_window(m, th)
            res["base"] = base_info(m.record)
            res["n_frames"] = int(m.record.n_frames)
            res["status"] = "measured"
        except Exception as e:
            if type(e).__name__ == "HostBusy":
                print(f"{w.id()}: host busy ({e}); stopping, rerun later", flush=True)
                break
            res["status"], res["error"] = "failed", f"{type(e).__name__}: {str(e)[:300]}"
        f.write_text(json.dumps(res, indent=1, default=str))
        print(f"{w.id()}: {res['status']} {res.get('outcome', '')}", flush=True)
    log = Path(a.out) / "runner_log.json"           # appended per run
    old = json.loads(log.read_text()) if log.exists() else []
    log.write_text(json.dumps(old + plain.log + moved.log, indent=1, default=str))


def summary(a):
    out = Path(a.out)
    cond = {r["id"]: r["condition"] for r in manifest_rows()}
    planned = batch_windows(a.batch)
    done = {p.stem: json.loads(p.read_text()) for p in sorted((out / "windows").glob("*.json"))}
    by = defaultdict(Counter)
    for w in planned:
        r = done.get(w.id())
        key = "not run" if r is None else r["outcome"] if r["status"] == "measured" else "failed"
        by[cond[w.root_id]][key] += 1
    cols = ["pass", "fail", "not computable", "failed", "not run"]
    flagged = sum(1 for r in done.values() if r.get("base", {}).get("flag"))
    s = {"planned": len(planned), "files": len(done),
         "measured": sum(r["status"] == "measured" for r in done.values()),
         "failed": sum(r["status"] == "failed" for r in done.values()),
         "moved_copies": sum(bool(r.get("moved_copy")) and r["status"] == "measured" for r in done.values()),
         "flag_base_may_be_in_growing_tissue": flagged,
         "closure_threshold_px_per_h": REAL_CLOSURE_PX_H, "by_condition": {k: dict(v) for k, v in sorted(by.items())},
         "errors": {k: r["error"] for k, r in done.items() if r["status"] == "failed"}}
    (out / "summary.json").write_text(json.dumps(s, indent=1))
    lines = ["| Condition | Windows | " + " | ".join(c.capitalize() for c in cols) + " |",
             "| :-- | --: | " + " | ".join("--:" for _ in cols) + " |"]
    for k, v in sorted(by.items()):
        lines.append(f"| {k} | {sum(v.values())} | " + " | ".join(str(v.get(c, 0)) for c in cols) + " |")
    tot = Counter()
    for v in by.values():
        tot.update(v)
    lines.append(f"| all | {sum(tot.values())} | " + " | ".join(str(tot.get(c, 0)) for c in cols) + " |")
    (out / "table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print({k: v for k, v in s.items() if k not in ("by_condition", "errors")})


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--batch", type=int, choices=(1, 2), default=1)
    r.add_argument("--config")
    r.add_argument("--cache")
    r.add_argument("--windows", nargs="*")
    r.add_argument("--out")
    s = sub.add_parser("summary")
    s.add_argument("--batch", type=int, choices=(1, 2), default=1)
    s.add_argument("--out")
    a = p.parse_args()
    a.out = a.out or str(OUTS[a.batch])
    if a.cmd == "run":
        a.config = a.config or str(ROOT / "private" / f"real_runner_fb{a.batch}.yaml")
        a.cache = a.cache or str(ROOT / "staging" / f"tracks_real_fb{a.batch}")
    run(a) if a.cmd == "run" else summary(a)


if __name__ == "__main__":
    main()
