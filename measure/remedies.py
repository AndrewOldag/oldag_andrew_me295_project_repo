"""What each remedy changes in a measurement run. Table: docs/decisions.md (2026-10-10).

A remedy is applied to the current settings and the measurement is re-run.
A remedy that cannot be carried out raises NotAvailable with the reason; it
is never imitated.
"""
from dataclasses import dataclass, asdict, replace
from typing import Optional


class NotAvailable(Exception):
    pass


@dataclass(frozen=True)
class TrackSettings:
    stride: int = 1                        # analysis frame stride (qb_track --stride)
    disk_radius: Optional[int] = None      # tracker disk radius, px; None = the tracker's split default
    register: bool = False                 # preprocess.register_frames before tracking
    register_from_px: Optional[int] = None # registration band start, px from the tip, from the record's profile
    midline_smooth: Optional[str] = None   # preprocess.smooth_midline level
    band_mask: Optional[str] = None        # preprocess.band_mask mode
    width_free: bool = False               # report centre strain rate and width-free ratio; skip plane sections

    def args(self):
        """Command-line arguments for scripts/remote/qb_track.py."""
        a = ["--stride", str(self.stride)]
        if self.disk_radius is not None:
            a += ["--disk-radius", str(self.disk_radius)]
        if self.register:
            if self.register_from_px is None:
                raise ValueError("register needs register_from_px (the 0.6-1.0 band of 2026-10-10 is retired)")
            a += ["--register", "--register-from-px", str(self.register_from_px)]
        if self.midline_smooth:
            a += ["--midline-smooth", self.midline_smooth]
        if self.band_mask:
            a += ["--band-mask", self.band_mask]
        return a

    def tag(self):
        """Names the tracker run. width_free changes no tracker run and is not in it."""
        parts = [f"st{self.stride}"]
        if self.disk_radius is not None:
            parts.append(f"r{self.disk_radius}")
        if self.register:                                  # reg: the retired 0.6-1.0 band (2026-10-10 runs)
            parts.append("reg" if self.register_from_px is None else f"reg2p{self.register_from_px}")
        if self.midline_smooth:
            parts.append(f"ms{self.midline_smooth}2")     # 2: linear-end smoothing (2026-10-11); no reuse of older runs
        if self.band_mask:
            parts.append({"mask_second_root": "mask", "crop_to_main_root": "crop"}[self.band_mask])
        return "_".join(parts)

    def to_dict(self):
        return asdict(self)


def apply_remedy(settings, remedy, setting, base_disk_radius, record=None):
    """New settings for a remedy, and a one-line description of the change.

    record: the current measurement; register_frames reads the band start from its strain-rate profile."""
    s = settings
    if remedy == "change_frame_stride":
        if setting == "half":
            if s.stride == 1:
                raise NotAvailable("every frame is already used (stride 1)")
            new = replace(s, stride=max(1, s.stride // 2))
        else:
            new = replace(s, stride=s.stride * 2)
        return new, f"frame stride {s.stride} -> {new.stride}"
    if remedy == "enlarge_patch":
        factor = {"1.5x": 1.5, "2x": 2.0}[setting]
        r = int(round(base_disk_radius * factor))
        if s.disk_radius == r:
            raise NotAvailable(f"disk radius is already {r} px")
        return replace(s, disk_radius=r), f"tracker disk radius {s.disk_radius or base_disk_radius} -> {r} px"
    if remedy == "register_frames":
        if s.register:
            raise NotAvailable("frames are already registered")
        from measure.preprocess import registration_band_start
        start = registration_band_start(record) if record is not None else None
        if start is None:
            raise NotAvailable("no strain-rate profile to find the non-growing tissue in")
        return (replace(s, register=True, register_from_px=int(round(start))),
                f"frames registered on the non-growing tissue (from {start:.0f} px from the tip) before tracking")
    if remedy == "smooth_midline":
        if s.midline_smooth == setting:
            raise NotAvailable(f"midline already smoothed ({setting})")
        return replace(s, midline_smooth=setting), f"midline source smoothed ({setting})"
    if remedy == "crop_or_mask":
        if s.band_mask == setting:
            raise NotAvailable(f"{setting} already applied")
        return replace(s, band_mask=setting), f"frames limited to the main root ({setting})"
    if remedy == "use_width_free_ratio":
        if s.width_free:
            raise NotAvailable("the width-free ratio is already reported")
        return (replace(s, width_free=True),
                "report the centre strain rate and the width-free ratio; plane-sections check skipped")
    raise NotAvailable(f"unknown remedy {remedy!r}")
