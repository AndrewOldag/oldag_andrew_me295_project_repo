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
    midline_smooth: Optional[str] = None   # preprocess.smooth_midline level
    band_mask: Optional[str] = None        # preprocess.band_mask mode

    def args(self):
        """Command-line arguments for scripts/remote/qb_track.py."""
        a = ["--stride", str(self.stride)]
        if self.disk_radius is not None:
            a += ["--disk-radius", str(self.disk_radius)]
        if self.register:
            a += ["--register"]
        if self.midline_smooth:
            a += ["--midline-smooth", self.midline_smooth]
        if self.band_mask:
            a += ["--band-mask", self.band_mask]
        return a

    def tag(self):
        parts = [f"st{self.stride}"]
        if self.disk_radius is not None:
            parts.append(f"r{self.disk_radius}")
        if self.register:
            parts.append("reg")
        if self.midline_smooth:
            parts.append(f"ms{self.midline_smooth}")
        if self.band_mask:
            parts.append({"mask_second_root": "mask", "crop_to_main_root": "crop"}[self.band_mask])
        return "_".join(parts)

    def to_dict(self):
        return asdict(self)


def apply_remedy(settings, remedy, setting, base_disk_radius):
    """New settings for a remedy, and a one-line description of the change."""
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
        return replace(s, register=True), "frames registered on the basal tissue before tracking"
    if remedy == "smooth_midline":
        if s.midline_smooth == setting:
            raise NotAvailable(f"midline already smoothed ({setting})")
        return replace(s, midline_smooth=setting), f"midline source smoothed ({setting})"
    if remedy == "crop_or_mask":
        if s.band_mask == setting:
            raise NotAvailable(f"{setting} already applied")
        return replace(s, band_mask=setting), f"frames limited to the main root ({setting})"
    if remedy == "switch_midline_source":
        raise NotAvailable("synthetic rods have one midline source (the true midline); "
                           "the ML and classical sources exist only for real movies")
    if remedy == "use_width_free_ratio":
        raise NotAvailable("the tracker has no setting for it; it changes the reported quantity, "
                           "not the measurement")
    raise NotAvailable(f"unknown remedy {remedy!r}")
