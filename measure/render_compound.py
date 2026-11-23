"""Held-out compound and novel faults (spec 2026-11-18, section D; proposal
docs/proposals/2026-11-18_heldout-compound.md). Not used in development.

Same interface as measure/render.py and measure/render_heldout.py: image_case(...) -> (spec, movie),
render(spec, movie) -> dict, build(out_dir, ...) -> rod id. Injected on v3 rods only.

Compound faults: two faults at their freeze v4 sizes in one movie
- drift_low_texture: rigid_drift 0.5 + low_texture 0.03
- second_root_occlusion: second_root 30 + partial_occlusion 20 (the drop is drawn over both roots)
- drift_jitter: rigid_drift 0.5 + midline_jitter 3
- low_texture_fast: low_texture 0.03 + displacement_exceeds_patch 2x6
Milder compound faults of the supplement c029b (proposal docs/proposals/2026-11-22_heldout-supplement.md), as
separate entries so the c029 entries do not change:
- drift_low_texture_mild: rigid_drift 0.5 + low_texture 0.2
- second_root_occlusion_mild: second_root 10 + partial_occlusion 5
- drift_jitter_mild: rigid_drift 0.5 + midline_jitter 0.5
- low_texture_fast_mild: low_texture 0.2 + displacement_exceeds_patch 1x4
Novel single faults, not in the remedy tree or the agents' fault list (size from the sizing rule):
- focus_drift: Gaussian blur rising linearly from 0 at frame 0 to `size` px at the last rendered frame
- illumination_flicker: each frame's image (background and root) times a gain 1 + size * N(0, 1), own
  random stream, clipped at 0.5-1.5

With no fault the movie equals render.render's output exactly; texture and camera noise use the same
random stream as render.render, so a compound rod differs from its components only by the faults.
"""
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter

from measure import render as base
from measure import render_heldout as ho
from measure.rod import make_record, simulate, stage_track

COMPOUND = {
    "drift_low_texture": {"rigid_drift": "0.5", "low_texture": "0.03"},
    "second_root_occlusion": {"second_root": "30", "partial_occlusion": "20"},
    "drift_jitter": {"rigid_drift": "0.5", "midline_jitter": "3"},
    "low_texture_fast": {"low_texture": "0.03", "displacement_exceeds_patch": "2x6"},
}
MILD = {
    "drift_low_texture_mild": {"rigid_drift": "0.5", "low_texture": "0.2"},
    "second_root_occlusion_mild": {"second_root": "10", "partial_occlusion": "5"},
    "drift_jitter_mild": {"rigid_drift": "0.5", "midline_jitter": "0.5"},
    "low_texture_fast_mild": {"low_texture": "0.2", "displacement_exceeds_patch": "1x4"},
}
NOVEL = ("focus_drift", "illumination_flicker")
COMPOUND_FAULTS = tuple(COMPOUND) + tuple(MILD) + NOVEL
FLICKER_SEED = 104729          # own stream: the texture and camera noise stay those of render.render
FLICKER_CLIP = (0.5, 1.5)


@dataclass
class CompoundMovie(base.Movie):
    second_root: float = 0.0        # px past the main root's near edge (render_heldout second_root)
    occlusion: float = 0.0          # px drop radius (render_heldout partial_occlusion)
    focus_end: float = 0.0          # px blur at the last rendered frame (focus_drift)
    flicker: float = 0.0            # gain std (illumination_flicker)


def components(fault, size=None):
    """{component fault: size string} of one compound or novel fault."""
    if fault in COMPOUND or fault in MILD:
        return dict(COMPOUND.get(fault) or MILD[fault])
    if fault in NOVEL:
        if size is None:
            raise ValueError(f"{fault} needs a size")
        return {fault: str(size)}
    raise ValueError(f"not a compound or novel fault: {fault}")


def movie_settings(fault, size=None):
    """Movie changes and tip-speed factor of a compound or novel fault."""
    kw, speed = {}, 1.0
    for f, z in components(fault, size).items():
        if f in base.DEV_FAULTS:
            m, override, sp = base.fault_settings(f, z)
            if override is not None:
                raise ValueError(f"{f} changes the rod; not a compound component")
            clash = set(m) & set(kw)
            if clash:
                raise ValueError(f"components set the same movie setting: {sorted(clash)}")
            kw.update(m)
            speed *= sp
        elif f == "second_root":
            kw["second_root"] = float(z)
        elif f == "partial_occlusion":
            kw["occlusion"] = float(z)
        elif f == "focus_drift":
            kw["focus_end"] = float(z)
        elif f == "illumination_flicker":
            kw["flicker"] = float(z)
        else:
            raise ValueError(f"no compound injector for {f}")
    return kw, speed


def blur_at(i, n_frames, movie):
    """Blur of rendered frame i, px: the movie's fixed blur, or the focus_drift ramp if larger."""
    ramp = movie.focus_end * i / max(n_frames - 1, 1)
    return max(movie.blur, ramp)


def gains(n_frames, movie):
    if movie.flicker == 0.0:
        return np.ones(n_frames)
    rng = np.random.default_rng(movie.seed + FLICKER_SEED)
    return np.clip(1.0 + movie.flicker * rng.standard_normal(n_frames), *FLICKER_CLIP)


def render(spec, movie):
    """render.render with the compound or novel faults of a CompoundMovie. Same output dict."""
    rng = np.random.default_rng(movie.seed)
    full = replace(spec, n_frames=(base.analysis_frames(spec, movie) - 1) * movie.stride + 1)
    times, X, S, K, centre = simulate(full)
    shift = np.array([0.0, movie.width / 2.0 - np.mean(centre[0, :, 1])])
    centre = centre + shift
    stage = stage_track(full, times, centre[:, 0])
    about = centre[0, 0].copy()
    tex_X, tex_q, tex = base._texture(spec, movie, rng)
    T = len(times)
    second = None
    if movie.second_root:
        second = ho._SecondRoot(spec, ho.HeldoutMovie(**{k: getattr(movie, k) for k in vars(base.Movie())},
                                                       fault="second_root", size=movie.second_root),
                                centre[0], times[-1])
    drop = ho._frame0_point(centre[0], ho.zone(spec)[0])[0]
    gain = gains(T, movie)

    from measure.render import _project, _rigid
    from scipy.ndimage import map_coordinates
    rows, cols = np.mgrid[0:movie.height, 0:movie.width]
    pix = np.stack([rows.ravel(), cols.ravel()], axis=1).astype(float)
    frames, mid_img, mask0 = [], [], None
    for i in range(T):
        ti = times[i]
        line_w = _rigid(centre[i], ti, movie, about)
        tng0 = line_w[0] - line_w[1]
        tng0 /= np.linalg.norm(tng0)
        tngb = line_w[-1] - line_w[-2]
        tngb /= np.linalg.norm(tngb)
        cap = line_w[0] + np.outer(np.arange(60.0, 0.0, -1.0), tng0)
        tail = line_w[-1] + np.outer(np.arange(1.0, 201.0), tngb)
        line = np.vstack([cap, line_w, tail]) - stage[i]
        Xl = np.concatenate([-np.arange(60.0, 0.0, -1.0), X, X[-1] + np.arange(1.0, 201.0)])
        k, u, n = _project(pix, line)
        Xp = Xl[k] + u * (Xl[k + 1] - Xl[k])
        R = 2.0 * float(spec.h(ti))
        dist = np.where(Xp < 0, np.hypot(Xp, n), np.abs(n))
        inside = 0.5 * (1.0 - np.tanh((dist - R) / 1.0))
        q = n / R
        tv = map_coordinates(tex, [(Xp - tex_X[0]), (q - tex_q[0]) / (tex_q[1] - tex_q[0])],
                             order=3, mode="nearest")
        shade = np.clip(1.0 - 0.3 * q ** 2, 0.0, 1.0)
        sig = movie.amplitude * inside * shade * (1.0 + movie.contrast * tv)
        occl = movie.occlusion and ho.occluded(i, T)
        if second is not None or occl:
            w0 = ho._unrigid(pix + stage[i], ti, movie, about)
            if second is not None:
                op, sig2 = second.signal(w0, ti, movie)
                sig = sig * (1.0 - op) + sig2
            if occl:
                m = 0.5 * (1.0 - np.tanh((np.linalg.norm(w0 - drop, axis=1) - movie.occlusion) / 1.0))
                sig = sig * (1.0 - m) + m * 0.5 * movie.amplitude
        img = (movie.background + sig).reshape(movie.height, movie.width)
        if movie.flicker:
            img = img * gain[i]
        b = blur_at(i, T, movie)
        if b > 0:
            img = gaussian_filter(img, b)
        img = img + rng.normal(0.0, movie.noise, img.shape)
        frames.append(np.clip(img, 0, 65535).astype(np.uint16))
        if mask0 is None:
            mask0 = (inside.reshape(movie.height, movie.width) > 0.5)
        mid_img.append(line_w - stage[i])
    mid_img = np.stack(mid_img)
    if movie.midline_jitter > 0:
        mid_img = base._jitter(mid_img, movie, rng)
    return {"frames": np.stack(frames), "times": times, "stage_px": stage,
            "midline_image": mid_img, "mask0": mask0, "shift": shift,
            "spec_frames": full.n_frames}


def image_case(case, fault=None, seed=0, moved=False, width_kappa_inv=None, rotation_deg=None, size=None):
    """Spec and CompoundMovie of one rod. v3 rods only (frame size, tracked length 500 px)."""
    if not case.startswith("v3_"):
        raise ValueError("compound and novel faults are injected on v3 rods only")
    kw, speed = movie_settings(fault, size) if fault else ({}, 1.0)
    dev = {k: v for k, v in kw.items() if k in vars(base.Movie())}
    extra = {k: v for k, v in kw.items() if k not in dev}
    spec, movie = base._image_case_v3(case, None, dev, speed, seed, moved)
    return spec, CompoundMovie(**vars(movie), **extra)


def build(out_dir, case, fault=None, seed=0, moved=False, pixel_um=2.105, width_kappa_inv=None,
          rotation_deg=None, size=None):
    """Render one rod into out_dir as render.build does. Returns the id."""
    spec, movie = image_case(case, fault, seed, moved, size=size)
    rid = base.rod_id(case, fault, seed, moved, size=size)
    r = render(spec, movie)
    out_dir = Path(out_dir)
    base.write_imgdir(out_dir / f"{rid}.imgdir", r["frames"], r["times"], r["stage_px"], pixel_um)
    np.savez_compressed(out_dir / f"{rid}_midline.npz", midline_image=r["midline_image"],
                        seed=base.seed_midline(r["midline_image"][0], movie.track_length),
                        mask0=r["mask0"], track_length=movie.track_length)
    truth = make_record(replace(spec, n_frames=r["spec_frames"])).truth
    np.savez_compressed(out_dir / f"{rid}_truth.npz", stride=movie.stride,
                        fault=str(fault), case=case, size=str(size), variant="",
                        frame_size=np.array([movie.height, movie.width]),
                        track_length=movie.track_length, **truth)
    return rid
