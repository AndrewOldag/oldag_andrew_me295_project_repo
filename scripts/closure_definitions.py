"""Closure on real windows under four tip definitions (spec 2026-10-24b A, tests 1-4), plus the stage checks.

  python scripts/closure_definitions.py --tips NET_TIPS.json --track ROOT TRACK.npz [--track ROOT TRACK.npz ...]

TRACK: a tracker output of the window (staging/tracks_real/); NET_TIPS: scripts/remote/net_tip_points.py output.
Per frame pair the checker residual is r = d(tip) - d(c_0 - c_b); value |sum r| / duration, px/h. Tip:
  (1) apex: the midline end (the checker's definition)
  (2) net tip: the net's own tip point plus the stage log
  (3) chain: the most apical tracked material point c_0 (value = base world displacement / duration)
  (4) apex, with the apical segment's growth added to the chain side: the apex speed minus the c_0 speed from a
      quadratic fit of the world speed along the chain (s <= 150 px), between s = 0 and the c_0 gap
Also: the split into a tip-side term |d(apex) - d(c_0)| and a base term |d(c_b)|; the linear trend in time of
apex - c_0 and net tip - c_0 (px/h); the stage steps in px and in um at 2.105 um/px; the stage sign and lag that
give the smoothest world motion of the chain (std of per-pair displacement); the world speed along the chain.
The checker is unchanged. Prints JSON.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from checker.checks import _common_base, closure  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402

PIXEL_UM = 2.105


def arc_gap(P, q):
    """Arc length along the polyline P (tip first) to the point nearest q."""
    seg = P[1:] - P[:-1]
    L = np.linalg.norm(seg, axis=1)
    s = np.concatenate([[0.0], np.cumsum(L)])
    u = np.clip(np.einsum("ij,ij->i", q - P[:-1], seg) / np.maximum(L ** 2, 1e-12), 0, 1)
    i = int(np.argmin(np.linalg.norm(P[:-1] + u[:, None] * seg - q, axis=1)))
    return float(s[i] + u[i] * L[i])


def trend(t, d):
    return float(np.linalg.norm([np.polyfit(t, d[:, k], 1)[0] for k in (0, 1)]))


def analyse(rec, tips):
    c, m, st = rec.centre, rec.midline, rec.stage_px
    b = _common_base(c)
    t = rec.frame_times_s / 3600.0
    dur = t[-1] - t[0]
    rel = c[:, 0] - c[:, b]
    value = lambda tip: float(np.linalg.norm((tip[-1] - tip[0]) - (rel[-1] - rel[0])) / dur)
    idx = [tips["htp_frames"].index(f) for f in tips["mid_frames"]]
    end_img = np.asarray(tips["end_rc"])
    off = (m[:, 0] - st) - end_img                      # crop offset of a reference copy; constant
    net = np.asarray(tips["tip_rc"])[idx] + off.mean(axis=0) + st
    s = np.concatenate([[0.0], np.cumsum(np.nanmean(np.linalg.norm(np.diff(c, axis=1), axis=2), axis=0))])
    u = (c[-1, 0] - c[0, 0]) / np.linalg.norm(c[-1, 0] - c[0, 0])
    speed = np.array([np.polyfit(t, c[:, j] @ u, 1)[0] for j in range(b + 1)])
    k = s[:b + 1] <= 150
    p = np.polyfit(s[:b + 1][k], speed[k], 2)
    gap = np.array([arc_gap(m[i], c[i, 0]) for i in range(len(t))])
    rate = np.polyval(p, 0.0) - np.polyval(p, gap)     # apex speed minus c_0 speed, px/h
    seg = np.concatenate([[0.0], np.cumsum(0.5 * (rate[1:] + rate[:-1]) * np.diff(t))])
    ds = np.diff(st, axis=0)
    steps = ds[np.linalg.norm(ds, axis=1) > 0.5]
    smooth = {}
    for sign in (1, -1):
        for lag in (-1, 0, 1):
            w = (c - st[:, None, :]) + sign * np.roll(st, lag, axis=0)[:, None, :]
            smooth[f"sign{sign:+d}_lag{lag:+d}"] = round(float(np.nanmean(np.nanstd(np.diff(w[1:-1], axis=0), axis=0))), 3)
    return {
        "checker_px_per_h": round(closure(rec).value, 3),
        "def1_apex": round(value(m[:, 0]), 3), "def2_net_tip": round(value(net), 3),
        "def3_chain_c0": round(value(c[:, 0]), 3), "def4_apex_minus_segment_growth": round(value(m[:, 0] - seg[:, None] * u), 3),
        "tip_side_term_px_per_h": round(float(np.linalg.norm((m[-1, 0] - m[0, 0]) - (c[-1, 0] - c[0, 0])) / dur), 3),
        "base_term_px_per_h": round(float(np.linalg.norm(c[-1, b] - c[0, b]) / dur), 3),
        "apex_minus_c0_trend_px_per_h": round(trend(t, m[:, 0] - c[:, 0]), 3),
        "net_tip_minus_c0_trend_px_per_h": round(trend(t, net - c[:, 0]), 3),
        "gap_apex_c0_px_first_last_max": [round(gap[0], 2), round(gap[-1], 2), round(float(gap.max()), 2)],
        "apical_segment_growth_px": round(float(seg[-1]), 3),
        "net_tip_ahead_of_end_median_px": round(float(np.median(np.linalg.norm(np.asarray(tips["tip_rc"])[idx] - end_img, axis=1))), 2),
        "net_tip_confidence_median": round(float(np.median(np.asarray(tips["tip_val"])[idx])), 3),
        "crop_offset_spread_px": np.ptp(off, axis=0).round(3).tolist(),
        "base_index": b, "base_s_px": round(float(s[b]), 1), "base_world_disp_px": (c[-1, b] - c[0, b]).round(2).tolist(),
        "stage_total_px": (st[-1] - st[0]).round(2).tolist(),
        "stage_steps_px": np.unique(steps.round(2), axis=0).tolist(),
        "stage_steps_um": np.unique((steps * PIXEL_UM).round(2), axis=0).tolist(),
        "stage_sign_lag_jitter_px": smooth,
        "speed_profile_px_per_h": [[round(float(s[j])), round(float(speed[j]), 2)] for j in range(0, b + 1, 3)],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tips", required=True)
    ap.add_argument("--track", nargs=2, action="append", required=True, metavar=("ROOT", "TRACK"))
    a = ap.parse_args()
    tips = json.loads(Path(a.tips).read_text())
    out = [{"root": r, "track": Path(f).name, **analyse(from_tracker_npz(f, root_id=r), tips[r])} for r, f in a.track]
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
