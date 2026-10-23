# Spec: spec audit against the specs, the rules and the literature network

From: planning account. Date: 2026-10-23. Status: open. Lane: course. The research-lane half is a separate spec in the tracker repository (planning branch `task-spec-audit`); it is not in this repo.

## Goal
- Check everything built and run so far against (a) the specs and approved proposals, (b) the rules in `CLAUDE.md`, (c) the published literature in the literature network
- Read-only. The audit reports findings. It changes no code, config, threshold, prompt or result
- Findings go to Andrew. He marks each one accepted or rejected. A finding that would change a frozen item needs Andrew and a new freeze version

## Inputs
- This repo at `origin/main`, all `docs/specs/`, `docs/proposals/`, `docs/decisions.md`, `docs/running_log.md`, `docs/reports/`, `results/`, `config/`, `checker/`, `measure/`, `agents/`, `audit/`, `tests/`, `manifest/`
- Unmerged branches: `wip/readme-check`, `status/gate2` (status file only)
- The literature network (1,693 papers). Location in `private/paths.md` under the lab data root, folder `root_kinematics_literature_network`. If `private/paths.md` lacks it, stop and tell Andrew
  - Copy it to a folder on the VM outside every git repo; record that location in `private/paths.md` as `litnet:`. `df` first; the folder is small. Pull with the server limits (nice, bandwidth cap). Never write into the server copy
  - Files: `papers.json` (one record per paper: key, doi, year, cluster, tags, `depth`, takeaway), `edges.json` (typed edges: `equation_from`, `assumption_from`, `method_from`, `data_compared`, `reports_conflict`, `extends`, `cites`), `digests/<Key>.md`, `articles/` (open-access full text), `AUDIT.md`, `METHODS.md`
- `docs/context/literature/paper_digests.md` (26 papers, includes the agent-systems papers)
- Nothing from the network goes into this repo except paper keys, DOIs, short paraphrases and section, figure or equation numbers

## Paper access rule
- Use digests, `articles/` (open-access full text only) and `paper_digests.md`
- Do not open any paper PDF, in `private/papers/` or anywhere else. Several core papers are OUP or Wiley subscription papers; AI use of those is not approved yet. Andrew reads those himself and may add notes later
- Evidence weight by `depth` in `papers.json`: full or partial read is evidence. `metadata_only` (most of the network) is a lead only. A finding rated "would change a reported number" cannot rest on metadata-only digests alone; mark it "needs Andrew to check the paper" and name the paper

## Sessions
| Name | Lane | Branch | Job |
| :-- | :-- | :-- | :-- |
| spec-audit | course | wip/spec-audit | lead; runs the six reviewers below as subagents, merges their output |
| spec-audit-check | course | wip/spec-audit-check | fresh session, starts after spec-audit is ready to merge; verifies findings |

- Reviewer subagents: `.claude/agents/audit-<name>.md`, tools Read, Grep, Glob, and Bash for read-only commands and small recomputations on the VM. No server jobs. No agent (LLM) runs of the pipeline: replay only
- Each reviewer writes `docs/reviews/2026-10-23_spec-audit/<name>.md`

## Reviewers
1. `specs`: spec conformance
   - For every spec in `docs/specs/` and every approved proposal in `docs/proposals/`: list each numbered work item and each "done means" line. For each: met, partial, not met, or changed by decision (cite the `docs/decisions.md` entry)
   - Evidence: file and line, commit hash, or result file. "Met" without evidence is "not shown"
   - Also: tasks on the board in a state that no longer matches the repo (for example c007)
   - Include the five literature-reviewer stages of the 2026-10-16 VM setup spec (items 4-9): state which were done
2. `rules`: the rules in `CLAUDE.md`
   - Run `scripts/hooks/pre_push_check.py` over the full history of `main` and every branch. Report hits by commit and file only; never print a matched pattern
   - Usable windows: every real-movie frame used anywhere (fq-real labelling set, real reference, any test) lies inside `usable_from_h`-`usable_to_h` of an `include` yes root. List any that does not
   - Checker has no LLM calls (grep imports and calls)
   - Model ID and Claude Code version pinned in config and consistent with what the log says was run
   - Remedies used in scored runs all come from the frozen list
   - Held-out separation: from git history, was any prompt, threshold or remedy changed after held-out results were seen without a new freeze? Order of commits with times
   - Server limits: from the log, any run over the worker cap, load rule or one-sweep rule; any server delete, move or rename
3. `numbers`: every number in `docs/reports/2026-10-16_lab-report-1.md`, `docs/context/project_summary.md` and the last 10 log entries
   - Trace each to a result file or commit. Recompute from the result file where it takes under 1 min. Mismatch, or no source: list it
   - Same counts used in different places (root counts, test counts, run counts) agree, or the difference is explained
4. `kinematics`: definitions and reference frames, against the network
   - Start nodes: SilkErickson1979, Silk1984, Erickson and Sax, and papers tagged `REGR/velocity field`, `continuity equation`, `material vs spatial derivative`. Follow `equation_from` and `assumption_from` edges into and out of them
   - Check in `docs/context/research_background.md`, `measure/`, `checker/`, synthetic rod generation: velocity referenced to the tip; REGR as dv/ds; spatial vs material derivatives labelled and not mixed; units; sign of the flank difference; the curvature rate relation, including the kappa·REGR term (material D(kappa)/Dt vs spatial rate)
5. `bending-and-tracking`: bending kinematics and image tracking
   - Start nodes: tags or clusters `tropism`, `imaging_tools`; papers ChavarriaKrauser2008, Bastien2016 (KymoRod), Henry2023 (PatchTrack), Krupar2026, and anything with a `reports_conflict` or `method_from` edge to them
   - Check: the Euler-Bernoulli / plane-sections check (which width enters it, what the literature uses for the flank separation); the injected fault list and the held-out faults against failure modes the literature reports (frame interval vs patch motion, patch rotation in bending roots, texture loss or brightness change in the elongation zone, stage correction, second root, occlusion). List failure modes reported in the literature that no injector or check covers
   - Check synthetic rods against reported Arabidopsis values: REGR peak, zone length, velocity at the end of the zone, bend rates. Give the range used here and the range reported, with sources
6. `evaluation`: the agent evaluation design
   - Sources: `paper_digests.md` (selective classification, ReAct, agent-system papers) and the course guidelines in `docs/context/course/`
   - Check: can an agent score well by declining everything; are abstention precision and recall defined so that they penalise that; are any thresholds or prompts set on rods later scored; baselines given the same information and step limits; repeated-run agreement measured as the summary says
   - Check the course deliverables still required (lab reports 2-4, final) against what exists. List gaps with due dates

## Finding format
```
### <reviewer>-<n>: one line
- Ours: file:line, commit, or result file
- Source: spec item, rule line, or paper key + digest section / figure / equation (+ depth)
- Evidence: what was checked, as measured
- Severity: would change a reported number | would change a design choice | record only
- Frozen item: yes (name it) | no
- Andrew: accepted | rejected | (blank)
```
- A literature finding needs both a paper location and our location. Drop it otherwise
- No editorializing. State what was found

## Output
- `docs/reviews/2026-10-23_spec-audit/<reviewer>.md`, one per reviewer
- `docs/reviews/2026-10-23_spec-audit/SUMMARY.md`: all findings ranked by severity, then by reviewer; a table of spec items with their state; a list "needs Andrew to check the paper"
- Task file `tasks/c008-spec-audit.md` kept current
- Log entry in `docs/running_log_pending/spec-audit.md`

## spec-audit-check (after spec-audit is ready to merge)
- Fresh session. Do not read the reviewer agent files or any reasoning traces; read only the finding files and the sources they cite
- For every finding rated "would change a reported number" or "would change a design choice": reproduce the evidence from the cited locations. Mark confirmed, not reproduced, or wrong location
- Sample 10 "record only" findings at random (seed 0) and do the same
- Check 10 literature citations at random against the digest: paper key, section and claim match
- Output `docs/reviews/2026-10-23_spec-audit/CHECK.md` with counts per reviewer. Do not edit the reviewer files

## Limits
- Read-only on code, config and results. No pipeline agent calls (replay only). No tracker runs
- Lab server: read and copy only, with the shared-machine limits. Never delete, move or rename anything there
- VM disk: `df` before writing more than 5 GB
- Nothing in tracked files names a machine, account, path outside the repo or a person's comments. The pre-push hook applies

## Stop and ask Andrew
- The literature network location is missing
- The pre-push scan finds a hit in history
- A real-movie frame outside a usable window was used in a reported result
- Any step would need a server delete

## Done means
- Six reviewer files and SUMMARY.md on `wip/spec-audit`; status ready to merge
- CHECK.md from spec-audit-check
- Task c008 done; log entries pending for the coordinator
