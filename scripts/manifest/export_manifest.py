"""Check the reviewed manifest and write the committed copy.

    python scripts/manifest/export_manifest.py

Reads data/manifest/manifest_reviewed.csv (from the review app) and writes
manifest/root_manifest.csv. Stops with a list of problems if any row is
unanswered, has an unknown condition, or has a bad usable window.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "manifest" / "manifest_reviewed.csv"
DST = ROOT / "manifest" / "root_manifest.csv"

CONDITIONS = {"control", "mannitol", "control then control", "mannitol then control", "mannitol then mannitol"}
COLUMNS = [
    "id", "experiment", "experiment_type", "position", "condition", "include",
    "usable_from_h", "usable_to_h", "notes", "flags",
    "montage_imgdir", "raw_imgdir", "capture_name", "start_time",
    "n_timepoints", "duration_h", "step_s", "max_step_s", "size_px", "stage_tracking_log",
]


def main():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    problems = []
    for r in rows:
        r["notes"] = r["notes"].strip()
        if r["include"] not in ("yes", "no", "unsure"):
            problems.append(f"{r['id']}: no keep/drop/unsure answer")
        if r["condition"] not in CONDITIONS:
            problems.append(f"{r['id']}: condition '{r['condition']}'")
        lo, hi = r.get("usable_from_h", "").strip(), r.get("usable_to_h", "").strip()
        dur = float(r["duration_h"])
        try:
            a = float(lo) if lo else 0.0
            b = float(hi) if hi else dur
        except ValueError:
            problems.append(f"{r['id']}: window '{lo}' to '{hi}' is not a number")
            continue
        if not 0 <= a < b <= dur + 0.05:
            problems.append(f"{r['id']}: window {a} to {b} h outside 0 to {dur} h")
        r["usable_from_h"], r["usable_to_h"] = f"{a:g}", f"{min(b, dur):g}"
    if problems:
        sys.exit("Not exported:\n  " + "\n  ".join(problems))

    DST.parent.mkdir(exist_ok=True)
    with DST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: r["id"]))
    keep = [r for r in rows if r["include"] == "yes"]
    windowed = [r for r in rows if r["include"] != "no" and (float(r["usable_from_h"]) > 0
                or float(r["usable_to_h"]) < float(r["duration_h"]) - 0.05)]
    print(f"Wrote {DST.relative_to(ROOT)}: {len(rows)} roots, {len(keep)} keep, {len(windowed)} with a usable window")


if __name__ == "__main__":
    main()
