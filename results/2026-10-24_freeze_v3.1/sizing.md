# Freeze v3.1 sizing: accept_repaired rods that need their repair

Sizing seeds 10, 11, 12. Rule, each part on 3 of 3 seeds: (1) a listed check fails unremedied; (2) the unremedied measurement fails the scoring tolerance; (3) a remedy state of the v3 label sweep passes every check and is good. Smallest size meeting the rule; at most 6 sizes per fault. States already in the v3 cache are reused.

| Fault | Size | Unremedied run | (1) check fails | (2) not good | (3) remedy repairs | Qualifies |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| rigid_drift | 0.5 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 1.5 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| rigid_drift | 2.5 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| rigid_drift | 3.5 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| rigid_drift | 4.5 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| rigid_drift | 5.5 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| width_change | v3 (one size) | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| bad_stage_correction | 3 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| bad_stage_correction | 4 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| bad_stage_correction | 5 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| bad_stage_correction | 6 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| bad_stage_correction | 7 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| bad_stage_correction | 8 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| stage_log_missing | 1 | 3 of 3 | 3 of 3 | 0 of 3 | 0 of 3 | no |
| displacement_exceeds_patch | 2x2 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| displacement_exceeds_patch | 2x3 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |
| displacement_exceeds_patch | 2x4 | 0 of 3 | 0 of 3 | 0 of 3 | 0 of 3 | not yet |

- Tracker states still needed: 51
- Sizes so far: {'rigid_drift': None, 'width_change': None, 'bad_stage_correction': None, 'stage_log_missing': None, 'displacement_exceeds_patch': None}

- Result: incomplete

## Per state

| Rod | State | rigid_invariance | closure | plane_sections | REGR err (limit) | Flank err (limit) | All pass | Good |
| :-- | :-- | --: | --: | --: | --: | --: | :-- | :-- |
| v3_growth_zone_rigid_drift_z0.5_s10 | none | 0.91 | 8.04 F | 0.67 | 0.34 (1.35) | 0.24 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s11 | none | 0.72 | 8.17 F | 0.51 | 0.36 (1.35) | 0.19 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z0.5_s12 | none | 0.77 | 8.08 F | 1.32 | 0.40 (1.35) | 0.30 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z1.5_s10 | none | 1.00 | 24.24 F | 0.69 | 0.32 (1.35) | 0.24 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z1.5_s11 | none | 0.80 | 24.37 F | 0.71 | 0.34 (1.35) | 0.18 (1.00) | no | yes |
| v3_growth_zone_rigid_drift_z1.5_s12 | none | 0.74 | 24.31 F | 0.91 | 0.37 (1.35) | 0.26 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s10 | none | 0.92 | 2.92 F | 0.41 | 0.34 (1.35) | 0.17 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s11 | none | 0.88 | 2.81 F | 0.39 | 0.32 (1.35) | 0.16 (1.00) | no | yes |
| v3_growth_zone_bad_stage_correction_z3_s12 | none | 0.65 | 2.87 F | 0.88 | 0.35 (1.35) | 0.20 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s10 | none | 0.92 | 95.92 F | 0.41 | 0.34 (1.35) | 0.17 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s11 | none | 0.87 | 95.81 F | 0.38 | 0.32 (1.35) | 0.16 (1.00) | no | yes |
| v3_growth_zone_stage_log_missing_z1_s12 | none | 0.64 | 95.87 F | 0.88 | 0.35 (1.35) | 0.20 (1.00) | no | yes |
