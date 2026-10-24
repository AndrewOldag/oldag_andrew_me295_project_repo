# freeze-v3
Updated: 2026-10-23 22:50 (local)
Lane: course
Branch: wip/freeze-v3
Last inbox item done: 9
State: working
Now: LLM runs (diagnostician, single agent, repeats 0-2; 306 runs, one at a time, CLI 2.1.310 checked per block). Restarted by Andrew (foreground choice). Method-phase tracker runs complete, 488 cached; script and remedy tree done (869f130)
Done since last update:
- Item 7: `v3_bend30_clean_s20` kept accept_clean (option a), recorded in decisions; labels complete: accept_clean 18, accept_repaired 12, decline 21; all-decline 21 of 51
- Item 8: `claude --version` on the VM is 2.1.310 (not 2.1.309). Re-pinned `config/models.yaml` and `tests/test_auditor.py` to 2.1.310; decisions entry; `check_cli.py` OK. Suite 243 passed, 5 skipped
- Tag `freeze-v3` on e1e672a (pushed)
- Labels (6ebc9db), sizing (f599564), basis (433fdcf). Tracker runs used 364 of 600
Needs Andrew:
- none. Note: the CLI updates itself; a version change during the v3 LLM runs stops them (item 8). Setting `DISABLE_AUTOUPDATER=1` in the Claude Code user settings (README setup step 3) would prevent that; I have not changed any settings
