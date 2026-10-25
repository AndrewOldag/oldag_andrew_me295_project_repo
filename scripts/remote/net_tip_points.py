"""Per-frame net tip point and net midline end of one window, for the closure tests (spec 2026-10-24b A).

usage: python net_tip_points.py NAME HTPMID.npz NETMID.npz [NAME HTPMID.npz NETMID.npz ...]

HTPMID: batch_midlines output covering the window; NETMID: the window's net midline file (net_to_midline.py).
Prints JSON {NAME: {htp_frames, mid_frames, tip_rc, tip_val, end_rc}}: the net's own tip point (`tip_xy`, as
row, col), its confidence, and the tip end of the midline polyline, image coordinates. Reads only.
"""
import json
import sys

import numpy as np

out = {}
args = sys.argv[1:]
for name, h, n in zip(args[0::3], args[1::3], args[2::3]):
    z, m = np.load(h, allow_pickle=True), np.load(n)
    out[name] = {"htp_frames": np.asarray(z["frames"], int).tolist(), "mid_frames": np.asarray(m["frames"], int).tolist(),
                 "tip_rc": np.asarray(z["tip_xy"], float)[:, ::-1].round(3).tolist(),
                 "tip_val": np.asarray(z["tip_val"], float).round(4).tolist(),
                 "end_rc": m["midline_image"][:, 0].round(3).tolist()}
print(json.dumps(out))
