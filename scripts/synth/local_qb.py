"""Run a tracker-side script (scripts/remote/qb_track.py, scripts/synth/make_rod.py) on this machine.

  <tracker env python> scripts/synth/local_qb.py <script> [args ...]

The tracker source (Quantum Borland, a private repository) is put on sys.path from
staging/qb_tracker (git-ignored; an export of the tracker commit the freeze runs used).
The VM tracker env has no torch: qb_track.py imports it only to pin its thread count, and
the CPU tracking path does not use it, so a stand-in module with the thread calls is
used when torch is missing. Tracks are checked against the freeze v4 cache before use
(results/2026-11-18_heldout_compound/README.md, local equivalence).
"""
import runpy
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRACKER = ROOT / "staging" / "qb_tracker"


def torch_stand_in():
    t = types.ModuleType("torch")
    t.set_num_threads = t.set_num_interop_threads = lambda n: None
    t.get_num_threads = lambda: 1
    t.__stand_in__ = True
    return t


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if not TRACKER.is_dir():
        sys.exit(f"tracker source not found: {TRACKER.relative_to(ROOT)}")
    sys.path.insert(0, str(TRACKER))
    try:
        import torch  # noqa: F401
    except ImportError:
        sys.modules["torch"] = torch_stand_in()
    script = str(Path(sys.argv[1]).resolve())
    sys.argv = [script] + sys.argv[2:]
    runpy.run_path(script, run_name="__main__")


if __name__ == "__main__":
    main()
