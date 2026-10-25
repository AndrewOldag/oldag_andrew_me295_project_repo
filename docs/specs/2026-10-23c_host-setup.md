# Spec: second compute host and host assignment

From: planning account. Date: 2026-10-23. Approved by Andrew. Lane: course (setup); serves both lanes. Session `host-setup`, branch `wip/host-setup`, task `c012`.

## Goal
- Add the lab workstation (CPU) as a compute host next to the lab server, so that freeze v3, the dispatcher and the research session do not queue behind one another before the 28 Oct build stop
- No task runs twice: every task has one host; outputs and done markers live in one place

## Hosts
| Host (name used in tracked files) | Role |
| :-- | :-- |
| VM | agents, git, orchestration, light checks. No tracking |
| workstation | CPU tracking: real-movie tracking, scale sweeps, overflow synthetic sweeps |
| lab server | data store and the home of every task's outputs and done markers; synthetic sweeps under its limits |
| cluster | GPU only (midline nets, runner), under the approved cap |

- Machine names, addresses and access: `private/workstation.md` (copy from the private cluster folder on the lab server: `me295/cluster/WORKSTATION.md` under the lab data root) and the private cluster file. Never in tracked files

## Work
1. Copy `WORKSTATION.md` to `private/workstation.md`; read it. Add the ssh config entry it gives. `ssh -o BatchMode=yes <host> hostname`; fail: stop and ask Andrew
2. Survey, recorded in `private/workstation.md` (append) and as counts only in your status: cores, RAM, free disk in the home folder, GPU (if any, model and driver), OS, Python/conda present, whether the tracker code and its environment exist there, whether the upload key reaches the lab server (`ssh -o BatchMode=yes` with that key, `hostname`), DNA drive mounted or not. Check other users' load first
3. Environment: if the tracker environment is missing, build it in the user folder from `envs/qb.yml` (conda or micromamba under the work folder; no sudo). Tracker code: clone the tracker repository branch `gate2-windowed-coupling` into the work folder with the lab server's GitLab route if the workstation has none (copy a `git archive` from the lab server). Record the commit
4. Test job: one synthetic v3 rod (`scripts/synth/` driver, one rod, seed 10) and one real window (the dispatcher's `0708_m12` t3 frames pulled from the lab server). Compare outputs with the lab-server runs: tracks equal to 1e-6 px for the synthetic rod; same checker values for the real window. Record wall time per run against the lab server
5. Task board: add a `host:` line to the task front matter (`tasks/README.md`, `scripts/board.py` shows it; test updated). Values: VM, workstation, lab server, cluster, or a comma list for a task with parts on several hosts. Set it for every open task
6. Proposed assignment, applied by the coordinator after the test passes (inbox items to each session):
   - turn-long (research): tracker runs on the workstation; outputs back to its lab-server work folder
   - dispatcher: scale sweep and closure probes on the workstation; cluster GPU runs as before
   - freeze-v3: stays on the lab server (sweep driver and caches there). If its queue is the bottleneck, the label sweep may move to the workstation only after a test that its cached outputs match
   - Lab-server limit (2 jobs) and workstation limit (2 Claude jobs, half the cores each) are separate
7. Log entry, decisions entry (the host roles and the no-duplicate rule), status ready to merge

## Rules
- Workstation: write only in the work folder named in the private file; the imaging drive is read only; no deletes anywhere; no sudo; nice 19; check other users' load before each job
- Lab server: rules unchanged (no deletes; 2-job limit)
- One task, one host per part; outputs and done markers on the lab server in the task's own folder
- Nothing in tracked files names a machine, address, account or path outside the repo

## Stop and ask Andrew
- Key login fails
- The test job does not reproduce the lab-server outputs
- Another user's work would be slowed (load from others above a quarter of the CPU for more than 30 min)

## Done means
- Survey and test recorded; `host:` field on the board; coordinator has the assignment items; log and decisions entries
