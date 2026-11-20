"""Track-integrity thresholds by the fixed rule of docs/proposals/2026-11-20_registration-fix.md (R4).

thresholds  Freeze v4 rods (seeds 26-28): the accept_clean base tracks (<rod>__st1) and the accept_repaired tracks
            at their labelled repair (register_frames: the cached <rod>__st1_reg2p<from> track; a repair that changes
            no tracker run: the base track). Per track the values of checker.track_integrity. Threshold = 99.5th
            percentile x 1.5, rounded up to 2 significant figures; inversions 0. Writes
            config/integrity_thresholds.yaml and results/2026-11-20_registration_fix/thresholds.json
report      The values and the pass count with those thresholds on a folder of real base tracks (information only)

  python scripts/integrity_thresholds.py thresholds --cache <freeze v4 track cache>
  python scripts/integrity_thresholds.py report --tracks staging/tracks_real_fb1 --out <json>
"""
import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from checker import track_integrity  # noqa: E402
from checker.checks import INTEGRITY_FILE  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402

LABELS = ROOT / "results" / "2026-10-25_freeze_v4" / "labels.json"
OUT = ROOT / "results" / "2026-11-20_registration_fix"
KEYS = {"integrity_gap_ratio": "gap_ratio", "integrity_lateral": "lateral_px"}
TRACKER_REPAIRS = {"register_frames": "_reg2p"}


def round_up_2sf(x):
    if x <= 0:
        return 0.0
    e = math.floor(math.log10(x)) - 1
    return round(math.ceil(x / 10 ** e - 1e-9) * 10 ** e, max(0, -e))


def track_set(cache):
    labels = json.loads(LABELS.read_text())["labels"]
    out = []
    for rod, lab in sorted(labels.items()):
        if lab["class"] == "accept_clean":
            out.append((rod, cache / f"{rod}__st1.npz"))
        elif lab["class"] == "accept_repaired":
            part = TRACKER_REPAIRS.get(lab["sequence"][-1])
            if part is None:
                out.append((rod, cache / f"{rod}__st1.npz"))
                continue
            found = sorted(cache.glob(f"{rod}__st1{part}*.npz"))
            if len(found) != 1:
                sys.exit(f"{rod}: expected one cached {part} track, found {len(found)}")
            out.append((rod, found[0]))
    return out


def values(path):
    return {r.check: r.value for r in track_integrity(from_tracker_npz(path))}


def thresholds(a):
    rows = [{"rod": rod, "track": p.name} | values(p) for rod, p in track_set(Path(a.cache))]
    th = {"inversions": 0}
    for check, key in KEYS.items():
        v = np.array([r[check] for r in rows], float)
        th[key] = float(round_up_2sf(1.5 * np.percentile(v, 99.5)))
    INTEGRITY_FILE.write_text("# Track-integrity thresholds, rule of docs/proposals/2026-11-20_registration-fix.md (R4),\n"
                              "# from scripts/integrity_thresholds.py thresholds. Gate only for tracks made by a remedy.\n"
                              + yaml.safe_dump(th, sort_keys=False))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "thresholds.json").write_text(json.dumps({"rule": "99.5th percentile x 1.5, rounded up to 2 significant "
                                                     "figures; inversions 0", "n_tracks": len(rows),
                                                     "thresholds": th, "tracks": rows}, indent=1))
    print(json.dumps({"n_tracks": len(rows), "thresholds": th,
                      "max_inversions": max(r["integrity_inversions"] for r in rows)}))


def report(a):
    th = yaml.safe_load(INTEGRITY_FILE.read_text())
    rows = []
    for p in sorted(Path(a.tracks).glob("*__st1__L1000.npz")):
        if "_wp_" in p.name:
            continue
        try:
            r = track_integrity(from_tracker_npz(p), th)
        except Exception as e:                       # noqa: BLE001 - reported, not raised
            rows.append({"track": p.name, "error": f"{type(e).__name__}: {e}"})
            continue
        rows.append({"track": p.name} | {x.check: x.value for x in r} | {"passed": all(x.passed is not False for x in r)})
    ok = [r for r in rows if "error" not in r]
    summ = {"tracks": len(rows), "errors": len(rows) - len(ok), "pass_all": sum(r["passed"] for r in ok),
            "inversions_zero": sum(r["integrity_inversions"] == 0 for r in ok),
            "gap_ratio_pass": sum(r["integrity_gap_ratio"] <= th["gap_ratio"] for r in ok),
            "lateral_pass": sum(r["integrity_lateral"] <= th["lateral_px"] for r in ok), "thresholds": th}
    Path(a.out).write_text(json.dumps({"summary": summ, "tracks": rows}, indent=1))
    print(json.dumps(summ))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("thresholds")
    t.add_argument("--cache", required=True)
    r = sub.add_parser("report")
    r.add_argument("--tracks", required=True)
    r.add_argument("--out", required=True)
    a = p.parse_args()
    {"thresholds": thresholds, "report": report}[a.cmd](a)


if __name__ == "__main__":
    main()
