# c027 example traces

Outcome and check values only; REGR, growth-zone and flank values are `[masked]`.

## Accepted after repair: 0714_m7__w18-20

- Initial closure 19.75 px/h; final 18.32 px/h; final settings st1_mslight4

### Step 1: request_info
- Arguments: `{"kind": "stage_log_summary"}`
- Rationale: Closure fails slightly (19.7 vs 19.0 px/h) and rigid invariance was not run. A closure failure usually means unlogged drift or rotation, or a bad stage correction, so the stage log comes first.
- Result: `{"stage_moves": 69, "frame_pairs": 69, "move_size_px_median": 1.0, "move_size_px_max": 1.0, "closure_residual_px_at_moves": 5.22, "closure_residual_px_elsewhere": null, "closure_residual_px_per_h_at_moves": 19.75, "closure_residual_px_per_h_elsewhere": 0.0, "velocity_jump_at_moves_px_per_h": "[masked]"}`

### Step 2: request_info
- Arguments: `{"kind": "velocity_profile"}`
- Rationale: The stage moved in all 69 of 69 frame pairs, so "at moves" and "elsewhere" cannot be compared, and the stage log cannot tell a bad stage correction from unlogged rigid drift. The velocity profile should show whether the residual is a uniform rigid offset (drift) or a jump tied to each correction.
- Result: `{"s_um": [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000, 2050, 2100, 2150], "velocity_um_per_h": "[masked]", "strain_rate_pct_per_h": "[masked]", "peak_strain_rate_pct_per_h": "[masked]", "peak_at_um": "[masked]", "negative_strain_rate_min_pct_per_h": "[masked]", "basal_velocity_um_per_h": "[masked]", "tip_path_um_per_h": 402.0, "tip_net_displacement_um_per_h": 65.2, "flank_spacing_rate_pct_per_h": "[masked]", "flank_spacing_rate_max_abs_pct_per_h": "[masked]"}`

### Step 3: request_info
- Arguments: `{"kind": "frame_quality"}`
- Rationale: The tip path (402 µm/h) is far longer than the net tip displacement (65.2 µm/h), and the flank-spacing rate swings noisily (±[masked]). Both point to a jittering midline or tip, so frame quality must be checked first to rule out low texture or blur before naming midline jitter.
- Result: `{"frames": [{"frame": 0, "texture_contrast": 0.061, "focus": 0.0288, "bright_objects_over_500px": 1}, {"frame": 35, "texture_contrast": 0.061, "focus": 0.0284, "bright_objects_over_500px": 1}, {"frame": 69, "texture_contrast": 0.0625, "focus": 0.0292, "bright_objects_over_500px": 1}], "note": "texture_contrast: high-pass std / mean inside the root band; focus: mean gradient / mean; bright_objects_over_500px: count", "reference": {"basis": "PROVISIONAL: 24 real 1 h windows labelled clean, 3 frames each; marks low texture and blur, not uneven lighting or debris", "texture_contrast": {"median": 0.0648, "lowest": 0.0439}, "focus": {"median": 0.0286, "lowest": 0.0213}}}`

### Step 4: request_info
- Arguments: `{"kind": "midline_jitter"}`
- Rationale: Frame quality is normal (texture 0.061–0.063 and focus about 0.029, both near the clean medians, with one bright object), so low texture and blur are ruled out. The tip path (402 µm/h) is much longer than the net tip displacement (65 µm/h), which points to midline jitter, so I'm requesting direct midline-jitter evidence before naming that fault.
- Result: `{"sideways_offset_rms_px": 2.22, "frame_to_frame_change_rms_px": 0.97, "tip_second_difference_rms_px": 19.83, "midline_smooth": null}`

### Step 5: apply_remedy
- Arguments: `{"fault": "midline_jitter", "remedy": "smooth_midline", "setting": "light"}`
- Rationale: Frame quality is normal, so low texture and blur are ruled out. The tip second difference is very large (19.8 px RMS) and the tip path is about six times the net tip displacement (402 vs 65 µm/h), which points to a jittering midline/tip inflating the closure residual, so I'm smoothing the midline lightly.
- Result: `{"rechecked": true, "change": "midline source smoothed (light)", "failed_checks": [], "passed_checks": ["closure"], "not_run": ["rigid_invariance"], "reported_not_gating": ["plane_sections"], "check_values": {"rigid_invariance": {"before": null, "after": null, "threshold": null, "unit": "%/h"}, "closure": {"before": 19.746, "after": 18.317, "threshold": 19.0, "unit": "px/h"}, "plane_sections": "[masked]"}, "settings_left": "no further setting: smooth_midline cannot be applied again or at another setting"}`

### Step 6: accept
- Arguments: `{"confidence": 0.7}`
- Rationale: Light midline smoothing brought closure from 19.7 down to 18.3 px/h, under the 19.0 px/h threshold. That fits tip jitter as the cause, since the tip second difference was 19.8 px RMS while frame quality was normal. The velocity profile looks like a normal growth curve, levelling off at about [masked]/h with a strain-rate peak of about [masked] near [masked], so I am reporting the kinematics with moderate confidence because the pass is narrow and rigid invariance was not run.

## Declined by the agent: 0708_c10__w0-2

- Initial closure 76.11 px/h; final 76.11 px/h; final settings st1

### Step 1: request_info
- Arguments: `{"kind": "stage_log_summary"}`
- Rationale: Closure fails badly (76.1 vs 19.0 px/h), and rigid invariance was not run. Unlogged drift, rotation or a bad stage correction are the likely causes, so the stage log is the first evidence to check.
- Result: `{"stage_moves": 74, "frame_pairs": 79, "move_size_px_median": 2.0, "move_size_px_max": 11.4, "closure_residual_px_at_moves": 7.17, "closure_residual_px_elsewhere": 3.59, "closure_residual_px_per_h_at_moves": 70.49, "closure_residual_px_per_h_elsewhere": 5.74, "velocity_jump_at_moves_px_per_h": "[masked]"}`

### Step 2: apply_remedy
- Arguments: `{"fault": "bad_stage_correction", "remedy": "register_frames", "setting": null}`
- Rationale: The closure error is concentrated at the logged stage moves (70.5 px/h at moves vs 5.7 px/h elsewhere), and the velocity jumps by 134.6 px/h at those moves, so the stage correction is wrong. Registering the frames to each other should replace the faulty stage-log correction.
- Result: `{"rechecked": true, "change": "frames registered on the non-growing tissue (from 1400 px from the tip) before tracking", "failed_checks": ["closure"], "passed_checks": [], "not_run": ["rigid_invariance"], "reported_not_gating": ["plane_sections"], "check_values": {"rigid_invariance": {"before": null, "after": null, "threshold": null, "unit": "%/h"}, "closure": {"before": 76.114, "after": 74.333, "threshold": 19.0, "unit": "px/h"}, "plane_sections": "[masked]"}, "rolled_back": true, "note": "the remedy made no failing check pass and lowered none by a quarter; the settings and measurement from before it are restored. The step counts"}`

### Step 3: request_info
- Arguments: `{"kind": "displacement_vs_patch_radius"}`
- Rationale: Registering the frames barely changed closure (76.1 to 74.3 px/h), so the stage correction may not be the real cause. The residual is still concentrated at stage moves, and those moves reach 11.4 px against a 5 px patch radius, so I need to check whether frame-to-frame displacement exceeds the patch before declining.
- Result: `{"disk_radius_px": 5, "frame_stride": 1, "frame_interval_s": 90.0, "tip_px_per_pair_median": 6.32, "tip_px_per_pair_max": 21.59, "tracked_px_per_pair_median": 1.63, "tracked_px_per_pair_p95": 5.01, "tip_step_over_radius": 1.26, "fraction_points_lost": 0.0}`

### Step 4: apply_remedy
- Arguments: `{"fault": "displacement_exceeds_patch", "remedy": "enlarge_patch", "setting": "1.5x"}`
- Rationale: The median tip step is 6.32 px per frame pair against a 5 px patch radius (ratio 1.26, maximum 21.59 px), so the tracker is losing the tip between frames. The stride is already 1 and can't be halved, so enlarging the patch is the remedy that fits.
- Result: `{"rechecked": true, "change": "tracker disk radius 5 -> 8 px", "failed_checks": ["closure"], "passed_checks": [], "not_run": ["rigid_invariance"], "reported_not_gating": ["plane_sections"], "check_values": {"rigid_invariance": {"before": null, "after": null, "threshold": null, "unit": "%/h"}, "closure": {"before": 76.114, "after": 80.879, "threshold": 19.0, "unit": "px/h"}, "plane_sections": "[masked]"}, "rolled_back": true, "note": "the remedy made no failing check pass and lowered none by a quarter; the settings and measurement from before it are restored. The step counts"}`

### Step 5: decline
- Arguments: `{"fault": "bad_stage_correction", "reason": "Closure fails (76.1 vs 19.0 px/h) and the error sits at the logged stage moves (70.5 vs 5.7 px/h elsewhere). Registering the frames lowered no failing check by a quarter and has no further setting, so the tip motion cannot be trusted."}`
- Rationale: The closure error sits at the stage moves, which points to a bad stage correction. Registering the frames (the remedy for that fault) left closure failing and cannot be reapplied. Enlarging the patch made closure worse and no point tracks were lost, so the displacement fault has no supporting evidence of its own.

## Auditor flag

- Root 0708_c10, run r02: `{"decision": "flag", "order": 1, "reason": "summary_outlier", "evidence": ["centre_peak_at_um", "growth_zone_length_um", "flank_difference_at_um", "centre_peak_regr_pct_per_h"]}`

