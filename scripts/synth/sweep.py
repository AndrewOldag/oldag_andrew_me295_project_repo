"""Run a plan of rods x tracker settings on the machine that has the tracker. No agent.

  python scripts/synth/sweep.py --plan plan.json --work DIR [--workers 4]

plan.json: {"rods": [{"options": [make_rod.py options], "runs": [{"tag": t, "args": [qb_track.py options]}]}]}
Each rod is rendered once as is and once rigidly moved (skipped if present),
and each run is tracked on both into DIR/tracks/<id>__<tag>.npz (skipped if
present). One JSON line per tracker run on stdout. Run with the tracker
environment's Python. Plans are written by scripts/synth/repair_plan.py.
"""
import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run_rod(item, work):
    out = []
    rods, tracks = work / "rods", work / "tracks"
    for moved in (False, True):
        opts = item["options"] + (["--moved"] if moved else [])
        base = [sys.executable, str(HERE / "make_rod.py"), "--out", str(rods)] + opts
        rid = json.loads(subprocess.run(base + ["--dry-run"], check=True, capture_output=True,
                                        text=True).stdout.strip().splitlines()[-1])["id"]
        if not (rods / f"{rid}.imgdir").exists():
            subprocess.run(base, check=True, capture_output=True, text=True)
        for run in item["runs"]:
            name = f"{rid}__{run['tag']}.npz"
            rec = {"id": rid, "tag": run["tag"]}
            if (tracks / name).exists():
                rec["cached"] = True
            else:
                t0 = time.time()
                p = subprocess.run([sys.executable, str(HERE.parent / "remote" / "qb_track.py"),
                                    "--imgdir", str(rods / f"{rid}.imgdir"),
                                    "--midline", str(rods / f"{rid}_midline.npz"),
                                    "--out", str(tracks / name)] + run["args"],
                                   capture_output=True, text=True)
                rec.update(ok=p.returncode == 0, s=round(time.time() - t0, 1))
                if p.returncode:
                    rec["error"] = p.stderr.strip().splitlines()[-1:]
            out.append(rec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    work = Path(a.work)
    (work / "rods").mkdir(parents=True, exist_ok=True)
    (work / "tracks").mkdir(parents=True, exist_ok=True)
    plan = json.loads(Path(a.plan).read_text())
    with ProcessPoolExecutor(a.workers) as ex:
        for recs in ex.map(run_rod, plan["rods"], [work] * len(plan["rods"])):
            for r in recs:
                print(json.dumps(r), flush=True)
    print(json.dumps({"done": True}), flush=True)


if __name__ == "__main__":
    main()
