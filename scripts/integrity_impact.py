"""Report-only impact of the integrity-gate fix (c033 audit S2-1, task c036).

Every remedied track in a cache (any track of a window other than its base `st1` track) is gated against its base
with the option A gate (relative_integrity, config/integrity_relative_k.yaml) twice: with checker/checks.py at
--old-rev and with the working tree. Lists every track whose gate result changes. Base tracks: frames that cannot be
measured and lost centre points, which decide whether an in-process (midline) remedy on them can change.
No committed outcome is changed.

    python scripts/integrity_impact.py --old-rev 24f64ed --cache c027=staging/c027/tracks \
        --cache c029=<compound>/staging/tracks_c029 --out results/2026-11-23_audit_fixes/integrity
"""
import argparse
import csv
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from checker import checks as new  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402

NAME = re.compile(r"^(?P<id>.+?)__(?P<setting>st\d[^_]*(?:_[A-Za-z0-9]+)*?)(?P<suffix>__L\d+)?\.npz$")


def load_old(rev):
    src = subprocess.run(["git", "show", f"{rev}:checker/checks.py"], cwd=ROOT, capture_output=True, text=True,
                         check=True).stdout
    path = Path(tempfile.mkdtemp()) / "checks_old.py"
    path.write_text(src, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("checks_old", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def base_setting(settings):
    """`st1` when cached; else the bare setting (no remedy part) with the most remedied tracks built on it
    (c029 low_texture_fast windows start from st12)."""
    if "st1" in settings:
        return "st1"
    bare = [s for s in settings if "_" not in s]
    return max(bare, key=lambda b: sum(s.startswith(b + "_") for s in settings), default=None)


def pairs(cache):
    """(window id, base path, remedied path) for every remedied track with its base in the cache. Rigid-motion
    copies (`<id>_moved`) are not remedied tracks and are skipped."""
    tracks = {}
    for p in sorted(Path(cache).glob("*.npz")):
        m = NAME.match(p.name)
        if m and not m.group("id").endswith("_moved"):
            tracks.setdefault(m.group("id"), {})[m.group("setting")] = p
    for wid, by in sorted(tracks.items()):
        b = base_setting(by)
        for setting, p in sorted(by.items()):
            if setting != b:
                yield wid, by.get(b), p


def base_state(rec):
    c = rec.centre
    n_ok = np.isfinite(c[..., 0]).sum(axis=1)
    return {"lost_frames": int(np.sum(n_ok < 3)), "lost_points": int(np.sum(~np.isfinite(c[..., 0])))}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--old-rev", required=True)
    ap.add_argument("--cache", action="append", required=True, help="NAME=DIR")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    old = load_old(args.old_rev)
    k = new.load_relative_k()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows, bases, summary = [], [], {}
    for spec in args.cache:
        name, cache = spec.split("=", 1)
        n = changed = no_base = 0
        seen = set()
        for wid, base, p in pairs(cache):
            if base is None:
                no_base += 1
                continue
            try:
                rb, rr = from_tracker_npz(base), from_tracker_npz(p)
            except Exception as e:  # unreadable cache file
                rows.append({"set": name, "window": wid, "track": p.name, "error": type(e).__name__})
                continue
            if base not in seen:
                seen.add(base)
                bases.append({"set": name, "window": wid, **base_state(rb)})
            g_old = old.integrity_gate(old.relative_integrity(rr, rb, k))
            res = new.relative_integrity(rr, rb, k)
            g_new = new.integrity_gate(res)
            v = {r.check: r.value for r in res}
            n += 1
            changed += g_old != g_new
            rows.append({"set": name, "window": wid, "track": p.name, "gate_old": g_old, "gate_new": g_new,
                         "changed": g_old != g_new, "lost_frames": int(v["integrity_lost_frames"]),
                         "lost_points": base_state(rr)["lost_points"],
                         "rel_inversions": round(v["integrity_rel_inversions"], 4),
                         "rel_gap_ratio": round(v["integrity_rel_gap_ratio"], 4),
                         "rel_lateral": round(v["integrity_rel_lateral"], 4)})
        bs = [b for b in bases if b["set"] == name]
        summary[name] = {"remedied_tracks": n, "gate_changed": changed, "no_base_track": no_base,
                         "base_tracks": len(bs), "bases_with_lost_points": sum(b["lost_points"] > 0 for b in bs),
                         "bases_with_lost_frames": sum(b["lost_frames"] > 0 for b in bs)}
        print(name, summary[name], flush=True)
    fields = ["set", "window", "track", "gate_old", "gate_new", "changed", "lost_frames", "lost_points",
              "rel_inversions", "rel_gap_ratio", "rel_lateral", "error"]
    with open(out / "tracks.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fields)
        w.writeheader()
        w.writerows(rows)
    with open(out / "bases.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, ["set", "window", "lost_frames", "lost_points"])
        w.writeheader()
        w.writerows(bases)
    (out / "summary.json").write_text(json.dumps({"old_rev": args.old_rev, "k": k, "sets": summary}, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
