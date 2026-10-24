# Spec audit: kinematics reviewer

Reviewer 4 of `docs/specs/2026-10-23_spec-audit.md`. Read-only. Worked on `origin/main` (c730662) plus the audit files. Code files checked were last changed in c8eeedd (2026-10-13).

- Start nodes: SilkErickson1979, Silk1984, EricksonSax1956, plus 73 papers tagged `continuity equation`, `material vs spatial derivative` or `dREGR = width x curvature rate`, and the `REGR/velocity field` papers. 170 `equation_from` / `assumption_from` edges into or out of this set were read. The ones on curvature, the material derivative and the origin are used below
- Depth: SilkErickson1979, Silk1984 and EricksonSax1956 are `metadata_only`. SilkErickson1978 and ChavarriaKrauser2006 are `abstract_only`. In this review `abstract_only` counts as a lead, not as evidence, as `metadata_only` does. Evidence comes from `full_text` digests: BastienEtAl2014, BastienMeroz2016, BastienEtAl2018, HenryEtAl2023, BeemsterBaskin1998, WolvertonEtAl2002, IshikawaEvans1992, MullenEtAl1998b
- Recomputations: field-level rods from `measure.rod.field_cases()`, tracker fixtures in `tests/fixtures/`. Each run took under 1 min. No tracker runs and no agent calls

## 1. Findings

### kinematics-1: the width-free ratio still contains the width-change term on a curved rod
- Ours: `docs/context/research_background.md:16`; `docs/context/project_summary.md:25`; `docs/decisions.md:48`; `measure/info.py:75-84`; the exact flank formula in `measure/rod.py:10-13`
- Source: BastienEtAl2014 Eq 3, Eq 5, Eq 7, Eq 8 (full_text). Delta = (flank 2 - flank 1)/(flank 1 + flank 2) is derived for a cylinder of constant radius R. It gives the curvature rate only through R: DC/Dt * R ~ E-dot * Delta
- Evidence: from `rod.py:10-13`, plus minus minus = -2 (h Dkappa/Dt + kappa dh/dt) / (1 - kappa^2 h^2). Dividing by the flank sum removes the factor 2h in front of Dkappa/Dt. It does not remove the kappa dh/dt term. Recomputed `measure.info.width_free_ratio` on the field-level `width_change` rod, which has zero curvature rate: the ratio is -0.035 to -0.435 at curvature 1/400 px and -0.017 to -0.214 at 1/800 px, over 12 grid points with flank sum > 5 %/h. Its magnitude is largest near the tip and the base, where the flank sum is small. On `growth_zone` (no width change) the ratio is 0.0. So the docs' statement that the ratio "has no width in it" holds for the factor 2h but not for a changing width. Scoring is not affected: `measure/score.py:79-84` skips the flank term when the ratio is reported
- Severity: would change a design choice
- Frozen item: yes (`use_width_free_ratio` remedy and the `width_change` label, freeze v2)
- Andrew: accepted, handled (freeze v3)

### kinematics-2: DGCR, which needs the kappa·REGR term, is required by the docs and computed nowhere
- Ours: `docs/context/research_background.md:11` ("Report it next to the flank difference"). No DGCR or angle-production rate exists in `measure/`, `checker/`, `audit/` or `agents/` (searched for `dgcr`, `turning`)
- Source: ChavarriaKrauser2006, abstract (abstract_only; lead): DGCR is the spatial derivative of the tropic speed, and dkappa/dt underestimated curvature production. `docs/context/literature/paper_digests.md:138`: DGCR = material curvature rate + curvature x REGR. BastienEtAl2014 Eq 15 (full_text): the change in angle across an element is E-dot (Delta + C R) delta-s / R, so the C·E-dot term appears in the angle per element and not in DC/Dt
- Evidence: kappa·REGR belongs to the angle produced per length per time (DGCR), not to the material curvature rate. `research_background.md` gives no formula for DGCR. Units in the literature are deg/mm/h (`paper_digests.md:29`); the code has no deg/mm/h quantity
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### kinematics-3: the arc-length origin is called both "tip" and "quiescent centre"; the code uses the tracked centre point 0
- Ours: `docs/context/research_background.md:6` ("from the tip (quiescent centre)"); `docs/context/measurement_record.md:35` (`v_mid` "from the tip"); `measure/record.py:138,154-156` (s and v measured from centre-chain index 0); `measure/render.py:201-205` (the seed starts at the frame-0 midline tip)
- Source: HenryEtAl2023, Results sec. 2 reference frame (full_text): the QC is the origin. BeemsterBaskin1998, velocity method (full_text): positions are moved to distance from the QC by subtracting the root-cap length. WolvertonEtAl2002 (full_text) and IshikawaEvans1992 (full_text): positions are given from the tip of the root cap. SilkErickson1978 abstract (abstract_only; lead): the time-derivative term is near zero if the apex is the origin
- Evidence: the cap apex and the QC are different origins, separated by the root-cap length. REGR values do not depend on the origin, because REGR is a derivative. Positions in um do depend on it. The code's origin is the tracked patch seeded at the frame-0 midline tip, not the per-frame midline tip. |centre[:,0] - midline[:,0]| on the tracker fixtures is at most 0.09 px on the clean fixtures (`growth_zone_clean_s0/s1`, `rigid_rotation_clean_s0`, `width_change_s0`, `rigid_drift`) and 4.72 px on `growth_zone_low_texture_z0.03_s0`. Not measured on real roots
- Severity: record only (the course paper reports no positions; any comparison with literature positions needs the origin stated)
- Frozen item: no
- Andrew: accepted, fixed (0469497)

### kinematics-4: the flank sign is fixed by image geometry, not by the per-root record the docs require
- Ours: `docs/context/research_background.md:9` (upper or left flank "set from the per-root record, not from the image"); `measure/record.py:203-213` (`orient_flanks`: plus = +N side at frame 0); `docs/context/measurement_record.md:27`. `manifest/root_manifest.csv` has no flank or orientation column
- Source: BastienEtAl2014 Eq 3 and Fig 2 (full_text): the two sides are named by position (upper side 1, lower side 2) within the bending plane. `paper_digests.md` Mullen1998 entry (repo digest, read in full): upper minus lower
- Evidence: +N = tip-to-base tangent turned +90 deg in (row, col), which is image left for a root growing toward +row. In a mirrored image kappa, plus and minus all change sign together, so the plane-sections check still passes. No check can tell which physical flank is plus. The sign agrees with the curvature sign inside the code (see section 4). Its mapping to the upper or lower flank is not implemented. No real-root flank difference has been reported
- Severity: record only
- Frozen item: no
- Andrew: accepted, no action

### kinematics-5: the docs state the plane-sections relation without a sign and with "root width"; the checker uses minus the tracked flank spacing
- Ours: `docs/context/research_background.md:14-15`; `checker/checks.py:116-134`; `docs/decisions.md:17`; `docs/context/measurement_record.md:28`
- Source: BastienEtAl2014 Eq 3 (full_text): DC/Dt = (1 - C^2 R^2)(eps2 - eps1)/(2R), with R the radius of the organ; BastienMeroz2016 Eq 13 (full_text), the same form
- Evidence: `research_background.md:14` reads "Flank difference = root width x material rate of change of curvature". The checker uses plus minus minus = -(spacing) x Dkappa/Dt, where spacing is the distance between the tracked plus and minus points (`record.py:142,161`). The relation holds for the lines whose strain rates are measured, so the tracked spacing is the consistent choice. It equals the root width only if the flank chains lie on the edges. The decisions entry and the record conventions give the sign; `research_background.md` does not. Which width enters the check is reviewed in full by `bending-and-tracking`
- Severity: record only
- Frozen item: no
- Andrew: accepted, fixed (0469497)

### kinematics-6: "flank spacing grows 40 %/h" is linear growth, not a constant relative rate
- Ours: `measure/rod.py:195-209`; `docs/decisions.md:25`
- Source: spec item 4 (units consistent across code and docs)
- Evidence: h(t) = 15 + 6 t px, with t in h. Over the 1 h window (40 pairs x 90 s) h goes from 15 to 21 px, so dh/dt / h falls from 40 to 28.6 %/h. The stated true residual 2 kappa dh/dt = 3.0 %/h at 1/400 px holds: dh/dt is constant, and the recomputed field-level plane-sections value is 3.01 %/h
- Severity: record only
- Frozen item: yes (the `width_change` fault size, freeze v2); the wording only, not the size
- Andrew: accepted, no action

## 2. Definitions table

| Quantity | Our definition (file:line) | Literature definition (paper key, section/eq, depth) | Agree |
| :-- | :-- | :-- | :-- |
| Arc length s, origin | from the tip, "quiescent centre" (`research_background.md:6`); code: from centre-chain point 0, seeded at the frame-0 midline tip (`record.py:138`, `render.py:201-205`) | from the QC (HenryEtAl2023, Results sec. 2, full_text; BeemsterBaskin1998, methods, full_text); from the cap tip (WolvertonEtAl2002, full_text; IshikawaEvans1992, methods, full_text); from the base (BastienEtAl2014 Eq 1, full_text; shoots) | partly; see kinematics-3 |
| Velocity v | tip-relative; generator ds/dt = v(s) - v(0) (`rod.py:78`); measured as the change in s of each centre point over dt (`record.py:156`) | velocity relative to the tip, from bead positions (IshikawaEvans1992, methods, full_text); v = integral of E-dot from the base (BastienEtAl2018 Eq 3, full_text; BastienMeroz2016 Eq 8, full_text) | yes (the origin differs from Bastien; D/Dt does not depend on the origin) |
| REGR | dv/ds (`research_background.md:8`); code: ln(l1/l0)/dt per chain segment (`record.py:158-160`); generator: analytic dv/ds (`rod.py:35-39`) | slope of velocity against position (IshikawaEvans1992, methods, full_text; BasuEtAl2007, Measurements, full_text); E-dot = relative elongation rate along the axis (BastienEtAl2018 Eq 3, full_text) | yes (log stretch = dv/ds to O(REGR dt) = 0.011 at 43 %/h, 90 s) |
| Units | 1/s in code; x 3.6e5 for %/h (`record.py:16`); curvature rate 1/(px s); checks in %/h and px/h (`checks.py`) | %/h (IshikawaEvans1992, full_text); DGCR deg/mm/h (`paper_digests.md:29`, Chavarria2008 repo digest) | yes (3.6e5 = 3600 x 100 checked) |
| Curvature kappa | dphi/ds, tangent tip to base, phi = atan2(dcol, drow) (`record.py:98-116`, `rod.py:99-105`) | C = dA/ds (BastienEtAl2014 Eq 1, full_text; HartmannEtAl2021, Introduction, full_text) | yes (sign convention our own) |
| Curvature rate in the checker | material Dkappa/Dt: curvature sampled at the tracked points in both frames (`record.py:162-165,172`); no kappa·REGR term (`checks.py:116-125`) | DC/Dt = dC/dt + v dC/ds (BastienEtAl2014 Eq 4, full_text; BastienEtAl2018 Eq 3, full_text; BastienMeroz2016 Eq 7, full_text) | yes |
| Curvature rate in the generator | material: dkappa/dt = c(s(t)) integrated along each material point (`rod.py:6-7,81-86`) | as above | yes |
| Flank difference vs curvature rate | plus - minus = -2(h Dkappa/Dt + kappa dh/dt)/(1 - kappa^2 h^2), exact (`rod.py:10-13`); checker: -(spacing) Dkappa/Dt (`checks.py:119-125`) | DC/Dt = (1 - C^2 R^2)(eps2 - eps1)/(2R) (BastienEtAl2014 Eq 3, full_text); flank REGR difference = 2 x radius x material curvature rate (ChavarriaKrauser2006, abstract_only; repo `paper_digests.md:137`) | yes, for constant h; the dh/dt term is not in the literature form (constant R) |
| kappa·REGR term | not used anywhere | belongs to the angle per element: d(C delta-s)/dt (BastienEtAl2014 Eq 15, full_text); DGCR = Dkappa/Dt + kappa REGR (`paper_digests.md:138`; ChavarriaKrauser2006, abstract_only) | yes for the checker; DGCR missing (kinematics-2) |
| Flank sign | plus = +N side at frame 0, image geometry (`record.py:203-213`); docs: from the per-root record (`research_background.md:9`) | sides named upper and lower within the bending plane (BastienEtAl2014 Eq 3, Fig 2, full_text) | no; see kinematics-4 |
| Width-free ratio | (plus - minus)/(plus + minus) (`info.py:75-84`) | Delta = (eps2 - eps1)/(eps1 + eps2), constant R (BastienEtAl2014 Eq 7, full_text) | the formula agrees; the "width-free" claim does not hold under width change (kinematics-1) |
| Spatial vs material | `research_background.md:10` and `measurement_record.md:39` label the curvature rate as material; REGR is the material segment stretch placed at the mean position | the two descriptions agree only for steady patterns (SilkErickson1979, metadata_only; repo `paper_digests.md:41-45`, Silk1979 targeted read); BastienEtAl2012 drops the comoving term (edge `assumption_from` Silk1984); WolvertonEtAl2002 and MullenEtAl1998b (full_text) use segments at a fixed distance from the tip | yes in our code; literature values from fixed-distance segments are not the same quantity |

## 3. Needs Andrew to check the paper
No finding is rated "would change a reported number". These checks would raise lead-level sources to evidence:
- ChavarriaKrauser2006: check the DGCR definition (Dkappa/Dt + kappa REGR), the sign and the width (2R or the flank spacing) in the flank-difference relation, and whether the curvature conservation equation has a width-change term. Findings kinematics-1, kinematics-2, kinematics-5
- SilkErickson1978: check the form of the equation (it is not rendered in the abstract record), the flank sign (outer minus inner) and the apex as origin. Findings kinematics-3, kinematics-4, kinematics-5
- Silk1984: check the curvature and differential-growth formula that BastienEtAl2014 calls "strictly equivalent", and its use of the material derivative. Finding kinematics-5
- SilkErickson1979 and EricksonSax1956: check the origin and the definition of the velocity (relative to the tip or to the QC). Finding kinematics-3

## 4. Checked, no finding
- The generator's velocity is referenced to the tip: rhs = v(s) - v(0), so the tip node stays at s = 0 (`rod.py:78`); `richards_velocity` gives v(0) = 0 (`rod.py:26-40`)
- Curvature sign and flank side agree: with T = (cos phi, sin phi) and N = (-sin phi, cos phi), dT/ds = kappa N, so the offset line r + nN has length element (1 - kappa n) ds, as in `measurement_record.md:28` and `rod.py:10`. `rigid_moved` is a pure rotation and translation and keeps handedness (`record.py:177-200`)
- The checker uses the material Dkappa/Dt and no kappa·REGR term; the generator does the same. Recomputed max |residual| on the field-level rods: `bending` 0.00, `bend_continue` 0.22, `bend_reverse` 0.12 %/h (these are the ignored 1/(1 - kappa^2 h^2) factor plus discretisation). The same residual with kappa·REGR added: 0.38, 9.59, 4.85 %/h. With the spatial rate at fixed s instead of the material rate: 0.58, 14.75, 18.99 %/h. The present form is the only one of the three that keeps clean bent rods under the 3.25 %/h threshold
- The measured material curvature rate matches the truth on the field-level rods: max |30 x (measured - true)| = 0.03 %/h (`bend_continue`), 0.04 %/h (`bend_reverse`)
- The 1/(1 - kappa^2 h^2) factor in `rod.py` matches BastienEtAl2014 Eq 3 (1 - C^2 R^2) on the other side of the equation. Its size on `bend_continue` at the end of the window: kappa h ~ 0.157, factor 2.5 %, in line with "about 2 %" in `research_background.md:14`
- The numbers in the generator notes were recomputed: `bend_continue` flank difference at the peak 15.67 %/h (stated 15.7); `bend_reverse` 23.5 %/h (23.5); `bending` 1.8 %/h (1.8); `width_change` 3.0 %/h at 1/400 px (3.0); `growth_zone` peak REGR 43.4 %/h ("about 43"); V_END 126 um/h at 2.105 um/px (126)
- Spatial and material quantities are not mixed in one expression: the plane-sections residual compares window means of material quantities on one s grid (`checks.py:124-126`). The truth fields use the same grid and mid-time (`rod.py:161-183`)
- BastienEtAl2014 measures s from the base and we measure it from the tip. D/Dt = d/dt + v d/ds gives the same material derivative in either frame, as long as v and d/dt come from the same frame
- The scoring compares measured and true flank differences with the same definition (`score.py:19-33`)
