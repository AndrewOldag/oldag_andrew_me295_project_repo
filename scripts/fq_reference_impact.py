"""Report-only impact of the real frame_quality reference recompute (c033 audit S3-1, task c036).

The reference moved from 24 windows (72 values) to the 23 inside the current usable-window rule (69 values):
texture_contrast median 0.0648 -> 0.0641, focus median 0.0286 -> 0.0285; lowest values unchanged. An answer can
read differently only where a frame value lies between the old and new median (above or below the median flips).
For every frame_quality answer on a real window in the given traces: frames, and frames in that band.
No committed outcome is changed.

    python scripts/fq_reference_impact.py --traces c027=staging/c027/run/traces --out <json>
"""
import argparse
import json
import sys
from pathlib import Path

OLD = {"texture_contrast": 0.0648, "focus": 0.0286}
NEW = {"texture_contrast": 0.0641, "focus": 0.0285}


def flips(frame):
    """Measures whose side of the median differs between the old and new reference."""
    return [k for k in OLD if frame.get(k) is not None and (frame[k] < OLD[k]) != (frame[k] < NEW[k])]


def answers(folder):
    """(task id, frames) of every executed frame_quality answer in the folder's trace files."""
    for p in sorted(Path(folder).rglob("*trace.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            act = d.get("action") or {}
            res = d.get("result")
            if (act.get("name") == "request_info" and (act.get("args") or {}).get("kind") == "frame_quality"
                    and isinstance(res, dict) and "frames" in res):
                yield d.get("task_id"), res["frames"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--traces", action="append", required=True, help="NAME=DIR")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    out = {"old": OLD, "new": NEW, "sets": {}}
    for spec in args.traces:
        name, folder = spec.split("=", 1)
        n_ans, n_frames, hit = 0, 0, {}
        windows = set()
        for task, frames in answers(folder):
            n_ans += 1
            windows.add(task)
            for f in frames:
                n_frames += 1
                for k in flips(f):
                    hit.setdefault(task, []).append(f"frame {f.get('frame')} {k}")
        out["sets"][name] = {"answers": n_ans, "windows": len(windows), "frames": n_frames,
                             "frames_in_band": sum(len(v) for v in hit.values()), "windows_in_band": hit}
        print(name, {k: v for k, v in out["sets"][name].items() if k != "windows_in_band"}, sorted(hit))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
