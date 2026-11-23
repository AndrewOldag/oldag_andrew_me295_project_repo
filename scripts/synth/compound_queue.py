"""c029 tracker runs on the cluster (spec 2026-11-20, Cluster for everything) with the synthetic-rod job kind
(scripts/rod_jobs.py). Submit and forget; both steps can be rerun at any time.

  python scripts/synth/compound_queue.py jobs [--equivalence]      # job list and worst-case cost, no submit
  python scripts/synth/compound_queue.py submit [--equivalence]
  python scripts/synth/compound_queue.py fetch
  python scripts/synth/compound_queue.py equivalence               # cluster vs VM tracks of the 2 check rods
  python scripts/synth/compound_queue.py --set c029b jobs|submit|fetch   # supplement c029b (heldout_supplement.py)

Jobs: every label state of heldout_compound.label_states not cached, on the rod and its moved copy. register_frames
states use `register_v2` (measure/remedies.apply_remedy; inbox compound items 5-6). `--equivalence`: the
unremedied run of 2 rods already tracked on the VM, into `tracks_eq`; `equivalence` compares them (limit 1e-6 px,
as 2026-10-23). Settings: private/compound_cluster.yaml (own cluster work and code folders; the c027 ledger, cap
and spend stop). Rods: staging/rods_c029 (heldout_compound.py render).
`--set c029b`: the 48 supplement candidates (staging/rods_c029b, tracks_c029b, queue staging/c029b_queue, job
prefix c029b); the cluster vs VM equivalence of c029 holds for it (same cluster folders, code and tracker).
"""
import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import retrack_queue as rq  # noqa: E402
import rod_jobs  # noqa: E402
import heldout_compound as hc  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402

STATE = ROOT / "staging" / "c029_queue"
EQ_RODS = ("v3_growth_zone_drift_low_texture_s40", "v3_growth_zone_focus_drift_z3_s40")
EQ_DIR = STATE / "equivalence"
PREFIX = "c029"
EQ_FILE = STATE / "equivalence.json"


def use_set(name):
    """Point this queue at a test set: c029 (default) or the supplement c029b."""
    global STATE, PREFIX
    if name == "c029b":
        import heldout_supplement
        heldout_supplement.use()
        STATE, PREFIX = ROOT / "staging" / "c029b_queue", "c029b"


def config_path():
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout.strip()
    for p in (ROOT / "private" / "compound_cluster.yaml",
              (ROOT / common).resolve().parent / "private" / "compound_cluster.yaml"):
        if p.exists():
            return p
    sys.exit("private/compound_cluster.yaml missing")


def paused_rows():
    """Rows for the states paused method runs need (heldout_compound.PAUSED), rod and moved copy, not cached."""
    rows, seen = [], set()
    for line in (hc.PAUSED.read_text().splitlines() if hc.PAUSED.exists() else []):
        d = json.loads(line)
        st = TrackSettings(**d["settings"])
        for rid in (d["rod"], d["rod"] + "_moved"):
            name = f"{rid}__{st.tag()}.npz"
            if name in seen or Path(f"{hc.CACHE / name}.ok").exists():
                continue
            seen.add(name)
            rows.append({"job": name, "rid": rid, "settings": json.dumps(asdict(st), sort_keys=True), "sub": "tracks"})
    return rows


def job_rows(equivalence=False, paused=False):
    """[{job, rid, settings, sub}]: one row per tracker run not cached."""
    hc.point_v3_here()
    if paused:
        return paused_rows()
    rows = []
    if equivalence:
        st = TrackSettings(stride=1)
        for rid in EQ_RODS:
            name = f"{rid}__{st.tag()}.npz"
            if not (EQ_DIR / f"{name}.ok").exists():
                rows.append({"job": name, "rid": rid, "settings": json.dumps(asdict(st), sort_keys=True),
                             "sub": "tracks_eq"})
        return rows
    for rod in hc.scored_rods():
        states = [st for _, st in hc.label_states(rod) if st is not None]
        for st in hc.tracked([([], s) for s in states]):
            for moved in (False, True):
                rid = rod.id(moved)
                name = f"{rid}__{st.tag()}.npz"
                if Path(f"{hc.CACHE / name}.ok").exists():
                    continue
                rows.append({"job": name, "rid": rid, "settings": json.dumps(asdict(st), sort_keys=True),
                             "sub": "tracks"})
    return rows


def local_dir(row):
    return EQ_DIR if row.get("sub") == "tracks_eq" else hc.CACHE


def equivalence():
    """Cluster tracks of the 2 check rods against their VM tracks."""
    from local_equivalence import compare
    out = []
    for rid in EQ_RODS:
        name = f"{rid}__{TrackSettings(stride=1).tag()}.npz"
        a, b = EQ_DIR / name, hc.CACHE / name
        if not a.exists():
            out.append({"rod": rid, "result": "cluster track not fetched"})
            continue
        c = compare(a, b)
        out.append({"rod": rid, "max_abs_diff": c["max_abs_diff"], "arrays": c["arrays"], "pass": c["max_abs_diff"] <= 1e-6})
    return out


def main(argv=None):
    import yaml
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["jobs", "submit", "fetch", "equivalence"])
    ap.add_argument("--equivalence", action="store_true")
    ap.add_argument("--paused", action="store_true", help="the states paused method runs need")
    ap.add_argument("--set", choices=["c029", "c029b"], default="c029")
    a = ap.parse_args(argv)
    use_set(a.set)
    if a.set != "c029" and (a.equivalence or a.step == "equivalence"):
        sys.exit("equivalence is checked on c029 only")
    STATE.mkdir(parents=True, exist_ok=True)
    if a.step == "equivalence":
        res = equivalence()
        (STATE / "equivalence.json").write_text(json.dumps(res, indent=1))
        print(json.dumps(res))
        return 0
    if a.step == "jobs":
        rows = job_rows(a.equivalence, a.paused)
        print(f"{len(rows)} tracker runs, {len({r['rid'] for r in rows})} array tasks; "
              f"worst case ${rod_jobs.worst_case_usd(rows)}")
        return 0
    cfg = config_path()
    runner = rq.make_runner(cfg)
    remote = rq.Remote(runner)
    sdir = yaml.safe_load(cfg.read_text())["c029_storage_dir"]
    if a.step == "submit":
        if not a.equivalence and not EQ_FILE.exists():
            sys.exit("equivalence first: submit --equivalence, fetch, equivalence")
        if not a.equivalence and not all(r.get("pass") for r in json.loads(EQ_FILE.read_text())):
            sys.exit("equivalence failed: stop, Needs Andrew")
        mover = rod_jobs.RodMover(runner, sdir, hc.RODS)
        print(rod_jobs.submit(runner, remote, mover, job_rows(a.equivalence, a.paused), STATE, prefix=PREFIX))
    else:
        print(rod_jobs.fetch(runner, remote, STATE, sdir, local_dir, prefix=PREFIX))
    return 0


if __name__ == "__main__":
    sys.exit(main())
