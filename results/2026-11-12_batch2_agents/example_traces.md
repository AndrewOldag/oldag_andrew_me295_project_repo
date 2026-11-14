# Example traces (c026)

Remedy tree on two batch-2 windows that fail closure. For each step: the action sent (name, arguments, rationale), the tool result, and the final outcome. REGR, growth-zone and flank values are `[masked]`.

## Remedy kept: 0711_c5__w6-8 (initial closure 22.8 px/h, threshold 19)

### Step 1: apply_remedy

- Arguments: `{"fault": "rigid_drift", "remedy": "register_frames", "setting": null}`
- Rationale: rule 1: failing closure
- Result: `{"rechecked": true, "change": "frames registered on the non-growing tissue (from 1075 px from the tip) before tracking", "failed_checks": [], "passed_checks": ["closure"], "not_run": ["rigid_invariance"], "reported_not_gating": ["plane_sections"], "check_values": {"rigid_invariance": {"before": null, "after": null, "threshold": null, "unit": "%/h"}, "closure": {"before": 22.829, "after": 14.032, "threshold": 19.0, "unit": "px/h"}, "plane_sections": "[masked]"}, "settings_left": "no further setting: register_frames cannot be applied again or at another setting"}`

### Step 2: accept

- Arguments: `{"confidence": null}`
- Rationale: rule 0: no check fails

Outcome: accept; final closure 14.0 px/h

## Declined: 0708_c4__w0-2 (initial closure 103.5 px/h, threshold 19)

### Step 1: apply_remedy

- Arguments: `{"fault": "rigid_drift", "remedy": "register_frames", "setting": null}`
- Rationale: rule 1: failing closure
- Result: `{"rechecked": true, "change": "frames registered on the non-growing tissue (from 470 px from the tip) before tracking", "failed_checks": ["closure"], "passed_checks": [], "not_run": ["rigid_invariance"], "reported_not_gating": ["plane_sections"], "check_values": {"rigid_invariance": {"before": null, "after": null, "threshold": null, "unit": "%/h"}, "closure": {"before": 103.549, "after": 77.885, "threshold": 19.0, "unit": "px/h"}, "plane_sections": "[masked]"}, "rolled_back": true, "note": "the remedy made no failing check pass and lowered none by a quarter; the settings and measurement from before it are restored. The step counts"}`

### Step 2: apply_remedy

- Arguments: `{"fault": "low_texture", "remedy": "enlarge_patch", "setting": "1.5x"}`
- Rationale: rule 1: failing closure
- Result: `{"rechecked": true, "change": "tracker disk radius 11 -> 16 px", "failed_checks": ["closure"], "passed_checks": [], "not_run": ["rigid_invariance"], "reported_not_gating": ["plane_sections"], "check_values": {"rigid_invariance": {"before": null, "after": null, "threshold": null, "unit": "%/h"}, "closure": {"before": 103.549, "after": 102.349, "threshold": 19.0, "unit": "px/h"}, "plane_sections": "[masked]"}, "rolled_back": true, "note": "the remedy made no failing check pass and lowered none by a quarter; the settings and measurement from before it are restored. The step counts"}`

### Step 3: apply_remedy

- Arguments: `{"fault": "low_texture", "remedy": "enlarge_patch", "setting": "2x"}`
- Rationale: rule 1: failing closure
- Result: `{"rechecked": true, "change": "tracker disk radius 11 -> 22 px", "failed_checks": ["closure"], "passed_checks": [], "not_run": ["rigid_invariance"], "reported_not_gating": ["plane_sections"], "check_values": {"rigid_invariance": {"before": null, "after": null, "threshold": null, "unit": "%/h"}, "closure": {"before": 103.549, "after": 103.071, "threshold": 19.0, "unit": "px/h"}, "plane_sections": "[masked]"}, "rolled_back": true, "note": "the remedy made no failing check pass and lowered none by a quarter; the settings and measurement from before it are restored. The step counts"}`

### Step 4: apply_remedy

- Arguments: `{"fault": "midline_jitter", "remedy": "smooth_midline", "setting": "light"}`
- Rationale: rule 1: failing closure
- Result: `{"rechecked": true, "change": "midline source smoothed (light)", "failed_checks": ["closure"], "passed_checks": [], "not_run": ["rigid_invariance"], "reported_not_gating": ["plane_sections"], "check_values": {"rigid_invariance": {"before": null, "after": null, "threshold": null, "unit": "%/h"}, "closure": {"before": 103.549, "after": 57.695, "threshold": 19.0, "unit": "px/h"}, "plane_sections": "[masked]"}, "settings_left": "no further setting: smooth_midline cannot be applied again or at another setting"}`

### Step 5: decline

- Arguments: `{"fault": "midline_jitter", "reason": "rule 3: no remedy left for closure"}`
- Rationale: rule 3: failing closure; list exhausted

Outcome: decline, fault midline_jitter; final closure 57.7 px/h

