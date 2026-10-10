# Paper Digests — 5 Oct 2026

Ten papers read from `Papers/` in the first batch. Eleven more in the second batch and three replacements in the third, at the end of this note. All notes are paraphrase. Read depth is stated for each.

## Wrong files
- `Shih2014.pdf` was Shi et al. 2018, a review of calcium-dependent protein kinases. Renamed `Shi2018_CDPK_review_WRONG_PAPER.pdf`. The right paper is Shih, Miller, Dai, Spalding & Monshausen 2014, Curr Biol 24:1887–1892
- `Nolan2023.pdf` was Nolan & Shahan 2023, a Current Opinion review on single-cell genomics. Renamed `NolanShahan2023_review.pdf`. The right paper is Nolan et al. 2023, Science 379:eadf4721, with its supplement
- `PMID37871136.pdf` is Root Walker. Renamed `Platre2024.pdf`

## Mullen1998 — read in full
Mullen, Ishikawa & Evans 1998, Planta 206:598–603.

- Charcoal markers on Col-0 roots, positions every 30 s, velocity over 20 min intervals, flexible logistic fit
- Roots 4–6 d old, 9–14 mm long
- Vertical roots: peak REGR 481 µm from the tip, elongation zone ends near 912 µm, distal elongation zone (DEZ) ends near 248 µm
- After turning to horizontal, measured at 45 min: REGR rises on the upper flank and falls on the lower flank in the DEZ
- Largest upper-minus-lower difference is at 270 ± 50 µm from the tip, and it falls off toward the base
- In the central zone both flanks are inhibited. In its basal part the lower flank can grow faster than the upper, so the sign reverses
- Flank profiles were not measured directly. Markers on the axis were projected onto splines fitted to the upper and lower edges
- Test with marker pairs on opposite flanks: no difference in axial velocity. All flank difference shows up as curvature. No slippage
- Notes that where the root is already bent, the angle changes faster than the REGR difference alone predicts (cites Silk & Erickson 1978)

## Chavarria2008 — read in full
Chavarría-Krauser et al. 2008, New Phytol 177:811–821.

- Optical flow (structure tensor) gives a velocity for every pixel. A hand-drawn midline is tracked through the stack. No markers, no fit function
- 4× objective, 2 frames per minute, field 1.41 × 1.06 mm. The whole set-up is rotated 90°. Same root recorded 3–4 h before and then after
- REGR from the change in length of midline segments. Time-averaged REGR uses only first and last segment length
- DGCR (differential growth curvature rate) = slope of segment turning rate along the root. Degrees per mm per hour. Defined and proved in Chavarría-Krauser 2006
- Fig. 2 maps REGR across the root width as well as along it. Flank asymmetry is shown directly
- WT after the turn: tip velocity drops from about 101 to 55 µm/h. REGR drops 22%. Lowest near 1 h
- Curvature production: 50–150 µm from the QC in the first hour, spreads to 50–300 µm after about 1 h, 200–300 µm by 3–3.5 h
- Two zones: 100–200 µm at about 60°/mm/h and a peak near 260 µm at up to 100°/mm/h. Growth maximum is near 290 µm
- pin3 keeps the apical zone and loses most of the basal one
- WT tip angle 70° at 6 h. Turning rate rises until about 3 h, then falls
- Average SE: REGR 1.6 %/h, DGCR 15°/mm/h
- Before averaging across roots, position is rescaled so each root's growth peak lines up

## Silk1979 — targeted read
Silk & Erickson 1979, J Theor Biol 76:481–501.

- Growth treated as a velocity field. Spatial (fixed position) and material (following tissue) descriptions agree only when the pattern is steady
- Steady patterns appear when the apex is the origin
- Local growth described by the rate-of-strain tensor and the vorticity. Vorticity adds rotation and no growth
- Material derivative = local change plus velocity times spatial gradient
- For curved organs it points to Silk & Erickson 1978, which uses arc length and distance along the radius of curvature as coordinates

## Henry2023 — method read in full
Henry, Miller & Spalding 2023, Int J Mol Sci 24:16475. PatchTrack.

- User clicks 10–12 midline points starting at the QC. Disks are placed every 10 px. Each disk is matched to the next frame with an affine warp (shift, stretch, rotation)
- 30 s frames, 120 frames, about 1,450–1,500 px/mm
- Output CSV is position in px from the QC and velocity in px per frame.
- Flexible logistic with four parameters (Morris & Silk 1992). Elongation zone = where REGR is above 20% of its peak
- WT on their platform: zone 0.52 mm, peak 23.7 %/h, peak at 0.35 mm, elongation 0.1 mm/h
- Says the rotation term lets it follow a patch on a root that bends during the run
- Closest relative is Stripflow

## Bastien2016 — read in full
Bastien et al. 2016, Plant J 88:468–475. KymoRod.

- Every frame: threshold, contour, Voronoi skeleton, longest path = midline
- Rod-PIV: a window on the midline at time t is correlated with windows slid along the midline at t + dt. Displacement is measured along the midline only. REGR is its derivative
- Built to keep working while the organ moves or bends
- Also gives angle, curvature, radius, radial REGR, anisotropy
- Describes a differential growth term: material rate of change of curvature divided by REGR (from Bastien et al. 2014)
- Their images: about 5 µm/px, organ 20 px wide, 16 px window, pictures every 5 min, 20 min step
- Midline end point moves between frames and makes total length unstable. They re-align successive midlines by correlating the radius profile
- Growth zone length = distance from the tip that holds 80% of the elongation
- Demonstrations are on hypocotyls: fluctuations in WT, isoxaben response, fer-4 with more irregular REGR
- Has a scriptable core (`kymorod.app.Analysis`), so it can run without the GUI
- Youssef et al. 2018 (J Exp Bot) used it on roots

## Baskin2020 — main text read
Baskin et al. 2020, iScience 23:101309.

- Stripflow. One 30 s image pair every 5 min for 3 h. Roots grow inside agar
- Tip velocity 5.5–8.3 µm/min (330–500 µm/h). Elongation-zone REGR 34–40 %/h. Meristem to elongation transition near 0.55 mm. Elongation-zone position marker near 0.95 mm. Zone runs past a 1.2 mm field
- The 37 profiles of one root nearly overlap
- PCA on the profiles: first component is over 60% of the variation and tracks the position of the elongation zone
- That position steps back and forth by about 17 µm per 5 min, over a span near 75 µm
- Runs test shows the steps are not random in 28 of 35 roots
- The pattern differed between the two labs
- Shoot removal makes the zone drift toward the tip

## Krupar2026 — strain-rate parts read
Krupař et al. 2026, Nat Plants 12:1334–1343.

- Longitudinal velocity from PIVlab (Thielicke & Sonntag 2021) on brightfield images registered to the tip. Strain rate by Savitzky–Golay derivative
- One-dimensional profile to 1 mm from the tip. Peak near 40 %/h
- aux1: lower peak, wider zone, same elongation. Fusicoccin widens the zone without raising the peak
- Gravistimulation was used for pH, not for strain. No flank strain

## Platre2024 — first half read
Platre et al. 2024, Plant J 117:632–646. Root Walker. Here as a model of a methods-plus-biology paper.

- Order of the paper: chamber and automated microscopes, then software, then validation against people, then auxin dose response, then two inhibitors, then a GWAS of 260 accessions
- Readout is root length over time. No strain profile
- Reports failure rates: 8% of roots lost in 60 min runs, 25% in 12 h runs
- Reports processing time per image
- Normal growth about 3.9 µm/min

## Chaiwanon2015 — BL passages read
Chaiwanon & Wang 2015, Curr Biol 25:1031–1042.

- dwf4 roots grow at about 40% of WT. BL speeds them up at once
- At 100 nM BL, growth starts to fall after about 12 h and is below WT by about 24 h. 0.1 nM rescues
- High BL makes meristem cells elongate early and shrinks the meristem
- BR depletion was by dwf4 or propiconazole (2 µM), not BRZ
- Growth measured by live imaging over 72 h. Whole-root rate, no profile

## Fridman2021 — abstract and method passages read
Fridman et al. 2021, Nat Plants 7:1475–1484.

- 3-D cell geometry with MorphoGraphX. BR changes cell shape and growth direction more than cell volume
- BL-treated roots are thinner. bri1 roots are thicker
- 3-D time-lapse at 3 h intervals for 10–13 h. Rates are start-to-end differences

## NolanShahan2023 review — skimmed
- Mentions the BR single-cell time course in one paragraph. No treatment conditions

# Second batch

Eleven papers, read later on 5 Oct.

## Wrong files, second batch
- All three were replaced with the right papers later the same day. Digests are in the third batch below
- `Chaudhary2025.pdf` was a clinical endocrinology mini-review on inhibin B. Renamed `WRONG_PAPER_saved_as_Chaudhary2025.pdf`. The right paper is Chaudhary et al. 2025, Mol Plant 18:603–618
- `Youssef2018.pdf` was a 2022 Plant Cell paper on Moso bamboo. Renamed `WRONG_PAPER_saved_as_Youssef2018.pdf`. The right paper is Youssef et al. 2018, J Exp Bot 69:5157–5168
- `deBang2020.pdf` was a Tansley review on mineral macronutrients, by a different de Bang. Renamed `WRONG_PAPER_saved_as_deBang2020.pdf`. The right paper is de Bang et al. 2020, Front Plant Sci 11:5, on brassinosteroids and autotropic root straightening. Open access
- `Silk1978.pdf` was added later the same day. Digest at the end of this note

## Chavarria2006 — main text read
Chavarría-Krauser 2006, New Phytol 171:633–641.

- Treats the root as a cylinder with a midline and two flanks. Derives how flank growth and curvature are tied
- Flank REGR difference = 2 × radius × material rate of change of curvature. So ΔREGR = width × material curvature rate
- DGCR = material curvature rate + curvature × REGR. It is the angle produced per length per time
- Says the equivalence of differential REGR and curvature rate was already shown (Silk & Erickson 1978, Silk 1989, Zieschang 1997)
- Argues DGCR is the better measure of curvature production. Says flank REGR profiles are error-prone
- Says the direction of the organ follows gradients in the rate of length change, not gradients in REGR
- Extends to three dimensions with a torsion term
- Asks whether a root has one bending motor or two
- Notes that root radius is not uniform close to the QC

## Bastien2014 — main text read
Bastien, Douady & Moulia 2014, Front Plant Sci 5:136.

- Material curvature rate = (flank REGR difference) / (2 × radius), times a factor (1 − curvature² × radius²)
- Dimensionless differential growth Δ = (flank difference) / (flank sum). Curvature rate × radius ≈ mean REGR × Δ
- Passive orientation drift: tissue that is already curved keeps changing its angle as it grows, with no flank difference
- Fixed curvature: once tissue leaves the growth zone its curvature stays
- Control model: Δ is set by the local angle (gravity sensing) minus a term in the local curvature (straightening)
- Active bending has to exceed curvature × radius to do more than keep up with growth
- Says the Silk 1984 and Chavarría-Krauser 2006 forms agree with this one at small curvature

## Shih2014 — main text read
Shih, Miller, Dai, Spalding & Monshausen 2014, Curr Biol 24:1887–1892.

- feronia (fer) roots grow with large swings in strain rate. Shown by kinematic analysis of time-lapse movies
- Stability metric, per root: standard deviation over time of the peak strain rate, and of where the peak sits
- Peak strain rate SD: WT 3.1 ± 1.1 %/h (n = 24), fer-2 8.3 ± 3.2, fer-4 11.9 ± 6.3
- Peak location SD: WT 13 ± 3 µm, fer-2 69 ± 25, fer-4 52 ± 25
- WT growth 2.37 µm/min, elongation zone 504 µm. fer-2 2.96 µm/min and 803 µm. fer-4 3.76 µm/min and 712 µm
- fer peaks reach 107 %/h. Swings are on a timescale of minutes
- Gravitropic curvature is the same in fer and WT. fer roots skew to the right
- Complemented lines and the1 behave like WT

## Nolan2023 — treatment conditions only
Nolan et al. 2023, Science 379:eadf4721, and supplement.

- Medium: half-strength LS, pH 5.7, 1% sucrose. Stratified 2–4 days. 22 °C, 16 h light
- Grown 7 days on 1 µM BRZ. Then transferred to 100 nM BL, or to fresh 1 µM BRZ as the control. DMSO mock
- Time course after transfer: 0.5, 1, 2, 4, 8 h
- Response is under way at the first time point
- Biology sections not read yet

## Mullen2000 — targeted read
Mullen, Wolverton, Ishikawa & Evans 2000, Plant Physiol 123:665–670.

- A feedback stage keeps the root tip at a set angle, so the stimulus stays constant
- Lag before bending: 10.5 ± 2.4 min with smooth rotation. 19.6 ± 2.6 min when the plate is turned by hand
- Rate of curvature becomes constant within an hour and stays constant while the stimulus is held
- Response follows the sine of the angle between 20° and 120°. About 15° gives half the full response
- Handling can hide the earliest events

## Wolverton2002 — targeted read
Wolverton, Ishikawa & Evans 2002, J Plant Growth Regul 21:102–112. Review.

- Two motors. One in the distal elongation zone (DEZ) starts the bend and does not seem to be set by the auxin asymmetry. One in the central elongation zone is auxin regulated
- DEZ end is defined as the point where REGR reaches 0.3 of the peak rate
- The DEZ share of the response grows as the stimulation angle grows
- Proposes gravity sensing outside the root cap as well

## Miller2007 — root sections read
Miller, Parks & Spalding 2007, Plant J 52:374–381.

- Midline from the outline of the organ in every frame. Curvature along the midline over time. No tracking of tissue
- About 5 µm per pixel, one frame every 2 min for roots
- Arabidopsis after a turn: first curvature detected at about 30 min, about 0.28–0.35 mm from the tip
- Curvature then spreads toward the tip and toward the base. Spread toward the tip is done by about 2 h
- Late in the response the curved region moves away from the tip at the growth rate. Curved tissue stays curved
- Works on two-dimensional projections only

## Basu2007 — targeted read
Basu, Pal, Lynch & Brown 2007, Plant Physiol 145:305–316. KineRoot.

- Graphite particles on the root. User picks 10–15 points. Points are tracked by pattern matching with three search methods
- Root edges by Canny edge detection. Midline = average of the two edges, with pairs chosen perpendicular to the midline
- Tracked points are projected onto the midline. Growth velocity and REGR come from that
- Curvature from the midline. Flank growth ratio is then calculated from curvature and diameter. Flanks are not tracked separately
- Bean basal roots, 5 min frames, 6 h. Upper edge grew 2–4% more than the lower over 6 h and it was detected
- Also run on an Arabidopsis root. Profile matches RootflowRT. REGR is flat and not zero in the first 300 µm
- Growth and curvature in one tool. Needs markers

## Beemster1998 — kinematics parts read
Beemster & Baskin 1998, Plant Physiol 116:1515–1526.

- Col roots at 20 °C, graphite marks, observed about once an hour for 5–6 h
- Elongation rate: 241 µm/h on day 6, 445 µm/h on day 10
- Growth zone: 1.23 mm on day 6, nearly double by day 10. Meristem 0.44 mm on day 6
- Peak strain rate and the shape of the profile do not change with age. Only the length of the zone does
- Strain rate is about 4 %/h in the first few hundred µm. It does not fall to zero at the tip
- Marked roots were picked for the least rotation. Marked roots grew about 10% slower than unmarked ones

## Morris1992 — targeted read
Morris & Silk 1992, Bull Math Biol 54:1069–1081.

- The flexible logistic for velocity against position. Final velocity, a spread parameter and a shape parameter that moves the inflection point
- Gives formulas for REGR, the peak position, the peak value and the length of the growth zone
- The REGR curve from this function has one peak
- Fits poorly where the real profile has a sharp peak followed by a long plateau (their stem example)

## Retzer2019 — bending and treatment parts read
Retzer et al. 2019, Nat Commun 10:5516.

- Used 24-epibrassinolide (eBL), not BL. Medium with 1% sucrose, 22 °C, 16 h light
- Germinated on 1 nM eBL: roots make small bends and turns. Same in the pin2 mutant
- Higher doses: roots drift further from vertical, dose dependent
- Gravitropism assay: 6-day seedlings moved to eBL plates, left overnight in the dark, turned 90°, scanned at 2, 4, 6, 8 h
- eBL roots at 2.5 and 100 nM bend more than controls and overshoot. Many form a hairpin
- BRZ lowers a fast-degrading PIN2 reporter at the membrane. eBL raises it
- Their model: the PIN2 gradient is not needed for bending. It limits the auxin asymmetry
- Molecular sections skimmed only

# Third batch

The three replaced files. All three are now the right papers. Read late on 5 Oct.

## Youssef2018 — methods read in full
Youssef, Bizet, Bastien, Legland, Bogeat-Triboulot & Hummel 2018, J Exp Bot 69:5157–5168.

- Poplar adventitious roots in nutrient solution, infrared time-lapse. Not Arabidopsis
- One image every 6 min for 1 h. 1.6 or 2.6 µm per pixel
- KymoRod v0.11.0. Image smoothing: box filter radius 2. Threshold set by hand for each root
- Frame step for matching: 6 min. Raised to 12 min for slow roots, so the displacement is large enough to measure
- Correlation window 50 px, chosen to stay inside the root. Spatial smoothing 0.3. Strain rate smoothed over 50 points
- Profiles checked by eye. Unreliable ones removed
- Growth zone ends where the strain rate drops below 3 %/h
- Peak strain rate 10–40 %/h across roots. Elongation rate 0.06–1.29 mm/h
- Finding: length of the elongation zone is the best single proxy for growth rate. Strain rate drives short-term changes after a treatment

## deBang2020 — bending parts read
de Bang et al. 2020, Front Plant Sci 11:5.

- Maize roots. Medicago used for actin imaging. No Arabidopsis data
- eBL at 500 nM for 1 h, then turned 90°. Imaged every 15 min for 12 h. Tip angle measured by hand
- eBL roots overshoot vertical: about 110° at 250 min. Correction starts near 300 min, swings back to about 60° at 450 min, settles at 90° by about 600 min
- At 12 h eBL roots and controls are at the same angle
- On a clinostat after a 20 min stimulus, eBL roots keep their curvature. Controls straighten
- Reading: the stronger bending under BR is a loss of straightening, not a stronger gravity response
- eBL changes actin organization, less than latrunculin B does
- Cites Lanza 2012 and Li 2005 for eBL increasing root waving and gravitropism in Arabidopsis
- No kinematics. No position along the root, no flank growth

## Chaudhary2025 — results on growth read, rest skimmed
Chaudhary et al. 2025, Mol Plant 18:603–618. FERONIA and brassinosteroid.

- fer mutants on BL: elongation speeds up faster than in WT, then cells in the elongation zone are damaged and burst, and growth falls
- Model: BR-driven expansion damages the wall, FER senses it and slows expansion. BR signalling also puts more FER at the membrane
- Root growth after transfer: 4 days on 1 µM propiconazole, then moved to 1 µM BL plus propiconazole, or mock plus propiconazole. Followed for 24 h on a vertical imaging system
- Before BL both WT and fer-4 grow at about 40 µm/h
- WT after BL: rate rises slowly to about 270 µm/h near 8 h, then falls
- fer-4 after BL: peak about 290 µm/h at 3 h, then falls
- Cell elongation also measured in a perfusion chip, at 5 min steps. BL is added by changing the medium, with no handling of the root
- Root length against dose: fer slightly longer than WT at 1 and 10 nM BL, shorter at 100 and 1000 nM
- Mannitol at 1% rescues the fer hypocotyl defect on BL
- Nothing on root curling or over-bending in the text

## Silk1978 — read in full
Silk & Erickson 1978, Am J Bot 65:310–319. Added after the third batch.

- Lettuce hypocotyl hook. Epidermal hairs as natural marks. Photographs every 2 h
- Curvature is defined at each point along the organ, not as one angle
- Exact relation: outer REGR minus inner REGR = material rate of change of ln(1 + curvature × width). Curvature is taken at the inner edge
- Material rate = change at a fixed position + growth velocity × gradient of curvature along the organ. The second part is there because tissue moves through the curved region as it grows
- An earlier formula left out the second part and the logarithm. They say that is only acceptable when growth is slow next to bending and curvature × width is under about 0.3
- Assumes no slip between the flanks, no bulging, no twisting. Marks on opposite edges stayed opposite, so the assumption held
- Hook maintained: the shape is steady when measured from the apex. Tissue entering the hook has the outer edge growing faster. Tissue leaving it has the inner edge growing faster and straightens
- Hook opening: the change at a fixed position dominates. The outer edge shrinks during straightening
- Their growth-rate estimates are crude and too low, because the marks are far apart
- States that the relation holds for any elongating organ that bends by bowing, roots included
