"""Audit c033 section 2: synthetic inputs with known answers for checker/checks.py, measure/score.py,
measure/metrics.py. Read-only; prints results. Run from the repo root:
  python results/2026-11-23_audit/scripts/s2_equations_check.py
"""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from measure.record import MeasurementRecord, rigid_moved, PER_S_TO_PCT_PER_H as P
from checker import checks as C
from measure import score, metrics

H = 3600.0
TH_INT = {"inversions": 0, "gap_ratio": 2.4, "lateral_px": 0.081}


def rec_from(times, centre, plus, minus, midline, stage=None):
    T = len(times)
    return MeasurementRecord("t", "field", np.asarray(times, float), 2.0,
                             np.zeros((T, 2)) if stage is None else stage, centre, plus, minus, midline)


def uniform_growth(r_pct_h=20.0, L0=800.0, M=81, h=40.0, times=None):
    """Straight rod along +row (tip at small row), base fixed at row 1000, uniform REGR r."""
    r = r_pct_h / P
    times = np.arange(0, 13) * 300.0 if times is None else np.asarray(times, float)
    X = np.linspace(L0, 0.0, M)                       # distance from base, tip first
    T = len(times)
    c = np.zeros((T, M, 2))
    for i, t in enumerate(times):
        c[i, :, 0] = 1000.0 - X * np.exp(r * t)
        c[i, :, 1] = 500.0
    plus = c.copy()
    plus[..., 1] += h                                  # N = (0, 1) for t = (1, 0)
    minus = c.copy()
    minus[..., 1] -= h
    return rec_from(times, c, plus, minus, c.copy())


def bend(kd_per_h=1 / 400.0, L=1000.0, M=101, h=50.0, nT=13, dt=300.0, sign=+1):
    """Non-growing arc, base fixed at (1000, 500), tip->base tangent (1, 0) at the base; curvature uniform in s,
    kappa(t) = sign * kd * t. Flanks at +-h N. Expected plus - minus = -2h kdot/(1 - k^2 h^2)."""
    times = np.arange(nT) * dt
    s = np.linspace(0.0, L, M)
    pb = np.array([1000.0, 500.0])
    c = np.zeros((nT, M, 2))
    p = np.zeros_like(c)
    m = np.zeros_like(c)
    for i, t in enumerate(times):
        k = sign * kd_per_h * t / H
        phi = k * (s - L)
        if abs(k) < 1e-15:
            off = np.stack([L - s, np.zeros_like(s)], 1)
        else:
            off = np.stack([np.sin(k * (L - s)) / k, (np.cos(k * (L - s)) - 1) / k], 1)
        c[i] = pb - off
        N = np.stack([-np.sin(phi), np.cos(phi)], 1)
        p[i] = c[i] + h * N
        m[i] = c[i] - h * N
    return rec_from(times, c, p, m, c.copy()), times


def show(name, res):
    for r in res if isinstance(res, list) else [res]:
        print(f"  {name}: {r.check} value={r.value:.4g} {r.unit} passed={r.passed} | {r.detail[:90]}")


th = C.load_thresholds()
th = {k: th[k] for k in ("rigid_invariance", "closure", "plane_sections")}

print("A. uniform growth 20 %/h, straight, anchored base, dt 300 s")
a = uniform_growth()
f = a.fields
wm = np.nanmean(f["regr_mid"], 0) * P
print("  regr_mid window mean (%%/h): min %.4f max %.4f" % (np.nanmin(wm), np.nanmax(wm)))
show("A", C.run_checks(a, rigid_moved(a, np.deg2rad(5) / H, (3 / H, -2 / H)), th))

print("A2. same, uneven frame times")
t2 = np.cumsum([0, 300, 600, 150, 300, 600, 150, 300, 600, 150])
a2 = uniform_growth(times=t2)
wm = np.nanmean(a2.fields["regr_mid"], 0) * P
print("  regr_mid window mean (%%/h): min %.4f max %.4f" % (np.nanmin(wm), np.nanmax(wm)))
show("A2", C.closure(a2, th["closure"]))

print("A3. unlogged rigid drift 5 px/h along col applied to every point (base included), stage log zero")
a3 = uniform_growth()
drift = (a3.frame_times_s - a3.frame_times_s[0])[:, None] * np.array([0.0, 5.0 / H])
for k in ("centre", "plus", "minus", "midline"):
    setattr(a3, k, getattr(a3, k) + drift[:, None, :])
a3._fields = None
show("A3", C.closure(a3, th["closure"]))

print("A4. midline tip only displaced 0.5 px per frame along row (chain unchanged)")
a4 = uniform_growth()
a4.midline = a4.midline.copy()
a4.midline[:, 0, 0] += 0.5 * np.arange(a4.n_frames)
show("A4 (expect 6 px/h)", C.closure(a4, th["closure"]))

print("A5. midline tip jitter +-3 px alternating per frame (zero net)")
a5 = uniform_growth()
a5.midline = a5.midline.copy()
a5.midline[:, 0, 0] += 3.0 * (np.arange(a5.n_frames) % 2)
show("A5 (12 frames: net 0)", C.closure(a5, th["closure"]))

print("B. pure bending, kdot = +1/400 per px per h, h = 50 px, no growth")
b, tb = bend()
f = b.fields
kd = 1 / 400.0 / H
diff = np.nanmean(f["regr_plus"] - f["regr_minus"], 0) * P
pred = -np.nanmean(f["spacing"] * f["kappa_rate"], 0) * P
print("  kappa_rate median %.4e /px/s, expected %.4e" % (np.nanmedian(f["kappa_rate"]), kd))
print("  flank diff median %.3f %%/h; -2h kdot = %.3f %%/h; predicted from fields median %.3f" %
      (np.nanmedian(diff), -2 * 50 * kd * P, np.nanmedian(pred)))
print("  spacing median %.3f px (expect 100)" % np.nanmedian(f["spacing"]))
show("B", C.run_checks(b, rigid_moved(b, np.deg2rad(5) / H), th))
bn, _ = bend(sign=-1)
fn = bn.fields
print("  B- flank diff median %.3f %%/h" % np.nanmedian(np.nanmean(fn["regr_plus"] - fn["regr_minus"], 0) * P))
show("B-", C.plane_sections(bn, th["plane_sections"]))
bs, _ = bend()
bs.plus, bs.minus = bs.minus, bs.plus
bs._fields = None
show("B swapped flanks (expect fail)", C.plane_sections(bs, th["plane_sections"]))

print("C. whole record rotated about frame-0 tip at 5 deg/h")
c = rigid_moved(a, np.deg2rad(5) / H)
show("C closure (decisions 2026-10-10: rotation about a basal point fails; here about the tip)", C.closure(c, th["closure"]))

print("D. integrity")
show("D straight", C.track_integrity(a, TH_INT))
e = uniform_growth()
e.centre = e.centre.copy()
e.centre[:, 2:, :] = np.nan                         # only 2 points tracked per frame
res_e = C.track_integrity(e, TH_INT)
show("D <3 points per frame", res_e)
print("  integrity_gate:", C.integrity_gate(res_e))
g = uniform_growth()
g.midline = g.midline[:, :61].copy()              # midline ends 20 chain points before the chain base
res_g = C.track_integrity(g, TH_INT)
show("D midline shorter than chain", res_g)
print("  ratios remedied == base:", C.integrity_ratios(C.track_integrity(a), C.track_integrity(a)))
print("  ratios remedied ok, base <3 points:", C.integrity_ratios(C.track_integrity(a), res_e))
print("  ratios remedied <3 points, base ok:", C.integrity_ratios(res_e, C.track_integrity(a)))
rel = C.relative_integrity(e, a, C.load_relative_k())
show("D relative, remedied <3 points", rel)
print("  integrity_gate:", C.integrity_gate(rel))

print("E. score")
a_t = uniform_growth()
s = a_t.fields["s_grid"]
nT = a_t.n_frames - 1
truth = {"s_grid": s, "regr_mid": np.full((nT, len(s)), 20.0 / P),
         "regr_plus": np.full((nT, len(s)), 20.0 / P), "regr_minus": np.full((nT, len(s)), 20.0 / P)}
print("  truth_error exact:", score.truth_error(a_t, truth))
cfg = score.load_tolerance()
print("  rod_tolerance (peak 20):", score.rod_tolerance(truth, 2.0, cfg))
for pk in (0.04, 0.06):
    tz = dict(truth, regr_mid=np.zeros_like(truth["regr_mid"]) + pk / P)
    print(f"  rod_tolerance, true peak {pk} %/h:", score.rod_tolerance(tz, 2.0, cfg))
tn = dict(truth, regr_mid=np.zeros_like(truth["regr_mid"]) - 0.5 / P)
print("  rod_tolerance, true peak negative (shrinking rod):", score.rod_tolerance(tn, 2.0, cfg))
print("  measurement_good, NaN flank error:", score.measurement_good(
    {"regr_rms_pct_per_h": 0.1, "flank_difference_rms_pct_per_h": float("nan")}, score.rod_tolerance(truth, 2.0, cfg)))
print("  measurement_good, NaN regr error, width_free:", score.measurement_good(
    {"regr_rms_pct_per_h": float("nan"), "flank_difference_rms_pct_per_h": 0.0}, score.rod_tolerance(truth, 2.0, cfg), True))

print("F. metrics")
cases = [("accept_clean", "accept", True), ("accept_clean", "decline", False),
         ("accept_repaired", "accept", False), ("decline", "decline", False),
         ("decline", "accept", True), ("decline", "error", False)]
runs = [dict(method="m", rod=f"r{i}", cls=c_, repeat=0, status=st, category=metrics.category(st, c_, g_))
        for i, (c_, st, g_) in enumerate(cases)]
sm = metrics.summarize(runs)
for k in ("accuracy_per_class", "balanced_accuracy", "overall_accuracy", "false_accept_rate", "coverage",
          "abstention_precision", "abstention_recall", "unnecessary_decline_rate", "categories"):
    print(f"  {k}: {sm[k]}")
fk = metrics.fleiss_kappa([[0, 0, 0, 0, 14], [0, 2, 6, 4, 2], [0, 0, 3, 5, 6], [0, 3, 9, 2, 0], [2, 2, 8, 1, 1],
                           [7, 7, 0, 0, 0], [3, 2, 6, 3, 0], [2, 5, 3, 2, 2], [6, 5, 2, 1, 0], [0, 2, 2, 3, 7]])
print("  fleiss_kappa on the Fleiss (1971) worked example: %.4f (published 0.210)" % fk)
