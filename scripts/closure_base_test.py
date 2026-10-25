"""Closure against the chain base on real windows (spec 2026-10-24b A): the same window tracked at several tracked
lengths, so the closure base moves from inside the growth zone to mature tissue.

  python scripts/closure_base_test.py --config private/closure_runner_lab.yaml --lengths 400 800 \
      --windows 0708_m12:4-6 0711_c2:4-6 0721_m10:4-6 [--out results/.../closure_base_test.json]

Tracks the movie window as is (no moved copy), one run at a time, through RealRunner (single thread, nice 19, load
and job checks before each run; outputs cached in staging/tracks_real/). Per run: closure (checker definition), the
basal point's arc length and its world displacement over the window, the tip-side term |d(tip) - d(c_0)| and the
world speed profile along the chain. Checker unchanged. Prints JSON.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from checker.checks import _common_base, closure  # noqa: E402
from measure.real_runner import RealRunner, RealWindow  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402


def summarize(rec):
    c, m = rec.centre, rec.midline
    b = _common_base(c)
    t = rec.frame_times_s / 3600.0
    dur = t[-1] - t[0]
    s = np.concatenate([[0.0], np.cumsum(np.nanmean(np.linalg.norm(np.diff(c, axis=1), axis=2), axis=0))])
    u = c[-1, 0] - c[0, 0]
    u = u / np.linalg.norm(u)
    speed = [float(np.polyfit(t, c[:, j] @ u, 1)[0]) for j in range(b + 1)]
    base = c[-1, b] - c[0, b]
    return {"closure_px_per_h": round(closure(rec).value, 3), "points": int(c.shape[1]), "base_index": b,
            "base_s_px": round(float(s[b]), 1), "base_world_disp_px": base.round(2).tolist(),
            "base_term_px_per_h": round(float(np.linalg.norm(base) / dur), 3),
            "tip_side_term_px_per_h": round(float(np.linalg.norm((m[-1, 0] - m[0, 0]) - (c[-1, 0] - c[0, 0])) / dur), 3),
            "speed_profile_px_per_h": [[round(float(s[j]), 0), round(speed[j], 2)] for j in range(0, b + 1, 4)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--lengths", type=float, nargs="+", default=[400.0, 800.0])
    ap.add_argument("--windows", nargs="+", required=True, help="ROOT:FROM-TO, hours")
    ap.add_argument("--out")
    a = ap.parse_args()
    rows = []
    synced = False
    for spec in a.windows:
        root, span = spec.split(":")
        w = RealWindow(root, *(float(x) for x in span.split("-")))
        for L in a.lengths:
            r = RealRunner(a.config, track_length=L, moved=False)
            if not synced:
                r.sync_code()
                synced = True
            rec = from_tracker_npz(r.track(w, r.initial_settings(w)), root_id=w.id())
            rows.append({"window": w.id(), "track_length_px": L, **summarize(rec), "host_log": r.log})
            print(json.dumps(rows[-1]), flush=True)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
