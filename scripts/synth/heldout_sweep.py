"""Checker-only sweep for the held-out faults (docs/proposals/2026-10-12_heldout-faults.md). No agent.

  python scripts/synth/heldout_sweep.py start [--dry-run]
  python scripts/synth/heldout_sweep.py status
  python scripts/synth/heldout_sweep.py stop
  python scripts/synth/heldout_sweep.py fetch          # to staging/tracks_heldout/
  python scripts/synth/heldout_sweep.py eval --out results/<dir>

Each candidate size on growth_zone, seeds 0-2, unremedied, uncoupled, each
rod tracked as is and rigidly moved. The sweep runs under the limits for the
shared machine in scripts/synth/sweep.py and takes the same sweep lock as
every other sweep. The code goes to the branch's own directory on the
tracker machine (measure/runner.py), as for every other sweep.

private/runner.yaml is read from this checkout, or else from the main
checkout (beside the git common directory) when run from a worktree.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from measure.remedies import TrackSettings  # noqa: E402
from measure.runner import RUNNER_CONFIG, RemoteRunner, Rod  # noqa: E402

NAME, TRACKS = "heldout_sizes", "tracks_heldout"
CACHE = ROOT / "staging" / TRACKS
SEEDS = (0, 1, 2)
SIZES = {"second_root": ["15", "30"], "fast_rotation": ["2", "4"], "bad_stage_correction": ["3", "10"],
         "flank_swap": ["0.5"], "partial_occlusion": ["20", "30"]}
UNITS = {"second_root": "px past the near edge", "fast_rotation": "deg/frame for 3 frames",
         "bad_stage_correction": "px under-reported", "flank_swap": "fraction of the window swapped",
         "partial_occlusion": "px drop radius"}


def rods():
    return [Rod("growth_zone", f, s, size=z) for f, zs in SIZES.items() for z in zs for s in SEEDS]


def plan():
    st = TrackSettings()
    return {"rods": [{"id": r.id(), "options": r.options(), "runs": [{"tag": st.tag(), "args": st.args()}]}
                     for r in rods()]}


def config():
    if RUNNER_CONFIG.exists():
        return RUNNER_CONFIG
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout.strip()
    return (ROOT / common).resolve().parent / "private" / "runner.yaml"


def runner():
    return RemoteRunner(config(), cache=CACHE)


def evaluate_all(out):
    from eval_fix import CHECKS, cell, evaluate
    rows = []
    lines = ["| Fault | Size | Seed | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | "
             "REGR RMS err (%/h) | Checker |", "| :-- | --: | --: | --: | --: | --: | --: | :-- |"]
    for rod in rods():
        r = evaluate(rod.id(), TrackSettings().tag(), [CACHE])
        if r is None:
            lines.append(f"| {rod.fault} | {rod.size} | {rod.seed} | not run | | | | |")
            continue
        r.pop("truth")
        rows.append({"fault": rod.fault, "size": rod.size, "seed": rod.seed,
                     **{k: v for k, v in r.items() if k != "preprocess"}})
        lines.append(f"| {rod.fault} | {rod.size} | {rod.seed} | " + " | ".join(cell(r, c) for c in CHECKS)
                     + f" | {r['regr_rms_pct_per_h']:.2f} | {'pass' if r['all_pass'] else 'fail'} |")
    summ = ["| Fault | Size | Unit | Seeds failing the checker | Checks failing (seeds) |",
            "| :-- | --: | :-- | :-- | :-- |"]
    for f, zs in SIZES.items():
        for z in zs:
            rs = [x for x in rows if x["fault"] == f and x["size"] == z]
            failing = sum(not x["all_pass"] for x in rs)
            which = {c: sum(x[f"{c}_pass"] is False for x in rs) for c in CHECKS}
            summ.append(f"| {f} | {z} | {UNITS[f]} | {failing} of {len(rs)} | "
                        + ", ".join(f"{c} {n}" for c, n in which.items() if n) + " |")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "checker_sizes.md").write_text("# Held-out faults: checker only, seeds 0-2, unremedied, uncoupled\n\n"
                                          "Thresholds: config/checker_thresholds.yaml (approved 2026-10-10). "
                                          "F = fails.\n\n" + "\n".join(summ) + "\n\n" + "\n".join(lines) + "\n")
    (out / "checker_sizes.json").write_text(json.dumps(rows, indent=1, default=float))
    print("\n".join(summ))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["start", "status", "stop", "fetch", "eval"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.cmd == "eval":
        if not a.out:
            ap.error("eval needs --out")
        evaluate_all(a.out)
        return
    if a.cmd == "start":
        p = plan()
        n = sum(2 * len(x["runs"]) for x in p["rods"])
        if a.dry_run:
            print(f"{len(p['rods'])} rods, {n} tracker runs")
            return
        runner().sweep_start(p, NAME, tracks=TRACKS)
        print(f"started: {len(p['rods'])} rods, {n} tracker runs")
        return
    r = runner()
    if a.cmd == "status":
        st = r.sweep_status(NAME)
        log = st.pop("log")
        print(json.dumps(st))
        runs = [x for x in log if "tag" in x]
        print(f"runs logged {len(runs)}, failed {sum(x.get('ok') is False for x in runs)}")
        for x in log:
            if "tag" not in x:
                print(json.dumps(x))
    elif a.cmd == "stop":
        print(json.dumps(r.sweep_stop()))
    else:
        cache = r.sweep_fetch(TRACKS, CACHE)
        print(f"fetched to {cache.relative_to(ROOT)}: {len(list(cache.glob('*__*.npz')))} files")


if __name__ == "__main__":
    main()
