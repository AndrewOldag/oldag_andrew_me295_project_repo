"""Image-level synthetic rods: textured movies moved by the field-level kinematics.

The texture is fixed to the material: a point at material arc length X and
relative normal offset q = n / R(t) keeps its texture value. The movie is
written as an .imgdir the tracker's own loader reads (one ImageData npy per
frame, stage log, elapsed times, axis signs).

Development fault injectors (spec 2026-10-09, item 3): rigid_drift,
displacement_exceeds_patch, midline_jitter, low_texture, width_change.
Held-out faults have no injector here.
"""
from dataclasses import dataclass, field, replace
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.spatial import cKDTree

from measure.rod import (RodSpec, field_cases, make_record, simulate, normals, stage_track,
                         width_change_spec, rigid_rotation_spec)

DEV_FAULTS = ("rigid_drift", "displacement_exceeds_patch", "midline_jitter",
              "low_texture", "width_change")


@dataclass
class Movie:
    height: int = 640
    width: int = 320
    background: float = 1000.0
    amplitude: float = 2000.0       # root brightness above background
    contrast: float = 0.30          # texture std relative to root brightness
    texture_sigma: float = 1.5      # px, texture correlation length
    noise: float = 20.0             # camera noise std, counts
    blur: float = 0.0               # px, Gaussian blur of each frame
    stride: int = 1                 # analysis frame stride; every frame is rendered
    track_length: float = 400.0     # length of the seed midline handed to the tracker, px
    rigid_rotation: float = 0.0     # unlogged rotation, rad/s, about the frame-0 tip
    rigid_velocity: tuple = (0.0, 0.0)   # unlogged translation, px/s
    midline_jitter: float = 0.0     # sideways jitter of the midline source, px std
    jitter_length: float = 50.0     # correlation length of the jitter along s, px
    analysis_frames: int = 0        # frames left after the stride; 0 = spec.n_frames
    seed: int = 0


def fault_settings(fault):
    """Movie and spec changes for one development fault."""
    if fault is None:
        return {}, None
    if fault == "rigid_drift":
        return {"rigid_velocity": (0.4 / 90.0, 0.2 / 90.0),
                "rigid_rotation": np.deg2rad(0.02) / 90.0}, None
    if fault == "displacement_exceeds_patch":
        return {"stride": 12, "analysis_frames": 21}, None
    if fault == "midline_jitter":
        return {"midline_jitter": 3.0}, None
    if fault == "low_texture":
        return {"contrast": 0.03, "blur": 2.0, "noise": 40.0}, None
    if fault == "width_change":
        return {}, "width_change"
    raise ValueError(f"unknown or held-out fault: {fault}")


def _texture(spec, movie, rng):
    """Material texture on (X, q): X from -60 to length + 260 px, q from -1.4 to 1.4."""
    r0 = 2.0 * float(spec.h(0.0))
    X = np.arange(-60.0, spec.length + 260.0, 1.0)
    q = np.arange(-1.4, 1.4 + 1e-9, 1.0 / r0)
    tex = gaussian_filter(rng.standard_normal((len(X), len(q))), movie.texture_sigma)
    tex /= tex.std()
    return X, q, tex


def _project(points, line):
    """Nearest point on a polyline for each pixel: segment index, parameter, signed normal offset."""
    tree = cKDTree(line)
    _, j = tree.query(points)
    best = None
    for k in (j - 1, j):
        k = np.clip(k, 0, len(line) - 2)
        a, b = line[k], line[k + 1]
        ab = b - a
        u = np.clip(np.sum((points - a) * ab, axis=1) / np.sum(ab * ab, axis=1), 0.0, 1.0)
        foot = a + u[:, None] * ab
        d = np.linalg.norm(points - foot, axis=1)
        if best is None:
            best = [k, u, foot, d]
        else:
            take = d < best[3]
            for i, v in enumerate((k, u, foot, d)):
                best[i] = np.where(take[:, None] if np.ndim(v) == 2 else take, v, best[i])
    k, u, foot, d = best
    tng = line[k + 1] - line[k]
    tng /= np.linalg.norm(tng, axis=1, keepdims=True)
    nrm = np.stack([-tng[:, 1], tng[:, 0]], axis=1)
    n = np.sum((points - foot) * nrm, axis=1)
    return k, u, n


def _rigid(points, ti, movie, about):
    if movie.rigid_rotation == 0.0 and movie.rigid_velocity == (0.0, 0.0):
        return points
    c, s = np.cos(movie.rigid_rotation * ti), np.sin(movie.rigid_rotation * ti)
    rot = np.array([[c, -s], [s, c]])
    return (points - about) @ rot.T + about + np.asarray(movie.rigid_velocity) * ti


def render(spec, movie):
    """Render a movie. Returns a dict of frames and the true geometry per kept frame."""
    rng = np.random.default_rng(movie.seed)
    full = replace(spec, n_frames=(analysis_frames(spec, movie) - 1) * movie.stride + 1)
    times, X, S, K, centre = simulate(full)
    # centre the frame-0 rod across the image
    shift = np.array([0.0, movie.width / 2.0 - np.mean(centre[0, :, 1])])
    centre = centre + shift
    stage = stage_track(full, times, centre[:, 0])
    about = centre[0, 0].copy()
    tex_X, tex_q, tex = _texture(spec, movie, rng)

    rows, cols = np.mgrid[0:movie.height, 0:movie.width]
    pix = np.stack([rows.ravel(), cols.ravel()], axis=1).astype(float)
    keep = np.arange(len(times))
    frames, mid_img, mask0 = [], [], None
    for i in keep:
        ti = times[i]
        line_w = _rigid(centre[i], ti, movie, about)           # world, incl. unlogged motion
        tng0 = line_w[0] - line_w[1]
        tng0 /= np.linalg.norm(tng0)
        tngb = line_w[-1] - line_w[-2]
        tngb /= np.linalg.norm(tngb)
        cap = line_w[0] + np.outer(np.arange(60.0, 0.0, -1.0), tng0)    # straight extension past the tip
        tail = line_w[-1] + np.outer(np.arange(1.0, 201.0), tngb)       # and past the base
        line = np.vstack([cap, line_w, tail]) - stage[i]                # image coordinates
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
        img = movie.background + movie.amplitude * inside * shade * (1.0 + movie.contrast * tv)
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
        mid_img = _jitter(mid_img, movie, rng)
    return {"frames": np.stack(frames), "times": times[keep], "stage_px": stage[keep],
            "midline_image": mid_img, "mask0": mask0, "shift": shift,
            "spec_frames": full.n_frames}


def analysis_frames(spec, movie):
    return movie.analysis_frames or spec.n_frames


def _jitter(mid, movie, rng):
    """Sideways jitter of the midline source, smooth along s, independent per frame."""
    out = mid.copy()
    step = np.median(np.linalg.norm(np.diff(mid[0], axis=0), axis=1))
    for i in range(len(mid)):
        w = gaussian_filter(rng.standard_normal(mid.shape[1]), movie.jitter_length / step / 2.0,
                            mode="nearest")
        w *= movie.midline_jitter / w.std()
        out[i] += w[:, None] * normals(mid[i])
    return out


def seed_midline(mid_img0, track_length, step=2.0):
    """Frame-0 midline for the tracker, tip first, cut at track_length px."""
    seg = np.linalg.norm(np.diff(mid_img0, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    return mid_img0[s <= track_length][::max(1, int(round(step / np.median(seg))))]


def write_imgdir(path, frames, times_s, stage_px, pixel_um):
    """Write frames, stage log and times in the layout the tracker's loader reads.

    Axis signs are both +1, so stage row = Y / pixel and col = X / pixel.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    for t, fr in enumerate(frames):
        np.save(path / f"ImageData_Ch0_TP{t:07d}.npy", fr[None, :, :])
    xyz = np.column_stack([stage_px[:, 1] * pixel_um, stage_px[:, 0] * pixel_um,
                           np.zeros(len(stage_px))])
    (path / "StagePositionData.yaml").write_text(
        "StructArrayValues: [" + ", ".join(f"{v:.4f}" for v in xyz.ravel()) + "]\n")
    ms = np.round(np.asarray(times_s) * 1000.0).astype(int)
    (path / "ElapsedTimes.yaml").write_text(
        f"theElapsedTimes: [{len(ms)}, " + ", ".join(str(v) for v in ms) + "]\n")
    (path / "ChannelRecord.yaml").write_text("mMoveFieldDownSign: 1\nmMoveFieldRightSign: 1\n")


# Expected outcome of each check for clean image-level cases. rigid_rotation
# turns about a point basal to the tracked length, so the basal tracked tissue
# moves and closure fails (decisions, 2026-10-10).
_PASS = {"rigid_invariance": True, "closure": True, "plane_sections": True}
IMAGE_EXPECTED = {
    "growth_zone": dict(_PASS), "bending": dict(_PASS), "rigid_translation": dict(_PASS),
    "rigid_rotation": {"rigid_invariance": True, "closure": False, "plane_sections": True},
}


def variant_tag(width_kappa_inv=None, rotation_deg=None):
    tag = ""
    if width_kappa_inv is not None:
        tag += f"_k{width_kappa_inv:g}"
    if rotation_deg is not None:
        tag += f"_r{rotation_deg:g}"
    return tag


def image_case(case, fault=None, seed=0, moved=False, width_kappa_inv=None, rotation_deg=None):
    """Spec and movie settings for one image-level rod.

    case: a field-level case name (growth_zone, bending, rigid_translation, ...).
    moved: add the rigid motion used by the rigid-invariance check.
    width_kappa_inv: curvature 1/width_kappa_inv px for the width_change fault (default 400).
    rotation_deg: rotation rate of the rigid_rotation case, deg/frame (default 0.1).
    """
    movie_kw, spec_override = fault_settings(fault)
    name = spec_override or case
    if name == "width_change":
        spec = width_change_spec(width_kappa_inv or 400.0)
        if (width_kappa_inv or 400.0) < 800.0:
            movie_kw = dict(movie_kw, width=640)      # the more curved rod leaves a 320 px frame
    elif name == "rigid_rotation" and rotation_deg is not None:
        spec = rigid_rotation_spec(rotation_deg)
    else:
        spec = next(s for s in field_cases() if s.name == name)
    movie = Movie(seed=seed, **movie_kw)
    if moved:
        movie = replace(movie, rigid_rotation=movie.rigid_rotation + np.deg2rad(0.1) / 90.0,
                        rigid_velocity=tuple(np.add(movie.rigid_velocity, (0.5 / 90.0, 0.3 / 90.0))))
    return spec, movie


def build(out_dir, case, fault=None, seed=0, moved=False, pixel_um=2.105, width_kappa_inv=None,
          rotation_deg=None):
    """Render one rod into out_dir: <id>.imgdir, <id>_midline.npz, <id>_truth.npz. Returns the id."""
    spec, movie = image_case(case, fault, seed, moved, width_kappa_inv, rotation_deg)
    rid = (f"{case}_{fault or 'clean'}{variant_tag(width_kappa_inv, rotation_deg)}_s{seed}"
           + ("_moved" if moved else ""))
    r = render(spec, movie)
    out_dir = Path(out_dir)
    write_imgdir(out_dir / f"{rid}.imgdir", r["frames"], r["times"], r["stage_px"], pixel_um)
    np.savez_compressed(out_dir / f"{rid}_midline.npz", midline_image=r["midline_image"],
                        seed=seed_midline(r["midline_image"][0], movie.track_length),
                        mask0=r["mask0"])
    truth = make_record(replace(spec, n_frames=r["spec_frames"])).truth
    np.savez_compressed(out_dir / f"{rid}_truth.npz", stride=movie.stride,
                        fault=str(fault), case=case, variant=variant_tag(width_kappa_inv, rotation_deg),
                        frame_size=np.array([movie.height, movie.width]),
                        track_length=movie.track_length, **truth)
    return rid
