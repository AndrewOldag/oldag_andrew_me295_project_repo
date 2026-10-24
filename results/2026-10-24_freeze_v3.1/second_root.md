# second_root in freeze v3: cause of 0 correct

Label: decline (v2 rule kept, Andrew 2026-10-13; `use_width_free_ratio` is not in its label states).

## Cause, from the v3 label sweep and traces
- Unremedied, every seed fails plane_sections only (4.79, 9.89, 9.07 %/h; threshold 3.25); rigid_invariance and closure pass. Centre RMS is within tolerance (1.09, 0.43, 0.60 against 1.35 %/h); flank-difference RMS is not (1.19, 2.05, 2.20 against 1.00 %/h)
- Both crop_or_mask states give the same checker values and errors as the unremedied run on every seed: at size 30 the mask does not change the tracked flanks
- `use_width_free_ratio` skips plane_sections and drops the flank error from the goodness test, so after it every check that is applied passes and the centre measurement is good. Methods then accept
- Scoring: an accept with a good measurement on a decline rod is accept_on_decline (not correct, not a false accept). The script accepts the unremedied run (flank not good): false accept

## Runs ending with a good field after `use_width_free_ratio` (alternative repair)

| Method | Runs | Alternative repair | Tried crop_or_mask | Accept, not good | Not reported |
| :-- | --: | --: | --: | --: | --: |
| script | 3 | 0 | 0 | 3 | 0 |
| remedy_tree | 3 | 3 | 0 | 0 | 0 |
| diagnostician | 9 | 9 | 6 | 0 | 0 |
| single_agent | 9 | 6 | 7 | 0 | 3 |

Label sweep rows (v3 `labels.md`):

| v3_growth_zone_second_root_z30_s20 | none | 0.85 | 0.17 | 4.79 F | 1.09 (1.35) | 1.19 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s20 | crop_or_mask/crop_to_main_root | 0.85 | 0.17 | 4.79 F | 1.09 (1.35) | 1.19 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s20 | crop_or_mask/mask_second_root | 0.85 | 0.17 | 4.79 F | 1.09 (1.35) | 1.19 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s21 | none | 0.76 | 0.16 | 9.89 F | 0.43 (1.35) | 2.05 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s21 | crop_or_mask/crop_to_main_root | 0.76 | 0.16 | 9.89 F | 0.43 (1.35) | 2.05 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s21 | crop_or_mask/mask_second_root | 0.76 | 0.16 | 9.89 F | 0.43 (1.35) | 2.05 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s22 | none | 0.71 | 0.02 | 9.07 F | 0.60 (1.35) | 2.20 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s22 | crop_or_mask/crop_to_main_root | 0.71 | 0.02 | 9.07 F | 0.60 (1.35) | 2.20 (1.00) | no | no |
| v3_growth_zone_second_root_z30_s22 | crop_or_mask/mask_second_root | 0.71 | 0.02 | 9.07 F | 0.60 (1.35) | 2.20 (1.00) | no | no |
