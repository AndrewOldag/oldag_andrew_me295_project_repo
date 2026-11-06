# Review: Batch 2 Audit (`origin/wip/real-calib`, Task A5)

- Auditor: `argon-audit` (Antigravity, Gemini 4 Argon)
- Branch: `audit/argon`
- Date: 2026-11-05
- Task: `docs/agents/inbox/argon-audit.md` item 5; `docs/specs/2026-11-03_argon-audit.md` section A5; `docs/specs/2026-11-04_storage-only-server.md`
- Audited commits: `origin/wip/real-calib` (`24d3539`, merged to `origin/main` at `2394b7d`) against pre-merge `main` (`20d5f51`)
- Audited files:
  - `results/2026-10-25_full_batch_2/README.md`, `summary.json`, `table.md`, `windows.csv`, `cluster_checker_equivalence.json`
  - `results/2026-10-25_full_batch_2/audit/deletes.csv`, `outputs.csv`, `ledger.csv`, `connection.csv`, `reverify.md`
  - `manifest/root_manifest.csv`, `docs/decisions.md`, `environment.yml`
  - `measure/remote_link.py`, `measure/cluster_compute.py`, `measure/hosts.py`, `measure/real_runner.py`, `measure/runner.py`, `scripts/full_batch.py`, `scripts/remote/check_window.py`, `scripts/synth/sweep.py`, `tests/test_remote_link.py`, `tests/test_storage_only.py`

---

## 1. Summary of Audit Checks

- **Deletes (`results/2026-10-25_full_batch_2/audit/deletes.csv`)**:
  - `170` data rows (`lines 2–171`): `90` rows with `kind = staged_root` (`4.3G` to `5.3G`) and `80` rows with `kind = moved_copy` (`369M` to `421M`, two per root across all `40` v2 roots in `lines 52–171`). Every row has `kind` in `{"staged_root", "moved_copy"}` and `root` in the `91` batch-2 roots (`scripts/full_batch.py:85-90`); the `1` un-deleted batch-2 root (`0727_cc7`, where the stage-tracking table was rejected) remains on the cluster (`results/2026-10-25_full_batch_2/README.md:18`, `docs/decisions.md:218`).
  - All `1,060` non-empty track MD5s listed on the `90` `staged_root` rows match the `1,060` `track_md5` values in `results/2026-10-25_full_batch_2/audit/outputs.csv:2-1064` $1$-to-$1$. However, none of the `80` whole-pixel reference and moved track MD5s listed in `checked_md5` on the `80` `moved_copy` rows appear in `outputs.csv` (**Finding `A5-F1`**), and on all `120` v2 rows (`lines 52–171`) the `outputs_verified` timestamp is $6\text{ s}$ to $7\text{ h }48\text{ min }53\text{ s}$ *later* than the `deleted` timestamp (**Finding `A5-F2`**).
- **Outputs (`results/2026-10-25_full_batch_2/audit/outputs.csv`, `reverify.md`, `README.md`, `table.md`, `summary.json`, `windows.csv`)**:
  - `manifest/root_manifest.csv` has `102` `include = yes` roots (`11` in batch 1 `scripts/full_batch.py:29-33`, `91` in batch 2 `scripts/full_batch.py:85-90`). Applying the dispatcher $2.0\text{ h}$ window rule with $1.0\text{ h}$ step (`scripts/full_batch.py:72-82`) to `usable_from_h` and `usable_to_h` produces exactly `1,063` batch-2 windows ($1,189$ total across all $102$ roots minus $126$ in batch 1).
  - `results/2026-10-25_full_batch_2/audit/outputs.csv` has `1,063` data rows (`lines 2–1064`), matching the `1,063` batch-2 windows in set and order: `1,060` rows have `on_lab_server = yes` with a 32-hex `track_md5`, a 32-hex `check_json_md5`, and a `verified` timestamp; `3` rows have `on_lab_server = no` and empty `track_md5` (`0721_m5__w0-2` at `line 530` where tracking failed, and `0727_cc7__w0-2`, `0727_cc7__w2-4` at `lines 698–699` where the root was not tracked; see **Finding `A5-F3`**).
  - Every count in `results/2026-10-25_full_batch_2/README.md:8-20`, `table.md:1-8`, and `summary.json:1-43` matches an independent recomputation from `windows.csv:1-1062` and `manifest/root_manifest.csv:1-162` (`0` discrepancies across all `5` treatments and `all`).
  - `results/2026-10-25_full_batch_2/audit/reverify.md:1-9` agrees with `outputs.csv` and `deletes.csv` on every count (`1,063` windows, `1,060` tracks matched, `1,063` check JSONs matched, `0` different, `0` missing, `170` deletes: `90` staged roots and `80` moved copies).
- **Spend (`results/2026-10-25_full_batch_2/audit/ledger.csv`)**:
  - `95` job rows (`lines 2–96`): `2` tail GPU jobs from batch 1 (`lines 2–3`, `$0.153` actual), `50` v1 per-root GPU jobs (`lines 4–53`, `$3.090` actual), `1` CPU job for Work 4 checker equivalence (`line 54`, `$0.000` actual), `41` v2 per-root GPU jobs (`lines 55–95`, `$2.668` actual), and `1` CPU job for Work 6 v1 re-check (`line 96`, `$0.001` actual).
  - Sum of `worst_case_usd` across all `95` rows is $\$23.682$ ($\$23.010$ across the `93` batch-2 rows in `lines 4–96`). Sum of `actual_usd` across all `95` rows is $\$5.912$ ($\$5.759$ across `lines 4–96`).
  - At every submit (`lines 2–96`), the worst-case projected total `running_total_usd` ranges from $\$1.599$ (`line 2`) to a maximum of $\$7.984$ (`line 95`, job `6265614`), staying below both the $\$12.00$ stop threshold (`measure/cluster_compute.py:18`) and the $\$15.00$ cap (`docs/specs/2026-11-04_storage-only-server.md:27`).
  - Final cumulative actual spend across the project is $\$7.314 - \$0.072 + \$0.001 = \$7.243$ ($\$7.24$ in `results/2026-10-25_full_batch_2/README.md:25` and `docs/decisions.md:217`), under the $\$15.00$ cap. Two equivalence jobs ($\$0.068$ combined) between rows `3` and `4` are reflected in `running_total_usd` but omitted as rows, and `time` mixes UTC and local timestamps (**Finding `A5-F4`**).
- **Rules (code diff `20d5f51..24d3539`)**:
  - Storage-only host refusal is enforced in `measure/hosts.py:30-42`, `measure/real_runner.py:137-148,184-203,216-220,243-307`, and `measure/runner.py:39,195-199`. Under `compute: cluster`, `RealRunner` runs no Python or compute jobs on the storage host.
  - One persistent connection is implemented in `measure/remote_link.py:20-141` (`paramiko==5.1.0` in `environment.yml:20`, `KEEPALIVE_S = 30`, `BACKOFF_S = (10, 30, 60)`, `REPEAT_S = 300`, `MAX_FAILED_RECONNECTS = 3`).
  - All cluster commands and transfers in `Relay` (`measure/remote_link.py:144-166`) route through the storage host over `self.link` rather than opening a direct connection from this machine to the cluster.
  - Three gaps against `docs/specs/2026-11-04_storage-only-server.md` were found in the code diff: `Relay.master_ok()` (`ssh -O check`) is defined at `measure/remote_link.py:150-152` but never called in production code (**Finding `A5-F5`**); `scripts/synth/sweep.py` does not check `refuse_storage_host` when invoked directly and `RemoteRunner.sweep_start()` syncs code before checking the host (**Finding `A5-F6`**); and `scripts/full_batch.py:122-165` still runs the checker locally on this machine and instantiates two separate `RealRunner` (`Link`) objects (**Finding `A5-F7`**).
- **Checker Equivalence Record (`docs/decisions.md:214`, `results/2026-10-25_full_batch_2/cluster_checker_equivalence.json`)**:
  - Recorded in `docs/decisions.md:214` and `results/2026-10-25_full_batch_2/cluster_checker_equivalence.json:1-57` across `5` batch-2 windows (`0708_c4__w0-2`, `0708_m8__w2-4`, `0708_c5__w12-14`, `0714_c4__w16-18`, `0708_c4__w10-12`): `record_equal = true` on all `5` windows and every numeric check difference equals $0.0 \le 10^{-9}$.

---

## 2. Findings

### Finding A5-F1
- **id**: `A5-F1`
- **severity**: `medium`
- **file and line**: `results/2026-10-25_full_batch_2/audit/deletes.csv:52-53,55-56,58-59,61-62,64-65,67-68,70-71,73-74,76-77,79-80,82-83,85-86,88-89,91-92,94-95,97-98,100-101,103-104,106-107,109-110,112-113,115-116,118-119,121-122,124-125,127-128,130-131,133-134,136-137,139-140,142-143,145-146,148-149,151-152,154-155,157-158,160-161,163-164,166-167,169-170` and `results/2026-10-25_full_batch_2/audit/outputs.csv:1-1064`
- **claim**: None of the `80` MD5 hashes recorded in `checked_md5` on the `80` `moved_copy` rows of `deletes.csv` appear in `outputs.csv`. In addition, the `90` `staged_root` rows in `deletes.csv` include `1,060` occurrences of `d41d8cd98f00b204e9800998ecf8427e` (the MD5 of an empty $0$-byte `.npz.ok` marker file) alongside the `1,060` non-empty track `.npz` MD5s, and `d41d8cd98f00b204e9800998ecf8427e` is not recorded in `outputs.csv`.
- **evidence**:
  - `results/2026-10-25_full_batch_2/audit/outputs.csv` has schema `window,on_lab_server,track_md5,check_json_md5,verified` (`line 1`) with `1` row per window (`1,063` rows total). For each `w10-12` window, `outputs.csv` records only the uncropped window track MD5 in `track_md5` and has no columns or rows for the whole-pixel reference track (`_wp_ref`) or whole-pixel shifted track (`_wp_moved`).
  - For example, for `0721_c6`, `deletes.csv:52-53` (`kind = moved_copy`) lists `checked_md5 = 941aba6a67734485ec5939ddc5a5cebc` and `e7ef0679a57ac8b54347131f48301f8b`, while `deletes.csv:54` (`kind = staged_root`) lists `44d241ce5891b67289aa79d4370bdc67` as the second window track MD5; `outputs.csv:607` (`0721_c6__w10-12`) records `track_md5 = 44d241ce5891b67289aa79d4370bdc67` and does not contain `941aba6a67734485ec5939ddc5a5cebc` or `e7ef0679a57ac8b54347131f48301f8b`.
  - Across all `170` rows of `deletes.csv`, `checked_md5` contains `2,200` semicolon-separated tokens (`1,141` unique MD5s): `1,060` non-empty `staged_root` track `.npz` MD5s (all `1,060` present in `outputs.csv`), `1,060` occurrences of `d41d8cd98f00b204e9800998ecf8427e` ($0$-byte `.npz.ok` marker MD5, absent from `outputs.csv`), and `80` `moved_copy` track MD5s (all `80` absent from `outputs.csv`).
- **what would confirm it**: Comparing the set of `checked_md5` tokens on the `80` `kind == "moved_copy"` rows of `results/2026-10-25_full_batch_2/audit/deletes.csv:52-170` against `track_md5` and `check_json_md5` in `results/2026-10-25_full_batch_2/audit/outputs.csv:2-1064`.

### Finding A5-F2
- **id**: `A5-F2`
- **severity**: `medium`
- **file and line**: `results/2026-10-25_full_batch_2/audit/deletes.csv:52-171` and `results/2026-10-25_full_batch_2/audit/outputs.csv:596-1064`
- **claim**: On all `120` v2 rows of `deletes.csv` (`lines 52–171`, covering the `40` finished v2 roots: `80` `moved_copy` rows and `40` `staged_root` rows), the recorded `outputs_verified` timestamp (and the matching `verified` timestamp in `outputs.csv:596-1064`) is later than the `deleted` timestamp rather than before or equal to it. Additionally, `deleted` includes a UTC offset (`-07:00` or `-08:00`) whereas `outputs_verified` and `outputs.csv:verified` omit the timezone offset.
- **evidence**:
  - On the `50` v1 rows (`deletes.csv:2-51`, `2026-10-25` to `2026-10-26`), `outputs_verified` equals `deleted` to the second ($\Delta t = 0\text{ s}$ on all `50` rows).
  - On the `120` v2 rows (`deletes.csv:52-171`, `2026-11-04` to `2026-11-05`), `outputs_verified - deleted` is strictly positive on every row:
    - `lines 52–54` (`0721_c6`): `deleted` is `2026-11-04T19:01:25-08:00`, `19:03:53-08:00`, and `19:06:23-08:00`, while `outputs_verified` is `2026-11-04T19:08:55` ($+450\text{ s}$, $+302\text{ s}$, and $+152\text{ s}$ after `deleted`; rebuilt after the audit helper bug noted in `docs/running_log.md:834`).
    - `lines 55–57` (`0721_m6`): `deleted` is `2026-11-04T19:09:19-08:00`, `19:11:47-08:00`, and `19:14:18-08:00`, while `outputs_verified` is `2026-11-04T19:16:51` ($+452\text{ s}$, $+304\text{ s}$, and $+153\text{ s}$ after `deleted`).
    - `line 112` (`0721_c8` first `moved_copy`): `deleted` is `2026-11-05T00:31:53-08:00`, while `outputs_verified` is `2026-11-05T08:20:46` ($+28,133\text{ s} = 7\text{ h }48\text{ min }53\text{ s}$ after `deleted`, spanning the overnight connection drop recorded in `results/2026-10-25_full_batch_2/audit/connection.csv:6-7` before the second `moved_copy` and `staged_root` of `0721_c8` were deleted at `08:20:33-08:00` and `08:20:40-08:00` on `lines 113–114`).
    - On the remaining `113` v2 rows (`lines 58–111` and `113–171`), `outputs_verified` is $+18\text{ s}$ to $+25\text{ s}$ after the first `moved_copy` delete, $+11\text{ s}$ to $+17\text{ s}$ after the second `moved_copy` delete, and $+6\text{ s}$ to $+8\text{ s}$ after the `staged_root` delete, consistent with the driver stamping `outputs_verified` after the three cluster `rm -rf` commands finished rather than when the pre-delete MD5 check completed.
- **what would confirm it**: Inspecting `deleted` and `outputs_verified` in `results/2026-10-25_full_batch_2/audit/deletes.csv:52-171` alongside `results/2026-10-25_full_batch_2/audit/connection.csv:6-7` and the cluster `DELETED.log` file.

### Finding A5-F3
- **id**: `A5-F3`
- **severity**: `low`
- **file and line**: `results/2026-10-25_full_batch_2/audit/outputs.csv:698-699`, `results/2026-10-25_full_batch_2/audit/reverify.md:5`, `results/2026-10-25_full_batch_2/summary.json:2-3`, and `results/2026-10-25_full_batch_2/windows.csv:1-1062`
- **claim**: For the two windows of `0727_cc7` (`0727_cc7__w0-2` and `0727_cc7__w2-4`), `outputs.csv:698-699` sets `on_lab_server = no` and `verified = ""` (empty) while recording non-empty `check_json_md5` values (`d9ea34375b01228673f126076041aa07` and `9650e31edbc3746f5aa1adae48d60bc9`) that `reverify.md:5` verifies as present on storage (`1063` check JSONs matched), whereas `summary.json:2-3` reports `"files": 1061` and `"not run": 2` and omits both windows from `windows.csv`.
- **evidence**:
  - In `results/2026-10-25_full_batch_2/audit/outputs.csv:698-699`:
    - `0727_cc7__w0-2,no,,d9ea34375b01228673f126076041aa07,`
    - `0727_cc7__w2-4,no,,9650e31edbc3746f5aa1adae48d60bc9,`
  - In `results/2026-10-25_full_batch_2/audit/reverify.md:5`: `"Window check JSONs with a recorded md5: 1063; on storage with matching md5: 1063; different: 0; missing: 0"`.
  - In `results/2026-10-25_full_batch_2/summary.json:2-3`: `"planned": 1063, "files": 1061`, and `results/2026-10-25_full_batch_2/windows.csv` has `1,061` data rows (`0` rows for `0727_cc7`).
- **what would confirm it**: Inspecting the two check JSON files for `0727_cc7__w0-2` and `0727_cc7__w2-4` on the storage host (where `check_window.py` wrote `"status": "failed", "error": "missing track"` after tracking exited on `0727_cc7`) and comparing with the local `staging/full_batch_2_cluster/windows/` directory used to build `windows.csv` and `summary.json`.

### Finding A5-F4
- **id**: `A5-F4`
- **severity**: `low`
- **file and line**: `results/2026-10-25_full_batch_2/audit/ledger.csv:2-4,80-96` and `docs/decisions.md:193,195`
- **claim**: Two cluster equivalence jobs run on `2026-10-25` between `ledger.csv` rows `3` (`5466341`) and `4` (`5470305`) totaling $\$0.068$ in actual spend are included in the cumulative `running_total_usd` column from row `4` onward but are missing as rows in `results/2026-10-25_full_batch_2/audit/ledger.csv`. In addition, the `time` column in `ledger.csv` omits timezone offsets and mixes UTC timestamps with local (`PDT`/`PST`) timestamps.
- **evidence**:
  - At row `3` (`5466341`, `ledger.csv:3`), `running_total_usd = 1.599`, `worst_case_usd = 0.336`, and `actual_usd = 0.037`, so cumulative actual spend after row `3` finished was $\$1.599 - \$0.336 + \$0.037 = \$1.300$ (or $\$1.416$ when including row `2`'s `actual_usd = 0.116`, matching `results/2026-10-25_full_batch_1/README.md:20` which reports $\$1.417$).
  - At row `4` (`5470305`, `ledger.csv:4`), `running_total_usd = 1.736` and `worst_case_usd = 0.252`, so cumulative actual spend prior to row `4` was $\$1.736 - \$0.252 = \$1.484$, a difference of $\$1.484 - \$1.416 = \$0.068$ accounted for by the two `0708_c2` equivalence jobs in `docs/decisions.md:193,195`. From row `4` through row `96`, the ledger is continuous: $\$1.484 + \sum_{i=4}^{95} \text{actual\_usd}_i = \$1.484 + \$5.758 = \$7.242 = \$7.314 - \$0.072$ (`line 96`).
  - In the `time` column of `ledger.csv`, row `3` is `2026-10-26T01:32:37` (UTC) while row `4` is `2026-10-25T20:49:30` (PDT); similarly, rows `80–83` (`2026-11-05T15:52:47` to `16:37:03` UTC) and `90–92` (`2026-11-05T17:38:48` to `18:09:58` UTC) are in UTC while rows `84–89` (`09:03:01` to `10:10:09` PST) and `93–96` (`10:10:15` to `11:02:13` PST) are in local time.
- **what would confirm it**: Checking `sacct` job records between job `5466341` and job `5470305` for the two `0708_c2` equivalence jobs and comparing the job submission scripts that wrote UTC vs local timestamps into `ledger.csv`.

### Finding A5-F5
- **id**: `A5-F5`
- **severity**: `medium`
- **file and line**: `measure/remote_link.py:150-166`, `measure/cluster_compute.py:26-122`, and `measure/real_runner.py:140-308`
- **claim**: `Relay.master_ok()` (`ssh -O check <cluster_alias>`) is defined in `measure/remote_link.py:150-152` and tested in `tests/test_remote_link.py:152`, but is never called by `Relay`, `ClusterCompute`, `RealRunner`, or `scripts/full_batch.py`. Furthermore, `Relay.run`, `Relay.push`, and `Relay.pull` (`measure/remote_link.py:154-165`) invoke `ssh -o BatchMode=yes` without `-o ControlPath=...` or `-o ControlMaster=no`, so code does not enforce the `ssh -O check` gate required by `docs/specs/2026-11-04_storage-only-server.md:15`.
- **evidence**:
  - `docs/specs/2026-11-04_storage-only-server.md:15` states: `"Before each batch step: ssh -O check <cluster alias> on the lab server; fails: stop, State: waiting on Andrew"`.
  - Searching the repository for `master_ok` returns only two lines: `measure/remote_link.py:150` (`def master_ok(self):`) and `tests/test_remote_link.py:152` (`assert r.master_ok()`).
  - In `measure/remote_link.py:154-165`, `Relay.run` executes `f"ssh -o BatchMode=yes {q(self.cluster_alias)} {q(cmd)}"`, and `Relay.push` / `Relay.pull` execute `rsync -a --partial -e 'ssh -o BatchMode=yes' ...` without calling `self.master_ok()` first.
- **what would confirm it**: Running `git grep -n "master_ok"` across the repository and reading `measure/remote_link.py:144-166` and `measure/cluster_compute.py:26-122`.

### Finding A5-F6
- **id**: `A5-F6`
- **severity**: `low`
- **file and line**: `scripts/synth/sweep.py:273-315` and `measure/runner.py:171-186,195-199,235-238`
- **claim**: `scripts/synth/sweep.py` was not modified to call `refuse_storage_host` if invoked directly, and `RemoteRunner.sweep_start()` in `measure/runner.py:235-238` calls `self.sync_code()` (which executes `mkdir -p` and `tar xkf -` on `self.host` over SSH) before `self.sweep_status()` triggers `RemoteRunner._py()`'s `refuse_storage_host` check.
- **evidence**:
  - `docs/specs/2026-11-04_storage-only-server.md:39` (Work 3 bullet 3) requires: `"scripts/synth/sweep.py and any lab-server runner path refuse to start a job on the lab server (clear error)"`.
  - `git diff 20d5f51..24d3539 -- scripts/synth/sweep.py` is empty (`0` lines changed in `scripts/synth/sweep.py`).
  - In `measure/runner.py:235-238`, `sweep_start()` runs `self.sync_code()` at `line 237` before `st = self.sweep_status(manifest, out_dir)` at `line 238`. `sync_code()` (`lines 171-186`) runs `self._ssh(f"mkdir -p {shlex.quote(self.code)}")` (`line 175`) and pipes `tar xkf -` over SSH (`line 183`) without calling `refuse_storage_host(self.host, ...)`; the `StorageOnlyHost` exception is only raised afterward at `line 238` $\to$ `line 221` $\to$ `line 196` (`_py`).
- **what would confirm it**: Reading `measure/runner.py:171-240` and `scripts/synth/sweep.py:273-315`.

### Finding A5-F7
- **id**: `A5-F7`
- **severity**: `low`
- **file and line**: `scripts/full_batch.py:122-165` and `measure/real_runner.py:134-144`
- **claim**: `scripts/full_batch.py` `run()` (`lines 122–165`) was not updated to run `scripts/remote/check_window.py` inside the per-root cluster job or to share a single `Link` instance across its two `RealRunner` instances (`plain` and `moved`).
- **evidence**:
  - `docs/specs/2026-11-04_storage-only-server.md:38` (Work 3 bullet 2) specifies: `"Checker step of the batch-2 driver and of scripts/full_batch.py: runs inside the per-root cluster job (CPU) after tracking; writes the check JSON next to the tracks"`.
  - In `scripts/full_batch.py:152-155`, `run()` still calls `m = r.measure_window(root, w0, w1, moved_copy=do_moved)` (`line 152`, which in `measure/real_runner.py:306,401` downloads the `.npz` tracks to this machine) and runs `rec = window_record(root, w0, w1, do_moved, m, th)` (`line 154`) locally on this machine rather than invoking `scripts/remote/check_window.py` on the cluster.
  - In `scripts/full_batch.py:123-124`, `plain = RealRunner(a.config, moved_copy=False, ...)` and `moved = RealRunner(a.config, moved_copy=True, ...)` are constructed without passing a shared `link=` parameter; in `measure/real_runner.py:144`, `self.link = link or Link(self.host)` therefore opens two `Link` connections when `scripts/full_batch.py run` is called with `compute: cluster`.
- **what would confirm it**: Reading `scripts/full_batch.py:122-165` and `measure/real_runner.py:134-148,289-307`.

---

## 3. Detailed Audit Results by Requirement

### 3.1 Deletes (`results/2026-10-25_full_batch_2/audit/deletes.csv`)

| Check | Result | Source |
|---|---|---|
| Total data rows in `deletes.csv` | $170$ (`lines 2–171`) | `results/2026-10-25_full_batch_2/audit/deletes.csv:2-171` |
| Allowed `kind` values (`staged_root` or `moved_copy` only) | $90$ `staged_root`, $80$ `moved_copy`, $0$ other | `results/2026-10-25_full_batch_2/audit/deletes.csv:2-171` |
| Distinct roots in `deletes.csv` | $90$ (all in the $91$ batch-2 roots; only `0727_cc7` not deleted) | `results/2026-10-25_full_batch_2/audit/deletes.csv:2-171`, `README.md:18` |
| `staged_root` rows (`lines 2–51` v1: $50$; `lines 54, 57, ..., 171` v2: $40$) | $90$ rows ($1$ per deleted root; sizes $4.3\text{G}\text{–}5.3\text{G}$) | `results/2026-10-25_full_batch_2/audit/deletes.csv:2-171` |
| `moved_copy` rows (`lines 52–53, 55–56, ..., 169–170` v2: $2$ per root $\times 40$ roots) | $80$ rows (sizes $369\text{M}\text{–}421\text{M}$) | `results/2026-10-25_full_batch_2/audit/deletes.csv:52-170` |
| Non-empty `staged_root` track `.npz` MD5s in `checked_md5` vs `outputs.csv:track_md5` | $1,060 / 1,060$ present in `outputs.csv` ($0$ missing) | `deletes.csv:2-171`, `outputs.csv:2-1064` |
| `moved_copy` track MD5s in `checked_md5` vs `outputs.csv` | $0 / 80$ present in `outputs.csv` (**Finding `A5-F1`**) | `deletes.csv:52-170`, `outputs.csv:2-1064` |
| `outputs_verified <= deleted` timestamp ordering | $50 / 50$ v1 rows (`lines 2–51`: $\Delta t = 0\text{ s}$); $0 / 120$ v2 rows (`lines 52–171`: $\Delta t \in [+6\text{ s}, +28,133\text{ s}]$; **Finding `A5-F2`**) | `results/2026-10-25_full_batch_2/audit/deletes.csv:2-171` |

### 3.2 Outputs (`outputs.csv`, `reverify.md`, `README.md`, `table.md`, `summary.json`, `windows.csv`)

- **Manifest usability and window counts (`manifest/root_manifest.csv:1-162`, `scripts/full_batch.py:29-33,72-90`)**:
  - `manifest/root_manifest.csv` contains `161` roots: `102` with `include = yes` and `59` with `include = no`.
  - Excluding the `11` batch-1 roots (`scripts/full_batch.py:29-33`, $126$ windows) leaves `91` batch-2 roots with $1,063$ usable $2.0\text{ h}$ windows stepped by $1.0\text{ h}$ within `[usable_from_h, usable_to_h]`.
  - Every one of the $1,063$ usable batch-2 windows has a row in `results/2026-10-25_full_batch_2/audit/outputs.csv:2-1064` ($0$ missing, $0$ extra, $0$ duplicates).
- **Per-treatment and total counts (`results/2026-10-25_full_batch_2/README.md:8-20`, `table.md:1-8`, `summary.json:1-43`, `windows.csv:1-1062`)**:

| Treatment | Roots (`manifest/root_manifest.csv`) | Windows (`outputs.csv` / `README.md`) | Accept (`windows.csv` = `README.md`) | Decline (`windows.csv` = `README.md`) | Not Computable in Decline (`windows.csv` = `README.md`) | Failed (`windows.csv` = `README.md`) | Not Run (`README.md`) | Moved Copies Measured (`windows.csv` = `README.md`) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `control` | $31$ | $369$ | $328$ | $28$ | $3$ | $13$ | $0$ | $31$ |
| `control then control` | $5$ | $49$ | $37$ | $6$ | $0$ | $4$ | $2$ | $4$ |
| `mannitol` | $26$ | $309$ | $261$ | $37$ | $11$ | $11$ | $0$ | $21$ |
| `mannitol then control` | $24$ | $276$ | $250$ | $22$ | $2$ | $4$ | $0$ | $24$ |
| `mannitol then mannitol` | $5$ | $60$ | $49$ | $9$ | $2$ | $2$ | $0$ | $5$ |
| **`all`** | **$91$** | **$1,063$** | **$925$** | **$102$** | **$18$** | **$34$** | **$2$** | **$85$** |

- **Additional summary checks (`results/2026-10-25_full_batch_2/README.md:16-20`, `summary.json:3-7`, `reverify.md:1-9`)**:
  - `moved_copy = True` in `windows.csv`: $87$ windows total, of which $85$ have `status = measured` (matching `moved_copies = 85` in `summary.json:6` and `README.md:14`) and $2$ (`0714_m4__w10-12` at `windows.csv:202` and `0721_m12__w10-12` at `windows.csv:852`) have `status = failed` (`logistic fitting`).
  - `flag_base_may_be_in_growing_tissue = True` (`frame0_midline_px < 1000.0`): $33$ windows in `windows.csv`, matching `summary.json:7` (`33`) and `README.md:20` (`33`).
  - Failed windows (`status = failed`): $34$ windows in `windows.csv` ($33$ at `1000 px` crop where `frame0_midline_px < 1000.0`, plus $1$ tracker failure on `0721_m5__w0-2` at `windows.csv:530` with `frame0_midline_px = 1495.56`), matching `summary.json:41` (`34`) and `README.md:16-17`.
  - `reverify.md:1-9` matches `outputs.csv:2-1064` and `deletes.csv:2-171` on every number: `1,063` windows, `1,060` tracks recorded and matched (`0` different, `0` missing), `1,063` check JSONs recorded and matched (`0` different, `0` missing), and `170` deletes (`90` staged roots, `80` moved copies).

### 3.3 Spend (`results/2026-10-25_full_batch_2/audit/ledger.csv`)

- **Rate formula (`measure/cluster_compute.py:13-17,30-32`)**:
  - CPU core-hour $= \$0.012$ (`1` SU), GPU-hour $= \$0.120$ (`10` SUs). For `gpu-shared` jobs (`1` GPU, `4` CPUs), rate $= 4 \times \$0.012 + 1 \times \$0.120 = \$0.168/\text{h}$, giving `worst_case_usd` $= \$0.336$ for `02:00:00` (`lines 2–3`) and $\$0.252$ for `01:30:00` (`lines 4–53, 55–95`). Every row's `worst_case_usd` and `actual_usd` (`lines 2–96`) matches the rate formula to within $\$0.001$ ($0$ discrepancies).
- **Breakdown of `ledger.csv` (`lines 2–96`)**:

| Row Range (`ledger.csv`) | Jobs | Partition & Resources | Sum of `worst_case_usd` | Sum of `actual_usd` | Max `running_total_usd` at Submit |
|---|---:|---|---:|---:|---:|
| `lines 2–3` (`5466204`–`5466341`, batch 1 tail) | $2$ | `gpu-shared`, $1$ GPU, $4$ CPUs, `02:00:00` | $\$0.672$ | $\$0.153$ | $\$1.636$ |
| *(unlisted between `lines 3` and `4`: `0708_c2` equivalence)* | *(2)* | *(`docs/decisions.md:193,195`; **Finding `A5-F4`**)* | — | *($\$0.068$)* | — |
| `lines 4–53` (`5470305`–`5506752`, batch 2 v1 roots 1–50) | $50$ | `gpu-shared`, $1$ GPU, $4$ CPUs, `01:30:00` | $\$12.600$ | $\$3.090$ | $\$5.061$ |
| `line 54` (`6231808`, Work 4 checker equivalence) | $1$ | `expansion`, $0$ GPU, $1$ CPU, `00:30:00` | $\$0.006$ | $\$0.000$ | $\$4.580$ |
| `lines 55–95` (`6232861`–`6265614`, batch 2 v2 roots 51–91) | $41$ | `gpu-shared`, $1$ GPU, $4$ CPUs, `01:30:00` | $\$10.332$ | $\$2.668$ | $\$7.984$ |
| `line 96` (`6267071`, Work 6 v1 checker re-run) | $1$ | `expansion`, $0$ GPU, $4$ CPUs, `01:30:00` | $\$0.072$ | $\$0.001$ | $\$7.314$ |
| **Total (`lines 2–96` in `ledger.csv`)** | **$95$** | — | **$\$23.682$** | **$\$5.912$** | **$\$7.984$** |
| **Batch-2 rows (`lines 4–96` in `ledger.csv`)** | **$93$** | — | **$\$23.010$** | **$\$5.759$** | **$\$7.984$** |

- **Cap verification**:
  - Worst-case projected total at submit (`running_total_usd`) peaks at $\$7.984$ (`ledger.csv:95`, job `6265614`), which is $\le \$12.00$ (`STOP_USD = 12.0` in `measure/cluster_compute.py:18`) and $\le \$15.00$ (`CAP_USD = 15.0` in `measure/cluster_compute.py:19`, `docs/specs/2026-11-04_storage-only-server.md:27`).
  - Final cumulative actual spend is $\$1.484 + \$3.090 + \$0.000 + \$2.668 + \$0.001 = \$7.243 < \$15.00$ (`results/2026-10-25_full_batch_2/README.md:25`, `docs/decisions.md:217`).

### 3.4 Rules (`origin/wip/real-calib` Code Diff Against Pre-Merge `main`, `20d5f51..24d3539`)

- **No Python or jobs on the storage host**:
  - `measure/hosts.py:30-42`: `storage_only_hosts()` reads host aliases from the local storage-only list (`measure/hosts.py:14`), and `refuse_storage_host(host, what)` raises `StorageOnlyHost` (`measure/hosts.py:25-27,39-42`).
  - `measure/real_runner.py:137-148`: When `compute: cluster` is set (`cfg.get("compute") not in (None, "cluster")` raises `ValueError` at `line 139`), `RealRunner.__init__` sets `self.host = cfg["storage_host"]` (`line 141`) and routes compute to `ClusterCompute` (` lines 146–147`).
  - `measure/real_runner.py:184-195`: In `cluster_mode`, `sync_code()` streams the code tarball directly to `self.code` on the cluster via `self.relay.run(...)` (`line 194`), writing nothing to the storage host.
  - `measure/real_runner.py:198-203,216-220`: In `cluster_mode`, `host_state()` calls `self.cc.own_jobs()` (`squeue` on the cluster) and `check_host()` returns `{"load1": None, "free_gb": None}` without running any command on the storage host. When `cluster_mode` is `False`, `check_host()` calls `refuse_storage_host(self.host, "a tracker or midline run")` at `line 220`.
  - `measure/real_runner.py:243-307` and `measure/cluster_compute.py:35-122`: Under `cluster_mode`, `_cluster_midline` (`lines 243–270`), `_cluster_moved` (`lines 272–287`), and `_cluster_track` (`lines 289–307`) run all segmentation, net midline, moved-copy creation, and tracking inside Slurm jobs on the cluster (`self.cc.run(...)`, `measure/cluster_compute.py:35-76`). The only commands executed on the storage host (`self.link.run`) are `test -f`, `ls`, `du -sm`, `mkdir -p`, `rsync`, `cat`, and `find ... | xargs md5sum` (`measure/real_runner.py:251,305`, `measure/cluster_compute.py:85-122`).
  - `measure/runner.py:39,195-199`: `RemoteRunner._py(script, args)` calls `refuse_storage_host(self.host, f"{script}")` at `line 196` before building any remote Python command (see **Finding `A5-F6`** for `sweep_start`'s `sync_code` call prior to `_py` and direct invocation of `scripts/synth/sweep.py`).
- **One persistent connection**:
  - `environment.yml:20`: Pins `paramiko==5.1.0`.
  - `measure/remote_link.py:20-23,36-141`: `_paramiko_connect(host)` opens a single `paramiko.SSHClient` with `transport.set_keepalive(KEEPALIVE_S)` (`KEEPALIVE_S = 30`, `lines 23,51`). `Link` executes every command by opening a channel (`self._client.get_transport().open_session()`, `line 108`) on that single transport, logs connect/drop/reconnect events with ISO timestamps (`lines 68–72`), backs off on drop by `BACKOFF_S = (10, 30, 60)` then `REPEAT_S = 300` (`lines 20–21,78–94`), and stops after `MAX_FAILED_RECONNECTS = 3` failed reconnect attempts (`lines 22,90–91,101–102`).
  - `results/2026-10-25_full_batch_2/audit/connection.csv:1-7`: Logs `5` `persistent connection,connected` events (`2026-11-04T18:07:08`, `18:17:42`, `19:22:01`, `22:59:14`, `2026-11-05T08:20:09`) and `1` driver error (`2026-11-05T08:17:04,driver,error: CommandFailed: remote command failed (-1)`). (See **Finding `A5-F7`** regarding `scripts/full_batch.py:123-124` if `full_batch.py run` is invoked.)
- **No new cluster login path**:
  - `measure/remote_link.py:144-166`: `Relay` takes a `Link` to the storage host (`self.link`) and a `cluster_alias` (`lines 147–148`), running all cluster commands (`Relay.run`, `lines 154–155`) and `rsync` transfers (`Relay.push`, `lines 157–160`; `Relay.pull`, `lines 162–165`) from the storage host over `self.link.run(...)`. No code in the diff opens a direct connection from this machine to the cluster. (See **Finding `A5-F5`** regarding `Relay.master_ok()` not being called before batch steps.)

### 3.5 Checker Equivalence Record in Decisions (`docs/decisions.md:214`, `cluster_checker_equivalence.json`)

- **Decision entry (`docs/decisions.md:214`)**:
  - Records the `2026-11-04` equivalence check of `scripts/remote/check_window.py` (`python 3.10.12`, `numpy 2.2.6`, `1` CPU task in Slurm job `6231808`, `results/2026-10-25_full_batch_2/audit/ledger.csv:54`) against the checker run on this machine over `5` batch-2 windows (`limit 1e-9`), citing `results/2026-10-25_full_batch_2/cluster_checker_equivalence.json`.
- **Per-window verification (`results/2026-10-25_full_batch_2/cluster_checker_equivalence.json:1-57`)**:

| Window | Category | `outcome_lab` | `outcome_cluster` | `record_equal` | `closure` Diff | `plane_sections` Diff | `rigid_invariance` Diff | `rigid_invariance_profile_window` Diff |
|---|---|---|---|---|---:|---:|---:|---:|
| `0708_c4__w0-2` | Closure fail | `fail` | `fail` | `true` | $0.0$ | $0.0$ | `null` | — |
| `0708_m8__w2-4` | Not computable | `not computable` | `not computable` | `true` | `null` | `null` | `null` | — |
| `0708_c5__w12-14` | Pass (1) | `pass` | `pass` | `true` | $0.0$ | $0.0$ | `null` | — |
| `0714_c4__w16-18` | Pass (2) | `pass` | `pass` | `true` | $0.0$ | $0.0$ | `null` | — |
| `0708_c4__w10-12` | Moved copy (`w10-12`) | `pass` | `pass` | `true` | $0.0$ | $0.0$ | $0.0$ | $0.0$ |

- All `5` windows have `record_equal = true` and maximum numeric difference $0.0 \le 10^{-9}$ (`cluster_checker_equivalence.json:56`).

---

## 4. What Was Not Checked

- Files on the storage host and on the computing cluster (including live `.npz` tracks, `.json` window checks, `DELETED.log` on the cluster, and cluster `sacct` records) were not inspected directly because this audit has no access to `private/`, the storage host, or the computing cluster (`docs/agents/inbox/argon-audit.md` item 5; `AGENTS.md`).
- Untracked files under `private/` (such as `private/storage_only_hosts.txt`, `private/hosts.yaml`, and any untracked batch-2 driver scripts or local staging files under `staging/`) are git-ignored and were not read.
- Raw `.npz` track arrays for the `1,060` tracked batch-2 windows are stored on the storage host and not committed to the repository; window outcomes and check values in `results/2026-10-25_full_batch_2/windows.csv` and `summary.json` were verified from the committed tabular and JSON artifacts rather than recomputed from raw `.npz` files.
