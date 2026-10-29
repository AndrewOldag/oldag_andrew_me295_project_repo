"""Track real windows ahead of the checks: `RealRunner.measure` with the initial settings for every window.

  python scripts/real_track.py --config private/real_runner_c019.yaml [--windows ROOT__wA-B ...] [--log FILE]

Every window listed in the config (or only --windows) is tracked on its host as the slice would track it: the
whole-pixel reference copy and its shifted twin, at TRACK_LENGTH (measure/real_runner.py). Outputs land in the
runner cache, so a later scripts/real_slice.py run reuses them and a restarted run skips finished windows. A busy
host (load, 2-job limit, disk) is waited out, 120 s per check. A window whose midline file is missing on the host is
skipped, not built there. One line of JSON per window goes to --log.
"""
import argparse
import json
import shlex
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from measure.real_runner import HostBusy, RealRunner, RealWindow  # noqa: E402


def parse_wid(wid):
    root, _, w = wid.partition("__w")
    a, b = w.split("-")
    return RealWindow(root, float(a), float(b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--windows", nargs="+", default=None)
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    runner = RealRunner(a.config)
    runner.sync_code()
    wids = a.windows or list(runner.windows)
    log = Path(a.log) if a.log else None
    for wid in wids:
        w = parse_wid(wid)
        try:                       # never build a net midline on the host here (lab server: storage, light jobs only)
            runner._ssh(f"test -f {shlex.quote(runner.midline_path(w))}")
        except RuntimeError:
            print(json.dumps({"window": wid, "skipped": "no midline file on the host"}), flush=True)
            continue
        t0 = time.time()
        while True:
            try:
                m = runner.measure(w, runner.initial_settings(w))
                break
            except HostBusy as e:
                print(f"{wid}: host busy ({e}); waiting 120 s", flush=True)
                time.sleep(120)
        row = {"window": wid, "wall_s": round(time.time() - t0, 1)}
        print(json.dumps(row), flush=True)
        if log:
            with log.open("a") as f:
                f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    main()
