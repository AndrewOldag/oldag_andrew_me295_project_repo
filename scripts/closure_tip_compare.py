"""Closure cause on one real window, two midline nets (inbox item 28): tip jitter against the closure change.

  python scripts/closure_tip_compare.py --net NAME TRACK.npz NETMID.npz [--net NAME TRACK.npz NETMID.npz ...]

TRACK is a cached tracker output (staging/tracks_real/), NETMID the window's net midline file. Per net: frame-to-frame
tip jump in image coordinates (px, median and p90), closure residual per frame pair (|r|, px, median, p90, max; checker
definition), closure as the checker computes it, and closure with the tip path replaced by a polynomial fit in time
(degree 1-3). The closure sum telescopes, so only the first and last tip positions enter it; the fit removes their
noise. Diagnostic only; the checker is unchanged. Prints JSON.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from checker.checks import _common_base, closure  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402


def compare(track, netmid, name):
    rec = from_tracker_npz(track, root_id=name)
    tip_img = np.load(netmid)["midline_image"][:, 0, :]
    jump = np.linalg.norm(np.diff(tip_img, axis=0), axis=1)
    b = _common_base(rec.centre)
    tip_w = rec.midline[:, 0, :]
    rel = rec.centre[:, 0, :] - rec.centre[:, b, :]
    r = np.linalg.norm(np.diff(tip_w, axis=0) - np.diff(rel, axis=0), axis=1)
    t = rec.frame_times_s / 3600.0
    dur = t[-1] - t[0]
    fitted = {}
    for deg in (1, 2, 3):
        fit = np.stack([np.polyval(np.polyfit(t, tip_w[:, k], deg), t) for k in (0, 1)], axis=1)
        fitted[f"deg{deg}"] = round(float(np.linalg.norm((fit[-1] - fit[0]) - (rel[-1] - rel[0])) / dur), 3)
    return {"net": name, "frames": int(len(t)), "closure_px_per_h": round(closure(rec).value, 3),
            "closure_fitted_tip_px_per_h": fitted,
            "tip_jump_px": {"median": round(float(np.median(jump)), 2), "p90": round(float(np.percentile(jump, 90)), 2)},
            "pair_residual_px": {"median": round(float(np.median(r)), 2), "p90": round(float(np.percentile(r, 90)), 2),
                                 "max": round(float(r.max()), 2)},
            "tip_world_first_last": [tip_w[0].round(1).tolist(), tip_w[-1].round(1).tolist()],
            "tip_net_change_px": (tip_w[-1] - tip_w[0]).round(2).tolist(),
            "chain_net_change_px": (rel[-1] - rel[0]).round(2).tolist()}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--net", nargs=3, action="append", required=True, metavar=("NAME", "TRACK", "NETMID"))
    print(json.dumps([compare(track, netmid, name) for name, track, netmid in ap.parse_args().net], indent=1))
