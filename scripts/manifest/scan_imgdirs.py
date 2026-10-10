"""Scan the 24 h kinematics folders and draft a root manifest.

Runs in the `qb` env. Reads SlideBook metadata and a few
frames per root. Writes nothing inside the data folders.

    python scan_imgdirs.py --data <folder holding the experiment folders> --out <output folder>

Outputs in --out:
    imgdirs.csv        one row per .imgdir
    manifest_draft.csv one row per root position (experiment x chamber code)
    thumbs/<id>_{start,mid,end}.png, thumbs/<id>.gif
"""
import argparse
import csv
import re
import statistics
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image

NAME_RE = re.compile(
    r"^(?P<prefix>.+?) - (?P<pos>[a-z]+)(?P<num>\d+) ?\[(?P<tag>[^\]]*)\]\s*(?P<kind>3DMontage|Montage)?\s*$"
)

# Condition guesses from chamber-code prefixes. Andrew confirms every row.
CONDITION_GUESS = {
    "drought": {"c": "control", "m": "mannitol"},
    "recovery_0721": {"c": "control?", "m": "mannitol then recovery?"},
    "recovery_0727": {"cc": "control then control?", "mc": "mannitol then control (recovery)?",
                      "mm": "mannitol then mannitol?"},
}


def decode(s):
    """SlideBook escapes: '_#32;' is a space, '#91;' is '['."""
    return re.sub(r"_?#(\d+);", lambda m: chr(int(m.group(1))), s).strip()


def first(text, key):
    m = re.search(rf"^\s*{key}: (.*)$", text, re.M)
    return m.group(1).strip() if m else None


def number_list(text, key):
    """Values of a SlideBook '<key>: [n, v1, v2, ...]' block."""
    m = re.search(rf"{key}: \[(.*?)\]", text, re.S)
    if not m:
        return []
    return [float(v) for v in m.group(1).replace("\n", "").split(",") if v.strip()]


def read_imgdir(d):
    rec = (d / "ImageRecord.yaml").read_text(errors="replace")
    chan = (d / "ChannelRecord.yaml").read_text(errors="replace")
    name = decode(first(rec, "mName") or "")
    m = NAME_RE.match(name)
    elapsed = number_list((d / "ElapsedTimes.yaml").read_text(errors="replace"), "theElapsedTimes")[1:]
    stage = number_list((d / "StagePositionData.yaml").read_text(errors="replace"), "StructArrayValues")
    xy = {(round(stage[i]), round(stage[i + 1])) for i in range(0, len(stage) - 2, 3)}
    aux = (d / "AuxData.yaml").read_text(errors="replace") if (d / "AuxData.yaml").exists() else ""
    tracking = "Stage_#32;Tracking" in aux
    gaps = np.diff(elapsed) / 1000 if len(elapsed) > 1 else np.array([])
    y, mo, dd, hh, mi = (int(first(rec, k) or 0) for k in ("mYear", "mMonth", "mDay", "mHour", "mMinute"))
    return {
        "experiment": d.parent.parent.name,
        "test_dir": d.parent.name,
        "imgdir": d.name,
        "name": name,
        "prefix": m.group("prefix") if m else "",
        "position": (m.group("pos") + m.group("num")) if m else "",
        "pos_letters": m.group("pos") if m else "",
        "tag": m.group("tag") if m else "",
        "kind": (m.group("kind") or "raw") if m else "unparsed",
        "n_timepoints": int(first(rec, "mNumTimepoints") or 0),
        "n_image_files": sum(1 for p in d.glob("ImageData_*.npy")),
        "width": int(first(rec, "mWidth") or 0),
        "height": int(first(rec, "mHeight") or 0),
        "interval_s": int(first(chan, "mTimeLapseInterval") or 0) / 1000,
        "start_time": f"{y:04d}-{mo:02d}-{dd:02d} {hh:02d}:{mi:02d}",
        "duration_h": round(elapsed[-1] / 3.6e6, 2) if elapsed else 0,
        "median_step_s": round(float(np.median(gaps)), 1) if gaps.size else 0,
        "max_step_s": round(float(gaps.max()), 1) if gaps.size else 0,
        "n_stage_xy": len(xy),
        "stage_tracking_log": "yes" if tracking else "no",
    }


def to_8bit(img, lo, hi):
    return (np.clip((img - lo) / max(hi - lo, 1), 0, 1) * 255).astype(np.uint8)


def frame(d, t):
    return np.load(d / f"ImageData_Ch0_TP{t:07d}.npy", mmap_mode="r")[0].astype(np.float32)


def shrink(img, f):
    h, w = (img.shape[0] // f) * f, (img.shape[1] // f) * f
    return img[:h, :w].reshape(h // f, f, w // f, f).mean(axis=(1, 3))


def make_previews(job):
    """Start, middle and end PNGs plus a GIF with one frame per 2 h."""
    root_id, d, n, step_s, out = job
    d, out = Path(d), Path(out)
    ref = frame(d, 0)
    lo, hi = np.percentile(ref, [1, 99.5])
    for label, t in (("start", 0), ("mid", n // 2), ("end", n - 1)):
        Image.fromarray(to_8bit(shrink(frame(d, t), 4), lo, hi)).save(out / f"{root_id}_{label}.png", optimize=True)
    every = max(1, round(7200 / step_s)) if step_s else max(1, n // 12)
    frames = [Image.fromarray(to_8bit(shrink(frame(d, t), 6), lo, hi)) for t in range(0, n, every)]
    frames[0].save(out / f"{root_id}.gif", save_all=True, append_images=frames[1:], duration=400, loop=0)
    return root_id


def experiment_key(exp):
    if "drought" in exp:
        return "drought"
    return "recovery_" + exp[4:8]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    data, out = Path(args.data), Path(args.out).expanduser()
    (out / "thumbs").mkdir(parents=True, exist_ok=True)

    dirs = sorted(data.glob("*/test*.dir/*.imgdir"))
    with ProcessPoolExecutor(args.workers) as ex:
        rows = list(ex.map(read_imgdir, dirs))
    with open(out / "imgdirs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    groups = {}
    for r in rows:
        groups.setdefault((r["experiment"], r["position"]), []).append(r)

    # Typical timepoint count per experiment, to flag short runs.
    typical = {}
    for exp in {r["experiment"] for r in rows}:
        typical[exp] = statistics.mode(r["n_timepoints"] for r in rows if r["experiment"] == exp and r["kind"] != "raw")

    roots, jobs = [], []
    for (exp, pos), rs in sorted(groups.items()):
        montages = [r for r in rs if r["kind"] in ("Montage", "3DMontage")]
        raws = [r for r in rs if r["kind"] == "raw"]
        main_r = montages[0] if montages else rs[0]
        root_id = f"{exp[4:8]}_{pos or 'unparsed'}"
        flags = []
        if not pos:
            flags.append("name not parsed")
        if len(montages) != 1:
            flags.append(f"{len(montages)} montage folders")
        if len(raws) > 1:
            flags.append(f"{len(raws)} raw folders")
        if any(r["kind"] == "3DMontage" for r in rs):
            flags.append("labelled 3DMontage")
        if any(r["tag"] not in ("2", "") for r in rs):
            flags.append("unusual tag [" + ",".join(sorted({r['tag'] for r in rs})) + "]")
        if main_r["n_image_files"] != main_r["n_timepoints"]:
            flags.append(f"{main_r['n_image_files']} image files for {main_r['n_timepoints']} timepoints")
        if main_r["n_timepoints"] < typical[exp] - 2:
            flags.append(f"short run ({main_r['n_timepoints']} vs {typical[exp]} timepoints)")
        if main_r["median_step_s"] and main_r["max_step_s"] > 2 * main_r["median_step_s"]:
            flags.append(f"gap of {main_r['max_step_s']:.0f} s")
        letters = main_r["pos_letters"]
        roots.append({
            "id": root_id,
            "experiment": exp,
            "experiment_type": "drought" if "drought" in exp else "recovery",
            "position": pos,
            "condition_guess": CONDITION_GUESS[experiment_key(exp)].get(letters, "?"),
            "montage_imgdir": f"{main_r['test_dir']}/{main_r['imgdir']}" if montages else "",
            "raw_imgdir": ";".join(f"{r['test_dir']}/{r['imgdir']}" for r in raws),
            "capture_name": main_r["name"],
            "start_time": main_r["start_time"],
            "n_timepoints": main_r["n_timepoints"],
            "duration_h": main_r["duration_h"],
            "step_s": main_r["median_step_s"],
            "max_step_s": main_r["max_step_s"],
            "size_px": f"{main_r['width']}x{main_r['height']}",
            "stage_tracking_log": main_r["stage_tracking_log"],
            "flags": "; ".join(flags),
            "root_label": "",
            "condition": "",
            "include": "",
            "notes": "",
        })
        jobs.append((root_id, str(data / exp / main_r["test_dir"] / main_r["imgdir"]),
                     main_r["n_timepoints"], main_r["median_step_s"], str(out / "thumbs")))

    with open(out / "manifest_draft.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(roots[0]))
        w.writeheader()
        w.writerows(roots)
    print(f"{len(rows)} imgdirs, {len(roots)} root positions")

    with ProcessPoolExecutor(args.workers) as ex:
        for i, rid in enumerate(ex.map(make_previews, jobs), 1):
            if i % 20 == 0:
                print(f"previews {i}/{len(jobs)}")
    print("done")


if __name__ == "__main__":
    main()
