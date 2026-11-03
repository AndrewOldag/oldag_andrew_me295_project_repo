# Spec: Antigravity (Gemini 4 Argon) as independent auditor

From: planning account. Date: 2026-11-03. Decisions by Andrew 2026-11-03. Lane: course. Session: `argon-audit`, branch `audit/argon`, task c025.

## Roles
- Planning account (Claude): specs, decisions, merges, triage of every Argon finding
- VM Claude sessions: build work and every scored run (model pinned in `config/models.yaml`)
- Argon: audits and bounded side tasks. Reads the repo; writes only to `audit/argon`. Findings change nothing until the planning account accepts them
- Rules: `AGENTS.md`. One Argon task at a time; not while a Claude LLM batch runs (check `docs/agents/status/` for `working` sessions with LLM runs; free VM memory at least 3 GB)

## A1. Second reader of the RAG gold set
- Inputs: `rag/gold.yaml`, `docs/context/literature/rag_corpus.csv`, the corpus zip `rag_corpus_2026-11-02b.zip` on the VM (Downloads; unzip into your clone's `staging/rag_corpus/`, check sha256 against the csv)
- Do not read `results/2026-11-02_rag/` or `staging/rag/` before the review file is written
- For each of the 25 questions:
  - Answerable ones (20): is the gold answer correct and is it stated on the gold page? List every other page in the same paper or another included paper that also states it (key, page, quote of at most 25 words)
  - Out-of-corpus ones (5): is the answer truly absent from all 17 included files? If present, give key, page, quote
  - Is the question clear and answerable from text alone (not only from a figure)?
- Output: `review.md` (findings) and `alt_pages.csv` (`qid, key, page, quote, agrees_with_gold`)
- Not in scope: re-scoring. The planning account decides whether alt pages enter a rescore

## A2. Independent recompute of freeze v4 and the v3-to-v4 split
- Inputs: `docs/proposals/2026-10-23_freeze-v3.md`, `docs/proposals/2026-10-25_freeze-v4-candidate.md`, `docs/decisions.md` (C3 option (a)), labels `results/2026-10-23_freeze_v3/labels.json` and `results/2026-10-25_freeze_v4/labels.json`, run summaries and traces in `results/2026-10-23_freeze_v3/runs/` and `results/2026-10-25_freeze_v4/runs/` (set-aside runs in `runs/usage_limit/` excluded, as in the README)
- Write your own scoring code under `docs/reviews/2026-11-03_argon-v4-recompute/code/` from the definitions in the proposals. Do not read `measure/metrics.py`, `scripts/synth/scored_v3.py` or `scripts/synth/scored_v4.py` until your numbers are written down
- Compute per method: balanced accuracy, accuracy per outcome class, false-accept rate, abstention precision and recall, agreement across repeats; and the split in `results/2026-10-25_freeze_v4/decompose_v3_v4.md` (v3 runs under v3 labels, v3 runs under C3 (a) labels, v4; unchanged rows)
- Then compare with the README tables and `decompose_v3_v4.md`. Output `review.md`: a table of each number, theirs vs yours; for every disagreement, the cause if found (definition, rows included, rounding, bug)

## A3. Synthetic trace audit of freeze v4
- Inputs: diagnostician and single-agent traces in `results/2026-10-25_freeze_v4/runs/`, labels, the prompts in `agents/prompts/` (read only), checker thresholds in `config/checker_thresholds.yaml`
- For each run: given the checker values the agent saw at each step, is the action it took justified by its prompt and the thresholds? Mark: justified, defensible, not justified
- Single agent: for the 66 of 153 runs that hit the step limit, where were the steps spent (repeated actions, invalid actions, remedies)? Is the limit the cause of the low decline accuracy, or would more steps not have helped?
- Output `review.md` with counts per method and outcome class, and one finding per not-justified decision (trace name and step)

## Later (not yet issued)
- Spec-conformance audit of the dispatcher evaluation (c023) when its status says ready to merge
- Audit of the inbox and status history: did each session do what its item asked; does each decision carry a reason

## Limits
- No change to any file outside `docs/reviews/` and your status file
- No LLM calls to other models from scripts; only your own agent session
- AI Use Declaration of Lab report 3 names Antigravity and Gemini 4 Argon and these tasks
