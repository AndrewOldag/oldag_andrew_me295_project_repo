# Project summary

Final summary settled 8 Oct 2026 (running log, 2026-10-08). The text is in `CLAUDE.md`.

## Design
| Part | Type | Job |
| :-- | :-- | :-- |
| Dispatcher | LLM agent | Splits roots into root-by-window tasks, estimates cost, submits jobs |
| Tracker and midline nets | Tools | Stage correction, midline, strain-rate field (Quantum Borland v1) |
| Checker | Deterministic code, no LLM | Rigid-body invariance, tip-displacement closure, Euler-Bernoulli kinematics |
| Diagnostician | LLM agent | Names the fault behind a failed check, picks a remedy from a fixed list, or declines to report |
| Auditor | LLM agent | Reviews the batch, flags outlier roots, compares control with stressed, writes the report with provenance |

- Why several agents: the jobs need different information. The dispatcher sees cost and queue; the diagnostician sees one root; the auditor sees all roots but not the diagnostician's reasoning
- Why an agent at all: an optimizer always returns an answer. The claim is that the agent can name the fault, choose a structurally different remedy, and refuse to report an untrustworthy result. This is tested on held-out faults not used during development

## Fault classes (initial list)
- Rigid drift or rotation not removed: register frames first
- Per-frame displacement above patch radius: change frame stride
- Midline sideways jitter: switch or smooth the midline source
- Second root in frame: crop or mask
- Low texture or blur: enlarge patch, or decline
- Fast rotation (synthetic `fast_rotation`, 2 degrees per frame, fails all three checks): decline
- Bad stage correction: jump in the velocity field at a stage move
- Width change (mannitol swelling) breaking the constant-width assumption: use the width-free ratio; this is a physical cause, not a measurement fault

## Evaluation
- Task unit: one root over one time window
- Truth: synthetic rods with prescribed velocity fields and injected faults; fixed non-growing roots (zero strain)
- Real data: 12-16 root subset for baselines and repeated runs; all roots once, unattended
- Independent check on real movies: integrated strain rate against tip displacement from the stage log
- Hand labelling by Andrew: the .imgdir-to-root manifest, and fault labels on a subset of real windows for diagnosis accuracy
- Metrics: strain-rate error against truth; diagnosis accuracy; false-accept rate; abstention precision and recall; agreement across repeated runs; failure rate, manual minutes and run time per root

## Limits
- Kinematics only. No stress, stiffness or constitutive law
- Real movies have no ground truth for the strain-rate field
- Tip closure constrains the integral of the strain rate, not its shape

## Open items
- Map .imgdir folders to roots and conditions (Andrew labels a draft manifest)
- Time the tracker on one 24 h root
- Decide whether the cluster is needed; if so, check cost
