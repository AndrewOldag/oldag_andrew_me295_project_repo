"""Registration diagnosis of one real window (spec 2026-11-20 R1). No tracking.

Runs in the tracker environment on a cluster node. Loads the window's frames and midline as qb_track.py does, then
(1) the chained pairwise fits of register_frames (v1): per pair t-1 -> t the rotation, band motion and ECC, the
chained map C_t = E_t ... E_1, and a check that its last map equals register_frames' own; (2) each frame fitted
directly to frame 0 (register_frames_v2, same band). Writes one JSON: rotations, motions and ECC values only.

  python scripts/remote/register_diag.py --imgdir R.imgdir --midline W_netmid.npz --from-h 6 --to-h 8 \
      --register-from-px 1075 --max-shift-px 46 --out W_register_diag.json
"""
import argparse
import json
import os
import sys
from dataclasses import replace
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"

import cv2                                      # noqa: E402
import numpy as np                              # noqa: E402

cv2.setNumThreads(1)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from measure import preprocess as pp                            # noqa: E402

from root_kinematics.slidebook_io import load_root_recording   # noqa: E402
from root_kinematics.stage_correction import cumulative_correction_px  # noqa: E402


def chained_pairs(frames, stage_px, midline, s_from, s_to, band_px=20.0, edge_px=25.0):
    """The pair loop of register_frames, keeping each pair's map and ECC."""
    T = len(frames)
    f = np.asarray(frames, np.float32)
    world = [cv2.warpAffine(f[t], pp._affine_cv(pp._shift(-stage_px[t])), f[t].shape[::-1],
                            flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP) for t in range(T)]
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
    E, ecc = [], []
    for t in range(1, T):
        line_w = midline[t - 1] + stage_px[t - 1]
        s = pp._arclength(line_w)
        part = line_w[(s >= s_from) & (s <= s_to)]
        mask = (pp._band(f[t].shape, part, band_px) & pp._inside(f[t].shape, stage_px[t - 1], edge_px)
                & pp._inside(f[t].shape, stage_px[t], edge_px)).astype(np.uint8)
        W = np.eye(2, 3, dtype=np.float32)
        try:
            cc, W = cv2.findTransformECC(world[t - 1], world[t], W, cv2.MOTION_EUCLIDEAN, crit, mask, 5)
        except cv2.error:
            cc = float("nan")
        E.append(pp._from_cv(W))
        ecc.append(float(cc))
    return E, ecc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--imgdir", required=True)
    ap.add_argument("--midline", required=True)
    ap.add_argument("--from-h", type=float, required=True)
    ap.add_argument("--to-h", type=float, required=True)
    ap.add_argument("--register-from-px", type=float, required=True)
    ap.add_argument("--max-shift-px", type=float, default=None)
    ap.add_argument("--pixel-um", type=float, default=2.105)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if Path(a.out).exists():
        sys.exit(f"output exists, not overwritten: {Path(a.out).name}")
    m = np.load(a.midline)
    rec = load_root_recording(Path(a.imgdir), pixel_size_um=a.pixel_um, lazy=True)
    t_h = rec.elapsed_s / 3600.0
    win = np.nonzero((t_h >= a.from_h) & (t_h <= a.to_h))[0]
    if "frames" in m.files and not np.array_equal(m["frames"], win):
        ap.error("midline file frames do not match the window")
    rec = replace(rec, images=rec.images[win].materialize(), stage_xy_um=rec.stage_xy_um[win],
                  elapsed_s=rec.elapsed_s[win])                 # as qb_track.py, stride 1
    frames = np.asarray(rec.images)
    mid = m["midline_image"].astype(float)
    stage = cumulative_correction_px(rec)
    line0 = mid[0] + stage[0]
    s0 = pp._arclength(line0)
    part = line0[s0 >= a.register_from_px]
    centre = np.nanmean(part, axis=0)

    E, ecc = chained_pairs(frames, stage, mid, a.register_from_px, np.inf)
    C = [np.eye(3)]
    for e in E:
        C.append(e @ C[-1])
    *_, C_v1, rep_v1 = pp.register_frames(frames, stage, mid, a.register_from_px, np.inf)
    pair = [pp._rigid_motion(e, centre) for e in E]
    chain = [pp._rigid_motion(c, centre) for c in C]
    *_, C_v2, rep_v2 = pp.register_frames_v2(frames, stage, mid, a.register_from_px, np.inf, a.max_shift_px)
    out = {"window_h": [a.from_h, a.to_h], "n_frames": int(len(win)), "register_from_px": a.register_from_px,
           "chained": {"pair_rotation_deg": [round(p[0], 4) for p in pair],
                       "pair_band_motion_px": [round(p[1], 3) for p in pair],
                       "pair_ecc": [None if not np.isfinite(e) else round(e, 5) for e in ecc],
                       "sum_pair_rotation_deg": round(float(np.sum([p[0] for p in pair])), 3),
                       "path_rotation_deg": [round(c[0], 4) for c in chain],
                       "path_band_motion_px": [round(c[1], 3) for c in chain],
                       "final_rotation_deg": round(chain[-1][0], 3), "final_band_motion_px": round(chain[-1][1], 2),
                       "equals_register_frames": bool(np.allclose(C[-1], C_v1[-1], atol=1e-6)),
                       "register_frames_report": rep_v1},
           "direct": rep_v2}
    Path(a.out).write_text(json.dumps(out, indent=1))
    print(json.dumps({"out": a.out, "chained_final_deg": out["chained"]["final_rotation_deg"],
                      "direct_final_deg": rep_v2["final_rotation_deg"]}))


if __name__ == "__main__":
    main()
