# Review: Independent recompute of freeze v4 and the v3-to-v4 split (Task A2)

- Auditor: `argon-audit` (Antigravity, Gemini 4 Argon)
- Branch: `audit/argon`
- Date: 2026-11-03
- Spec: `docs/specs/2026-11-03_argon-audit.md`, section A2
- Recompute script: `docs/reviews/2026-11-03_argon-v4-recompute/code/recompute.py`
- Inputs read before writing `recompute.py`:
  - `docs/proposals/2026-10-23_freeze-v3.md`
  - `docs/proposals/2026-10-25_freeze-v4-candidate.md`
  - `docs/decisions.md` (decision `2026-10-25`, C1, C2, C3 option (a))
  - `docs/specs/2026-10-10_repair-criteria.md`
  - `config/scoring_tolerance.yaml`
  - `results/2026-10-23_freeze_v3/labels.json` and `results/2026-10-23_freeze_v3/runs/*_summary.json`, `*_trace.jsonl` (`408` runs)
  - `results/2026-10-25_freeze_v4/labels.json` and `results/2026-10-25_freeze_v4/runs/*_summary.json`, `*_trace.jsonl` (`408` runs; `95` files in `runs/usage_limit/` excluded)
- Files compared after recording our independent numbers:
  - `results/2026-10-23_freeze_v3/README.md`, `results/2026-10-23_freeze_v3/table_metrics.md`, `results/2026-10-23_freeze_v3/metrics.json`, `results/2026-10-23_freeze_v3/labels.md`
  - `results/2026-10-25_freeze_v4/README.md`, `results/2026-10-25_freeze_v4/table_metrics.md`, `results/2026-10-25_freeze_v4/metrics.json`, `results/2026-10-25_freeze_v4/decompose_v3_v4.md`, `results/2026-10-25_freeze_v4/labels.md`, `results/2026-10-25_freeze_v4/switch_check.md`
  - `measure/metrics.py`, `measure/score.py`, `scripts/synth/scored_v3.py`, `scripts/synth/scored_v4.py`

## Summary of comparison

- Every primary metric in `results/2026-10-25_freeze_v4/README.md`, `results/2026-10-25_freeze_v4/table_metrics.md`, `results/2026-10-23_freeze_v3/README.md`, `results/2026-10-23_freeze_v3/table_metrics.md`, and `results/2026-10-25_freeze_v4/decompose_v3_v4.md` matches our independent recomputation to within $10^{-9}$ before rounding (`0` disagreements across balanced accuracy, per-class accuracies, overall accuracy, false-accept counts and rates, coverage, abstention precision and recall, `not_reported` counts, unanimity rates, Fleiss' $\kappa$, and all 5 columns of the v3-to-v4 split).
- Four findings (`A2-F1` to `A2-F4`) were identified in the prose explanation of `decompose_v3_v4.md` / `README.md`, the header of `results/2026-10-25_freeze_v4/labels.md`, and two secondary columns of `table_metrics.md`.

## Findings

### Finding A2-F1
- **id**: `A2-F1`
- **severity**: `medium`
- **file and line**: `results/2026-10-25_freeze_v4/decompose_v3_v4.md:3`, `scripts/synth/scored_v4.py:278`, and `results/2026-10-25_freeze_v4/README.md:55`
- **claim**: The decomposition text misstates what `script` and `single_agent` did on the 3 `stage_log_missing` rods in freeze v3 (`v3_growth_zone_stage_log_missing_z1_s20`, `s21`, `s22`). `decompose_v3_v4.md:3` states `"Every method declined those rods in v3"`, and `README.md:55` states `"In v3 every non-script method declined those 3 rods"`. Neither statement holds for `single_agent`.
- **evidence**:
  - In `results/2026-10-23_freeze_v3/runs/`, on `v3_growth_zone_stage_log_missing_z1_s20`, `s21`, `s22`:
    - `script` accepted all `3` runs (`status = "accept"`, `good_report` under v3 labels; `accept_on_decline` under C3 (a) labels), reducing `script` overall accuracy from $\frac{30}{51} = 0.59$ to $\frac{27}{51} = 0.53$ (`decompose_v3_v4.md:33`).
    - `remedy_tree` (`3 / 3`) and `diagnostician` (`9 / 9`) declined all runs (`status = "decline"`, moving from `unnecessary_decline` under v3 labels to `correct_decline` under C3 (a) labels).
    - `single_agent` declined `0 / 9` runs; all `9` runs (`s20`, `s21`, `s22` across repeats `0`, `1`, `2`) ended at `status = "step_limit"` (`category = "not_reported"` under both v3 labels and C3 (a) labels; see `results/2026-10-23_freeze_v3/table_metrics.md:344-367`).
  - Because `single_agent` produced `not_reported` (`0 / 9` correct) under both labelings, relabelling `stage_log_missing` from `accept_repaired` to `decline` in `decompose_v3_v4.md` leaves `single_agent` overall accuracy unchanged at $\frac{90}{153} = 0.5882$ (`0.59`, `decompose_v3_v4.md:36`), lowers `single_agent` `decline` accuracy from $\frac{27}{63} = 0.4286$ (`0.43`) to $\frac{27}{72} = 0.3750$ (`0.38`, `decompose_v3_v4.md:56`), raises `accept_repaired` accuracy from $\frac{22}{36} = 0.6111$ (`0.61`) to $\frac{22}{27} = 0.8148$ (`0.81`, `decompose_v3_v4.md:46`), and raises balanced accuracy by $\frac{1}{3}\left(\frac{22}{27}-\frac{22}{36}+\frac{27}{72}-\frac{27}{63}\right) = +0.0500$ (`0.60` to `0.65`, `decompose_v3_v4.md:26`) solely from shifting 3 `not_reported` rods per repeat from the `accept_repaired` denominator to the `decline` denominator.
- **what would confirm it**: Inspecting `results/2026-10-23_freeze_v3/runs/single_agent_v3_growth_zone_stage_log_missing_z1_s2{0,1,2}_r{0,1,2}_summary.json`, where `outcome.status` is `"step_limit"` in all `9` files.

### Finding A2-F2
- **id**: `A2-F2`
- **severity**: `low`
- **file and line**: `results/2026-10-25_freeze_v4/labels.md:3`, `scripts/synth/scored_v4.py:61-65,347-352`, and `scripts/synth/scored_v3.py:393`
- **claim**: `results/2026-10-25_freeze_v4/labels.md:3` prints `"Scoring seeds 20, 21, 22."` in the header of the freeze v4 label report even though all 51 rods in `results/2026-10-25_freeze_v4/labels.md:7-57` and `labels.json` use scoring seeds `26, 27, 28`.
- **evidence**: `point_v3_at_v4()` in `scripts/synth/scored_v4.py:61-65` overrides `v3.scored_rods` (which uses `SCORING_SEEDS = (26, 27, 28)` from `scored_v4.py:43`), and `scored_v4.py:348-351` replaces the H1 title and repair-criteria parenthetical in the string returned by `v3.labels_report()`, but `point_v3_at_v4()` does not override `v3.seeds`. Consequently, `scripts/synth/scored_v3.py:393` calls `seeds('scoring_seeds')` (`scored_v3.py:88-90`), which reads `v3.scoring_seeds` (`[20, 21, 22]`) from `config/scoring_seeds.yaml:5`.
- **what would confirm it**: Reading `results/2026-10-25_freeze_v4/labels.md:1-10` alongside `scripts/synth/scored_v4.py:61-65,346-355`.

### Finding A2-F3
- **id**: `A2-F3`
- **severity**: `low`
- **file and line**: `measure/metrics.py:63`, `scripts/synth/scored_v3.py:567,643`, `results/2026-10-23_freeze_v3/table_metrics.md:28`, and `results/2026-10-25_freeze_v4/table_metrics.md:28`
- **claim**: The metric `runs_with_remedy_kept_per_class["accept_clean"]` (`measure/metrics.py:63`, printed as `"Runs keeping a remedy, accept_clean"` in `table_metrics.md:23-28`) counts runs on `accept_clean` rods where `len(remedies) - 2 * roll_backs > 0` even when the run ended in `decline` or `step_limit` (`reported = false`).
- **evidence**:
  - In `docs/proposals/2026-10-23_freeze-v3.md:101`, the diagnostic metric is defined as `"Remedies kept on accept_clean rods (count; target 0): a remedy kept on a clean rod is an unnecessary remedy"`.
  - For `single_agent` on `accept_clean` rods (`54` runs across 3 repeats):
    - In freeze v3 (`results/2026-10-23_freeze_v3/table_metrics.md:28`), `runs_with_remedy_kept_per_class["accept_clean"]` is `21` (`6 + 7 + 8`), comprising `9` accepted runs (`status = "accept"`, all on `v3_growth_zone_clean_s20/21/22` with `use_width_free_ratio`), `10` declined runs (`status = "decline"` after `register_frames`), and `2` `step_limit` runs (`status = "step_limit"` after `register_frames`).
    - In freeze v4 (`results/2026-10-25_freeze_v4/table_metrics.md:28`), `runs_with_remedy_kept_per_class["accept_clean"]` is `23` (`7 + 8 + 8`), comprising `14` accepted runs (`9` on `v3_growth_zone_clean_s26/27/28` with `use_width_free_ratio` and `5` on clean bent rods with `register_frames`), `6` declined runs, and `3` `step_limit` runs.
- **what would confirm it**: Comparing `remedies_on_clean_accepted` (`status == "accept"` and `remedies_kept > 0`) vs `remedies_on_clean_any` (`remedies_kept > 0` regardless of `status`) in `docs/reviews/2026-11-03_argon-v4-recompute/code/recompute.py:249-256`.

### Finding A2-F4
- **id**: `A2-F4`
- **severity**: `low`
- **file and line**: `scripts/synth/scored_v3.py:483,527,563`
- **claim**: Rule-method summary files (`script_*_summary.json` and `remedy_tree_*_summary.json`) omit the `"trace"` and `"repeat"` fields that LLM summary files include.
- **evidence**: `run_rules()` (`scripts/synth/scored_v3.py:483`) calls `write_summary(summ, rod, sl, o, m, {})`, whereas `run_agents()` (`scored_v3.py:527`) passes `{"repeat": repeat, "trace": trace.name, ...}`. When scoring `named_fault` on accepted `remedy_tree` runs (`outcome.args == {}`), `scored_v3.py:563` relies on filename substitution (`s.get("trace", f.name.replace("_summary.json", "_trace.jsonl"))`). Without that filename fallback, reading `summary.get("trace")` yields `7 / 33` instead of `14 / 33` for `remedy_tree` in freeze v3, and `9 / 33` instead of `16 / 33` in freeze v4.
- **what would confirm it**: Inspecting any `results/2026-10-25_freeze_v4/runs/remedy_tree_*_summary.json` file (which has no `"trace"` key) alongside `scripts/synth/scored_v3.py:483,563`.

---

## Side-by-side comparison tables (Theirs vs Ours)

### 1. Freeze v4 main metrics (`results/2026-10-25_freeze_v4/README.md:19-26`, `table_metrics.md:5-12`)

51 rods (`accept_clean` 18, `accept_repaired` 9, `decline` 24). Values for 3-repeat LLM methods are mean over repeats with `(min-max)` where repeats differ.

| Method | Metric | Theirs (`table_metrics.md`) | Ours (`recompute.py`, exact mean [min, max]) | Match |
| :-- | :-- | :-- | :-- | :-- |
| `script` | Runs | `51` | `51` | Exact |
| `script` | Balanced accuracy | `0.67` | $0.6667$ | Exact |
| `script` | Acc. `accept_clean` | `1.00` | $1.0000$ ($18/18$) | Exact |
| `script` | Acc. `accept_repaired` | `1.00` | $1.0000$ ($9/9$) | Exact |
| `script` | Acc. `decline` | `0.00` | $0.0000$ ($0/24$) | Exact |
| `script` | Overall accuracy | `0.53` | $0.5294$ ($27/51$) | Exact |
| `script` | False accepts | `18.0` | $18.0$ ($18$) | Exact |
| `script` | False-accept rate | `0.35` | $0.3529$ ($18/51$) | Exact |
| `script` | Coverage | `1.00` | $1.0000$ ($51/51$) | Exact |
| `script` | Abst. precision | `-` | `None` ($0/0$) | Exact |
| `script` | Abst. recall | `0.00` | $0.0000$ ($0/24$) | Exact |
| `script` | `not_reported` | `0` | `0` | Exact |
| `remedy_tree` | Runs | `51` | `51` | Exact |
| `remedy_tree` | Balanced accuracy | `0.93` | $0.9306$ | Exact |
| `remedy_tree` | Acc. `accept_clean` | `1.00` | $1.0000$ ($18/18$) | Exact |
| `remedy_tree` | Acc. `accept_repaired` | `1.00` | $1.0000$ ($9/9$) | Exact |
| `remedy_tree` | Acc. `decline` | `0.79` | $0.7917$ ($19/24$) | Exact |
| `remedy_tree` | Overall accuracy | `0.90` | $0.9020$ ($46/51$) | Exact |
| `remedy_tree` | False accepts | `2.0` | $2.0$ ($2$) | Exact |
| `remedy_tree` | False-accept rate | `0.06` | $0.0625$ ($2/32$) | Exact |
| `remedy_tree` | Coverage | `0.63` | $0.6275$ ($32/51$) | Exact |
| `remedy_tree` | Abst. precision | `1.00` | $1.0000$ ($19/19$) | Exact |
| `remedy_tree` | Abst. recall | `0.79` | $0.7917$ ($19/24$) | Exact |
| `remedy_tree` | `not_reported` | `0` | `0` | Exact |
| `diagnostician` | Runs | `153` | `153` | Exact |
| `diagnostician` | Balanced accuracy | `0.93 (0.92-0.94)` | $0.9306$ ($[0.9167, 0.9444]$) | Exact |
| `diagnostician` | Acc. `accept_clean` | `1.00` | $1.0000$ ($[1.0000, 1.0000]$, $54/54$) | Exact |
| `diagnostician` | Acc. `accept_repaired` | `1.00` | $1.0000$ ($[1.0000, 1.0000]$, $27/27$) | Exact |
| `diagnostician` | Acc. `decline` | `0.79 (0.75-0.83)` | $0.7917$ ($[0.7500, 0.8333]$, $57/72$) | Exact |
| `diagnostician` | Overall accuracy | `0.90 (0.88-0.92)` | $0.9020$ ($[0.8824, 0.9216]$, $138/153$) | Exact |
| `diagnostician` | False accepts | `0.0` | $0.0$ ($0$) | Exact |
| `diagnostician` | False-accept rate | `0.00` | $0.0000$ ($0/89$) | Exact |
| `diagnostician` | Coverage | `0.58 (0.57-0.59)` | $0.5817$ ($[0.5686, 0.5882]$, $89/153$) | Exact |
| `diagnostician` | Abst. precision | `1.00` | $1.0000$ ($[1.0000, 1.0000]$, $57/57$) | Exact |
| `diagnostician` | Abst. recall | `0.79 (0.75-0.83)` | $0.7917$ ($[0.7500, 0.8333]$, $57/72$) | Exact |
| `diagnostician` | `not_reported` | `7` | `7` ($1 + 4 + 2$) | Exact |
| `single_agent` | Runs | `153` | `153` | Exact |
| `single_agent` | Balanced accuracy | `0.63 (0.58-0.69)` | $0.6312$ ($[0.5802, 0.6852]$) | Exact |
| `single_agent` | Acc. `accept_clean` | `0.83 (0.78-0.89)` | $0.8333$ ($[0.7778, 0.8889]$, $45/54$) | Exact |
| `single_agent` | Acc. `accept_repaired` | `0.96 (0.89-1.00)` | $0.9630$ ($[0.8889, 1.0000]$, $26/27$) | Exact |
| `single_agent` | Acc. `decline` | `0.10 (0.04-0.17)` | $0.0972$ ($[0.0417, 0.1667]$, $7/72$) | Exact |
| `single_agent` | Overall accuracy | `0.51 (0.47-0.57)` | $0.5098$ ($[0.4706, 0.5686]$, $78/153$) | Exact |
| `single_agent` | False accepts | `0.3 (0.0-1.0)` | $0.3333$ ($[0, 1]$, total $1$) | Exact |
| `single_agent` | False-accept rate | `0.01 (0.00-0.04)` | $0.0133$ ($[0.0000, 0.0400]$; pooled $1/74 = 0.0135$) | Exact |
| `single_agent` | Coverage | `0.48 (0.43-0.55)` | $0.4837$ ($[0.4314, 0.5490]$, $74/153$) | Exact |
| `single_agent` | Abst. precision | `0.50 (0.33-0.67)` | $0.5000$ ($[0.3333, 0.6667]$; pooled $7/13 = 0.5385$) | Exact |
| `single_agent` | Abst. recall | `0.10 (0.04-0.17)` | $0.0972$ ($[0.0417, 0.1667]$, $7/72$) | Exact |
| `single_agent` | `not_reported` | `66` | `66` ($19 + 26 + 21$) | Exact |
| `all_decline` | Balanced / Overall / Abst. prec. | `0.33` / `0.47` / `0.47` | $0.3333$ / $0.4706$ ($24/51$) / $0.4706$ ($24/51$) | Exact |
| `all_accept` | Balanced / Overall / FAR | `0.67` / `0.53` / `0.35` | $0.6667$ / $0.5294$ ($27/51$) / $0.3529$ ($18/51$) | Exact |

### 2. Freeze v3 main metrics (`results/2026-10-23_freeze_v3/README.md:27-34`, `table_metrics.md:5-12`)

51 rods (`accept_clean` 18, `accept_repaired` 12, `decline` 21).

| Method | Balanced acc. (Theirs / Ours) | Acc. `accept_clean` (Theirs / Ours) | Acc. `accept_repaired` (Theirs / Ours) | Acc. `decline` (Theirs / Ours) | Overall (Theirs / Ours) | False accepts (Theirs / Ours) | FAR (Theirs / Ours) | Coverage (Theirs / Ours) | Abst. prec. (Theirs / Ours) | Abst. recall (Theirs / Ours) | `not_reported` (Theirs / Ours) |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `script` | `0.67` / $0.6667$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `0.00` / $0.0000$ | `0.59` / $0.5882$ | `18.0` / $18.0$ | `0.35` / $0.3529$ | `1.00` / $1.0000$ | `-` / `None` | `0.00` / $0.0000$ | `0` / `0` |
| `remedy_tree` | `0.81` / $0.8056$ | `1.00` / $1.0000$ | `0.75` / $0.7500$ | `0.67` / $0.6667$ | `0.80` / $0.8039$ | `4.0` / $4.0$ | `0.12` / $0.1176$ | `0.67` / $0.6667$ | `0.82` / $0.8235$ | `0.67` / $0.6667$ | `0` / `0` |
| `diagnostician` | `0.69 (0.69-0.69)` / $0.6887$ ($[0.6852, 0.6918]$) | `0.91 (0.89-0.94)` / $0.9074$ ($[0.8889, 0.9444]$) | `0.44 (0.42-0.50)` / $0.4444$ ($[0.4167, 0.5000]$) | `0.71 (0.67-0.76)` / $0.7143$ ($[0.6667, 0.7619]$) | `0.72 (0.71-0.73)` / $0.7190$ ($[0.7059, 0.7255]$) | `0.0` / $0.0$ | `0.00` / $0.0000$ | `0.48 (0.47-0.49)` / $0.4837$ ($[0.4706, 0.4902]$) | `0.64 (0.64-0.65)` / $0.6428$ ($[0.6364, 0.6522]$) | `0.71 (0.67-0.76)` / $0.7143$ ($[0.6667, 0.7619]$) | `9` / `9` |
| `single_agent` | `0.60 (0.57-0.64)` / $0.5996$ ($[0.5661, 0.6402]$) | `0.76 (0.72-0.78)` / $0.7593$ ($[0.7222, 0.7778]$) | `0.61 (0.50-0.67)` / $0.6111$ ($[0.5000, 0.6667]$) | `0.43 (0.33-0.48)` / $0.4286$ ($[0.3333, 0.4762]$) | `0.59 (0.57-0.63)` / $0.5882$ ($[0.5686, 0.6275]$) | `0.0` / $0.0$ | `0.00` / $0.0000$ | `0.45 (0.43-0.47)` / $0.4510$ ($[0.4314, 0.4706]$) | `0.65 (0.58-0.71)` / $0.6548$ ($[0.5833, 0.7143]$; pooled $0.6585$) | `0.43 (0.33-0.48)` / $0.4286$ ($[0.3333, 0.4762]$) | `43` / `43` |
| `all_decline` | `0.33` / $0.3333$ | `0.00` / $0.0000$ | `0.00` / $0.0000$ | `1.00` / $1.0000$ | `0.41` / $0.4118$ | `0.0` / $0.0$ | `-` / `None` | `0.00` / $0.0000$ | `0.41` / $0.4118$ | `1.00` / $1.0000$ | `0` / `0` |
| `all_accept` | `0.67` / $0.6667$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `0.00` / $0.0000$ | `0.59` / $0.5882$ | `18.0` / $18.0$ | `0.35` / $0.3529$ | `1.00` / $1.0000$ | `-` / `None` | `0.00` / $0.0000$ | `0` / `0` |

### 3. Agreement across repeats (`table_metrics.md:16-19`)

| Freeze | Method | Rods (Theirs / Ours) | Unanimous (Theirs / Ours) | Unanimity rate (Theirs / Ours) | `accept_clean` (Theirs / Ours) | `accept_repaired` (Theirs / Ours) | `decline` (Theirs / Ours) | Fleiss' $\kappa$ (Theirs / Ours) |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `freeze_v3` | `diagnostician` | `51` / `51` | `39` / `39` | `0.76` / $0.7647$ | `0.94` / $0.9444$ ($17/18$) | `0.67` / $0.6667$ ($8/12$) | `0.67` / $0.6667$ ($14/21$) | `0.776` / $0.7760$ |
| `freeze_v3` | `single_agent` | `51` / `51` | `24` / `24` | `0.47` / $0.4706$ | `0.44` / $0.4444$ ($8/18$) | `0.67` / $0.6667$ ($8/12$) | `0.38` / $0.3810$ ($8/21$) | `0.503` / $0.5032$ |
| `freeze_v4` | `diagnostician` | `51` / `51` | `46` / `46` | `0.90` / $0.9020$ | `1.00` / $1.0000$ ($18/18$) | `1.00` / $1.0000$ ($9/9$) | `0.79` / $0.7917$ ($19/24$) | `0.887` / $0.8875$ |
| `freeze_v4` | `single_agent` | `51` / `51` | `34` / `34` | `0.67` / $0.6667$ | `0.56` / $0.5556$ ($10/18$) | `0.89` / $0.8889$ ($8/9$) | `0.67` / $0.6667$ ($16/24$) | `0.626` / $0.6258$ |

### 4. Categories, remedies kept, unnecessary declines, and fault named correct (`table_metrics.md:23-30`)

| Freeze | Method | Categories `good_report` / `false_accept` / `correct_decline` / `unnecessary_decline` / `not_reported` / `accept_on_decline` (Theirs vs Ours) | Runs keeping a remedy, `accept_clean` (Theirs / Ours all statuses / Ours accepted only) | Unnecessary-decline rate `accept_clean` / `accept_repaired` (Theirs vs Ours) | Fault named correct (Theirs / Ours with trace fallback / Ours from summary key) |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `freeze_v3` | `script` | `30 / 18 / 0 / 0 / 0 / 3` (Exact) | `0` / `0` / `0` | `0.00 / 0.00` (Exact) | `0 of 33` / `0 of 33` / `0 of 33` |
| `freeze_v3` | `remedy_tree` | `27 / 4 / 14 / 3 / 0 / 3` (Exact) | `1` / `1` / `1` | `0.00 / 0.25` (Exact) | `14 of 33` / `14 of 33` / `7 of 33` (`A2-F4`) |
| `freeze_v3` | `diagnostician` | `65 / 0 / 45 / 25 / 9 / 9` (Exact) | `0` / `0` / `0` | `0.09 (0.06-0.11) / 0.56 (0.50-0.58)` (Exact) | `54 of 99` / `54 of 99` / `54 of 99` |
| `freeze_v3` | `single_agent` | `63 / 0 / 27 / 14 / 43 / 6` (Exact) | `21` / `21` / `9` (`A2-F3`) | `0.20 (0.17-0.22) / 0.08 (0.00-0.17)` (Exact) | `31 of 99` / `31 of 99` / `31 of 99` |
| `freeze_v4` | `script` | `27 / 18 / 0 / 0 / 0 / 6` (Exact) | `0` / `0` / `0` | `0.00 / 0.00` (Exact) | `0 of 33` / `0 of 33` / `0 of 33` |
| `freeze_v4` | `remedy_tree` | `27 / 2 / 19 / 0 / 0 / 3` (Exact) | `0` / `0` / `0` | `0.00 / 0.00` (Exact) | `16 of 33` / `16 of 33` / `9 of 33` (`A2-F4`) |
| `freeze_v4` | `diagnostician` | `81 / 0 / 57 / 0 / 7 / 8` (Exact) | `2` / `2` / `2` | `0.00 / 0.00` (Exact) | `54 of 99` / `54 of 99` / `54 of 99` |
| `freeze_v4` | `single_agent` | `71 / 1 / 7 / 6 / 66 / 2` (Exact) | `23` / `23` / `14` (`A2-F3`) | `0.11 / 0.00` (Exact) | `39 of 99` / `39 of 99` / `39 of 99` |

### 5. Freeze v3 to v4 decomposition (`results/2026-10-25_freeze_v4/decompose_v3_v4.md:19-66`)

Columns:
- **Col 1**: `v3 runs, v3 labels` (`51` rods: `accept_clean` 18, `accept_repaired` 12, `decline` 21)
- **Col 2**: `v3 runs, C3 (a) labels` (`51` rods: `accept_clean` 18, `accept_repaired` 9, `decline` 24)
- **Col 3**: `v4 runs, v4 labels` (`51` rods: `accept_clean` 18, `accept_repaired` 9, `decline` 24)
- **Col 4**: `v3 runs, unchanged rows` (`48` rods: `accept_clean` 18, `accept_repaired` 9, `decline` 21; `stage_log_missing` excluded)
- **Col 5**: `v4 runs, unchanged rows` (`48` rods: `accept_clean` 18, `accept_repaired` 9, `decline` 21; `stage_log_missing` excluded)

| Table | Method | Col 1 (Theirs / Ours) | Col 2 (Theirs / Ours) | Col 3 (Theirs / Ours) | Col 4 (Theirs / Ours) | Col 5 (Theirs / Ours) | Match |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **Balanced accuracy** | `script` | `0.67` / $0.6667$ | `0.67` / $0.6667$ | `0.67` / $0.6667$ | `0.67` / $0.6667$ | `0.67` / $0.6667$ | Exact |
| **Balanced accuracy** | `remedy_tree` | `0.81` / $0.8056$ | `0.90` / $0.9028$ | `0.93` / $0.9306$ | `0.89` / $0.8889$ | `0.92` / $0.9206$ | Exact |
| **Balanced accuracy** | `diagnostician` | `0.69 (0.69-0.69)` / $0.6887$ | `0.75 (0.75-0.75)` / $0.7500$ | `0.93 (0.92-0.94)` / $0.9306$ | `0.74 (0.74-0.74)` / $0.7381$ | `0.92 (0.90-0.94)` / $0.9206$ | Exact |
| **Balanced accuracy** | `single_agent` | `0.60 (0.57-0.64)` / $0.5996$ | `0.65 (0.60-0.69)` / $0.6497$ | `0.63 (0.58-0.69)` / $0.6312$ | `0.67 (0.62-0.71)` / $0.6675$ | `0.64 (0.59-0.69)` / $0.6358$ | Exact |
| **Balanced accuracy** | `all_decline` | `0.33` / $0.3333$ | `0.33` / $0.3333$ | `0.33` / $0.3333$ | `0.33` / $0.3333$ | `0.33` / $0.3333$ | Exact |
| **Overall accuracy** | `script` | `0.59` / $0.5882$ | `0.53` / $0.5294$ | `0.53` / $0.5294$ | `0.56` / $0.5625$ | `0.56` / $0.5625$ | Exact |
| **Overall accuracy** | `remedy_tree` | `0.80` / $0.8039$ | `0.86` / $0.8627$ | `0.90` / $0.9020$ | `0.85` / $0.8542$ | `0.90` / $0.8958$ | Exact |
| **Overall accuracy** | `diagnostician` | `0.72 (0.71-0.73)` / $0.7190$ | `0.78 (0.76-0.78)` / $0.7778$ | `0.90 (0.88-0.92)` / $0.9020$ | `0.76 (0.75-0.77)` / $0.7639$ | `0.90 (0.88-0.92)` / $0.8958$ | Exact |
| **Overall accuracy** | `single_agent` | `0.59 (0.57-0.63)` / $0.5882$ | `0.59 (0.57-0.63)` / $0.5882$ | `0.51 (0.47-0.57)` / $0.5098$ | `0.62 (0.60-0.67)` / $0.6250$ | `0.54 (0.50-0.60)` / $0.5417$ | Exact |
| **Overall accuracy** | `all_decline` | `0.41` / $0.4118$ | `0.47` / $0.4706$ | `0.47` / $0.4706$ | `0.44` / $0.4375$ | `0.44` / $0.4375$ | Exact |
| **Acc. `accept_repaired`** | `script` | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | Exact |
| **Acc. `accept_repaired`** | `remedy_tree` | `0.75` / $0.7500$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | Exact |
| **Acc. `accept_repaired`** | `diagnostician` | `0.44 (0.42-0.50)` / $0.4444$ | `0.59 (0.56-0.67)` / $0.5926$ | `1.00` / $1.0000$ | `0.59 (0.56-0.67)` / $0.5926$ | `1.00` / $1.0000$ | Exact |
| **Acc. `accept_repaired`** | `single_agent` | `0.61 (0.50-0.67)` / $0.6111$ | `0.81 (0.67-0.89)` / $0.8148$ | `0.96 (0.89-1.00)` / $0.9630$ | `0.81 (0.67-0.89)` / $0.8148$ | `0.96 (0.89-1.00)` / $0.9630$ | Exact |
| **Acc. `accept_repaired`** | `all_decline` | `0.00` / $0.0000$ | `0.00` / $0.0000$ | `0.00` / $0.0000$ | `0.00` / $0.0000$ | `0.00` / $0.0000$ | Exact |
| **Acc. `decline`** | `script` | `0.00` / $0.0000$ | `0.00` / $0.0000$ | `0.00` / $0.0000$ | `0.00` / $0.0000$ | `0.00` / $0.0000$ | Exact |
| **Acc. `decline`** | `remedy_tree` | `0.67` / $0.6667$ | `0.71` / $0.7083$ | `0.79` / $0.7917$ | `0.67` / $0.6667$ | `0.76` / $0.7619$ | Exact |
| **Acc. `decline`** | `diagnostician` | `0.71 (0.67-0.76)` / $0.7143$ | `0.75 (0.71-0.79)` / $0.7500$ | `0.79 (0.75-0.83)` / $0.7917$ | `0.71 (0.67-0.76)` / $0.7143$ | `0.76 (0.71-0.81)` / $0.7619$ | Exact |
| **Acc. `decline`** | `single_agent` | `0.43 (0.33-0.48)` / $0.4286$ | `0.38 (0.29-0.42)` / $0.3750$ | `0.10 (0.04-0.17)` / $0.0972$ | `0.43 (0.33-0.48)` / $0.4286$ | `0.11 (0.05-0.19)` / $0.1111$ | Exact |
| **Acc. `decline`** | `all_decline` | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | `1.00` / $1.0000$ | Exact |
| **False accepts / rep.** | `script` | `18.0` / $18.0$ | `18.0` / $18.0$ | `18.0` / $18.0$ | `18.0` / $18.0$ | `18.0` / $18.0$ | Exact |
| **False accepts / rep.** | `remedy_tree` | `4.0` / $4.0$ | `4.0` / $4.0$ | `2.0` / $2.0$ | `4.0` / $4.0$ | `2.0` / $2.0$ | Exact |
| **False accepts / rep.** | `diagnostician` | `0.0` / $0.0$ | `0.0` / $0.0$ | `0.0` / $0.0$ | `0.0` / $0.0$ | `0.0` / $0.0$ | Exact |
| **False accepts / rep.** | `single_agent` | `0.0` / $0.0$ | `0.0` / $0.0$ | `0.3 (0.0-1.0)` / $0.3333$ ($[0, 1]$) | `0.0` / $0.0$ | `0.3 (0.0-1.0)` / $0.3333$ ($[0, 1]$) | Exact |

### 6. Per-row breakdown (`results/2026-10-23_freeze_v3/table_metrics.md:34-52`, `results/2026-10-25_freeze_v4/table_metrics.md:34-52`, `README.md:67-85`)

All `17` rows $\times$ `4` methods in both freeze v3 and freeze v4 match `table_metrics.md:34-52` and `results/2026-10-25_freeze_v4/README.md:67-85` identically:

| Row | v3 Class | v4 Class | v3 `script` / `remedy_tree` / `diagnostician` / `single_agent` (Theirs = Ours) | v4 `script` / `remedy_tree` / `diagnostician` / `single_agent` (Theirs = Ours) |
| :-- | :-- | :-- | :-- | :-- |
| `v3_growth_zone` | `accept_clean` | `accept_clean` | `3/3`, `3/3`, `9/9`, `9/9` | `3/3`, `3/3`, `9/9`, `9/9` |
| `v3_bend16` | `accept_clean` | `accept_clean` | `3/3`, `3/3`, `9/9`, `6/9` | `3/3`, `3/3`, `9/9`, `6/9` |
| `v3_bend20` | `accept_clean` | `accept_clean` | `3/3`, `3/3`, `9/9`, `5/9` | `3/3`, `3/3`, `9/9`, `7/9` |
| `v3_bend24` | `accept_clean` | `accept_clean` | `3/3`, `3/3`, `9/9`, `7/9` | `3/3`, `3/3`, `9/9`, `8/9` |
| `v3_bend30` | `accept_clean` | `accept_clean` | `3/3`, `3/3`, `6/9`, `5/9` | `3/3`, `3/3`, `9/9`, `6/9` |
| `v3_still` | `accept_clean` | `accept_clean` | `3/3`, `3/3`, `7/9`, `9/9` | `3/3`, `3/3`, `9/9`, `9/9` |
| `rigid_drift` | `accept_repaired` | `accept_repaired` | `3/3`, `3/3`, `3/9`, `6/9` | `3/3`, `3/3`, `9/9`, `9/9` |
| `displacement_exceeds_patch` | `decline` | `decline` | `0/3`, `2/3`, `6/9`, `3/9` | `0/3`, `3/3`, `7/9`, `0/9` |
| `width_change` | `accept_repaired` | `accept_repaired` | `3/3`, `3/3`, `9/9`, `9/9` | `3/3`, `3/3`, `9/9`, `9/9` |
| `low_texture` | `decline` | `decline` | `0/3`, `3/3`, `9/9`, `9/9` | `0/3`, `3/3`, `9/9`, `0/9` |
| `midline_jitter` | `decline` | `decline` | `0/3`, `3/3`, `9/9`, `4/9` | `0/3`, `3/3`, `7/9`, `0/9` |
| `bad_stage_correction` | `accept_repaired` | `accept_repaired` | `3/3`, `3/3`, `4/9`, `7/9` | `3/3`, `3/3`, `9/9`, `8/9` |
| `stage_log_missing` | `accept_repaired` | `decline` | `3/3`, `0/3`, `0/9`, `0/9` (C3(a): `0/3`, `3/3`, `9/9`, `0/9`) | `0/3`, `3/3`, `9/9`, `0/9` |
| `second_root` | `decline` | `decline` | `0/3`, `0/3`, `0/9`, `0/9` | `0/3`, `0/3`, `1/9`, `0/9` |
| `fast_rotation` | `decline` | `decline` | `0/3`, `3/3`, `7/9`, `5/9` | `0/3`, `3/3`, `6/9`, `2/9` |
| `flank_swap` | `decline` | `decline` | `0/3`, `3/3`, `7/9`, `4/9` | `0/3`, `3/3`, `9/9`, `2/9` |
| `partial_occlusion` | `decline` | `decline` | `0/3`, `0/3`, `7/9`, `2/9` | `0/3`, `1/3`, `9/9`, `3/9` |

## What was not checked

- Raw `.npz` tracker outputs in `staging/tracks_freeze_v3/` and `staging/tracks_freeze_v4/` were not recomputed because `staging/` is git-ignored and contains `0` `.npz` files in this clone.
- Error values (`error_before`, `error_after`) and truth summaries (`truth`) inside `results/2026-10-23_freeze_v3/runs/*_summary.json` and `results/2026-10-25_freeze_v4/runs/*_summary.json` were taken from the committed run summaries rather than re-integrated from raw `.npz` arrays.
- Label-sweep states in `results/2026-10-23_freeze_v3/labels.md` and `results/2026-10-25_freeze_v4/labels.md` were checked against `labels.json` from the reported per-state tables rather than from `staging/tracks_freeze_v3/` and `staging/tracks_freeze_v4/`.
- Set-aside runs in `results/2026-10-25_freeze_v4/runs/usage_limit/` (`95` summary files) and development-check runs in `results/2026-10-25_freeze_v4/dev_check/` (`17` summary files) were excluded from the scored metrics per `docs/specs/2026-11-03_argon-audit.md` section A2.
