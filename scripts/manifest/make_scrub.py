"""Make time-stamped scrub frames for the review app.

Runs in the `qb` env, after scan_imgdirs.py:

    python make_scrub.py --data <folder holding the experiment folders> --out <output folder>

For each root in manifest_draft.csv: one JPEG every --every-min minutes of
elapsed time, with the time printed in the corner, in scrub/<id>/, plus
scrub/<id>.json with the time of each frame in hours.
"""
import argparse
import csv
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from scan_imgdirs import frame, number_list, shrink, to_8bit


def make(job):
    root_id, d, out, every_min, factor = job
    d, out = Path(d), Path(out)
    elapsed_h = np.array(number_list((d / "ElapsedTimes.yaml").read_text(errors="replace"), "theElapsedTimes")[1:]) / 3.6e6
    n = sum(1 for _ in d.glob("ImageData_*.npy"))
    elapsed_h = elapsed_h[:n]
    targets = np.arange(0, elapsed_h[-1] + 1e-9, every_min / 60)
    picks = sorted({int(np.argmin(np.abs(elapsed_h - t))) for t in targets} | {n - 1})
    ref = frame(d, 0)
    lo, hi = np.percentile(ref, [1, 99.5])
    font = ImageFont.load_default(size=18)
    rdir = out / root_id
    rdir.mkdir(parents=True, exist_ok=True)
    times = []
    for k, t in enumerate(picks):
        img = Image.fromarray(to_8bit(shrink(frame(d, t), factor), lo, hi)).convert("L")
        label = f"{elapsed_h[t]:5.2f} h  (frame {t})"
        draw = ImageDraw.Draw(img)
        x0, y0, x1, y1 = draw.textbbox((6, 4), label, font=font)
        draw.rectangle((x0 - 4, y0 - 3, x1 + 4, y1 + 3), fill=0)
        draw.text((6, 4), label, fill=255, font=font)
        img.save(rdir / f"{k:03d}.jpg", quality=82)
        times.append(round(float(elapsed_h[t]), 3))
    (out / f"{root_id}.json").write_text(json.dumps({"times_h": times, "frames": picks}))
    return root_id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--every-min", type=float, default=15)
    ap.add_argument("--factor", type=int, default=5, help="downsampling factor")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    out = Path(args.out).expanduser()
    rows = list(csv.DictReader((out / "manifest_draft.csv").open()))
    jobs = []
    for r in rows:
        d = r["montage_imgdir"] or r["raw_imgdir"].split(";")[0]
        jobs.append((r["id"], str(Path(args.data) / r["experiment"] / d), str(out / "scrub"), args.every_min, args.factor))
    with ProcessPoolExecutor(args.workers) as ex:
        for i, _ in enumerate(ex.map(make, jobs), 1):
            if i % 20 == 0:
                print(f"{i}/{len(jobs)}")
    print("done")


if __name__ == "__main__":
    main()
