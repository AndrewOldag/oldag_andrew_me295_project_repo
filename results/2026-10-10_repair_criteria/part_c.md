Proposed tolerance (not approved): centre REGR RMS error <= 1.0 %/h, flank-difference RMS error <= 0.5 %/h.
Basis: largest clean values 0.77 and 0.37 %/h over part A settings that keep every clean run passing (st1, st1_crop, st1_mask, st1_r22, st1_r30), rounded up to the next 0.25 %/h.

Labels, from the part B states only (the fitting remedy's one- and two-step states). A label is final only for the approved sizes:

| Rod | Label | Repairing sequence |
| :-- | :-- | :-- |
| growth_zone_rigid_drift_z0.25_s0 | not repairable | - |
| growth_zone_rigid_drift_z0.25_s1 | not repairable | - |
| growth_zone_rigid_drift_z0.25_s2 | not repairable | - |
| growth_zone_rigid_drift_z0.5_s0 | not repairable | - |
| growth_zone_rigid_drift_z0.5_s1 | not repairable | - |
| growth_zone_rigid_drift_z0.5_s2 | not repairable | - |
| growth_zone_rigid_drift_z0.75_s0 | not repairable | - |
| growth_zone_rigid_drift_z0.75_s1 | not repairable | - |
| growth_zone_rigid_drift_z0.75_s2 | not repairable | - |
| growth_zone_rigid_drift_z1_s0 | not repairable | - |
| growth_zone_rigid_drift_z1_s1 | not repairable | - |
| growth_zone_rigid_drift_z1_s2 | not repairable | - |
| growth_zone_displacement_exceeds_patch_z2x6_s0 | repairable | change_frame_stride/half + change_frame_stride/half |
| growth_zone_displacement_exceeds_patch_z2x6_s1 | repairable | change_frame_stride/half + change_frame_stride/half |
| growth_zone_displacement_exceeds_patch_z2x6_s2 | repairable | change_frame_stride/half + change_frame_stride/half |
| growth_zone_displacement_exceeds_patch_z3x4_s0 | not repairable | - |
| growth_zone_displacement_exceeds_patch_z3x4_s1 | not repairable | - |
| growth_zone_displacement_exceeds_patch_z3x4_s2 | not repairable | - |
| growth_zone_displacement_exceeds_patch_z4x3_s0 | not repairable | - |
| growth_zone_displacement_exceeds_patch_z4x3_s1 | not repairable | - |
| growth_zone_displacement_exceeds_patch_z4x3_s2 | not repairable | - |
| growth_zone_midline_jitter_z0.5_s0 | not repairable | - |
| growth_zone_midline_jitter_z0.5_s1 | repairable | smooth_midline/light |
| growth_zone_midline_jitter_z0.5_s2 | not repairable | - |
| growth_zone_midline_jitter_z1_s0 | not repairable | - |
| growth_zone_midline_jitter_z1_s1 | not repairable | - |
| growth_zone_midline_jitter_z1_s2 | not repairable | - |
| growth_zone_midline_jitter_z2_s0 | not repairable | - |
| growth_zone_midline_jitter_z2_s1 | not repairable | - |
| growth_zone_midline_jitter_z2_s2 | not repairable | - |
| growth_zone_midline_jitter_z3_s0 | not repairable | - |
| growth_zone_midline_jitter_z3_s1 | not repairable | - |
| growth_zone_midline_jitter_z3_s2 | not repairable | - |
| growth_zone_low_texture_z0.06_s0 | not repairable | - |
| growth_zone_low_texture_z0.06_s1 | not repairable | - |
| growth_zone_low_texture_z0.06_s2 | not repairable | - |
| growth_zone_low_texture_z0.1_s0 | not repairable | - |
| growth_zone_low_texture_z0.1_s1 | not repairable | - |
| growth_zone_low_texture_z0.1_s2 | not repairable | - |
| growth_zone_low_texture_z0.15_s0 | not repairable | - |
| growth_zone_low_texture_z0.15_s1 | not repairable | - |
| growth_zone_low_texture_z0.15_s2 | not repairable | - |
| growth_zone_low_texture_z0.03_s0 | not repairable | - |
| growth_zone_low_texture_z0.03_s1 | not repairable | - |
| growth_zone_low_texture_z0.03_s2 | not repairable | - |
| growth_zone_width_change_s0 | repairable | use_width_free_ratio |
| growth_zone_width_change_s1 | repairable | use_width_free_ratio |
| growth_zone_width_change_s2 | repairable | use_width_free_ratio |
