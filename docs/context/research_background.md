# Research background

Background for the measurement: quantities, mechanics relations, the tracker and its known limits.

## Quantities
- s: arc length along the root midline, measured from the tracked point seeded at the frame-0 midline tip (centre-chain index 0). This is the tip, not the quiescent centre; the two differ by the root-cap length. REGR does not depend on the origin; positions do
- v_s(s): velocity of tissue along the midline, relative to the tip
- REGR(s) = dv_s/ds: relative elemental growth rate, the local axial strain rate (%/h)
- Flank difference (written dREGR in lab notes): REGR on one flank minus the other. The upper or left flank is set from the per-root record, not from the image
- Curvature rate: rate of change of midline curvature, taken following the tissue (material derivative), not at a fixed distance from the tip
- DGCR: differential growth curvature rate, a published related measure (Chavarria-Krauser 2006). Report it next to the flank difference

## Mechanics relations
- Flank difference (plus minus minus) = -(flank spacing) x material rate of change of curvature, sign as in `docs/context/measurement_record.md`, for constant width and no slip between flanks (Silk and Erickson 1978; Chavarria-Krauser 2006; Bastien 2014). This is Euler-Bernoulli plane-sections kinematics. Bastien 2014 adds a factor (1 - curvature^2 x radius^2), about 2% at realistic bends; ignore it. The flank spacing is the distance between the tracked flank lines; it equals the root width only when those lines lie on the edges
- Flank difference = 2h x d^2 v_s / (ds dw), where w is the coordinate across the width and 2h the flank spacing
- (Flank difference) / (flank sum) has no width in it. Use it when width changes, as under mannitol, which swells the root radially
- Integrated strain rate along the root equals tip velocity. With a moving stage, tip displacement comes independently from the stage log
- Rigid-body motion produces zero strain. Any apparent strain on a non-growing root is measurement error
- A uniform error in the reference frame does not change REGR shape, because REGR is a derivative. A sideways error in the midline does change the flank difference, because it moves tissue between flanks

## Tracker (Quantum Borland v1)
- Patch tracking: disk patches matched frame to frame with an affine Lucas-Kanade warp. This is local subset digital image correlation
- Midline predicted every frame by a neural-network cascade (contour, midline, tip)
- Coupled tracking (`couple=True`): neighbouring patches along the midline are linked; length-changing relative motion is penalised, sideways motion is free
- Two-side tracking splits the root into flanks along the normal and gives the flank difference
- Lagrangian particle worldlines from integrating v(s,t)
- The older uncoupled path (`couple=False`) is a fair stand-in for PatchTrack

## Known numbers and limits
- On synthetic rods, 2 degrees of rotation per frame fails all three checks (`results/2026-10-12_heldout_faults/checker_sizes.md`); no run near 7 degrees per frame. Real roots turn about 0.1 degrees per frame
- Classical midline jittered about 3 px per frame at the origin. The ML midline has not been tested on still roots
- Pixel scale 0.84 um/px is nominal, not calibrated
- The flexible logistic fit (Morris 1992) has one peak and goes to zero at the tip. Real REGR near the tip is about 4 %/h. Flank profiles should come from tracked velocities, not from the difference of two fits
- Temporal stability metric (Shih 2014): per root, SD over time of peak strain rate and of its position. Wild type 3.1 +/- 1.1 %/h and 13 +/- 3 um. The feronia mutant is the published positive control (8-12 %/h, 52-69 um)
