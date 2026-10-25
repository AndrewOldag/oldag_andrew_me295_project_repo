"""Real-movie noise floor on the calibration set (spec 2026-10-24b, section B; task c018).

  python scripts/real_calib.py run --config private/real_runner_c018.yaml [--windows W ...]
  python scripts/real_calib.py summary [--out DIR]

Set and rule: docs/proposals/2026-10-24_real-calibration.md (committed before any value was computed).
`run`, per window: the screen (ft2 net tip point within 15 px of the root-mask apex, median over 5 window
frames, scripts/remote/tip_apex_probe.py), then the window is measured with RealRunner at its initial settings
(every frame, uncoupled, 1000 px, inbox item 3; whole-pixel moved copy and cropped reference copy) and checked: rigid
invariance (full range, the reported value; and the profile-window value), closure, plane sections. No remedy,
no agent. One JSON per window in DIR/windows/; a window with a file is skipped, so an interrupted run resumes.
`summary`: per check, the 95th percentile (numpy linear) over the windows that passed the screen, rounded up
to 2 significant figures; with every value, count, min, median and max. Writes DIR/summary.json and DIR/table.md.

Closure carries the definition it was computed with (`closure_definition`); after section A is merged it is
recomputed from the cached tracker outputs with the A definition.
"""
import argparse
import json
import math
import shlex
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents.executors import real_rigid_invariance  # noqa: E402
from checker import run_checks  # noqa: E402
from measure.real_runner import TRACK_LENGTH, RealRunner, RealWindow  # noqa: E402
from closure_base_test import summarize  # noqa: E402

OUT = ROOT / "results" / "2026-10-25_real_calibration"
ROOTS = ["0708_c8", "0708_c9", "0711_c5", "0711_c7", "0714_c4", "0714_c9", "0721_c5", "0721_c6"]
SPANS = [(7.0, 9.0), (15.0, 17.0)]
WINDOWS = [RealWindow(r, a, b) for r in ROOTS for a, b in SPANS]
# Proposal replacement order (roots not reserved for section C), added only while fewer than 12 windows or 3
# experiments are measured; `run --replacements N` adds the first N
REPLACEMENTS = ["0714_c13", "0711_c1"]
SCREEN_PX, SCREEN_FRAMES = 15.0, 5
CLOSURE_DEFINITION = ("2026-10-10 definition kept by section A (midline end against the most basal centre point "
                      "tracked in every frame), 1000 px tracks")
MIDLINE = "ft2 (net2_midline_ft2.pt, tile mode, low 0.1 %, high 99.5 %)"
CHECKS = ("rigid_invariance", "rigid_invariance_profile_window", "closure", "plane_sections")
C019 = "me295/c019"          # the section C chain's lab-server folder, under the lab data root (read only)


def ceil_2sf(x):
    """Round up to 2 significant figures: 6.213 -> 6.3, 0.4471 -> 0.45, 20.0 -> 20."""
    if not math.isfinite(x) or x <= 0:
        return x
    q = 10.0 ** (math.floor(math.log10(x)) - 1)
    return round(math.ceil(round(x / q, 9)) * q, 12)


def screen(runner, w):
    """The tip-apex screen on 5 window frames. Inputs from the c019 chain: htpmid and seg midline."""
    q = shlex.quote
    base = runner.work.rsplit("/me295/", 1)[0] + "/" + C019
    imgdir = runner.windows[w.id()]["imgdir"]
    cmd = (f"cd {q(runner.code)} && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 "
           f"PYTHONPATH={q(runner.tracker)}:{q(runner.code)} nice -n 19 {q(runner.python)} "
           f"scripts/remote/tip_apex_probe.py {q(runner.tracker)} {base}/bm/{q(w.id())}_ft2_bm/*_htpmid.npz "
           f"{base}/seg/{q(w.id())}_seg.npz {q(imgdir)} {SCREEN_FRAMES}")
    out = json.loads(runner._ssh(cmd).decode().strip().splitlines()[-1])
    d = out.get("median_net_tip_to_apex_px")
    return {"median_net_tip_to_apex_px": d, "frames": out["frames"],
            "passed": d is not None and d <= SCREEN_PX}


def base_info(rec):
    """Inbox item 3: tracked length reached, base arc length, world speed of the basal points (closure_base_test),
    and the flag for a frame-0 midline shorter than the tracked length (reported, not a gate)."""
    b = summarize(rec)
    c = rec.centre
    reach = float(np.nansum(np.nanmean(np.linalg.norm(np.diff(c, axis=1), axis=2), axis=0)))
    m0 = rec.midline[0]
    m0 = m0[np.all(np.isfinite(m0), axis=1)]
    mid0 = float(np.linalg.norm(np.diff(m0, axis=0), axis=1).sum())
    return {"tracked_length_reached_px": round(reach, 1), "base_s_px": b["base_s_px"],
            "base_term_px_per_h": b["base_term_px_per_h"], "tip_side_term_px_per_h": b["tip_side_term_px_per_h"],
            "basal_speed_px_per_h": b["speed_profile_px_per_h"][-4:], "frame0_midline_px": round(mid0, 1),
            "flag": "base may be in growing tissue" if mid0 < TRACK_LENGTH else None}


def check_values(m, thresholds=None):
    checks = {c.check: c for c in run_checks(m.record, m.moved, thresholds)}
    win = real_rigid_invariance(m.record, m.moved, thresholds or {})
    vals = {k: (None if not math.isfinite(c.value) else round(c.value, 4)) for k, c in checks.items()}
    vals["rigid_invariance_profile_window"] = (None if win is None or not math.isfinite(win.value)
                                               else round(win.value, 4))
    detail = {k: c.detail for k, c in checks.items()}
    if win is not None:
        detail["rigid_invariance_profile_window"] = win.detail
    return vals, detail


def run(a):
    runner = RealRunner(a.config)
    if runner.track_length != 1000.0:              # inbox item 3: thresholds only from 1000 px tracks
        sys.exit(f"tracked length {runner.track_length:g} px; calibration needs 1000 px")
    runner.sync_code()
    out = Path(a.out) / "windows"
    out.mkdir(parents=True, exist_ok=True)
    extra = [RealWindow(r, x, y) for r in REPLACEMENTS[:a.replacements] for x, y in SPANS]
    wins = [w for w in WINDOWS + extra if not a.windows or w.id() in a.windows]
    for w in wins:
        f = out / f"{w.id()}.json"
        if f.exists():
            print(f"{w.id()}: done, skipped", flush=True)
            continue
        res = {"window": w.id(), "root": w.root_id, "window_h": [w.from_h, w.to_h], "midline": MIDLINE}
        try:
            res["screen"] = screen(runner, w)
        except Exception as e:
            if "Error:" not in str(e):                # ssh or missing input: no file, retried on the next run
                print(f"{w.id()}: screen not ready: {e}", flush=True)
                continue
            # the probe itself raised (e.g. a segmentation midline shorter than its 40 px step): the screen
            # fails for this window; listed with the reason, left out (proposal)
            res["screen"] = {"passed": False, "error": str(e)[:300]}
        if res["screen"]["passed"]:
            try:
                m = runner.measure(w, runner.initial_settings(w))
                res["values"], res["detail"] = check_values(m)
                res["base"] = base_info(m.record)
                res["track_length_px"] = runner.track_length
                res["closure_definition"] = CLOSURE_DEFINITION
                res["n_frames"] = int(m.record.n_frames)
                res["status"] = "measured"
            except Exception as e:
                if type(e).__name__ == "HostBusy":
                    print(f"{w.id()}: host busy ({e}); stopping, rerun later", flush=True)
                    return
                res["status"], res["error"] = "failed", f"{type(e).__name__}: {str(e)[:300]}"
        else:
            res["status"] = "screen failed" if res["screen"].get("error") else "screened out"
        f.write_text(json.dumps(res, indent=1))
        print(f"{w.id()}: {res['status']} {res.get('values', '')}", flush=True)
    log = Path(a.out) / "runner_log.json"           # appended per run, so a resumed run keeps earlier entries
    old = json.loads(log.read_text()) if log.exists() else []
    log.write_text(json.dumps(old + runner.log, indent=1, default=str))


def summary(a):
    out = Path(a.out)
    rows = [json.loads(p.read_text()) for p in sorted((out / "windows").glob("*.json"))]
    meas = [r for r in rows if r["status"] == "measured"]
    exps = sorted({r["root"][:4] for r in meas})
    s = {"midline": MIDLINE, "closure_definition": sorted({r.get("closure_definition") for r in meas} - {None}),
         "windows": len(rows), "measured": len(meas), "experiments": exps,
         "flagged": {r["window"]: r["base"]["flag"] for r in meas if r.get("base", {}).get("flag")},
         "not_measured": {r["window"]: r["status"] + (f": {r.get('error')}" if r.get("error") else "")
                          for r in rows if r["status"] != "measured"},
         "minimums_met": len(meas) >= 12 and len(exps) >= 3, "checks": {}}
    for k in CHECKS:
        v = [r["values"][k] for r in meas if r["values"].get(k) is not None]
        if not v:
            continue
        p95 = float(np.percentile(v, 95))
        by = sorted(((r["values"][k], r["window"]) for r in meas if r["values"].get(k) is not None), reverse=True)
        s["checks"][k] = {"n": len(v), "min": min(v), "median": float(np.median(v)), "max": max(v),
                          "p95": round(p95, 4), "threshold_rule": ceil_2sf(p95),
                          # sensitivity, reported only (proposal): no window is dropped
                          "largest_two": [{"window": w, "value": x} for x, w in by[:2]],
                          "p95_without_largest": (round(float(np.percentile([x for x, _ in by[1:]], 95)), 4)
                                                  if len(by) > 1 else None),
                          "values": {r["window"]: r["values"][k] for r in meas}}
    (out / "summary.json").write_text(json.dumps(s, indent=1))
    lines = ["| Window | Screen (px) | " + " | ".join(CHECKS) + " |", "| :-- | --: |" + " --: |" * len(CHECKS)]
    for r in rows:
        sc = r.get("screen", {}).get("median_net_tip_to_apex_px")
        vals = [("" if r.get("values", {}).get(k) is None else f"{r['values'][k]:.3g}") for k in CHECKS]
        lines.append(f"| {r['window']} | {sc} | " + " | ".join(vals if r["status"] == "measured" else
                                                              [r["status"]] + [""] * (len(CHECKS) - 1)) + " |")
    for lab, key in (("p95", "p95"), ("threshold (p95 rounded up, 2 s.f.)", "threshold_rule")):
        lines.append(f"| {lab} | | " + " | ".join(f"{s['checks'][k][key]:.4g}" if k in s["checks"] else ""
                                               for k in CHECKS) + " |")
    (out / "table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "summary"])
    ap.add_argument("--config", default=str(ROOT / "private" / "real_runner_c018.yaml"))
    ap.add_argument("--windows", nargs="*", default=None)
    ap.add_argument("--replacements", type=int, default=0, help="add the first N replacement roots (proposal)")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    {"run": run, "summary": summary}[a.cmd](a)


if __name__ == "__main__":
    main()
