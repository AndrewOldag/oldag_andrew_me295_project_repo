"""Freeze v3 (docs/proposals/2026-10-23_freeze-v3.md, approved 2026-10-23): basis check, held-out sizing,
labels, all methods with repeats, metrics.

  python scripts/synth/scored_v3.py plan   --phase basis|sizing|labels|methods [--dry-run]   # start one sweep
  python scripts/synth/scored_v3.py status
  python scripts/synth/scored_v3.py fetch                                     # to staging/tracks_freeze_v3/
  python scripts/synth/scored_v3.py basis                                     # clean basis table, stop rule
  python scripts/synth/scored_v3.py sizing                                    # held-out sizes at v3 geometry
  python scripts/synth/scored_v3.py labels                                    # labels of the 51 scored rods
  python scripts/synth/scored_v3.py rules                                     # script and remedy tree
  python scripts/synth/scored_v3.py agents --method diagnostician|single_agent --repeat 0|1|2
  python scripts/synth/scored_v3.py eval                                      # metrics and tables

Rods: measure.rod.v3_cases (tip 96 px/h, growth zone at 200 px, tracked length 500 px, stage follows the tip).
Seeds (config/scoring_seeds.yaml, v3): sizing 10-12, clean basis 10-14, scoring 20-22. Tracker runs: one sweep
per `plan` (scripts/synth/sweep.py limits and lock); LLM runs add single load-checked jobs. Every tracker output
of this freeze is in CACHE; the cap is MAX_TRACKER_RUNS (Andrew, 2026-10-23). Outputs under OUT.
Stop rules (proposal sections 1 and 5): a clean basis value failing a threshold or the flank tolerance; held-out
sizes differing from v2; more than half of the labelled set in decline; a clean scored rod not accept_clean.
"""
import argparse
import json
import subprocess
import sys
import time
import traceback
import warnings
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agents import candidate  # noqa: E402
from agents.baselines import run_script, run_tree  # noqa: E402
from agents.executors import BlindSlice, Slice  # noqa: E402
from agents.launcher import load_config  # noqa: E402
from checker import load_thresholds, run_checks  # noqa: E402
from fix_sweep import BASE_RADIUS, entry  # noqa: E402
from heldout_sweep import config as runner_config  # noqa: E402
from measure import metrics  # noqa: E402
from measure.preprocess import registration_band_start  # noqa: E402
from measure.record import from_tracker_npz  # noqa: E402
from measure.remedies import TrackSettings  # noqa: E402
from measure.render_heldout import HELDOUT_FAULTS  # noqa: E402
from measure.rod import V3_BEND_RATES  # noqa: E402
from measure.runner import Measurement, RemoteRunner, Rod  # noqa: E402
from measure.score import (checks_pass, label_rod, load_tolerance, measurement_good, rod_tolerance,  # noqa: E402
                           truth_error, truth_summary)

warnings.simplefilter("ignore", RuntimeWarning)
FREEZE_TAG = "freeze-v3"
OUT = ROOT / "results" / "2026-10-23_freeze_v3"
CACHE = ROOT / "staging" / "tracks_freeze_v3"
TRACKS, SWEEP = "tracks_freeze_v3", "freeze_v3"
MAX_TRACKER_RUNS = 600                     # Andrew, 2026-10-23 (inbox freeze-v3 item 4)
PIXEL_UM = 2.105
GZ = "v3_growth_zone"
CLEAN = [GZ] + [f"v3_bend{d}" for d in V3_BEND_RATES] + ["v3_still"]
DEV = {"rigid_drift": "0.5", "displacement_exceeds_patch": "2x6", "width_change": None, "low_texture": "0.03",
       "midline_jitter": "3"}                                   # freeze v2 sizes
HELDOUT = {"bad_stage_correction": "3", "stage_log_missing": "1", "second_root": "30", "fast_rotation": "2",
           "flank_swap": "0.5", "partial_occlusion": "20"}       # v2 sizes; stage_log_missing new (approved)
LARGER = {"second_root": "45", "fast_rotation": "4", "bad_stage_correction": "10", "flank_swap": "1",
          "partial_occlusion": "30"}                            # sizing: tried only if the v2 size fails < 3 of 3
EXPECTED = {**{c: "accept_clean" for c in CLEAN},
            "rigid_drift": "accept_repaired", "displacement_exceeds_patch": "accept_repaired",
            "width_change": "accept_repaired", "bad_stage_correction": "accept_repaired",
            "stage_log_missing": "accept_repaired", "low_texture": "decline", "midline_jitter": "decline",
            "second_root": "decline", "fast_rotation": "decline", "flank_swap": "decline",
            "partial_occlusion": "decline"}
# fault names counted correct (v2 rule; stage_log_missing: proposal section 1)
NAMES = {**{f: {f} for f in DEV}, "second_root": {"second_root"}, "fast_rotation": {"fast_rotation"},
         "bad_stage_correction": {"bad_stage_correction"}, "flank_swap": {"unknown"},
         "partial_occlusion": {"low_texture", "unknown"}, "stage_log_missing": {"bad_stage_correction", "rigid_drift"}}
# clean scored rods whose good unremedied run fails a check: kept accept_clean, reported as checker false alarms
# (Andrew, 2026-10-23 18:15, inbox freeze-v3 item 7, option a)
CLEAN_FALSE_ALARM = {"v3_bend30_clean_s20"}
METHODS = ("script", "remedy_tree", "diagnostician", "single_agent")
LLM = ("diagnostician", "single_agent")
REPEATS = (0, 1, 2)
TH = load_thresholds()


def seeds(kind):
    v3 = yaml.safe_load((ROOT / "config" / "scoring_seeds.yaml").read_text())["v3"]
    return tuple(v3[kind])


# ------------------------------------------------------------------ rod sets

def kind(rod):
    """The scoring-set row of a rod: clean case name or fault name."""
    return rod.fault or rod.case


def basis_rods():
    return [Rod(c, None, s) for c in CLEAN for s in seeds("basis_seeds")]


def scored_rods():
    out = [Rod(c, None, s) for c in CLEAN for s in seeds("scoring_seeds")]
    sizes = {**DEV, **approved_heldout_sizes()}
    out += [Rod(GZ, f, s, size=sizes[f]) for f in list(DEV) + list(HELDOUT) for s in seeds("scoring_seeds")]
    return out


def approved_heldout_sizes():
    f = OUT / "sizing.json"
    if not f.exists():
        return dict(HELDOUT)
    return json.loads(f.read_text())["sizes"]


def initial(rod):
    from measure import render, render_heldout
    mod = render_heldout if rod.fault in HELDOUT_FAULTS else render
    _, movie = mod.image_case(rod.case, rod.fault, rod.seed, False, size=rod.size)
    return TrackSettings(stride=movie.stride)


# ------------------------------------------------------------------ cache

def out_file(rod, st, moved=False):
    return CACHE / f"{rod.id(moved)}__{replace(st, width_free=False).tag()}.npz"


def cached(rod, st):
    return out_file(rod, st).exists() and out_file(rod, st, True).exists()


def truth(rod):
    f = CACHE / f"{rod.id()}_truth.npz"
    if not f.exists():
        return None
    with np.load(f) as z:
        return {k: z[k] for k in z.files}


def tracker_runs_cached():
    return len(list(CACHE.glob("*__*.npz"))) if CACHE.exists() else 0


def evaluate(rod, st, after_remedy=False):
    """Checks, truth error and goodness of one state. None if not cached. after_remedy: the state follows a
    remedy; with the freeze v4 candidate on, a check it cannot compute counts as failing (C3 option a)."""
    if not cached(rod, st) or truth(rod) is None:
        return None
    rec, moved = from_tracker_npz(out_file(rod, st)), from_tracker_npz(out_file(rod, st, True))
    checks = run_checks(rec, moved, TH, ("plane_sections",) if st.width_free else ())
    t = truth(rod)
    err = truth_error(rec, t)
    tol = rod_tolerance(t, PIXEL_UM, load_tolerance())
    return {"rod": rod.id(), "tag": st.tag() + ("_wf" if st.width_free else ""),
            **{c.check: c.value for c in checks}, **{f"{c.check}_pass": c.passed for c in checks},
            "all_pass": checks_pass(checks, after_remedy and candidate.v4()), **err,
            "good": measurement_good(err, tol, st.width_free),
            "regr_limit": tol["regr_rms_pct_per_h"], "flank_limit": tol["flank_difference_rms_pct_per_h"],
            "truth": truth_summary(t, PIXEL_UM), "preprocess": rec.settings.get("preprocess", {})}


def band_start(rod):
    st = initial(rod)
    if not cached(rod, st):
        return None
    return int(round(registration_band_start(from_tracker_npz(out_file(rod, st)))))


def base_radius(rod):
    """The tracker's own disk radius on the unremedied run (14 px on the v3 rods, 15 on v2), as the executors
    use it for enlarge_patch (measure/remedies.py). None until that run is cached."""
    st = initial(rod)
    if not cached(rod, st):
        return None
    return int(from_tracker_npz(out_file(rod, st)).settings.get("disk_radius") or BASE_RADIUS)


def enlarged(rod, base, factor):
    r = base_radius(rod)
    return None if r is None else replace(base, disk_radius=int(round(r * factor)))


def label_states(rod):
    """[(remedy sequence, TrackSettings)]: unremedied first, then the fitting remedy's states (v2 rules: freeze
    v2 dev seeds 3-5 and the held-out label sweep). None in place of a state that needs the unremedied run
    (registration band start, base disk radius)."""
    base = initial(rod)
    f = rod.fault
    out = [([], base)]
    if f in ("rigid_drift", "fast_rotation", "bad_stage_correction", "stage_log_missing"):
        b = band_start(rod)
        reg = None if b is None else replace(base, register=True, register_from_px=b)
        out.append((["register_frames"], reg))
    elif f == "displacement_exceeds_patch":
        h = "change_frame_stride/half"
        out += [([h], replace(base, stride=3)), ([h, h], replace(base, stride=1))]
    elif f == "width_change":
        out.append((["use_width_free_ratio"], replace(base, width_free=True)))
    elif f == "low_texture":
        out += [(["enlarge_patch/1.5x"], enlarged(rod, base, 1.5)), (["enlarge_patch/2x"], enlarged(rod, base, 2))]
    elif f == "midline_jitter":
        out.append((["smooth_midline/light"], replace(base, midline_smooth="light")))
    elif f == "second_root":
        out += [([f"crop_or_mask/{m}"], replace(base, band_mask=m)) for m in ("crop_to_main_root", "mask_second_root")]
    elif f in ("flank_swap", "partial_occlusion"):
        d, s2 = "change_frame_stride/double", replace(base, stride=2)
        out += [(["enlarge_patch/1.5x"], enlarged(rod, base, 1.5)), (["enlarge_patch/2x"], enlarged(rod, base, 2)),
                ([d], s2), ([d, "enlarge_patch/1.5x"], enlarged(rod, s2, 1.5)),
                ([d, "enlarge_patch/2x"], enlarged(rod, s2, 2))]
    return out


# ------------------------------------------------------------------ tracker plans

def need_basis():
    need = []
    for rod in basis_rods():
        need += [(rod, st) for st in basis_states(rod) if st is not None and not cached(rod, st)]
    return need


def basis_states(rod):
    """Unremedied; bent rods also enlarge_patch 2x (flank tolerance basis, as v2), once the unremedied run gives
    the base radius."""
    return [TrackSettings()] + ([enlarged(rod, TrackSettings(), 2)] if rod.case.startswith("v3_bend") else [])


def sizing_rows():
    """Per held-out fault: sizes tried in order, seeds failing a check. The larger size is needed only when the
    v2 size fails on fewer than 3 of 3 sizing seeds."""
    rows, need = {}, []
    for f, z in HELDOUT.items():
        rows[f] = []
        for size in [z] + ([LARGER[f]] if f in LARGER else []):
            rods = [Rod(GZ, f, s, size=size) for s in seeds("sizing_seeds")]
            ev = [evaluate(r, initial(r)) for r in rods]
            missing = [r for r, e in zip(rods, ev) if e is None]
            need += [(r, initial(r)) for r in missing]
            done = [e for e in ev if e is not None]
            rows[f].append({"size": size, "evaluated": len(done), "fail": sum(not e["all_pass"] for e in done),
                            "runs": done})
            if missing or rows[f][-1]["fail"] == len(rods):
                break
    return rows, need


def need_labels():
    need = []
    for rod in scored_rods():
        for _, st in label_states(rod):
            if st is not None and not cached(rod, st):
                need.append((rod, st))
    return need


class Missing(Exception):
    def __init__(self, rod, settings):
        super().__init__(f"{rod.id()} {settings.tag()}")
        self.rod, self.settings = rod, settings


class V3Runner(RemoteRunner):
    """Measurements from CACHE. remote=False: a run not cached raises Missing. remote=True: it runs as a single
    load-checked job on the tracker machine and is fetched into CACHE."""

    def __init__(self, remote=False):
        self.remote, self.log, self.cache, self.couple = remote, [], CACHE, False
        if remote:
            super().__init__(runner_config(), cache=CACHE)

    @staticmethod
    def initial_stride(rod):
        return initial(rod).stride

    def measure(self, rod, settings):
        st = replace(settings, width_free=False)
        if not cached(rod, st) or truth(rod) is None:
            if not self.remote:
                raise Missing(rod, st)
            if tracker_runs_cached() + 2 > MAX_TRACKER_RUNS:
                raise RuntimeError(f"tracker-run cap {MAX_TRACKER_RUNS} reached; ask Andrew")
            rid, rid_m = self.render(rod), self.render(rod, moved=True)
            self.track(rid, st), self.track(rid_m, st)
            if truth(rod) is None:
                self.truth(rid)
        return Measurement(from_tracker_npz(out_file(rod, st)), from_tracker_npz(out_file(rod, st, True)),
                           settings, truth(rod))


def need_methods():
    need = {}
    for rod in scored_rods():
        for m, fn in RULES.items():
            try:
                fn(Slice(V3Runner(), rod), None)
            except Missing as e:
                need[(e.rod.id(), e.settings.tag())] = (e.rod, e.settings)
    return list(need.values())


def start_sweep(need, dry):
    by_rod = {}
    for rod, st in need:
        by_rod.setdefault(rod, []).append(replace(st, width_free=False))
    plan = {"rods": [entry(rod, list({s.tag(): s for s in sts}.values())) for rod, sts in by_rod.items()]}
    n_new = sum(2 * len(x["runs"]) for x in plan["rods"])
    n_have = tracker_runs_cached()
    print(f"tracker runs cached {n_have}; this plan {n_new} ({len(plan['rods'])} rods); cap {MAX_TRACKER_RUNS}")
    for x in plan["rods"]:
        print(f"  {x['id']} {[r['tag'] for r in x['runs']]}")
    if not n_new or dry:
        return
    if n_have + n_new > MAX_TRACKER_RUNS:
        sys.exit(f"stop: {n_have + n_new} tracker runs would pass the cap {MAX_TRACKER_RUNS}; ask Andrew")
    r = RemoteRunner(runner_config(), cache=CACHE)
    if r.sweep_status().get("running"):
        sys.exit("a sweep is running; wait and try again")
    log = r.sweep_start(plan, SWEEP, tracks=TRACKS)
    print(f"started: {len(plan['rods'])} rods, {n_new} tracker runs; log {log}")


# ------------------------------------------------------------------ tables: basis, sizing, labels

CHECKS = ("rigid_invariance", "closure", "plane_sections")


def _cell(r, c):
    return f"{r[c]:.2f}" + {False: " F", None: " skip", True: ""}[r[f"{c}_pass"]]


def basis_report():
    tol = load_tolerance()["flank_difference_rms_pct_per_h"]
    L = ["# Clean basis at v3 geometry", "", f"Seeds {', '.join(map(str, seeds('basis_seeds')))}. Approved thresholds: "
         f"rigid_invariance {TH['rigid_invariance']} %/h, closure {TH['closure']} px/h, plane_sections "
         f"{TH['plane_sections']} %/h. Flank tolerance {tol} %/h (bent rods, unremedied and enlarge_patch 2x).", "",
         "| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err | All pass |",
         "| :-- | :-- | --: | --: | --: | --: | --: | :-- |"]
    rows, missing = [], 0
    for rod in basis_rods():
        for st in basis_states(rod):
            e = evaluate(rod, st) if st is not None else None
            if e is None:
                missing += 1
                continue
            rows.append((rod, st, e))
            L.append(f"| {rod.id()} | {st.tag()} | " + " | ".join(_cell(e, c) for c in CHECKS)
                     + f" | {e['regr_rms_pct_per_h']:.2f} ({e['regr_limit']:.2f}) | "
                     f"{e['flank_difference_rms_pct_per_h']:.2f} | {'yes' if e['all_pass'] else 'no'} |")
    fails = [(r, s, e) for r, s, e in rows if not e["all_pass"] and s.disk_radius is None]
    flank = [e["flank_difference_rms_pct_per_h"] for r, s, e in rows if r.case.startswith("v3_bend")]
    maxes = {c: max((e[c] for _, s, e in rows if s.disk_radius is None), default=float("nan")) for c in CHECKS}
    stop = bool(fails) or (flank and max(flank) > tol)
    L += ["", f"- Evaluated {len(rows)} states; not yet run {missing}",
          "- Largest clean value, unremedied: " + ", ".join(f"{c} {maxes[c]:.2f}" for c in CHECKS),
          f"- Largest clean flank-difference error, bent rods: {max(flank):.3f} %/h (tolerance {tol})" if flank else "",
          f"- Clean unremedied runs failing a threshold: {len(fails)}" + (": " + ", ".join(r.id() for r, _, _ in fails) if fails else ""),
          f"- Result: {'STOP for Andrew' if stop else ('thresholds and tolerance stay' if not missing else 'incomplete')}"]
    return "\n".join(x for x in L if x is not None) + "\n", {"stop": stop, "missing": missing, "max": maxes,
                                                              "flank_max": max(flank) if flank else None}


def sizing_report():
    rows, need = sizing_rows()
    L = ["# Held-out sizes at v3 geometry", "", f"Sizing seeds {', '.join(map(str, seeds('sizing_seeds')))}, "
         "checker only. Rule (v2): the smallest tested size at which the checker fails 3 of 3.", "",
         "| Fault | v2 size | Size | Seeds failing | rigid_invariance | closure | plane_sections | REGR err |",
         "| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |"]
    sizes, changed = {}, []
    for f, tried in rows.items():
        for t in tried:
            rng = lambda k: f"{min(e[k] for e in t['runs']):.2f}-{max(e[k] for e in t['runs']):.2f}" if t["runs"] else "-"
            L.append(f"| {f} | {HELDOUT[f]} | {t['size']} | {t['fail']} of {t['evaluated']} | {rng('rigid_invariance')} | "
                     f"{rng('closure')} | {rng('plane_sections')} | {rng('regr_rms_pct_per_h')} |")
        last = tried[-1]
        if last["evaluated"] == len(seeds("sizing_seeds")) and last["fail"] == last["evaluated"]:
            sizes[f] = last["size"]
            if last["size"] != HELDOUT[f]:
                changed.append(f)
        else:
            sizes[f] = None
    done = not need and all(v is not None for v in sizes.values())
    L += ["", f"- Sizes: {sizes}", f"- Differ from v2: {changed or 'none'}",
          f"- Result: {'complete' if done else 'incomplete'}{'; STOP for Andrew (size changed or none fails 3 of 3)' if done and changed else ''}"]
    if not need and any(v is None for v in sizes.values()):
        L[-1] = "- Result: STOP for Andrew: no tested size fails 3 of 3 for " + ", ".join(f for f, v in sizes.items() if v is None)
    return "\n".join(L) + "\n", {"sizes": sizes, "changed": changed, "complete": done, "need": len(need)}


def labels_report():
    L = ["# Labels of the freeze v3 scored set", "", f"Scoring seeds {', '.join(map(str, seeds('scoring_seeds')))}. "
         "Tracker only, no agent. Repair criteria (spec 2026-10-10, part C; measure.score.label_rod): a state of at most "
         "two remedy steps with three passes and a good measurement. Clean rods: accept_clean if the unremedied run "
         "passes and is good.", "",
         "| Rod | Expected class | Label class | Repairing remedy | Unremedied: checks pass, good |",
         "| :-- | :-- | :-- | :-- | :-- |"]
    per = ["| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err (limit) | All pass | Good |",
           "| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |"]
    labels, missing, odd = {}, 0, []
    for rod in scored_rods():
        sts = label_states(rod)
        ev = []
        for seq, st in sts:
            e = evaluate(rod, st, after_remedy=bool(seq)) if st is not None else None
            if e is None:
                missing += 1
                continue
            ev.append((seq, e))
            per.append(f"| {rod.id()} | {' + '.join(seq) or 'none'} | " + " | ".join(_cell(e, c) for c in CHECKS)
                       + f" | {e['regr_rms_pct_per_h']:.2f} ({e['regr_limit']:.2f}) | "
                       f"{e['flank_difference_rms_pct_per_h']:.2f} ({e['flank_limit']:.2f}) | "
                       f"{'yes' if e['all_pass'] else 'no'} | {'yes' if e['good'] else 'no'} |")
        if len(ev) < len(sts):
            continue
        exp = EXPECTED[kind(rod)]
        u = ev[0][1]
        if rod.fault is None:
            ok = (u["all_pass"] or rod.id() in CLEAN_FALSE_ALARM) and u["good"]
            cls, seq = ("accept_clean" if ok else "clean_fails"), None
        else:
            lab, seq = label_rod([{"sequence": s, "checks_pass": e["all_pass"], "good": e["good"]} for s, e in ev])
            cls = "accept_repaired" if lab == "repairable" else "decline"
        if cls != exp:
            odd.append(rod.id())
        labels[rod.id()] = {"class": cls, "expected": exp, "sequence": seq, "kind": kind(rod), "seed": rod.seed,
                            "size": rod.size}
        L.append(f"| {rod.id()} | {exp} | {cls} | {' + '.join(seq) if seq else '-'} | "
                 f"{'yes' if u['all_pass'] else 'no'}, {'yes' if u['good'] else 'no'} |")
    n = len(scored_rods())
    counts = {c: sum(v["class"] == c for v in labels.values()) for c in metrics.CLASSES + ("clean_fails",)}
    complete = len(labels) == n
    stop = complete and (counts["decline"] > n / 2 or counts["clean_fails"] > 0)
    L += ["", f"- Rods labelled {len(labels)} of {n}; states not yet run {missing}",
          f"- Classes: {counts}", f"- All-decline would score {counts['decline']} of {n}",
          f"- Label differs from the expected class: {len(odd)}" + (": " + ", ".join(odd) if odd else ""),
          f"- Result: {'STOP for Andrew' if stop else ('complete' if complete else 'incomplete')}", "", "## Per state", ""]
    return "\n".join(L + per) + "\n", {"labels": labels, "counts": counts, "complete": complete, "stop": stop}


# ------------------------------------------------------------------ methods

def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def stem(method, rod, repeat=0):
    return (f"{method}_{rod.id()}" + (f"_r{repeat}" if method in LLM else ""))


def write_summary(path, rod, sl, outcome, method, extra):
    first, last = sl.runs[0][1], sl.current
    s = {"freeze_tag": FREEZE_TAG, "commit": git("rev-parse", "--short", "HEAD"), "method": method,
         "rod": {"case": rod.case, "fault": rod.fault, "size": rod.size, "seed": rod.seed, "id": rod.id()},
         "runner": "remote_job", "truth": truth_summary(first.truth, PIXEL_UM),
         "error_before": truth_error(first.record, first.truth),
         "initial_checks": [c.to_dict() for c in sl.runs[0][2]],
         "outcome": outcome.__dict__, "error_after": truth_error(last.record, last.truth),
         "remedies": [ch for _, _, _, ch in sl.runs[1:]],
         "roll_backs": sum(ch.startswith("rolled back") for _, _, _, ch in sl.runs[1:]),
         "final_settings": sl.runs[-1][0].to_dict(), "final_checks": [c.to_dict() for c in sl.checks],
         "reported": outcome.status == "accept", **extra}
    path.write_text(json.dumps(s, indent=1, default=str))


RULES = {"script": lambda sl, trace: run_script(sl, trace),
         "remedy_tree": lambda sl, trace: run_tree(sl, load_config()["agents"]["diagnostician"]["step_limit"], trace)}


def run_rules():
    out = OUT / "runs"
    out.mkdir(parents=True, exist_ok=True)
    same = 0
    for rod in scored_rods():
        for m, fn in RULES.items():
            summ, trace = out / f"{stem(m, rod)}_summary.json", out / f"{stem(m, rod)}_trace.jsonl"
            if summ.exists():
                continue
            trace.unlink(missing_ok=True)                    # local file of an unfinished rule run
            sl = Slice(V3Runner(), rod)
            o = fn(sl, trace)
            write_summary(summ, rod, sl, o, m, {})
            o2 = fn(Slice(V3Runner(), rod), None)             # second run from the cache: deterministic?
            same += (o2.status, o2.steps, o2.args) == (o.status, o.steps, o.args)
            with (out / "deterministic.jsonl").open("a") as f:
                f.write(json.dumps({"run": stem(m, rod), "identical": (o2.status, o2.steps, o2.args) == (o.status, o.steps, o.args)}) + "\n")
    print(f"rule-method runs written; second runs identical in this call: {same}")


def run_agents(method, repeat, max_runs=None):
    """max_runs: stop after this many new runs (blocks of at most 25, Andrew 2026-10-24, inbox item 11)."""
    from agents.launcher import Launcher
    from agents.orchestrator import Orchestrator
    if git("status", "--porcelain", "--untracked-files=no"):
        sys.exit("tracked files are modified; commit first (each run records the commit)")
    out = OUT / "runs"
    out.mkdir(parents=True, exist_ok=True)
    launcher = Launcher()
    cls = {"diagnostician": Slice, "single_agent": BlindSlice}[method]
    errors, started = [], 0
    for rod in scored_rods():
        name = stem(method, rod, repeat)
        summ, trace = out / f"{name}_summary.json", out / f"{name}_trace.jsonl"
        if summ.exists():
            continue
        if max_runs is not None and started >= max_runs:
            break
        started += 1
        if trace.exists():                            # a stopped run: kept, the repeat starts a new trace name
            trace = out / f"{name}_trace_{time.strftime('%H%M%S')}.jsonl"
        runner = V3Runner(remote=True)
        t0 = time.time()
        try:
            sl = cls(runner, rod)
            o = Orchestrator(launcher, trace).run(method, sl.label, sl.task(), sl.executors())
        except Exception as e:
            errors.append(name)
            with (out / "harness_errors.jsonl").open("a") as f:
                f.write(json.dumps({"run": name, "error": f"{type(e).__name__}: {e}",
                                    "traceback": traceback.format_exc()[-2000:]}) + "\n")
            print(f"{name}: HARNESS ERROR {type(e).__name__}: {e}", flush=True)
            if "cap" in str(e):
                break
            continue
        tracker = [x["track"] for x in runner.log if "track" in x]
        write_summary(summ, rod, sl, o, method, {"repeat": repeat, "trace": trace.name,
                                                 "claude_code": launcher.version, "wall_s": round(time.time() - t0, 1),
                                                 "tracker_runs_new": len(tracker), "runner_log": runner.log})
        print(f"{name}: {o.status} {o.args.get('fault', '')} steps {o.steps} tokens {o.input_tokens}/{o.output_tokens} "
              f"call {o.call_ms / 1000:.1f} s; new tracker runs {len(tracker)}", flush=True)
    print(f"harness errors: {len(errors)} {errors}")


# ------------------------------------------------------------------ scoring

def named_fault(trace):
    name = None
    if not trace.exists():
        return None
    for line in trace.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        act = d.get("action") or {}
        if act.get("name") in ("apply_remedy", "decline") and d.get("status") in ("executed", "terminal"):
            name = act["args"].get("fault")
    return name


def score_runs(labels):
    cfg, rows = load_tolerance(), []
    for rod in scored_rods():
        lab = labels[rod.id()]
        tol = rod_tolerance(truth(rod), PIXEL_UM, cfg)
        for m in METHODS:
            for k in (REPEATS if m in LLM else (0,)):
                f = OUT / "runs" / f"{stem(m, rod, k)}_summary.json"
                if not f.exists():
                    rows.append({"method": m, "rod": rod.id(), "repeat": k, "missing": True})
                    continue
                s = json.loads(f.read_text())
                o = s["outcome"]
                good = measurement_good(s["error_after"], tol, bool(s["final_settings"].get("width_free")))
                nf = named_fault(f.parent / s.get("trace", f.name.replace("_summary.json", "_trace.jsonl")))
                rows.append({"method": m, "rod": rod.id(), "kind": kind(rod), "seed": rod.seed, "repeat": k,
                             "cls": lab["class"], "status": o["status"], "good": good,
                             "category": metrics.category(o["status"], lab["class"], good),
                             "remedies_kept": len(s["remedies"]) - 2 * s["roll_backs"], "remedies": s["remedies"],
                             "roll_backs": s["roll_backs"], "named_fault": nf,
                             "fault_correct": (nf in NAMES[rod.fault]) if rod.fault else None,
                             "steps": o["steps"], "tokens_in": o.get("input_tokens", 0),
                             "tokens_out": o.get("output_tokens", 0), "call_s": round(o.get("call_ms", 0) / 1000, 1),
                             "regr_rms": s["error_after"].get("regr_rms_pct_per_h"),
                             "flank_rms": s["error_after"].get("flank_difference_rms_pct_per_h"),
                             "regr_tol": round(tol["regr_rms_pct_per_h"], 3), "commit": s.get("commit"),
                             "freeze_tag": s.get("freeze_tag"), "claude_code": s.get("claude_code"),
                             "tracker_runs_new": s.get("tracker_runs_new")})
    return rows


def _f(x, n=2):
    if x is None:
        return "-"
    if isinstance(x, dict):
        return "-" if x is None else (f"{x['mean']:.{n}f}" + ("" if x["min"] == x["max"] else f" ({x['min']:.{n}f}-{x['max']:.{n}f})"))
    return f"{x:.{n}f}" if isinstance(x, float) else str(x)


def evaluate_all():
    _, lab = labels_report()
    if not lab["complete"]:
        sys.exit("labels incomplete")
    labels = lab["labels"]
    rows = score_runs(labels)
    done = [r for r in rows if not r.get("missing")]
    (OUT / "scores.json").write_text(json.dumps(rows, indent=1, default=str))
    rods = [(rid, v["class"]) for rid, v in labels.items()]
    good0 = {}
    for rod in scored_rods():
        e = evaluate(rod, initial(rod))
        good0[rod.id()] = e["good"] if e else False
    refs = {"all_decline": metrics.reference_runs(rods, "all_decline"),
            "all_accept": metrics.reference_runs(rods, "all_accept", good0)}
    res = {}
    for m in METHODS:
        x = [r for r in done if r["method"] == m]
        if x:
            res[m] = metrics.over_repeats(x)
            if m in LLM:
                res[m]["agreement"] = metrics.agreement(x)
    for k, v in refs.items():
        res[k] = metrics.over_repeats(v)
    (OUT / "metrics.json").write_text(json.dumps(res, indent=1, default=str))
    L = ["# Freeze v3 scored runs: metrics", "",
         f"{len(rods)} rods: " + ", ".join(f"{c} {sum(v == c for _, v in rods)}" for c in metrics.CLASSES)
         + f". LLM methods {len(REPEATS)} repeats; values are the mean over repeats, (min-max) where they differ. "
         "Definitions: `docs/proposals/2026-10-23_freeze-v3.md`, section 3; code `measure/metrics.py`.", "",
         "| Method | Runs | Balanced accuracy | Acc. accept_clean | Acc. accept_repaired | Acc. decline | Overall | "
         "False accepts | False-accept rate | Coverage | Abst. precision | Abst. recall | not_reported |",
         "| :-- | --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |"]
    for m, v in res.items():
        a = v["accuracy_per_class"]
        nr = sum(p["categories"]["not_reported"] for p in v["per_repeat"])
        L.append(f"| {m} | {sum(p['runs'] for p in v['per_repeat'])} | {_f(v['balanced_accuracy'])} | "
                 f"{_f(a['accept_clean'])} | {_f(a['accept_repaired'])} | {_f(a['decline'])} | {_f(v['overall_accuracy'])} | "
                 f"{_f(v['false_accepts'], 1)} | {_f(v['false_accept_rate'])} | {_f(v['coverage'])} | "
                 f"{_f(v['abstention_precision'])} | {_f(v['abstention_recall'])} | {nr} |")
    L += ["", "## Agreement across repeats (LLM methods)", "",
          "| Method | Rods | Unanimous | Unanimity rate | accept_clean | accept_repaired | decline | Fleiss kappa |",
          "| :-- | --: | --: | :-- | :-- | :-- | :-- | :-- |"]
    for m in LLM:
        if m in res:
            g = res[m]["agreement"]
            u = g["unanimity_rate_per_class"]
            L.append(f"| {m} | {g['rods']} | {g['unanimous']} | {_f(g['unanimity_rate'])} | {_f(u['accept_clean'])} | "
                     f"{_f(u['accept_repaired'])} | {_f(u['decline'])} | {_f(g['fleiss_kappa'], 3)} |")
    L += ["", "## Categories, remedies kept, unnecessary declines (summed over repeats)", "",
          "| Method | " + " | ".join(metrics.CATEGORIES) + " | Runs keeping a remedy, accept_clean | "
          "Unnecessary-decline rate accept_clean / accept_repaired | Fault named correct |",
          "| :-- | " + " | ".join("--:" for _ in metrics.CATEGORIES) + " | --: | :-- | :-- |"]
    for m, v in res.items():
        P = v["per_repeat"]
        L.append(f"| {m} | " + " | ".join(str(sum(p["categories"][c] for p in P)) for c in metrics.CATEGORIES)
                 + f" | {sum(p['runs_with_remedy_kept_per_class']['accept_clean'] for p in P)} | "
                 f"{_f(v['unnecessary_decline_rate']['accept_clean'])} / {_f(v['unnecessary_decline_rate']['accept_repaired'])} | "
                 f"{sum(p['fault_named_correct'] for p in P)} of {sum(p['fault_rods'] for p in P)} |")
    L += ["", "## Per row of the set (correct runs / runs)", "",
          "| Row | Class | " + " | ".join(METHODS) + " |", "| :-- | :-- | " + " | ".join(":--" for _ in METHODS) + " |"]
    for kd in CLEAN + list(DEV) + list(HELDOUT):
        x = [r for r in done if r["kind"] == kd]
        if not x:
            continue
        cls = sorted({r["cls"] for r in x})
        L.append(f"| {kd} | {', '.join(cls)} | " + " | ".join(
            f"{sum(metrics.correct(r) for r in x if r['method'] == m)} / {sum(r['method'] == m for r in x)}" for m in METHODS) + " |")
    L += ["", "## Cost (LLM methods, all repeats)", "", "| Method | Runs | Steps | Tokens in | Tokens out | Call time (s) |",
          "| :-- | --: | --: | --: | --: | --: |"]
    for m in METHODS:
        x = [r for r in done if r["method"] == m]
        if x:
            L.append(f"| {m} | {len(x)} | {sum(r['steps'] for r in x)} | {sum(r['tokens_in'] for r in x)} | "
                     f"{sum(r['tokens_out'] for r in x)} | {sum(r['call_s'] for r in x):.1f} |")
    miss = [r for r in rows if r.get("missing")]
    if miss:
        L += ["", f"Not run: {len(miss)}"]
    L += ["", "## Per run", "", "| Method | Rod | Repeat | Class | Status | Category | Named fault | Steps | Remedies | Centre RMS (tol) | Flank RMS |",
          "| :-- | :-- | --: | :-- | :-- | :-- | :-- | --: | :-- | :-- | --: |"]
    for r in done:
        L.append(f"| {r['method']} | {r['rod']} | {r['repeat']} | {r['cls']} | {r['status']} | {r['category']} | "
                 f"{r['named_fault'] or '-'} | {r['steps']} | {'; '.join(r['remedies']) or 'none'} | "
                 f"{r['regr_rms']} ({r['regr_tol']}) | {r['flank_rms']} |")
    (OUT / "table_metrics.md").write_text("\n".join(L) + "\n")
    print("\n".join(L).split("\n## Per row")[0])


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "status", "fetch", "basis", "sizing", "labels", "rules", "agents", "eval"])
    ap.add_argument("--phase", choices=["basis", "sizing", "labels", "methods"])
    ap.add_argument("--method", choices=LLM)
    ap.add_argument("--repeat", type=int, choices=REPEATS)
    ap.add_argument("--max-runs", type=int, default=None, help="agents: at most this many new runs")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.cmd == "plan":
        if not a.phase:
            ap.error("--phase is required")
        need = {"basis": need_basis, "sizing": lambda: sizing_rows()[1], "labels": need_labels,
                "methods": need_methods}[a.phase]()
        start_sweep(need, a.dry_run)
    elif a.cmd == "status":
        st = RemoteRunner(runner_config(), cache=CACHE).sweep_status(SWEEP)
        log = st.pop("log")
        print(json.dumps(st))
        runs = [x for x in log if "tag" in x]
        print(f"runs logged {len(runs)}, failed {sum(x.get('ok') is False for x in runs)}, "
              f"partial {sum(bool(x.get('partial')) for x in runs)}")
        for x in log:
            if "tag" not in x:
                print(json.dumps(x))
    elif a.cmd == "fetch":
        r = RemoteRunner(runner_config(), cache=CACHE)
        st = r.sweep_status(SWEEP)
        if st.get("running"):
            sys.exit("a sweep is running; fetch after it ends")
        CACHE.mkdir(parents=True, exist_ok=True)
        with (CACHE / "sweeps.jsonl").open("a") as f:
            for x in st["log"]:
                if "tag" not in x:
                    f.write(json.dumps(x) + "\n")
        r.sweep_fetch(TRACKS, CACHE)
        print(f"fetched: {tracker_runs_cached()} tracker outputs in the cache")
    elif a.cmd == "basis":
        text, info = basis_report()
        (OUT / "basis.md").write_text(text)
        print(text.split("\n| Rod")[0] + "\n" + text.split("|\n\n")[-1])
    elif a.cmd == "sizing":
        text, info = sizing_report()
        (OUT / "sizing.md").write_text(text)
        if info["complete"] and not info["changed"]:
            (OUT / "sizing.json").write_text(json.dumps({"sizes": info["sizes"]}, indent=1))
        print(text)
    elif a.cmd == "labels":
        text, info = labels_report()
        (OUT / "labels.md").write_text(text)
        if info["complete"]:
            (OUT / "labels.json").write_text(json.dumps(info, indent=1, default=str))
        print(text.split("## Per state")[0])
    elif a.cmd == "rules":
        run_rules()
    elif a.cmd == "agents":
        if a.method is None or a.repeat is None:
            ap.error("--method and --repeat are required")
        run_agents(a.method, a.repeat, a.max_runs)
    else:
        evaluate_all()


if __name__ == "__main__":
    main()
