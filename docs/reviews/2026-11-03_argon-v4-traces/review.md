# Task A3: Synthetic Trace Audit of Freeze v4

Audit of all $306$ scored agent runs in `results/2026-10-25_freeze_v4/runs/` ($153$ `diagnostician` runs and $153$ `single_agent` runs across $17$ rod rows, $3$ seeds $26, 27, 28$, and $3$ repeats $0, 1, 2$ in `results/2026-10-25_freeze_v4/scores.json`) against `agents/prompts/diagnostician_v4.md`, `agents/prompts/single_agent_v4.md`, `agents/actions.py`, `agents/executors.py`, and `config/checker_thresholds.yaml`.

---

## 1. Summary of Trace Classifications

Each of the $153$ runs per method is classified by whether its `apply_remedy`, `accept`, and `decline` decisions match the evidence seen up to that step under the prompt rules (`agents/prompts/diagnostician_v4.md`, `agents/prompts/single_agent_v4.md`) and checker thresholds (`config/checker_thresholds.yaml:13-31`).

### 1.1 Per-Method and Per-Class Summary (`results/2026-10-25_freeze_v4/scores.json`)

| Method | Class | Total Runs | Justified | Defensible | Not Justified |
|---|---|---:|---:|---:|---:|
| `diagnostician` | `accept_clean` | $54$ | $47$ | $5$ | $2$ |
| `diagnostician` | `accept_repaired` | $27$ | $20$ | $4$ | $3$ |
| `diagnostician` | `decline` | $72$ | $29$ | $28$ | $15$ |
| **`diagnostician` total** | **All classes** | **$153$** | **$96$** | **$37$** | **$20$** |
| `single_agent` | `accept_clean` | $54$ | $31$ | $0$ | $23$ |
| `single_agent` | `accept_repaired` | $27$ | $9$ | $0$ | $18$ |
| `single_agent` | `decline` | $72$ | $0$ | $57$ | $15$ |
| **`single_agent` total** | **All classes** | **$153$** | **$40$** | **$57$** | **$56$** |

### 1.2 Per-Row Breakdown: `diagnostician` (`results/2026-10-25_freeze_v4/runs/diagnostician_*.jsonl`)

| Class | Row (`kind`) | Runs | Justified | Defensible | Not Justified | Outcome Categories (`scores.json`) |
|---|---|---:|---:|---:|---:|---|
| `accept_clean` | `v3_still` | $9$ | $6$ | $3$ | $0$ | $9$ `good_report` |
| `accept_clean` | `v3_growth_zone` | $9$ | $9$ | $0$ | $0$ | $9$ `good_report` |
| `accept_clean` | `v3_bend16` | $9$ | $9$ | $0$ | $0$ | $9$ `good_report` |
| `accept_clean` | `v3_bend20` | $9$ | $8$ | $0$ | $1$ | $9$ `good_report` ($1$ with remedy kept) |
| `accept_clean` | `v3_bend24` | $9$ | $8$ | $1$ | $0$ | $9$ `good_report` |
| `accept_clean` | `v3_bend30` | $9$ | $7$ | $1$ | $1$ | $9$ `good_report` ($1$ with remedy kept) |
| `accept_repaired` | `width_change` | $9$ | $9$ | $0$ | $0$ | $9$ `good_report` |
| `accept_repaired` | `bad_stage_correction` | $9$ | $8$ | $0$ | $1$ | $9$ `good_report` ($1$ with $2$ remedies kept) |
| `accept_repaired` | `rigid_drift` | $9$ | $3$ | $4$ | $2$ | $9$ `good_report` ($2$ with $2$ remedies kept) |
| `decline` | `stage_log_missing` | $9$ | $9$ | $0$ | $0$ | $9$ `correct_decline` |
| `decline` | `low_texture` | $9$ | $9$ | $0$ | $0$ | $9$ `correct_decline` |
| `decline` | `flank_swap` | $9$ | $0$ | $9$ | $0$ | $9$ `correct_decline` |
| `decline` | `second_root` | $9$ | $0$ | $0$ | $9$ | $8$ `accept_on_decline`, $1$ `correct_decline` |
| `decline` | `partial_occlusion` | $9$ | $3$ | $6$ | $0$ | $9$ `correct_decline` |
| `decline` | `displacement_exceeds_patch` | $9$ | $3$ | $2$ | $4$ | $7$ `correct_decline`, $2$ `not_reported` |
| `decline` | `midline_jitter` | $9$ | $5$ | $3$ | $1$ | $7$ `correct_decline`, $2$ `not_reported` |
| `decline` | `fast_rotation` | $9$ | $0$ | $8$ | $1$ | $6$ `correct_decline`, $3$ `not_reported` |

### 1.3 Per-Row Breakdown: `single_agent` (`results/2026-10-25_freeze_v4/runs/single_agent_*.jsonl`)

| Class | Row (`kind`) | Runs | Justified | Defensible | Not Justified | Outcome Categories (`scores.json`) |
|---|---|---:|---:|---:|---:|---|
| `accept_clean` | `v3_still` | $9$ | $9$ | $0$ | $0$ | $9$ `good_report` |
| `accept_clean` | `v3_growth_zone` | $9$ | $0$ | $0$ | $9$ | $9$ `good_report` (all $9$ with remedy kept) |
| `accept_clean` | `v3_bend16` | $9$ | $6$ | $0$ | $3$ | $6$ `good_report`, $2$ `unnecessary_decline`, $1$ `not_reported` |
| `accept_clean` | `v3_bend20` | $9$ | $6$ | $0$ | $3$ | $7$ `good_report` ($1$ with remedy kept), $2$ `unnecessary_decline` |
| `accept_clean` | `v3_bend24` | $9$ | $6$ | $0$ | $3$ | $8$ `good_report` ($2$ with remedy kept), $1$ `unnecessary_decline` |
| `accept_clean` | `v3_bend30` | $9$ | $4$ | $0$ | $5$ | $6$ `good_report` ($2$ with remedy kept), $1$ `unnecessary_decline`, $2$ `not_reported` |
| `accept_repaired` | `width_change` | $9$ | $9$ | $0$ | $0$ | $9$ `good_report` |
| `accept_repaired` | `bad_stage_correction` | $9$ | $0$ | $0$ | $9$ | $8$ `good_report` ($7$ unrepaired `closure`, $1$ with $2$ remedies), $1$ `not_reported` |
| `accept_repaired` | `rigid_drift` | $9$ | $0$ | $0$ | $9$ | $9$ `good_report` (all $9$ with $2$ remedies kept) |
| `decline` | `stage_log_missing` | $9$ | $0$ | $4$ | $5$ | $8$ `not_reported`, $1$ `accept_on_decline` |
| `decline` | `low_texture` | $9$ | $0$ | $9$ | $0$ | $9$ `not_reported` |
| `decline` | `flank_swap` | $9$ | $0$ | $8$ | $1$ | $6$ `not_reported`, $2$ `correct_decline`, $1$ `false_accept` |
| `decline` | `second_root` | $9$ | $0$ | $0$ | $9$ | $8$ `not_reported`, $1$ `accept_on_decline` |
| `decline` | `partial_occlusion` | $9$ | $0$ | $9$ | $0$ | $6$ `not_reported`, $3$ `correct_decline` |
| `decline` | `displacement_exceeds_patch` | $9$ | $0$ | $9$ | $0$ | $9$ `not_reported` |
| `decline` | `midline_jitter` | $9$ | $0$ | $9$ | $0$ | $9$ `not_reported` |
| `decline` | `fast_rotation` | $9$ | $0$ | $9$ | $0$ | $7$ `not_reported`, $2$ `correct_decline` |

---

## 2. Analysis of the $66$ `single_agent` Runs Hitting `step_limit`

### 2.1 Breakdown of the $528$ Steps Across the $66$ `step_limit` Runs

In `results/2026-10-25_freeze_v4/scores.json`, $66 / 153$ `single_agent` runs terminate with `status = "step_limit"` (`category = "not_reported"`): $3 / 54$ in `accept_clean` (`v3_bend16_clean_s26_r0`, `v3_bend30_clean_s27_r2`, `v3_bend30_clean_s28_r2`), $1 / 27$ in `accept_repaired` (`v3_growth_zone_bad_stage_correction_z3_s27_r2`), and $62 / 72$ in `decline` ($9$ `displacement_exceeds_patch`, $9$ `low_texture`, $9$ `midline_jitter`, $8$ `second_root`, $8$ `stage_log_missing`, $7$ `fast_rotation`, $6$ `flank_swap`, $6$ `partial_occlusion`).

Across all $66$ `step_limit` runs ($66 \times 8 = 528$ executed steps in `results/2026-10-25_freeze_v4/runs/single_agent_*.jsonl`):

| Step Category | Steps | Share of $528$ | Source / Mechanism |
|---|---:|---:|---|
| Step 1 `request_info(kind="check_report")` (unavailable error) | $66$ | $12.5\%$ | `ACTION_SETS["single_agent"]` (`agents/actions.py:165`) reuses `DIAGNOSTICIAN`, which lists `check_report` first (`agents/actions.py:55`), while `BlindSlice.request_info` (`agents/executors.py:219-220`) returns `{"error": "check_report is not available for this task"}`. All $153 / 153$ `single_agent` runs spend Step 1 on `check_report`. |
| Initial `request_info` calls (before first remedy) | $224$ | $42.4\%$ | Mean $3.39$ initial info calls per run ($6$ runs request $2$ of the $5$ valid info kinds across the run, $17$ request $3$, $23$ request $4$, and $20$ request all $5$). |
| `apply_remedy` calls (executed) | $102$ | $19.3\%$ | $30$ runs apply $1$ remedy, $35$ runs apply $2$ remedies, and $1$ run (`single_agent_v3_growth_zone_displacement_exceeds_patch_z2x6_s28_r2`) issues $3$ `apply_remedy` calls ($19$ `bad_stage_correction:register_frames`, $19$ `width_change:use_width_free_ratio`, $14$ `rigid_drift:register_frames`, $14$ `midline_jitter:smooth_midline/light`, $11$ `displacement_exceeds_patch:change_frame_stride/half`, $9$ `low_texture:enlarge_patch/1.5x`, $9$ `low_texture:enlarge_patch/2x`, $8$ `second_root:crop_or_mask/mask_second_root`). |
| `apply_remedy` call (executor `RuntimeError`) | $1$ | $0.2\%$ | In `single_agent_v3_growth_zone_displacement_exceeds_patch_z2x6_s28_r2.jsonl` step 7, `apply_remedy(fault="bad_stage_correction", remedy="register_frames")` fails inside `Orchestrator.run` (`agents/orchestrator.py:129-133`), which logs `status="executed"` and consumes Step 7, forcing a retry at Step 8. |
| Post-remedy `request_info` calls (after `apply_remedy`) | $135$ | $25.6\%$ | `BlindSlice.apply_remedy` (`agents/executors.py:224-239`) returns only `{"rerun": True, "change": ...}` with no numbers and no rollback. The agent must spend $1\text{–}2$ steps after each remedy re-requesting `velocity_profile`, `stage_log_summary`, `displacement_vs_patch_radius`, or `midline_jitter` to observe whether the remedy worked. |
| Repeated `request_info` calls without an intervening remedy | $0$ | $0.0\%$ | `single_agent` never repeats the same `request_info` kind unless a remedy has been applied in between. |
| Invalid-schema or failed model calls (`failed_steps`) | $0$ | $0.0\%$ | `outcome.failed_steps = 0` across all $66$ `step_limit` runs (`results/2026-10-25_freeze_v4/runs/single_agent_*_summary.json`). |

By info kind across the $425$ `request_info` steps in the $66$ `step_limit` runs: `velocity_profile` ($113$), `displacement_vs_patch_radius` ($74$), `stage_log_summary` ($72$), `check_report` ($66$), `frame_quality` ($53$), `midline_jitter` ($47$).

### 2.2 Is the 8-Step Limit the Cause of the Low `decline` Accuracy ($7 / 72 = 0.097$), or Would More Steps Not Have Helped?

Both mechanisms operate simultaneously across different fault rows:

1. **Where the 8-step limit directly blocks valid `decline` trajectories ($37 / 62$ `decline` `step_limit` runs)**:
   - Because Step 1 is always lost to `request_info(kind="check_report")` (`agents/actions.py:55,165`) and `BlindSlice.apply_remedy` (`agents/executors.py:224-239`) returns no re-checked numbers, every remedy requires $1$ step to apply plus $1\text{–}2$ steps of post-remedy `request_info` calls to evaluate.
   - On two-setting remedies (`low_texture` with `enlarge_patch` `1.5x` $\to$ `2x` across $9 / 9$ runs, and `displacement_exceeds_patch` with `change_frame_stride` `6` $\to$ `3` $\to$ `1` in `s26_r0` and `s27_r1`), obeying the prompt rules in `agents/prompts/single_agent_v4.md` (*"After a stride or patch remedy, request `displacement_vs_patch_radius` again before choosing the next action"* and *"If a remedy improved the measurement and can be applied again or has a next setting, apply it again or at the next setting before testing another fault or declining"*) requires a minimum of $10$ steps ($1$ `check_report` + $2$ initial info + $1$ first setting + $2$ post-remedy info + $1$ second setting + $2$ post-remedy info + $1$ `decline`). All $9 / 9$ `low_texture` runs and $9 / 9$ `displacement_exceeds_patch` runs are cut off at Step 8 in the middle of this sequence.
   - On `fast_rotation` ($7$ `step_limit`), `flank_swap` ($6$ `step_limit`), and `partial_occlusion` ($6$ `step_limit`), the agent spends Steps 2–6 gathering $4\text{–}5$ info kinds to rule out listed faults, applies a remedy at Step 5–7, and spends Step 8 re-requesting `velocity_profile` or `stage_log_summary`. In the $7$ runs across these same three rows where `single_agent` requested one fewer initial info item, it saw the unfixed post-remedy `velocity_profile` / `stage_log_summary` by Step 7 and called `decline` at Step 7 or 8 ($7 / 7$ `correct_decline`).

2. **Where more steps would NOT have improved `decline` accuracy, and would instead have produced `accept_on_decline` ($19\text{–}20 / 62$ `decline` `step_limit` runs)**:
   - **`stage_log_missing` ($8$ `step_limit` runs, $1$ `accept_on_decline` run)**: On `stage_log_missing` (`stage_moves = 0`), `diagnostician` declines $9 / 9$ runs because `register_frames` sets `closure` to `not_run` (`after: None`), which `no_progress` in `ExecSlice.apply_remedy` (`agents/executors.py:92`) treats as non-progress and rolls back (`rolled_back: True`). In `single_agent`, `BlindSlice.apply_remedy` (`agents/executors.py:224-239`) never calls `no_progress` and never rolls back `register_frames`. After `register_frames` registers the frames on non-growing tissue, the post-remedy `velocity_profile` shows tip motion matching basal velocity and `stage_log_summary` returns `null` closure residuals. In all $8$ `step_limit` runs on `stage_log_missing` (`sa_sl62` step 8 rationales in `single_agent_v3_growth_zone_stage_log_missing_z1_*.jsonl`), `single_agent` concludes at Step 7–8 that `register_frames` fixed the drift, applies `use_width_free_ratio` ($4$ runs: `s26_r0`, `s26_r1`, `s27_r0`, `s28_r0`) or inspects `velocity_profile` / `frame_quality` ($4$ runs: `s26_r2`, `s27_r2`, `s28_r1`, `s28_r2`), and is on the exact trajectory of `single_agent_v3_growth_zone_stage_log_missing_z1_s27_r1` (which finished at Step 8 with `accept` / `accept_on_decline`).
   - **`second_root` ($8$ `step_limit` runs, $1$ `accept_on_decline` run)**: In all $9$ runs of `second_root`, `single_agent` applies `crop_or_mask(setting="mask_second_root")`, re-requests `velocity_profile`, and sees no change. Without `no_progress` rollback feedback, in $7$ of the $8$ `step_limit` runs (`s26_r0`, `s26_r1`, `s26_r2`, `s27_r0`, `s27_r2`, `s28_r0`, `s28_r2`) it abandons `second_root` without trying `crop_to_main_root`, reinterprets the anomaly as `width_change`, applies `use_width_free_ratio` at Step 7 or 8, and is on track to `accept` (`accept_on_decline`), exactly as `single_agent_v3_growth_zone_second_root_z30_s28_r1` did at Step 8 (only `s27_r1` re-checked `velocity_profile` after `use_width_free_ratio` and noticed the remaining anomaly).
   - **`midline_jitter` ($9$ `step_limit` runs)**: Applying `smooth_midline(setting="light")` lowers `tip_second_difference_rms_px` from $22.53\text{–}23.02\text{ px}$ to $3.80\text{–}4.79\text{ px}$ while `closure` ($25.74\text{–}33.62\text{ px/h} > 1.0\text{ px/h}$) and `plane_sections` (above the $3.25$ threshold in `config/checker_thresholds.yaml:30`) still fail the hidden checker. Without the checker thresholds, in $4$ of the $9$ runs (`s26_r0`, `s26_r1`, `s28_r0`, `s28_r1`) the Step 8 rationale explicitly states that the agent is requesting one final diagnostic *"before accepting"*, while the other $5$ runs (`s26_r2`, `s27_r0`, `s27_r1`, `s27_r2`, `s28_r2`) are checking `stage_log_summary` or `midline_jitter` to evaluate the remaining $2.19\text{–}3.45\text{ px/pair}$ closure residual.

---

## 3. Findings on `not justified` Decisions

### Finding A3-F1
- **ID**: `A3-F1`
- **Severity**: High
- **Trace and step**:
  - `diagnostician` ($8$ `accept_on_decline` runs and $1$ `correct_decline` run with unjustified steps on `second_root` in `results/2026-10-25_freeze_v4/runs/`):
    - `diagnostician_v3_growth_zone_second_root_z30_s26_r0.jsonl` (steps 5–7)
    - `diagnostician_v3_growth_zone_second_root_z30_s26_r1.jsonl` (steps 5–6)
    - `diagnostician_v3_growth_zone_second_root_z30_s26_r2.jsonl` (steps 4, 6–7)
    - `diagnostician_v3_growth_zone_second_root_z30_s27_r0.jsonl` (steps 5–7)
    - `diagnostician_v3_growth_zone_second_root_z30_s27_r1.jsonl` (steps 5–7)
    - `diagnostician_v3_growth_zone_second_root_z30_s27_r2.jsonl` (steps 5–6)
    - `diagnostician_v3_growth_zone_second_root_z30_s28_r0.jsonl` (steps 5–7)
    - `diagnostician_v3_growth_zone_second_root_z30_s28_r1.jsonl` (steps 5–7)
    - `diagnostician_v3_growth_zone_second_root_z30_s28_r2.jsonl` (steps 5–7)
  - `single_agent` ($1$ `accept_on_decline` run and $7$ `step_limit` runs on `second_root` in `results/2026-10-25_freeze_v4/runs/`):
    - `single_agent_v3_growth_zone_second_root_z30_s28_r1.jsonl` (steps 6, 8)
    - `single_agent_v3_growth_zone_second_root_z30_s26_r0.jsonl` (step 8)
    - `single_agent_v3_growth_zone_second_root_z30_s26_r1.jsonl` (step 7)
    - `single_agent_v3_growth_zone_second_root_z30_s26_r2.jsonl` (step 8)
    - `single_agent_v3_growth_zone_second_root_z30_s27_r0.jsonl` (step 8)
    - `single_agent_v3_growth_zone_second_root_z30_s27_r2.jsonl` (step 8)
    - `single_agent_v3_growth_zone_second_root_z30_s28_r0.jsonl` (step 8)
    - `single_agent_v3_growth_zone_second_root_z30_s28_r2.jsonl` (step 8)
- **Claim**: On `second_root`, both `diagnostician` ($9 / 9$ runs) and `single_agent` ($8 / 9$ runs) fail to try the second setting `crop_to_main_root` of `crop_or_mask` (`agents/prompts/diagnostician_v4.md:45`, `agents/prompts/single_agent_v4.md:44`) and instead apply `use_width_free_ratio` (`fault="width_change"`), which merely skips the failing `plane_sections` check (`not_run: ["plane_sections"]`, `failed_checks: []`) and leads to $8 / 9$ `accept_on_decline` outcomes in `diagnostician` and $1 / 9$ `accept_on_decline` (plus $7$ truncated acceptance trajectories) in `single_agent`.
- **Evidence**:
  - In all $9$ `second_root` rods, `frame_quality` reports `bright_objects_over_500px: 2` in frames $0$ and $20$ and `1` in frame $40$, and only `plane_sections` fails initially (`passed: false` against the $3.25$ threshold in `config/checker_thresholds.yaml:30`).
  - In $6$ `diagnostician` runs (`s26_r0`, `s26_r2`, `s27_r1`, `s28_r0`, `s28_r1`, `s28_r2`), the agent applies `crop_or_mask(setting="mask_second_root")`, which leaves `plane_sections` unchanged and is rolled back (`rolled_back: True`). Instead of trying `crop_to_main_root` or declining on `second_root`, the agent switches to `apply_remedy(fault="width_change", remedy="use_width_free_ratio")` at Step 6, sees `failed_checks: []` (`not_run: ["plane_sections"]`), and calls `accept` at Step 7.
  - In $3$ `diagnostician` runs (`s26_r1`, `s27_r0`, `s27_r2`), the agent applies `use_width_free_ratio` first at Step 5 despite seeing `bright_objects_over_500px: 2` at Step 2. Run `s27_r2` accepts immediately at Step 6; runs `s27_r0` and `s26_r1` then call `apply_remedy(fault="second_root", remedy="crop_or_mask", setting="mask_second_root")` at Step 6 while `failed_checks` is already `[]` (`plane_sections` is `not_run`, so `no_progress` in `agents/executors.py:100-102` does not roll back `mask_second_root`), after which `s27_r0` accepts at Step 7 and `s26_r1` declines at Step 8.
- **What would confirm it**: Inspecting `diagnostician_v3_growth_zone_second_root_z30_*_summary.json` and `single_agent_v3_growth_zone_second_root_z30_*_summary.json` in `results/2026-10-25_freeze_v4/runs/`, where `crop_to_main_root` is applied $0$ times across all $18$ runs and `use_width_free_ratio` is kept in $9 / 9$ `diagnostician` runs and $8 / 9$ `single_agent` runs.

---

### Finding A3-F2
- **ID**: `A3-F2`
- **Severity**: High
- **Trace and step**:
  - `diagnostician` ($2$ `accept_clean` runs and $3$ `accept_repaired` runs in `results/2026-10-25_freeze_v4/runs/`):
    - `diagnostician_v3_bend20_clean_s28_r0.jsonl` (step 4: `apply_remedy` `bad_stage_correction` / `register_frames`)
    - `diagnostician_v3_bend30_clean_s28_r0.jsonl` (step 3: `apply_remedy` `bad_stage_correction` / `register_frames`)
    - `diagnostician_v3_growth_zone_bad_stage_correction_z3_s26_r1.jsonl` (step 4: `apply_remedy` `width_change` / `use_width_free_ratio`)
    - `diagnostician_v3_growth_zone_rigid_drift_z0.5_s26_r2.jsonl` (step 5: `apply_remedy` `width_change` / `use_width_free_ratio`)
    - `diagnostician_v3_growth_zone_rigid_drift_z0.5_s28_r1.jsonl` (step 4: `apply_remedy` `width_change` / `use_width_free_ratio`)
- **Claim**: In $5$ `diagnostician` runs ($2$ on `accept_clean` and $3$ on `accept_repaired`), the agent calls `apply_remedy` when all three kinematic checks already pass (`failed_checks == []`), and `no_progress` in `agents/executors.py:86-103` fails to roll back any remedy applied when `failed_before` is empty.
- **Evidence**:
  - In `diagnostician_v3_bend20_clean_s28_r0` and `diagnostician_v3_bend30_clean_s28_r0`, all three checks pass in `initial_checks` (`rigid_invariance` $\le 2.0$, `closure` $0.154$ and $0.149 \le 1.0$, `plane_sections` $\le 3.25$ in `config/checker_thresholds.yaml:13-31`, so `failed_checks: []`). The agent requests `velocity_profile` and `stage_log_summary`, misinterprets the difference between tip displacement (which includes bending rotation) and basal velocity as a stage-correction error, and applies `register_frames` at Step 4 and Step 3, respectively.
  - In `diagnostician_v3_growth_zone_bad_stage_correction_z3_s26_r1` (after `register_frames` at Step 2 reduces `closure` from $19.655$ to $0.056 \le 1.0$ with `failed_checks: []`), `diagnostician_v3_growth_zone_rigid_drift_z0.5_s26_r2` (after `register_frames` at Step 3 reduces `closure` from $8.234$ to $0.193 \le 1.0$ with `failed_checks: []`), and `diagnostician_v3_growth_zone_rigid_drift_z0.5_s28_r1` (after `register_frames` at Step 2 reduces `closure` from $8.299$ to $0.132 \le 1.0$ with `failed_checks: []`), all three checks pass after `register_frames`. The agent then requests `velocity_profile` and applies a second remedy `use_width_free_ratio` (`fault="width_change"`) when `failed_checks == []`.
  - In `agents/executors.py:90-91`, `no_progress(before, after)` begins with `if not failed_before: return False`, so any remedy applied when `failed_checks == []` is never rolled back and is counted in `remedies_kept`.
- **What would confirm it**: Inspecting `agents/executors.py:90-91` and the `check_values` dictionary at the cited steps in the $5$ trace files, where `failed_checks` before the remedy is `[]`.

---

### Finding A3-F3
- **ID**: `A3-F3`
- **Severity**: High
- **Trace and step**:
  - `single_agent` on `bad_stage_correction` ($7$ `accept` runs in `results/2026-10-25_freeze_v4/runs/`):
    - `single_agent_v3_growth_zone_bad_stage_correction_z3_s26_r0.jsonl` (steps 4–5)
    - `single_agent_v3_growth_zone_bad_stage_correction_z3_s26_r1.jsonl` (steps 4–5)
    - `single_agent_v3_growth_zone_bad_stage_correction_z3_s26_r2.jsonl` (steps 4–5)
    - `single_agent_v3_growth_zone_bad_stage_correction_z3_s27_r0.jsonl` (steps 5–6)
    - `single_agent_v3_growth_zone_bad_stage_correction_z3_s27_r1.jsonl` (steps 4–5)
    - `single_agent_v3_growth_zone_bad_stage_correction_z3_s28_r0.jsonl` (steps 3–4)
    - `single_agent_v3_growth_zone_bad_stage_correction_z3_s28_r1.jsonl` (steps 4–5)
- **Claim**: On $7$ of the $8$ `single_agent` runs on `bad_stage_correction` that are scored as `good_report` in `results/2026-10-25_freeze_v4/scores.json`, `single_agent` never requests `stage_log_summary`, never diagnoses `bad_stage_correction`, and never applies `register_frames`; instead, it applies `use_width_free_ratio` (`fault="width_change"`) and calls `accept` while `closure` still fails at $19.655\text{–}19.721\text{ px/h} > 1.0\text{ px/h}$.
- **Evidence**:
  - In all $7$ listed runs, `single_agent` requests `displacement_vs_patch_radius` and `velocity_profile` (plus `frame_quality` in `s27_r0`), applies `apply_remedy(fault="width_change", remedy="use_width_free_ratio")`, and calls `accept`.
  - In the corresponding `*_summary.json` files (`single_agent_v3_growth_zone_bad_stage_correction_z3_s26_r0_summary.json`, etc.), `final_checks` shows `closure` still failing (`passed: false`, `value: 19.65504691030638` on `s26`, `19.66996393772348` on `s27`, `19.721332234625184` on `s28` vs `threshold: 1.0`), `plane_sections` `passed: null`, and `fault_correct: false` in `scores.json`.
  - Because `bad_stage_correction` shifts whole-frame velocities by a constant offset without altering spatial velocity derivatives, the unrepaired measurement already satisfies the ground-truth `regr` MSE threshold (`good: true`), so `measure/metrics.py:16-22` (`category("accept", "accept_repaired", good=True)`) scores all $7$ unrepaired runs as `good_report`.
- **What would confirm it**: Checking `final_checks` and `remedies_applied` in `single_agent_v3_growth_zone_bad_stage_correction_z3_*_summary.json` and `fault_correct` in `results/2026-10-25_freeze_v4/scores.json`, where `fault_named_correct` for `single_agent` across `accept_repaired` + `decline` is $19 / 99$ (`results/2026-10-25_freeze_v4/metrics.json`).

---

### Finding A3-F4
- **ID**: `A3-F4`
- **Severity**: Medium
- **Trace and step**:
  - `single_agent` on `v3_growth_zone_clean` ($9 / 9$ runs), `bad_stage_correction` ($2 / 9$ runs), `rigid_drift` ($9 / 9$ runs), and `stage_log_missing` ($5 / 9$ runs) in `results/2026-10-25_freeze_v4/runs/`:
    - `single_agent_v3_growth_zone_clean_s26_r0.jsonl` (step 4), `s26_r1` (step 3), `s26_r2` (step 3), `s27_r0` (step 3), `s27_r1` (step 5), `s27_r2` (step 5), `s28_r0` (step 4), `s28_r1` (step 3), `s28_r2` (step 3)
    - `single_agent_v3_growth_zone_bad_stage_correction_z3_s27_r2.jsonl` (step 7), `s28_r2` (step 7)
    - `single_agent_v3_growth_zone_rigid_drift_z0.5_s26_r0.jsonl` (step 7), `s26_r1` (step 7), `s26_r2` (step 7), `s27_r0` (step 6), `s27_r1` (step 7), `s27_r2` (step 7), `s28_r0` (step 6), `s28_r1` (step 7), `s28_r2` (step 6)
    - `single_agent_v3_growth_zone_stage_log_missing_z1_s26_r0.jsonl` (step 8), `s26_r1` (step 8), `s27_r0` (step 8), `s27_r1` (step 7), `s28_r0` (step 8)
- **Claim**: Without the `plane_sections` checker threshold ($3.25$ in `config/checker_thresholds.yaml:30`), `single_agent` systematically misdiagnoses the clean baseline `v3_growth_zone` rod geometry as having a `width_change` fault whenever it inspects `velocity_profile` on a clean or drift-repaired `v3_growth_zone` rod, applying an unnecessary `use_width_free_ratio` remedy across $25$ runs (plus the $7$ unrepaired `bad_stage_correction` runs in `A3-F3` and $8$ `second_root` runs in `A3-F1`).
- **Evidence**:
  - On all $9$ `v3_growth_zone_clean` runs, `plane_sections` already passes (`passed: true` against the $3.25$ threshold in `single_agent_v3_growth_zone_clean_*_summary.json`). Seeing `velocity_profile`, `single_agent` applies `use_width_free_ratio` in $9 / 9$ runs before calling `accept`.
  - On all $9$ `rigid_drift` runs and on the $2$ `bad_stage_correction` runs (`s27_r2`, `s28_r2`) where `single_agent` first applies `register_frames` (which fixes `closure` so all three checks pass), `single_agent` then requests `velocity_profile` and applies a second remedy `use_width_free_ratio` at Step 6 or 7 (`s27_r2` then hits `step_limit` at Step 8).
  - On `stage_log_missing`, after `register_frames` at Step 4 or 5, $5$ runs (`s26_r0`, `s26_r1`, `s27_r0`, `s27_r1`, `s28_r0`) apply `use_width_free_ratio` at Step 7 or 8, with `s27_r1` accepting at Step 8 (`accept_on_decline`).
- **What would confirm it**: Inspecting `remedies_applied` in `single_agent_v3_growth_zone_clean_*_summary.json`, `single_agent_v3_growth_zone_rigid_drift_z0.5_*_summary.json`, and `single_agent_v3_growth_zone_bad_stage_correction_z3_*_summary.json`.

---

### Finding A3-F5
- **ID**: `A3-F5`
- **Severity**: Medium
- **Trace and step**:
  - `single_agent` on clean bending rods (`v3_bend16`, `v3_bend20`, `v3_bend24`, `v3_bend30` — $14$ runs in `results/2026-10-25_freeze_v4/runs/`):
    - $6$ `unnecessary_decline` runs:
      - `single_agent_v3_bend16_clean_s28_r1.jsonl` (step 5 `register_frames`, step 7 `decline`)
      - `single_agent_v3_bend16_clean_s28_r2.jsonl` (step 5 `register_frames`, step 7 `decline`)
      - `single_agent_v3_bend20_clean_s27_r1.jsonl` (step 4 `register_frames`, step 7 `decline`)
      - `single_agent_v3_bend20_clean_s28_r0.jsonl` (step 5 `register_frames`, step 7 `decline`)
      - `single_agent_v3_bend24_clean_s27_r0.jsonl` (step 5 `register_frames`, step 8 `decline`)
      - `single_agent_v3_bend30_clean_s26_r2.jsonl` (step 5 `register_frames`, step 7 `decline`)
    - $3$ `step_limit` (`not_reported`) runs:
      - `single_agent_v3_bend16_clean_s26_r0.jsonl` (step 5 `register_frames`, step 8 `step_limit`)
      - `single_agent_v3_bend30_clean_s27_r2.jsonl` (step 7 `register_frames`, step 8 `step_limit`)
      - `single_agent_v3_bend30_clean_s28_r2.jsonl` (step 6 `register_frames`, step 8 `step_limit`)
    - $5$ `accept` (`good_report`) runs with unnecessary `register_frames` kept:
      - `single_agent_v3_bend20_clean_s28_r1.jsonl` (step 5 `register_frames`, step 7 `accept`)
      - `single_agent_v3_bend24_clean_s28_r1.jsonl` (step 5 `register_frames`, step 7 `accept`)
      - `single_agent_v3_bend24_clean_s28_r2.jsonl` (step 5 `register_frames`, step 7 `accept`)
      - `single_agent_v3_bend30_clean_s27_r0.jsonl` (step 5 `register_frames`, step 7 `accept`)
      - `single_agent_v3_bend30_clean_s28_r1.jsonl` (step 5 `register_frames`, step 7 `accept`)
- **Claim**: On $14 / 36$ clean bending-rod runs (`v3_bend16`, `v3_bend20`, `v3_bend24`, `v3_bend30`), `single_agent` misinterprets the difference between `tip_net_displacement_um_per_h` (which includes lateral tip displacement from bending) and `basal_velocity_um_per_h` in `velocity_profile` as rigid drift or a bad stage correction despite `stage_log_summary` showing `closure_residual_px_per_pair_median = 0.02 px` (`max 0.03–0.04 px`), applies `register_frames` on a clean rod, and then either declines ($6$ runs), hits `step_limit` ($3$ runs), or accepts with the unnecessary remedy kept ($5$ runs).
- **Evidence**:
  - In all $14$ runs, `initial_checks` pass (`closure` is $0.117\text{–}0.200\text{ px/h} \le 1.0\text{ px/h}$) and `stage_log_summary` reports `closure_residual_px_per_pair_median: 0.02` and `closure_residual_px_per_pair_max: 0.03` or `0.04`.
  - Ignoring the near-zero closure residual in `stage_log_summary`, the agent applies `register_frames` (`fault="rigid_drift"` in $8$ runs, `fault="bad_stage_correction"` in $6$ runs). When the post-remedy `velocity_profile` shows the same gap between tip net displacement and basal velocity, $6$ runs declare that `register_frames` failed and call `decline` (`unnecessary_decline`).
- **What would confirm it**: Inspecting the $14$ trace files in `results/2026-10-25_freeze_v4/runs/single_agent_v3_bend*_clean_*.jsonl` and `results/2026-10-25_freeze_v4/scores.json`.

---

### Finding A3-F6
- **ID**: `A3-F6`
- **Severity**: Medium
- **Trace and step**:
  - `diagnostician` on `displacement_exceeds_patch` ($4$ runs in `results/2026-10-25_freeze_v4/runs/`):
    - `diagnostician_v3_growth_zone_displacement_exceeds_patch_z2x6_s26_r0.jsonl` (step 3: `request_info(kind="frame_quality")` after `change_frame_stride` at step 2)
    - `diagnostician_v3_growth_zone_displacement_exceeds_patch_z2x6_s26_r1.jsonl` (step 3: `request_info(kind="frame_quality")` after `change_frame_stride` at step 2)
    - `diagnostician_v3_growth_zone_displacement_exceeds_patch_z2x6_s28_r1.jsonl` (step 3: `request_info(kind="frame_quality")` after `change_frame_stride` at step 2)
    - `diagnostician_v3_growth_zone_displacement_exceeds_patch_z2x6_s28_r2.jsonl` (step 3: `request_info(kind="frame_quality")` after `change_frame_stride` at step 2)
- **Claim**: In $4 / 9$ `diagnostician` runs on `displacement_exceeds_patch`, the agent violates the explicit prompt rule in `agents/prompts/diagnostician_v4.md:54` (*"After a stride or patch remedy, request `displacement_vs_patch_radius` again before choosing the next action"*), and on seeds $26$ and $28$ `no_progress` (`agents/executors.py:94-99`) rolls back the first `change_frame_stride(setting="half")` call (`stride 6 -> 3`) because `closure` only drops by $21.8\%$ on seed $26$ ($170.371 \to 133.226\text{ px/h}$) and $16.5\%$ on seed $28$ ($182.976 \to 152.712\text{ px/h}$) — just short of the $25\%$ (`1/4`) rollback threshold, whereas on seed $27$ `closure` drops by $25.1\%$ ($183.095 \to 137.090\text{ px/h}$) and is kept.
- **Evidence**:
  - On all $9$ `displacement_exceeds_patch` runs, Step 1 `request_info(kind="displacement_vs_patch_radius")` shows `frame_stride: 6`, `disk_radius_px: 14`, and `tip_step_over_radius: 2.06`, and Step 2 applies `change_frame_stride(setting="half")` (`stride 6 -> 3`).
  - On seed $27$ (`s27_r0`, `s27_r1`, `s27_r2`), `closure` drops from $183.095$ to $137.090\text{ px/h}$ ($25.13\% \ge 25\%$), so `stride 3` is kept; the agent requests `displacement_vs_patch_radius` at Step 3 (`tip_step_over_radius: 1.03`), halves the stride again (`3 -> 1`) at Step 4, requests `displacement_vs_patch_radius` at Step 5 (`tip_step_over_radius: 0.34`), and declines with `fault="displacement_exceeds_patch"`.
  - On seeds $26$ and $28$, `closure` drops by $21.80\%$ and $16.54\%$ ($< 25\%$), so `change_frame_stride` is rolled back (`rolled_back: True`). In $4$ of the $6$ runs (`s26_r0`, `s26_r1`, `s28_r1`, `s28_r2`), the agent skips the required `displacement_vs_patch_radius` call at Step 3 and instead requests `frame_quality`, then chases `midline_jitter` (`smooth_midline`) and `bad_stage_correction` (`register_frames`), causing `s26_r0` (and `s26_r2`, which did call `displacement_vs_patch_radius` at Step 3) to hit `step_limit` at Step 8.
- **What would confirm it**: Comparing `check_values.closure` at Step 2 across `diagnostician_v3_growth_zone_displacement_exceeds_patch_z2x6_s26_r0.jsonl`, `s27_r0.jsonl`, and `s28_r0.jsonl`, and inspecting Step 3 in `s26_r0`, `s26_r1`, `s28_r1`, and `s28_r2`.

---

### Finding A3-F7
- **ID**: `A3-F7`
- **Severity**: Low
- **Trace and step**:
  - `diagnostician_v3_growth_zone_midline_jitter_z3_s26_r0.jsonl` (step 8: `apply_remedy(fault="displacement_exceeds_patch", remedy="change_frame_stride", setting="half")`)
  - `diagnostician_v3_growth_zone_fast_rotation_z2_s28_r0.jsonl` (step 8: `apply_remedy(fault="second_root", remedy="crop_or_mask", setting="mask_second_root")`)
  - `single_agent_v3_growth_zone_flank_swap_z0.5_s28_r1.jsonl` (step 7: `accept(confidence=0.6)`)
- **Claim**: Three individual runs make late-step decisions that directly contradict the evidence already returned in their own trace histories:
  1. `diagnostician_v3_growth_zone_midline_jitter_z3_s26_r0` calls `change_frame_stride(setting="half")` at Step 8 when `frame_stride` is already $1$ and `tip_step_over_radius` is $0.73 < 1.0$, triggering `{"rechecked": false, "error": "remedy not available: every frame is already used (stride 1)"}` and exhausting Step 8 (`step_limit`).
  2. `diagnostician_v3_growth_zone_fast_rotation_z2_s28_r0` calls `crop_or_mask(setting="mask_second_root")` at Step 8 despite `frame_quality` at Step 2 reporting `bright_objects_over_500px: 1` across all sampled frames, exhausting Step 8 (`step_limit`).
  3. `single_agent_v3_growth_zone_flank_swap_z0.5_s28_r1` calls `accept(confidence=0.6)` at Step 7 without applying any remedy (`false_accept`) even though its own Step 7 rationale notes that `basal_velocity_um_per_h` exceeds `tip_path_um_per_h` and that the profile is noisy (all three checks fail in `initial_checks`: `rigid_invariance` $> 2.0$, `closure` $= 15.611 > 1.0$, `plane_sections` $> 3.25$ in `single_agent_v3_growth_zone_flank_swap_z0.5_s28_r1_summary.json`).
- **Evidence**:
  - In `diagnostician_v3_growth_zone_midline_jitter_z3_s26_r0.jsonl`, `stride: 1` is shown in `initial_summary`, in `check_report` at Step 2, and in `displacement_vs_patch_radius` at Step 7 (`frame_stride: 1`, `tip_step_over_radius: 0.73`, `fraction_points_lost: 0.0`).
  - In `diagnostician_v3_growth_zone_fast_rotation_z2_s28_r0.jsonl`, Step 2 `frame_quality` reports `bright_objects_over_500px: 1` in frames $0$, $20$, and $40$; at Step 8 `mask_second_root` leaves all three checks unchanged (`closure` $= 10.454 > 1.0$, `rigid_invariance` $> 2.0$, `plane_sections` $> 3.25$) and is rolled back.
  - In `single_agent_v3_growth_zone_flank_swap_z0.5_s28_r1.jsonl`, the agent requests all $5$ info kinds across Steps 2–6 and calls `accept` at Step 7, yielding the sole `false_accept` across all $306$ agent runs in freeze v4.
- **What would confirm it**: Inspecting step 8 of `diagnostician_v3_growth_zone_midline_jitter_z3_s26_r0.jsonl`, step 8 of `diagnostician_v3_growth_zone_fast_rotation_z2_s28_r0.jsonl`, and step 7 of `single_agent_v3_growth_zone_flank_swap_z0.5_s28_r1.jsonl`.

---

## 4. What Was Not Checked

- The $2$ runs in `results/2026-10-25_freeze_v4/runs/usage_limit/` (excluded per `docs/specs/2026-11-03_argon-audit.md` section A2/A3).
- Any raw synthetic movie frames or `.npz` arrays on disk; this audit inspected the logged `.jsonl` traces and `*_summary.json` files in `results/2026-10-25_freeze_v4/runs/`.
- Any traces from `results/2026-10-23_freeze_v3/runs/` (other than the aggregate v3-to-v4 split verified in Task A2).
- Any real-data or unpublished lab traces (`private/` was not accessed).
