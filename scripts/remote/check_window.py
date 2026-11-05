"""Checker for one real window inside a cluster job (spec 2026-11-04 Work 3): reads the window's tracks, writes the
same per-window record as scripts/full_batch.py (real profile, closure gates at 19 px/h).

  python scripts/remote/check_window.py --window ROOT__wA-B --track T.npz --out W.json
  python scripts/remote/check_window.py --window ROOT__wA-B --ref REF.npz --moved MOVED.npz --out W.json

With --ref and --moved (the w10-12 whole-pixel copies) the record is the cropped reference and rigid invariance is
computed against the moved copy, as RealRunner.measure does. A tracker output that cannot be read or checked gives
a record with status 'failed'. An existing output is not overwritten.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from full_batch import thresholds, window_record  # noqa: E402
from measure.real_runner import TRACK_LENGTH, RealWindow  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402
from measure.runner import Measurement  # noqa: E402


def parse_window(wid):
    m = re.fullmatch(r"(.+)__w([\d.]+)-([\d.]+)", wid)
    return RealWindow(m.group(1), float(m.group(2)), float(m.group(3)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", required=True)
    ap.add_argument("--track")
    ap.add_argument("--ref")
    ap.add_argument("--moved")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists():
        sys.exit(f"output exists, not overwritten: {out.name}")
    w = parse_window(a.window)
    moved_copy = bool(a.ref and a.moved)
    try:
        rec = from_tracker_npz(a.ref if moved_copy else a.track, root_id=w.id())
        mv = from_tracker_npz(a.moved, root_id=w.id() + "_moved") if moved_copy else None
        res = window_record(w, Measurement(rec, mv, TrackSettings(stride=1), {}), moved_copy, TRACK_LENGTH, thresholds())
    except Exception as e:                          # noqa: BLE001 - recorded as a failed window
        res = window_record(w, None, moved_copy, TRACK_LENGTH, thresholds(), error=e)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({"window": w.id(), "status": res["status"], "outcome": res.get("outcome")}))


if __name__ == "__main__":
    main()
