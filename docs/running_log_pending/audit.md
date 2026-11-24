## 2026-11-23 (build account, session audit)
- Done: c033 independent audit per spec 2026-11-23_audit, sections 1-7, read-only; `results/2026-11-23_audit/README.md`, `findings.csv`, `s1_rules.md` to `s7_repro.md`, scripts in `scripts/`
- Done: 62 findings: 5 blocker, 12 major, 45 minor. Blockers are wording and counts in Lab reports 2 and 3 (S3-5, S6-2, S6-3, S6-4, S6-9)
- Done: all recomputable tables in integrated run, held-out compound (and supplement), auditor check, registration fix and freeze v4 match their READMEs; spend peak $8.51 of $15; no secrets, no lab-server deletes, no lab-server jobs after 2026-11-04
- Demo: `python results/2026-11-23_audit/scripts/merge_findings.py` (run inside that folder) prints counts by section and severity and rewrites `findings.csv`
- Remaining: Andrew reviews findings; planning account turns accepted ones into fixes
- Bottlenecks: history-level findings S1-1, S1-2, S1-5 need Andrew's decision before the repo goes public
