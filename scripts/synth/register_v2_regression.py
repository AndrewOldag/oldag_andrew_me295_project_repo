"""c031 R5 (spec 2026-11-20): register_v2 against the old register_frames on the freeze v4 rods it repaired.

  python scripts/synth/register_v2_regression.py seed --from <freeze v4 track cache>   # base, v1 and truth files
  python scripts/synth/register_v2_regression.py render       # the rods and moved copies, on this machine
  python scripts/synth/register_v2_regression.py jobs         # tracker runs and worst-case cost, no submit
  python scripts/synth/register_v2_regression.py submit       # scripts/rod_jobs.py, one array task per rod
  python scripts/synth/register_v2_regression.py fetch
  python scripts/synth/register_v2_regression.py report       # results/2026-11-20_registration_fix/regression.*

Rods: the 6 freeze v4 rods labelled accept_repaired with register_frames (rigid_drift z0.5 and
bad_stage_correction z3, seeds 26-28). register_v2 settings come from measure/remedies.apply_remedy on the cached
unremedied run, as an agent's remedy step makes them. Outcome by the freeze v4 rule (scored_v3.evaluate with the v4
candidate): accepted after the remedy if every check passes, correct if the measurement is good against truth.
Also the option A integrity gate against the rod's own unremedied track. Settings: private/c031_cluster.yaml (own
cluster work and code folders; the c027 ledger, cap and spend stop). No tracker run on this machine.
"""
import argparse
import json
import subprocess
import sys
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import retrack_queue as rq  # noqa: E402
import rod_jobs  # noqa: E402
import scored_v3 as v3  # noqa: E402
import scored_v4  # noqa: E402
from checker import integrity_gate, load_relative_k, relative_integrity  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.remedies import apply_remedy  # noqa: E402

CACHE = ROOT / "staging" / "tracks_c031"
RODS = ROOT / "staging" / "rods_c031"
STATE = ROOT / "staging" / "c031_queue"
OUT = ROOT / "results" / "2026-11-20_registration_fix"
LABELS = ROOT / "results" / "2026-10-25_freeze_v4" / "labels.json"
PREFIX = "c031"


def point():
    scored_v4.point_v3_at_v4()
    v3.CACHE = CACHE


def rods():
    labels = json.loads(LABELS.read_text())["labels"]
    return [r for r in v3.scored_rods() if labels.get(r.id(), {}).get("sequence") == ["register_frames"]]


def states(rod):
    """(unremedied, v1 as labelled, register_v2 as apply_remedy gives it)."""
    base = v3.initial(rod)
    v1 = replace(base, register=True, register_from_px=v3.band_start(rod))
    v2, _ = apply_remedy(base, "register_frames", None, v3.base_radius(rod), from_tracker_npz(v3.out_file(rod, base)))
    return base, v1, v2


def seed(src):
    src, n = Path(src), 0
    CACHE.mkdir(parents=True, exist_ok=True)
    for rod in rods():                         # unremedied and v1 runs of the rod and its moved copy, and the truth
        for p in src.glob(f"{rod.id()}*.npz"):
            if not (CACHE / p.name).exists():
                (CACHE / p.name).write_bytes(p.read_bytes())
                n += 1
    print(f"seeded {n} files into {CACHE.name}")


def render():
    RODS.mkdir(parents=True, exist_ok=True)
    for rod in rods():
        for moved in (False, True):
            rid = rod.id(moved)
            if (RODS / f"{rid}.ok").exists():
                continue
            if (RODS / f"{rid}.imgdir").exists():
                sys.exit(f"{rid}: a stopped render; remove staging/rods_c031/{rid}* by hand and rerun")
            subprocess.run([sys.executable, "scripts/synth/make_rod.py", "--out", str(RODS)] + rod.options()
                           + (["--moved"] if moved else []), cwd=ROOT, check=True)
        with np.load(RODS / f"{rod.id()}_truth.npz") as a, np.load(CACHE / f"{rod.id()}_truth.npz") as b:
            # floats within 1e-12 (the re-render differs from the 2026-10-25 one by about 1e-18); the rest exactly
            same = sorted(a.files) == sorted(b.files) and all(
                np.allclose(a[k], b[k], rtol=0, atol=1e-12, equal_nan=True) if b[k].dtype.kind in "fc"
                else np.array_equal(a[k], b[k]) for k in b.files)
        print(f"{rod.id()}: rendered; truth equal to the freeze v4 truth within 1e-12: {same}")
        if not same:
            sys.exit("rendered rod differs from freeze v4: stop")


def job_rows():
    rows = []
    for rod in rods():
        _, _, v2 = states(rod)
        for moved in (False, True):
            name = f"{rod.id(moved)}__{v2.tag()}.npz"
            if not Path(f"{CACHE / name}.ok").exists():
                rows.append({"job": name, "rid": rod.id(moved), "settings": json.dumps(asdict(v2), sort_keys=True),
                             "sub": "tracks"})
    return rows


def config_path():
    common = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=ROOT, capture_output=True, text=True,
                            check=True).stdout.strip()
    for p in (ROOT / "private" / "c031_cluster.yaml", (ROOT / common).resolve().parent / "private" / "c031_cluster.yaml"):
        if p.exists():
            return p
    sys.exit("private/c031_cluster.yaml missing")


def report():
    k = load_relative_k()
    rows = []
    for rod in rods():
        base, v1, v2 = states(rod)
        row = {"rod": rod.id(), "v1_tag": v1.tag(), "v2_tag": v2.tag()}
        for name, st in (("v1", v1), ("v2", v2)):
            e = v3.evaluate(rod, st, after_remedy=True)
            if e is None:
                row[name] = "not cached"
                continue
            gate = relative_integrity(from_tracker_npz(v3.out_file(rod, st)), from_tracker_npz(v3.out_file(rod, base)), k)
            reg = e["preprocess"].get("register", {})
            row[name] = {"closure": e.get("closure"), "all_pass": e["all_pass"], "good": e["good"],
                         "outcome": "accept_repaired correct" if e["all_pass"] and e["good"]
                         else "false accept" if e["all_pass"] else "not accepted",
                         "gate": integrity_gate(gate), **{g.check: g.value for g in gate},
                         "final_rotation_deg": reg.get("final_rotation_deg"),
                         "final_band_motion_px": reg.get("final_band_motion_px"), "plausible": reg.get("plausible")}
        rows.append(row)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "regression.json").write_text(json.dumps({"k": k, "rods": rows}, indent=1, default=str))
    lines = ["| Rod | v1 outcome | v1 gate | v2 outcome | v2 gate | v2 rotation, deg | v2 band motion, px |",
             "| :-- | :-- | :-- | :-- | :-- | --: | --: |"]
    for r in rows:
        a, b = r["v1"], r["v2"]
        f = lambda d, key: d.get(key) if isinstance(d, dict) else d
        lines.append(f"| {r['rod']} | {f(a, 'outcome')} | {f(a, 'gate')} | {f(b, 'outcome')} | {f(b, 'gate')} | "
                     f"{f(b, 'final_rotation_deg')} | {f(b, 'final_band_motion_px')} |")
    (OUT / "regression.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main(argv=None):
    import yaml
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["seed", "render", "jobs", "submit", "fetch", "report"])
    ap.add_argument("--from", dest="src")
    a = ap.parse_args(argv)
    point()
    STATE.mkdir(parents=True, exist_ok=True)
    if a.step == "seed":
        return seed(a.src)
    if a.step == "render":
        return render()
    if a.step == "report":
        return report()
    if a.step == "jobs":
        rows = job_rows()
        for r in rows:
            print(r["job"])
        print(f"{len(rows)} tracker runs, {len({r['rid'] for r in rows})} array tasks; "
              f"worst case ${rod_jobs.worst_case_usd(rows)}")
        return 0
    cfg = config_path()
    runner = rq.make_runner(cfg)
    remote = rq.Remote(runner)
    sdir = yaml.safe_load(cfg.read_text())["c031_storage_dir"]
    if a.step == "submit":
        print(rod_jobs.submit(runner, remote, rod_jobs.RodMover(runner, sdir, RODS), job_rows(), STATE, prefix=PREFIX))
    else:
        print(rod_jobs.fetch(runner, remote, STATE, sdir, lambda row: CACHE, prefix=PREFIX))
    return 0


if __name__ == "__main__":
    sys.exit(main())
