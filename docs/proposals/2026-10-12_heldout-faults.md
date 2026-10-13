# Held-out faults: injectors, sizes and outcomes, for Andrew's approval

From: build account. Date: 2026-10-12. Branch `heldout/faults`; not merged to main before the freeze. Status: proposal. No size here is used in a scored run until Andrew approves it.

## 1. Faults
- Held-out: the fault names in `agents/actions.py` with no injector in `measure/render.py` (`second_root`, `fast_rotation`, `bad_stage_correction`), plus two that are not on the agent's list (`flank_swap`, `partial_occlusion`)
- Injectors: `measure/render_heldout.py`. Same interface as `measure/render.py` (`image_case`, `render`, `build`); `scripts/synth/make_rod.py --fault <name> --size <z>` renders them
- Every injector is on the `growth_zone` rod (tip speed 60 px/h, REGR peak at s = 150 px, root radius 30 px, flank lines at +-15 px, 41 frames 90 s apart, stage steps of 10.5 px at frames 7, 14, 21, 28, 35)
- Second root and drop are fixed to the sample: the rigid motion of the invariance check moves them with the root

| Fault | What the injector does | Size (unit) | What a real root does |
| :-- | :-- | :-- | :-- |
| `second_root` | A second root (same radius and texture statistics, own texture), drawn on top of the main root, grows at 60 px/h along a line at 45 deg to the main root and enters it at s = 150 px during the window | how far its outline ends past the main root's near edge, px; 0 = no second root | a neighbouring or lateral root crosses the root under study |
| `fast_rotation` | Unlogged rotation burst: `size` deg/frame for 3 frames from frame 20, about the frame-0 midline point at s = 200 px (half the tracked length); the midline source turns with the root | deg/frame | plate or sample jolt; tracker fails at about 7 deg/frame (`docs/context/research_background.md`) |
| `bad_stage_correction` | Images as recorded; the stage log under-reports the first stage move from mid-window on (frame 21) by `size` px along the move, and keeps the error after it | px | stage position logged wrong at a move |
| `flank_swap` | The texture is mirrored across the midline for the last `size` fraction of the frame pairs (0.5: frames 21-40), so the two flanks exchange | fraction of the window | root rolls about its own axis; flank tracks exchange |
| `partial_occlusion` | An opaque, featureless drop (level background + half the root brightness) of radius `size` px, centred on the frame-0 midline at s = 150 px, covers the growth zone for frames 13-26 (middle third) | px radius | water drop or debris on the sample over part of the growth zone |

Tests (`tests/test_render_heldout.py`): each injector changes the movie, only in the frames (or log entries) it should; each at size 0 gives `render.render`'s clean output exactly; the second root's outline reaches the main midline at size 30 and stays outside the root at size 1; `make_rod.py --dry-run` names held-out rods.

## 2. Fault name and correct outcome
Expected outcomes; the code copy is `EXPECTED` in `measure/render_heldout.py`. Labels in the sense of `docs/specs/2026-10-10_repair-criteria.md` part C need the remedy sweep at the approved sizes (section 5).

| Fault | Name the agent should give | Correct outcome | Basis |
| :-- | :-- | :-- | :-- |
| `second_root` | `second_root` | decline | the second root covers the growth zone inside the 45 px band that `mask_second_root` and `crop_to_main_root` keep, so neither remedy removes it |
| `fast_rotation` | `fast_rotation` | accept after `register_frames` | the basal band is rigid and in frame; ECC registration removes rigid motion before tracking (repaired `rigid_drift`). Not yet run at 2-4 deg/frame |
| `bad_stage_correction` | `bad_stage_correction` | accept after `register_frames` | registration aligns the world frames on the basal band, which removes a stage-log error. Not yet run |
| `flank_swap` | `unknown` | decline | no listed fault fits; no remedy restores flank identity |
| `partial_occlusion` | `low_texture` | decline | texture lost over part of the growth zone; no remedy recovers covered tissue. `unknown` is a defensible second answer (see open item 3) |

## 3. Sizes: checker only, seeds 0-2
- `python scripts/synth/heldout_sweep.py start`, then `fetch`, `eval --out results/2026-10-12_heldout_faults`. No agent, no remedy
- growth_zone, uncoupled, stride 1, tracker defaults (disk radius 15 px). Each rod tracked as is and rigidly moved. Approved thresholds (rigid_invariance 2.0 %/h, closure 1.0 px/h, plane_sections 3.25 %/h)
- 27 rods, 54 tracker runs, 0 failed. 204 s wall, 4 workers, 4.5 s per run. Load (1 min) 4.30 before, 5.63 max, 4.99 after, on 32 cores. Work space 5.83 -> 6.70 GB. Started after the baselines sweep released the lock (waited 245 s)
- Full table: `results/2026-10-12_heldout_faults/checker_sizes.md`

| Fault | Size | Seeds failing | rigid_invariance (%/h) | closure (px/h) | plane_sections (%/h) | REGR RMS err (%/h) |
| :-- | --: | :-- | :-- | :-- | :-- | :-- |
| `second_root` | 15 | 0 of 3 | 0.58-0.70 | 0.08-0.10 | 1.80-2.37 | 0.41-0.44 |
| `second_root` | 30 | 3 of 3 | 0.58-0.70 | 0.08-0.10 | 9.03-11.33 F | 0.48-0.83 |
| `fast_rotation` | 2 | 3 of 3 | 58.6-124.8 F | 4.76-29.6 F | 31.7-91.8 F | 11.4-23.2 |
| `fast_rotation` | 4 | 3 of 3 | 127.9-352.5 F | 4.40-34.4 F | 191.2-330.8 F | 32.8-60.3 |
| `bad_stage_correction` | 3 | 3 of 3 | 0.58-0.70 | 2.92-2.93 F | 0.37-1.38 | 0.41-0.44 |
| `bad_stage_correction` | 10 | 3 of 3 | 42.2-66.1 F | 5.58-12.2 F | 95.4-251.4 F | 25.2-29.5 |
| `flank_swap` | 0.5 | 3 of 3 | 39.9-51.8 F | 1.42-2.49 F | 83.0-172.6 F | 4.36-6.63 |
| `partial_occlusion` | 20 | 3 of 3 | 42.6-99.2 F | 0.08-0.10 | 5.71-34.5 F | 22.6-32.8 |
| `partial_occlusion` | 30 | 3 of 3 | 117.3-211.2 F | 0.08-0.10 | 111.8-255.1 F | 24.8-46.3 |

- `second_root` 15: the second root reaches the flank line only at the last frame; the checker values equal those of the unaffected rods (rigid_invariance 0.70, 0.58, 0.70; closure 0.10, 0.08, 0.09). Not detected
- `second_root` 30: only plane_sections fails; the centre REGR error stays small (at most 0.83 %/h). The near flank tracks the second root
- `bad_stage_correction` 3: only closure fails, at the injected error (3 px in 1 h = 2.9 px/h); strain rates unaffected. At 10 px (2/3 of the disk radius) the tracker loses the tissue at the jump and every check fails
- `fast_rotation`: every check fails at both sizes, with large errors
- `partial_occlusion`: closure passes (tip and base are not covered); rigid_invariance and plane_sections fail

## 4. Proposed sizes
Rule: the smallest tested size at which the checker fails on 3 of 3 seeds.

| Fault | Proposed size | Reason |
| :-- | :-- | :-- |
| `second_root` | 30 px (outline reaches the main midline) | 15 px fails 0 of 3; 30 fails 3 of 3 (plane_sections 9.0-11.3, threshold 3.25) |
| `fast_rotation` | 2 deg/frame for 3 frames (6 deg in all) | smallest tested; fails all three checks on 3 of 3. 4 deg/frame is closer to the tracker limit (7) and also fails 3 of 3: alternative if "near the tracker limit" should set the size |
| `bad_stage_correction` | 3 px | fails closure on 3 of 3 (2.9 px/h, threshold 1.0); the measurement is otherwise intact, so the fault is the log, not the tracking. 10 px is the alternative if the fault should also corrupt tracking |
| `flank_swap` | 0.5 (swap at frame 21) | only size tested; fails all three checks on 3 of 3 |
| `partial_occlusion` | 20 px radius | fails rigid_invariance and plane_sections on 3 of 3; 30 px covers the full root width |

## 5. Open, for Andrew
1. Approve or change the sizes in section 4 (fast_rotation 2 or 4; bad_stage_correction 3 or 10). No scored run uses them before that
2. Approve the names and outcomes of section 2. Two choices: `partial_occlusion` named `low_texture` or `unknown`; `flank_swap` named `unknown`
3. Labels by the 2026-10-10 rule need a remedy sweep at the approved sizes, no agent: `register_frames` on fast_rotation and bad_stage_correction (accept expected), both `crop_or_mask` settings on second_root, `enlarge_patch` and `change_frame_stride` on partial_occlusion and flank_swap (decline expected). About 15 remedy states x 3 seeds x 2 = 90 tracker runs, under 10 min at the measured rate. Not run
4. The branch `heldout/faults` is on origin (pushed per the routine), so the injectors are readable on GitHub before the freeze. The diagnostician does not read the repository, but development sessions could
5. `second_root` at 30 px leaves the centre REGR error small (at most 0.83 %/h). If decline is the correct outcome, the centre measurement is discarded with it, as with `width_change` before `use_width_free_ratio`
