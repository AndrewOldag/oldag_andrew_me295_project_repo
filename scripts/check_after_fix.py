"""Checker on the batch-2 windows that failed with `arange: cannot compute length` (spec 2026-11-18 C3, inbox item 21).

The fix (measure/record.py derive(), dc1cfe6) does not change the tracks, so the windows are checked again on their
batch-2 tracks, on this machine, with scripts/remote/check_window.py; a window with both moved-copy tracks is checked
with them, as in batch 2. Tracks are read from the cache folder (copied from storage with md5 checks against
results/2026-10-25_full_batch_2/audit/outputs.csv). Records go to staging/full_batch_2_after_fix/windows/
(git-ignored); an existing record is kept, so a rerun resumes.

Then windows.csv of batch 2 gets a column `checked_after_fix`: the batch-2 rows keep their values with the column
empty; one row per window checked after the fix is appended with `yes`. A reader keyed by window id that keeps the
last row gets the row after the fix.

  python scripts/check_after_fix.py --tracks staging/tracks_real_fb2
"""
import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from full_batch import public_row  # noqa: E402

BATCH2 = ROOT / "results" / "2026-10-25_full_batch_2"
COLUMN = "checked_after_fix"


def arange_rows(rows):
    return [r for r in rows if r["status"] == "failed" and "arange" in r["error"] and r.get(COLUMN) != "yes"]


def check(wid, tracks, out, tracker):
    base = tracks / f"{wid}_ft2__st1__L1000.npz"
    ref, moved = (tracks / f"{wid}_ft2_wp_{k}__st1__L1000.npz" for k in ("ref", "moved"))
    args = ["--ref", str(ref), "--moved", str(moved)] if ref.exists() and moved.exists() else ["--track", str(base)]
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(tracker), str(ROOT)]))
    subprocess.run([sys.executable, "scripts/remote/check_window.py", "--window", wid, "--out", str(out)] + args,
                   cwd=ROOT, env=env, check=True, capture_output=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tracks", required=True, help="folder with the batch-2 track files")
    p.add_argument("--tracker", default=os.environ.get("QB_TRACKER", ""), help="tracker code folder (or QB_TRACKER)")
    p.add_argument("--records", default=str(ROOT / "staging" / "full_batch_2_after_fix"))
    a = p.parse_args()
    tracks, rec = Path(a.tracks), Path(a.records) / "windows"
    rec.mkdir(parents=True, exist_ok=True)
    with open(BATCH2 / "windows.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    md5 = {r["window"]: r["track_md5"] for r in csv.DictReader(open(BATCH2 / "audit" / "outputs.csv", newline=""))
           if r["kind"] == "track"}
    new, missing = [], []
    for r in arange_rows(rows):
        wid = r["window"]
        t = tracks / f"{wid}_ft2__st1__L1000.npz"
        if not t.exists() or hashlib.md5(t.read_bytes()).hexdigest() != md5.get(wid):
            missing.append(wid)
            continue
        out = rec / f"{wid}.json"
        if not out.exists():
            check(wid, tracks, out, a.tracker)
        new.append(public_row(json.loads(out.read_text()), r["condition"]) | {COLUMN: "yes"})
    if missing:
        sys.exit(f"track missing or md5 differs, nothing written: {', '.join(missing)}")
    kept = [r for r in rows if r.get(COLUMN) != "yes"]
    cols = [c for c in rows[0] if c != COLUMN] + [COLUMN]
    with open(BATCH2 / "windows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in kept + new:
            w.writerow({c: r.get(c, "") for c in cols})
    counts = {}
    for r in new:
        counts[r["outcome"] or r["status"]] = counts.get(r["outcome"] or r["status"], 0) + 1
    print(json.dumps({"checked": len(new), "outcomes": counts}))


if __name__ == "__main__":
    main()
