# Spec audit 2026-10-23: bending-and-tracking

Reviewer 5 of `docs/specs/2026-10-23_spec-audit.md`. Worktree `wip/spec-audit` (origin/main plus audit files). Read-only. One recomputation of the synthetic growth-zone and bend values from `measure/rod.py` (numpy, under 1 s). No agent call, no tracker run, no server access.

No STOP item.

Depth labels in the network are `full_text`, `partial`, `abstract_only`, `metadata_only`. Here `full_text` and `partial` count as evidence. `abstract_only` and `metadata_only` count as leads. No finding below is rated "would change a reported number".

## 1. Findings

### bending-and-tracking-1: Synthetic rods use 2.105 um/px; the stated scale of the real movies is 0.84 um/px. At 0.84 the rods are slower and shorter than reported Arabidopsis roots, and real roots would move 2-6 times further per frame than the clean basis rods
- Ours: `measure/rod.py:153` and `measure/render.py:284` (`pixel_um=2.105`); `measure/rod.py:188` (`V_END` 60 px/h, "126 um/h at 2.105 um/px"); `measure/rod.py:191-192` (growth zone); `measure/render.py:37` (`track_length` 400 px); `docs/context/research_background.md:32` ("Pixel scale 0.84 um/px is nominal"); `manifest/root_manifest.csv` column `step_s` 90.0
- Source: spec Reviewers item 5 (synthetic rods against reported Arabidopsis values); HenryEtAl2024 Reported numbers, trait ranges across RILs (full_text); HenryEtAl2023 Abstract, wild-type averages (full_text); BeemsterBaskin1998 Fig. 2 legend and Table I (full_text)
- Evidence: no entry in `docs/decisions.md` gives a reason for 2.105. It entered with commit 6547010
- Evidence: recomputed from `growth_zone()`. Peak REGR 43.4 %/h at 150 px. Zone where REGR > 20 % of peak (the HenryEtAl2023 definition): 49-251 px, 202 px long. Tip speed 60 px/h = 1.5 px per 90 s frame
- Evidence: at 2.105 um/px: 126 um/h, peak at 316 um, zone 425 um. All three are inside the HenryEtAl2024 RIL ranges (0.08-0.32 mm/h; peak position 0.25-0.57 mm; zone 0.25-0.8 mm)
- Evidence: at 0.84 um/px: 50 um/h, peak at 126 um, zone 170 um. All three are below those ranges
- Evidence: a real root at 0.84 um/px and 90 s per frame moves 2.4-9.5 px per frame at 0.08-0.32 mm/h (HenryEtAl2024), 3.0 at 0.1 mm/h (HenryEtAl2023), and 7.2 at 241 um/h (BeemsterBaskin1998, day 6). Clean basis rods move 1.5 px per frame. The tracker disk radius is 15 px
- Evidence: at 0.84 um/px a reported zone of 0.25-0.8 mm is 300-950 px long, and the BeemsterBaskin1998 day-6 growth zone (1231 um) is 1465 px. The synthetic tracked length is 400 px. Closure assumes the most basal tracked point is not growing (`checker/checks.py:87-96`)
- Severity: would change a design choice
- Frozen item: yes (checker thresholds, approved 2026-10-10, basis: clean rods at 1.5 px/frame; synthetic rod geometry under freeze v2)
- Andrew:

### bending-and-tracking-2: The development `low_texture` fault has texture and focus values inside the range of real windows labelled clean
- Ours: `measure/render.py:71-72` (`low_texture`: contrast 0.03, blur 2 px, noise 40); `config/frame_quality_reference.yaml:8-9` (clean synthetic: texture_contrast median 0.193, lowest 0.155; focus median 0.090, lowest 0.073); `config/frame_quality_reference.yaml:22-23` (real, provisional: texture_contrast median 0.0648, lowest 0.0439; focus median 0.0286, lowest 0.0213); `results/2026-10-12b_scored_v1/dev/diagnostician_low_texture_s1_trace.jsonl` (frame_quality result)
- Source: spec Reviewers item 5 (texture loss in the elongation zone); HenryEtAl2023 Results and Methods as stated, tracking relies on endogenous cell walls and air spaces with no applied markers (full_text); MooreEtAl2013 Methods, replication, blur from lid condensation as a stated failure mode (full_text)
- Evidence: the `low_texture` rod s1 measures texture_contrast 0.0598-0.0599 and focus 0.0351-0.0354 at frames 0 and 20. Both lie above the real clean lowest values, and focus lies above the real clean median
- Evidence: the clean synthetic rods have about 3 times the real clean texture contrast (0.193 against 0.0648)
- Evidence: the real reference is provisional, and its band follows a segmentation ridge, not the real-tracking midline source (`config/frame_quality_reference.yaml:11-18`). Its values may not be comparable with the synthetic values
- Evidence: the checker fails every `low_texture` rod (`config/checker_thresholds.yaml:9`, rigid_invariance >= 152 %/h). Its label is decline (`docs/decisions.md`, 2026-10-10 and 2026-10-11)
- Severity: would change a design choice
- Frozen item: yes (`low_texture` development size, approved 2026-10-11; frame_quality reference, approved 2026-10-12)
- Andrew:

### bending-and-tracking-3: The strongly bent clean rods bend 30 and 45 deg/h. Reported Arabidopsis gravitropic rates are 16-24 deg/h. The flank-difference tolerance takes its basis from the 45 deg/h rod
- Ours: `measure/rod.py:236-237` (`bend_continue` 30 deg/h, `bend_reverse` 45 deg/h, both centred at s = 150 px, sigma 40 px); `measure/rod.py:261` (`bending` bump, 3.4 deg/h recomputed); `config/scoring_tolerance.yaml:12-13` (flank_difference_rms 1.0 %/h, basis "largest clean 0.797 (bend_reverse s0, enlarge_patch 2x)"); `docs/decisions.md` 2026-10-11 (flank-difference tolerance)
- Source: MullenEtAl1998b Reported numbers and Table I, wild type 18 deg/h mean, 22 +- 8 (clockwise, n = 4) and 16 +- 5 (counterclockwise, n = 10), curvature initiated 200-300 um from the tip (full_text); WolvertonEtAl2002 Fig. 6, fitted maximum about 24 deg/h near 90-110 deg stimulus, read from the plot (full_text); MooreEtAl2013 Reported numbers, about 90 deg within 8 h (full_text)
- Evidence: `bend_continue` (30 deg/h) is at the upper end of the MullenEtAl1998b clockwise mean + 1 SD (30). `bend_reverse` (45 deg/h) is about 2 times the WolvertonEtAl2002 maximum. `bending` (3.4 deg/h) is below every reported rate
- Evidence: bend site 150 px = 316 um at 2.105 um/px, sigma 84 um. This matches the 200-300 um initiation site of MullenEtAl1998b. At 0.84 um/px it is 126 um (see bending-and-tracking-1)
- Evidence: no literature value of the material curvature rate (1/(mm h)) was found in the digests read. Peak rates here are 2.48 (`bend_continue`) and 3.72 (`bend_reverse`) per mm per h at 2.105 um/px
- Evidence: a rod that bends faster than biology makes the checks harder, not easier. The tolerance basis is the case where this has an effect: the largest clean flank-difference error comes from the fastest-bending rod. Whether a 16-24 deg/h rod gives a smaller error was not run
- Severity: would change a design choice
- Frozen item: yes (scoring tolerance `flank_difference_rms_pct_per_h` 1.0, approved 2026-10-12)
- Andrew:

### bending-and-tracking-4: The plane-sections check uses the measured flank-track separation, which is half the rendered root diameter. The literature uses the full organ diameter. `research_background.md` says "root width"
- Ours: `checker/checks.py:116-125` (`pred = -_window_mean(f["spacing"] * f["kappa_rate"])`); `measure/record.py:141,165,170` (`spacing` = mean Euclidean distance between paired plus and minus track points over the frame pair); `measure/rod.py:54` (h = 15 px), `measure/rod.py:179` (truth spacing 2h = 30 px); `measure/render.py:161` (rendered root radius R = 2h = 30 px); `docs/proposals/2026-10-12_heldout-faults.md:257` ("root radius 30 px, flank lines at +-15 px"); `docs/context/research_background.md:14` ("Flank difference = root width x material rate of change of curvature")
- Source: BastienEtAl2014 Equations, DC/Dt = (1/2R)(1 - C^2 R^2)(eps_2 - eps_1), R the organ radius, eps_1 and eps_2 the two sides (full_text); ChauvetEtAl2019 Eq. (1), R dC/dt = Delta eps / 2, R the shoot radius assumed uniform (full_text); HartmannEtAl2021 Equations, lower and upper faces, R the organ radius (full_text)
- Evidence: the literature relation is side difference = 2R x DC/Dt with the sides at the organ surface (2R = diameter). The check uses the separation of the tracked flank lines (2h). On the synthetic rods 2h = 30 px = R, half the 60 px diameter
- Evidence: the check is internally consistent: flank strain rates and spacing come from the same tracks. The exact form in `measure/rod.py:10-14` (offset h) matches BastienEtAl2014 with R replaced by h. At the offset used, the largest kappa x h is 0.15 (spec 2026-10-10 part C trial), so the neglected factor is about 2 %. At the surface, kappa x R would be 0.30, about 9 %
- Evidence: `research_background.md:14` says "root width". For the tracks used here this is a factor of 2 too large
- Evidence: the width-free ratio (plus - minus)/(plus + minus) at offset +-h is not the BastienEtAl2014 Delta at the surfaces. For a strain rate linear across the section it is h/R = 0.5 of it. `research_background.md:11` asks for DGCR (ChavarriaKrauser2006, abstract_only) to be reported next to the flank difference. Any comparison with a published Delta, Delta-tilde or DGCR needs the offset stated
- Severity: record only
- Frozen item: no
- Andrew:

### bending-and-tracking-5: No injector changes brightness over time or puts different background behind the root
- Ours: `measure/render.py:168` (`img = background + amplitude * inside * shade * (1 + contrast * tv)`; background, amplitude and contrast constant over frames and along the root); `measure/render_heldout.py:206` (same)
- Source: HenryEtAl2023 Definitions and stated assumptions, constant illumination and a stationary camera are assumed for the D_t I = 0 constraint (full_text); BasuEtAl2007 Reported numbers, correlation search failed more often when the root grew over background that differed from the reference image (full_text)
- Evidence: the image-level injectors are `rigid_drift`, `displacement_exceeds_patch`, `midline_jitter`, `low_texture`, `width_change` (`measure/render.py:22-23`) and `second_root`, `fast_rotation`, `bad_stage_correction`, `flank_swap`, `partial_occlusion` (`measure/render_heldout.py:37`). None changes illumination between frames or varies the background along the root
- Severity: record only
- Frozen item: no
- Andrew:

### bending-and-tracking-6: No injector models out-of-plane growth
- Ours: `measure/rod.py:99-116` (planar rod); `measure/render.py:132-182`
- Source: MullenEtAl1998b Methods as stated, two cameras at right angles to follow circumnutation in 3D (full_text); HenryEtAl2023 System, plates at 80 deg "to promote root growth along the coverslip surface" (full_text)
- Evidence: every rod lies in the image plane. If the root tilts out of the plane, the projected lengths shorten and an apparent strain rate appears. No injector or check targets this. Rigid invariance covers only in-plane rigid motion (`checker/checks.py:56-77`)
- Severity: record only
- Frozen item: no
- Andrew:

### bending-and-tracking-7: Every synthetic rod has a growth field that is steady over the window. The elongation-zone position of real Arabidopsis roots moves within an hour
- Ours: `measure/rod.py:50-51` (`v(s)`, `regr(s)` with no time argument); `measure/rod.py:166-169` (truth broadcast over frame pairs); `checker/checks.py:42-47` (window means)
- Source: BaskinEtAl2020 Results, elongation-zone position saltates by 17 um every 5 min on average, span about 75 um, period about 90 min (full_text); HenryEtAl2024 Reported numbers, quoting Baskin et al. (full_text); BastienEtAl2018 Reported numbers, REGR oscillation period median 2.9 h, wheat coleoptile (full_text)
- Evidence: a 75 um span is 36 px at 2.105 um/px and 89 px at 0.84 um/px. The synthetic growth zone is 202 px long (20 % rule). The checks are linear in the fields and do not assume a steady state. Scoring compares against a time-constant truth, so no scored rod tests a moving zone
- Severity: record only
- Frozen item: no
- Andrew:

### bending-and-tracking-8: The lower frame-rate bound and faults that begin mid-window are not injected
- Ours: `measure/render.py:63-68` (`displacement_exceeds_patch`: stride raised only); `measure/render.py:71-72` (`low_texture` applies to every frame); `agents/actions.py:33` (`change_frame_stride`: half, double)
- Source: HenryEtAl2023 Definitions and stated assumptions, the frame rate must be "slow enough that material expands enough during the interval to be measured, but fast enough that disks do not enter a substantially different region" (full_text); MooreEtAl2013 Methods, blur from lid condensation (full_text)
- Evidence: the "too fast" side of the requirement (too little displacement per frame) has no injector. `change_frame_stride double` exists as a remedy but no fault calls for it
- Evidence: blur from condensation builds up over time. `low_texture` blurs every frame from frame 0. The held-out faults `fast_rotation`, `bad_stage_correction`, `flank_swap` and `partial_occlusion` begin mid-window. No development fault does
- Severity: record only
- Frozen item: no
- Andrew:

### bending-and-tracking-9: No rod has a width that varies along s
- Ours: `measure/rod.py:54-55` (`h(t)`, no s argument); `measure/rod.py:198-209` (`width_change`: varies in time only)
- Source: BasuEtAl2007 Reported numbers, root diameter is smallest near the tip and nearly constant from about 1.5 mm, common bean (full_text). Not shown for Arabidopsis in the digests read
- Evidence: if the width varies along s, tissue moving basally through a taper changes width as it moves (Dh/Dt = v dh/ds). This adds 2 kappa Dh/Dt to the plane-sections residual in a curved region. This is the same term the `width_change` fault injects, but with no change in time at fixed s. No rod tests it
- Severity: record only
- Frozen item: no
- Andrew:

## 2. Failure modes: literature against our injectors and checks

| Failure mode | Literature (key, location, depth) | Our injector or check (file:line) | Covered |
| :-- | :-- | :-- | :-- |
| Frame interval too long for patch motion | HenryEtAl2023, Definitions, frame-rate requirement (full_text); BeemsterBaskin1998, Reported numbers, excess displacement < 20 % of growth zone (full_text) | `measure/render.py:63-68` `displacement_exceeds_patch`; remedy `change_frame_stride` `agents/actions.py:33` | yes |
| Frame interval too short (too little expansion per frame) | HenryEtAl2023, same sentence (full_text) | none | no (finding 8) |
| Patch rotation in bending roots | HenryEtAl2023, Conclusions, rotation term lets the axial velocity be measured while the root bends (full_text) | `measure/rod.py:231-250` `bend_continue`, `bend_reverse` (clean); `measure/render.py:59-62` `rigid_drift` rotation; `measure/render_heldout.py:82-85,176-177` `fast_rotation`; `checker/checks.py:56-77` rigid invariance | yes |
| Texture loss or blur | HenryEtAl2023, Results, endogenous features (full_text); MooreEtAl2013, Methods, condensation blur (full_text) | `measure/render.py:71-72` `low_texture`; `measure/info.py` frame_quality | yes, whole window only; size against real movies in finding 2 |
| Brightness or illumination change over time | HenryEtAl2023, Definitions, constant illumination assumed (full_text) | none (`measure/render.py:168`) | no (finding 5) |
| Background differs where the root grows | BasuEtAl2007, Reported numbers (full_text) | none | no (finding 5) |
| Stage correction error | not found in the digests read; HenryEtAl2023 assumes a stationary camera (full_text) | `measure/render_heldout.py:97-109,218` `bad_stage_correction`; `measure/render.py:59-62` `rigid_drift`; `checker/checks.py:87-113` closure | yes |
| Second root or roots colliding | MooreEtAl2013, Methods, two roots colliding (full_text) | `measure/render_heldout.py:112-145,198-202` `second_root` | yes |
| Occlusion | not found in the digests read | `measure/render_heldout.py:93-94,203-205` `partial_occlusion` | yes |
| Root rolling, flank exchange | not found in the digests read | `measure/render_heldout.py:88-90,193` `flank_swap` | yes |
| Width change in time | BastienEtAl2014, Definitions, cylinder of radius R (full_text); ChauvetEtAl2019, R assumed uniform (full_text) | `measure/rod.py:198-209`, `measure/render.py:73-74` `width_change`; `checker/checks.py:116-134` | yes |
| Width varying along s (taper) | BasuEtAl2007, Reported numbers, bean (full_text) | none | no (finding 9) |
| Out-of-plane growth, 3D circumnutation | MullenEtAl1998b, Methods (full_text); HenryEtAl2023, System (full_text) | none | no (finding 6) |
| Elongation zone moving within the window | BaskinEtAl2020, Results (full_text); BastienEtAl2018, Reported numbers (full_text, coleoptile) | none (`measure/rod.py:50-51`) | no (finding 7) |
| Midline source error | not found as a reported failure in the digests read | `measure/render.py:69-70,189-198` `midline_jitter` | yes |

## 3. Synthetic rods against reported Arabidopsis values

Our values recomputed from `measure/rod.py`; um at 2.105 um/px (`measure/rod.py:153`), with 0.84 um/px (`docs/context/research_background.md:32`) in brackets.

| Quantity | Our range (file:line) | Reported range (key, location, depth) |
| :-- | :-- | :-- |
| Peak REGR | 43.4 %/h (`measure/rod.py:191-192`, `:274`); 86.9 %/h on `displacement_exceeds_patch` 2x6 (`config/scoring_tolerance.yaml:8`) | 23.7 %/h wild-type mean, about 45 %/h example root, 30-50 %/h quoted from other tools (HenryEtAl2023, Abstract and Results, full_text); 32-60 %/h across RILs (HenryEtAl2024, Reported numbers, full_text); about 43 %/h (WolvertonEtAl2002, Fig. 2, read from plot, full_text) |
| Position of peak REGR | 150 px = 316 um [126 um] (`measure/rod.py:192`) | 0.35 mm (HenryEtAl2023, Abstract, full_text); 0.25-0.57 mm (HenryEtAl2024, full_text); about 0.45 mm (WolvertonEtAl2002, Fig. 2, full_text) |
| Growth zone length | 202 px = 425 um [170 um], REGR > 20 % of peak, 49-251 px (`measure/rod.py:191-192`) | 0.52 mm, same 20 % rule (HenryEtAl2023, Abstract, full_text); 0.25-0.8 mm (HenryEtAl2024, full_text); 1231 +- 28 um growth zone, day 6, other definition (BeemsterBaskin1998, Table I, full_text) |
| Velocity at the end of the zone | 60 px/h = 126 um/h [50 um/h]; 120 px/h on 2x6 (`measure/rod.py:188`; `measure/render.py:63-68`) | 0.1 mm/h (HenryEtAl2023, Abstract, full_text); 0.08-0.32 mm/h (HenryEtAl2024, full_text); 241 +- 6 um/h day 6, 445 +- 12 um/h day 10 (BeemsterBaskin1998, Fig. 2 legend, full_text) |
| Bend rate (tip-angle rate) | 3.4 deg/h `bending` (`measure/rod.py:261`); 30 deg/h `bend_continue`, 45 deg/h `bend_reverse` (`measure/rod.py:236-237`) | 18 deg/h mean, 16 +- 5 and 22 +- 8 (MullenEtAl1998b, Table I, full_text); about 24 deg/h maximum (WolvertonEtAl2002, Fig. 6, full_text); about 90 deg in 8 h (MooreEtAl2013, Reported numbers, full_text) |
| Bend site | Gaussian at 150 px = 316 um [126 um], sigma 40 px (`measure/rod.py:239-246`, `:262`) | initiation 200-300 um from the tip (MullenEtAl1998b, Reported numbers, full_text); DEZ about 0.1-0.3 mm (WolvertonEtAl2002, Fig. 2, full_text) |
| Material curvature rate, peak | 2.48 (`bend_continue`), 3.72 (`bend_reverse`) per mm per h at 2.105 um/px (`measure/rod.py:236-237`) | no value found in the digests read |
| Frame interval | 90 s (`measure/rod.py:49`; real `manifest/root_manifest.csv` `step_s`) | 30 s (HenryEtAl2023, System, full_text; HenryEtAl2024, full_text); 2 min (MooreEtAl2013, full_text) |
| Pixel size | 2.105 um/px synthetic; 0.84 um/px real, nominal | 0.7 um/px (HenryEtAl2023, Discussion, full_text) |
| REGR near the tip | about 0 at s = 0 (flexible logistic, `measure/rod.py:26-40`) | about 4 %/h in the apical few hundred um (BeemsterBaskin1998, Reported numbers, full_text); `research_background.md:33` states the same |

## 4. Needs Andrew to check the paper

| Paper key | What to check | Finding |
| :-- | :-- | :-- |
| WolvertonEtAl2002 | Fig. 6 maximum curvature rate (digest value about 24 deg/h, read from the plot) and the Fig. 2 REGR peak and position (about 0.43 /h at 0.45 mm, read from the plot) | 3; table 3 |
| ChauvetEtAl2016 | The digest gives both Delta e-dot = R dC/dt and Delta-tilde = Delta e-dot/(2 E-dot) = (R/E-dot) dC/dt, which together imply a factor 2. Check which side offset R refers to | 4 |
| ChavarriaKrauser2006 (abstract_only) | Definition of DGCR and the width or offset it uses, before DGCR is reported next to the flank difference (`research_background.md:11`) | 4 |
| BastienEtAl2016 (KymoRod, abstract_only) | Which width enters its curvature and differential-growth relation, and the failure modes it reports for complex organ movement | 4; table 2 |

## 5. Checked, no finding
- Start nodes: `ChavarriaKrauser2008` and `Krupar2026` are not in `papers.json`. The nearest keys are ChavarriaKrauser2006, ChavarriaKrauserEtAl2007 and ChavarriaKrauserEtAl2005 (all abstract_only). No `Krupar` key or mention exists in the network
- `method_from` edges at the start nodes: BastienEtAl2018 -> BastienEtAl2016; HenryEtAl2024 -> HenryEtAl2023; HenryEtAl2023 -> LewisEtAl2007, GoodwinStepka1945, SilkErickson1979. None is a tracking failure mode. The network has no `reports_conflict` edge to a start node. The two `reports_conflict` edges in tropism and imaging_tools (BeemsterBaskin1998 -> IshikawaEvans1995, meristem boundary; ChauvetEtAl2016 -> PerbalEtAl2002, dose response) do not bear on bending kinematics or tracking
- None of the cited full_text digests (HenryEtAl2023, HenryEtAl2024, BaskinEtAl2020, BasuEtAl2007, ChauvetEtAl2016, ChauvetEtAl2019, MooreEtAl2013) has an error recorded in the network's blind audit. MullenEtAl1998b, WolvertonEtAl2002, BeemsterBaskin1998, BastienEtAl2014 and HartmannEtAl2021 were not in the audit sample
- Exact flank relation: `measure/rod.py:10-14` and `measure/rod.py:174-176` (truth) match BastienEtAl2014 Eq. (DC/Dt with the (1 - C^2 R^2) factor), with h for R and the kappa dh/dt term added. Sign: plus minus minus = -2h dkappa/dt, as `checker/checks.py:119-121` states
- The curvature rate in the check is material: `measure/record.py:162-166` samples the midline curvature at the tracked material points in each frame. BastienEtAl2014 uses DC/Dt (Modelling, material derivative replaces the partial derivative) (full_text)
- Spacing in the check is measured per frame pair from the tracks, not assumed (`measure/record.py:141,165`). A flank-spacing change is shown to the diagnostician as `flank_spacing_rate_pct_per_h` (`docs/decisions.md` 2026-10-12, P4). Width change routes to `use_width_free_ratio` (`agents/prompts/diagnostician.md:20`)
- The texture is fixed to the material (`measure/render.py:3-5`, `:164-166`), so it stretches with the tissue in the elongation zone, as real endogenous texture does (HenryEtAl2023, Results, full_text)
- Every held-out fault named in `agents/actions.py:18-28` (`second_root`, `fast_rotation`, `bad_stage_correction`) has an injector in `measure/render_heldout.py:37`. `flank_swap` and `partial_occlusion` are injected but have no fault name, and their labels use `unknown` or `low_texture` (`measure/render_heldout.py:41-47`)
- Bending case placement: the `bend_reverse` permanent bend at X = 300 px is basal to the zone (REGR 5 % of peak at 302 px, recomputed), which is consistent with the spec 2026-10-10 part C statement
