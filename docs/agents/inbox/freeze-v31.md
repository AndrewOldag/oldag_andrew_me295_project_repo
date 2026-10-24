# Inbox: freeze-v31

1. Read `CLAUDE.md`, `docs/agents/README.md`, `docs/specs/2026-10-24_freeze-v3.1.md`, `results/2026-10-23_freeze_v3/README.md`. Branch `wip/freeze-v31` from `main`. Task `tasks/c014-freeze-v31.md`. First status, push
2. Do the spec in order. Andrew approved v3.1 on 2026-10-24; no further approval is needed unless a stop rule in the spec is met
3. Push status after every sizing sweep, label sweep and LLM block. Ready to merge when done
4. Andrew (delegated to planning for this answer), 2026-10-24 11:55: (a) work space: raise the sweep work-space limit from 10 GB to 16 GB for freeze v3.1 only (`--max-gb 16`); no deletes. Record it in `docs/decisions.md` with the reason (about 6 GB more needed; lab-server disk has terabytes free; sessions may not delete). All other shared-machine limits unchanged. (b) Size steps as you chose (rigid_drift factor steps of 1 from 0.5 to 5.5; bad_stage_correction 1 px from 3 to 8 px): finer steps find the smallest qualifying size. Continue with the next sweep
5. Andrew, 2026-10-24 12:00: work-space limit is 50 GB (`--max-gb 50`), replacing the 16 GB of item 3. Decisions entry on main. Continue
