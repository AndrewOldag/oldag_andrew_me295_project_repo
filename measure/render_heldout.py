"""Held-out fault injectors for final scoring. Not used in development.

Same interface as measure/render.py: image_case(...) -> (spec, movie),
render(spec, movie) -> dict, build(out_dir, ...) -> rod id. The movie is a
HeldoutMovie: a render.Movie with the fault and its size. At size 0 (or no
fault) the movie equals render.render's output exactly.

Faults (proposal docs/proposals/2026-10-12_heldout-faults.md; sizes and
outcomes wait for Andrew):
- second_root: a second root, drawn on top, grows at 45 deg toward the
  main root at s = 150 px and enters it during the window. size = how far
  its outline ends past the main root's near edge, px (0 = no second root)
- fast_rotation: unlogged rotation burst near the tracker limit: `size`
  deg/frame for 3 frames from mid-window, about the frame-0 midline point
  at s = track_length / 2
- bad_stage_correction: at the first stage move from mid-window on, the log
  under-reports the move by `size` px; the error stays in the log after it
- flank_swap: the texture is mirrored across the midline (the two flanks
  exchange) for the last `size` fraction of the frame pairs
- partial_occlusion: an opaque drop of radius `size` px, fixed on the
  sample, covers the frame-0 midline at s = 150 px (the REGR peak) for the
  middle third of the frames
- stage_log_missing (freeze v3): images as recorded; the stage log stays at
  its last logged value for the last `size` fraction of the frames (1 = no
  stage move logged). Basis: the real montage movies, whose stage-tracking
  moves are not in the table the tracker reads

On a v3 rod (case `v3_...`) the growth-zone position and tip speed are the
v3 values (measure.rod.V3_S_MID, V3_V_END).

Second root and drop are fixed to the sample: the rigid motion of the
invariance check moves them with the root.
"""
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates

from measure import render as base
from measure.rod import make_record, normals, simulate, stage_track
from measure.rod import V_END, V3_S_MID, V3_V_END

HELDOUT_FAULTS = ("second_root", "fast_rotation", "bad_stage_correction", "flank_swap", "partial_occlusion",
                  "stage_log_missing")

# Name the diagnostician should give (agents/actions.py FAULTS) and the expected correct outcome.
# Proposal of 2026-10-12, not approved; labels need the remedy sweep at the approved sizes.
EXPECTED = {
    "second_root": {"fault": "second_root", "outcome": "decline"},
    "fast_rotation": {"fault": "fast_rotation", "outcome": "accept", "remedy": "register_frames"},
    "bad_stage_correction": {"fault": "bad_stage_correction", "outcome": "accept", "remedy": "register_frames"},
    "flank_swap": {"fault": "unknown", "outcome": "decline"},
    "partial_occlusion": {"fault": "low_texture", "outcome": "decline"},
    "stage_log_missing": {"fault": "bad_stage_correction", "outcome": "accept", "remedy": "register_frames"},
}

GROWTH_PEAK_S = 150.0          # px from the tip, REGR peak of the growth_zone case
SECOND_ROOT_ANGLE = 45.0       # deg between the second root and the main root
BURST_FRAMES = 3               # fast_rotation
SECOND_ROOT_SEED = 7919        # second root texture: own stream, so the main root's texture and noise are unchanged


@dataclass
class HeldoutMovie(base.Movie):
    fault: str = None
    size: float = 0.0


def _frame0_point(centre0, s):
    """Frame-0 world midline point at arc length s px from the tip, and the index."""
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(centre0, axis=0), axis=1))])
    j = int(np.argmin(np.abs(arc - s)))
    return centre0[j].copy(), j


def _unrigid(points, ti, movie, about):
    """Inverse of render._rigid: sample coordinates of world points."""
    if movie.rigid_rotation == 0.0 and movie.rigid_velocity == (0.0, 0.0):
        return points
    c, s = np.cos(movie.rigid_rotation * ti), np.sin(movie.rigid_rotation * ti)
    rot = np.array([[c, -s], [s, c]])
    return (points - about - np.asarray(movie.rigid_velocity) * ti) @ rot + about


def _rotate(points, angle, about):
    c, s = np.cos(angle), np.sin(angle)
    return (points - about) @ np.array([[c, -s], [s, c]]).T + about


def burst_angle(i, n_frames, size_deg):
    """fast_rotation: cumulative burst angle at frame i, rad."""
    k0 = n_frames // 2
    return np.deg2rad(size_deg) * np.clip(i - k0 + 1, 0, BURST_FRAMES)


def swap_from(n_frames, size):
    """flank_swap: first mirrored frame (n_frames = no swap)."""
    return n_frames - int(round(size * (n_frames - 1)))


def occluded(i, n_frames):
    return n_frames // 3 <= i < (2 * n_frames) // 3


def zone(spec):
    """(REGR peak position px, tip speed px/s) of the rod the fault is injected on: v2 growth_zone or v3."""
    return (V3_S_MID, V3_V_END) if spec.name.startswith("v3_") else (GROWTH_PEAK_S, V_END)


def missing_stage_log(stage, size):
    """stage_log_missing: the stage log stays at its last logged value for the last `size` fraction of the
    frames (1 = the frame-0 value throughout: no stage move is logged)."""
    out = stage.copy()
    k = max(1, swap_from(len(stage), size))
    out[k:] = stage[k - 1]
    return out


def logged_stage(stage, size):
    """bad_stage_correction: the stage log with one move under-reported by size px."""
    T = len(stage)
    out = stage.copy()
    moves = [i for i in range(max(1, T // 2), T) if np.any(stage[i] != stage[i - 1])]
    if moves:
        k = moves[0]
        d = stage[k] - stage[k - 1]
        d = d / np.linalg.norm(d)
    else:
        k, d = T // 2, np.array([1.0, 0.0])
    out[k:] -= size * d
    return out, k


class _SecondRoot:
    """Straight second root fixed to the sample; its tip grows at the main tip speed toward the main root."""

    def __init__(self, spec, movie, centre0, t_end):
        self.R = 2.0 * float(spec.h(0.0))
        peak_s, self.speed = zone(spec)
        C, j = _frame0_point(centre0, peak_s)
        nrm = normals(centre0)[j]
        tng = centre0[max(j - 1, 0)] - centre0[j + 1]          # toward the tip
        tng /= np.linalg.norm(tng)
        a = np.deg2rad(SECOND_ROOT_ANGLE)
        self.e = np.cos(a) * tng - np.sin(a) * nrm              # its growth direction: tipward and across
        self.p = np.array([-self.e[1], self.e[0]])
        # Tip centre at the end of the window. The rounded tip has radius R, so the outline reaches
        # (R - size) from the main midline: size px past the main root's near edge
        self.tip_end = C + (self.R - movie.size + self.R) * nrm
        self.t_end = t_end
        rng = np.random.default_rng(movie.seed + SECOND_ROOT_SEED)
        self.a = np.arange(-2000.0, 100.0, 1.0)
        self.q = np.arange(-1.4, 1.4 + 1e-9, 1.0 / self.R)
        tex = gaussian_filter(rng.standard_normal((len(self.a), len(self.q))), movie.texture_sigma)
        self.tex = tex / tex.std()

    def signal(self, w0, ti, movie):
        """(opacity, brightness) at sample points w0."""
        rel = w0 - self.tip_end
        a, n = rel @ self.e, rel @ self.p
        a_tip = -self.speed * (self.t_end - ti)
        dist = np.where(a > a_tip, np.hypot(a - a_tip, n), np.abs(n))
        inside = 0.5 * (1.0 - np.tanh((dist - self.R) / 1.0))
        q = n / self.R
        tv = map_coordinates(self.tex, [a - self.a[0], (q - self.q[0]) / (self.q[1] - self.q[0])],
                             order=3, mode="nearest")
        shade = np.clip(1.0 - 0.3 * q ** 2, 0.0, 1.0)
        return inside, movie.amplitude * inside * shade * (1.0 + movie.contrast * tv)


def render(spec, movie):
    """render.render with the held-out fault of a HeldoutMovie. Same output dict."""
    fault = getattr(movie, "fault", None)
    size = float(getattr(movie, "size", 0.0) or 0.0)
    if fault is not None and fault not in HELDOUT_FAULTS:
        raise ValueError(f"not a held-out fault: {fault}")
    on = fault is not None and size != 0.0
    rng = np.random.default_rng(movie.seed)
    full = replace(spec, n_frames=(base.analysis_frames(spec, movie) - 1) * movie.stride + 1)
    times, X, S, K, centre = simulate(full)
    shift = np.array([0.0, movie.width / 2.0 - np.mean(centre[0, :, 1])])
    centre = centre + shift
    stage = stage_track(full, times, centre[:, 0])
    about = centre[0, 0].copy()
    tex_X, tex_q, tex = base._texture(spec, movie, rng)
    T = len(times)

    pivot = _frame0_point(centre[0], movie.track_length / 2.0)[0]
    second = _SecondRoot(spec, movie, centre[0], times[-1]) if on and fault == "second_root" else None
    drop = _frame0_point(centre[0], zone(spec)[0])[0]
    k_swap = swap_from(T, size) if on and fault == "flank_swap" else T

    rows, cols = np.mgrid[0:movie.height, 0:movie.width]
    pix = np.stack([rows.ravel(), cols.ravel()], axis=1).astype(float)
    frames, mid_img, mask0 = [], [], None
    for i in range(T):
        ti = times[i]
        c_i = centre[i]
        if on and fault == "fast_rotation":
            c_i = _rotate(c_i, burst_angle(i, T, size), pivot)
        line_w = base._rigid(c_i, ti, movie, about)
        tng0 = line_w[0] - line_w[1]
        tng0 /= np.linalg.norm(tng0)
        tngb = line_w[-1] - line_w[-2]
        tngb /= np.linalg.norm(tngb)
        cap = line_w[0] + np.outer(np.arange(60.0, 0.0, -1.0), tng0)
        tail = line_w[-1] + np.outer(np.arange(1.0, 201.0), tngb)
        line = np.vstack([cap, line_w, tail]) - stage[i]
        Xl = np.concatenate([-np.arange(60.0, 0.0, -1.0), X, X[-1] + np.arange(1.0, 201.0)])
        k, u, n = base._project(pix, line)
        Xp = Xl[k] + u * (Xl[k + 1] - Xl[k])
        R = 2.0 * float(spec.h(ti))
        dist = np.where(Xp < 0, np.hypot(Xp, n), np.abs(n))
        inside = 0.5 * (1.0 - np.tanh((dist - R) / 1.0))
        q = n / R
        q_tex = -q if i >= k_swap else q
        tv = map_coordinates(tex, [(Xp - tex_X[0]), (q_tex - tex_q[0]) / (tex_q[1] - tex_q[0])],
                             order=3, mode="nearest")
        shade = np.clip(1.0 - 0.3 * q ** 2, 0.0, 1.0)
        sig = movie.amplitude * inside * shade * (1.0 + movie.contrast * tv)
        if second is not None or (on and fault == "partial_occlusion" and occluded(i, T)):
            w0 = _unrigid(pix + stage[i], ti, movie, about)
            if second is not None:
                op, sig2 = second.signal(w0, ti, movie)
                sig = sig * (1.0 - op) + sig2
            else:
                m = 0.5 * (1.0 - np.tanh((np.linalg.norm(w0 - drop, axis=1) - size) / 1.0))
                sig = sig * (1.0 - m) + m * 0.5 * movie.amplitude
        img = movie.background + sig
        img = img.reshape(movie.height, movie.width)
        if movie.blur > 0:
            img = gaussian_filter(img, movie.blur)
        img = img + rng.normal(0.0, movie.noise, img.shape)
        frames.append(np.clip(img, 0, 65535).astype(np.uint16))
        if mask0 is None:
            mask0 = (inside.reshape(movie.height, movie.width) > 0.5)
        mid_img.append(line_w - stage[i])
    mid_img = np.stack(mid_img)
    if movie.midline_jitter > 0:
        mid_img = base._jitter(mid_img, movie, rng)
    stage_log = stage
    if on and fault == "bad_stage_correction":
        stage_log = logged_stage(stage, size)[0]
    elif on and fault == "stage_log_missing":
        stage_log = missing_stage_log(stage, size)
    return {"frames": np.stack(frames), "times": times, "stage_px": stage_log,
            "midline_image": mid_img, "mask0": mask0, "shift": shift,
            "spec_frames": full.n_frames}


def image_case(case, fault=None, seed=0, moved=False, width_kappa_inv=None, rotation_deg=None, size=None):
    """Spec and HeldoutMovie for one image-level rod with a held-out fault (size: string or number)."""
    if fault is not None and fault not in HELDOUT_FAULTS:
        raise ValueError(f"not a held-out fault: {fault}")
    spec, movie = base.image_case(case, None, seed, moved, width_kappa_inv, rotation_deg, None)
    return spec, HeldoutMovie(**vars(movie), fault=fault, size=float(size) if size else 0.0)


def build(out_dir, case, fault=None, seed=0, moved=False, pixel_um=2.105, width_kappa_inv=None,
          rotation_deg=None, size=None):
    """Render one rod into out_dir as render.build does. Returns the id."""
    spec, movie = image_case(case, fault, seed, moved, width_kappa_inv, rotation_deg, size)
    rid = base.rod_id(case, fault, seed, moved, width_kappa_inv, rotation_deg, size)
    r = render(spec, movie)
    out_dir = Path(out_dir)
    base.write_imgdir(out_dir / f"{rid}.imgdir", r["frames"], r["times"], r["stage_px"], pixel_um)
    np.savez_compressed(out_dir / f"{rid}_midline.npz", midline_image=r["midline_image"],
                        seed=base.seed_midline(r["midline_image"][0], movie.track_length),
                        mask0=r["mask0"], track_length=movie.track_length)
    truth = make_record(replace(spec, n_frames=r["spec_frames"])).truth
    np.savez_compressed(out_dir / f"{rid}_truth.npz", stride=movie.stride,
                        fault=str(fault), case=case, size=str(size),
                        variant=base.variant_tag(width_kappa_inv, rotation_deg),
                        frame_size=np.array([movie.height, movie.width]),
                        track_length=movie.track_length, **truth)
    return rid
