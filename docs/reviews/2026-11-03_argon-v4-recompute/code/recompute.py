"""Independent recomputation of freeze v3, freeze v4, and the v3-to-v4 split.

Written from the definitions in:
- docs/proposals/2026-10-23_freeze-v3.md
- docs/proposals/2026-10-25_freeze-v4-candidate.md
- docs/decisions.md (C3 option (a))
- docs/specs/2026-10-10_repair-criteria.md
- config/scoring_tolerance.yaml
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[4]

OUTCOME_CATEGORIES = (
    "good_report",
    "false_accept",
    "correct_decline",
    "unnecessary_decline",
    "not_reported",
    "accept_on_decline",
)

CLASSES = ("accept_clean", "accept_repaired", "decline")

FAULT_NAMES_CORRECT: dict[str, set[str]] = {
    "rigid_drift": {"rigid_drift"},
    "displacement_exceeds_patch": {"displacement_exceeds_patch"},
    "width_change": {"width_change"},
    "bad_stage_correction": {"bad_stage_correction"},
    "stage_log_missing": {"bad_stage_correction", "rigid_drift"},
    "low_texture": {"low_texture"},
    "midline_jitter": {"midline_jitter"},
    "second_root": {"second_root"},
    "fast_rotation": {"fast_rotation"},
    "flank_swap": {"unknown"},
    "partial_occlusion": {"low_texture", "unknown"},
}


def load_tolerance_config() -> dict[str, Any]:
    tol_path = REPO_ROOT / "config" / "scoring_tolerance.yaml"
    return yaml.safe_load(tol_path.read_text(encoding="utf-8"))


def is_measurement_good(
    error_dict: dict[str, Any] | None,
    truth_dict: dict[str, Any],
    width_free: bool,
    tol_cfg: dict[str, Any],
) -> bool:
    if not error_dict:
        return False
    keys = sorted(k for k in error_dict if k.endswith("_rms_pct_per_h"))
    if len(keys) < 2:
        return False
    # Centre and flank RMS keys from summary error_after / error_before
    centre_key = [k for k in keys if not k.startswith("flank")][0]
    flank_key = [k for k in keys if k.startswith("flank")][0]
    centre_rms = error_dict.get(centre_key)
    flank_rms = error_dict.get(flank_key)
    if centre_rms is None:
        return False
    peak_key = [k for k in truth_dict if k.startswith("peak_") and k.endswith("_pct_per_h")][0]
    peak_val = float(truth_dict[peak_key])
    frac = float(tol_cfg["regr_rms_fraction_of_true_peak"])
    no_growth_tol = float(tol_cfg["regr_rms_no_growth_pct_per_h"])
    centre_tol = frac * peak_val if peak_val > 0.0 else no_growth_tol
    if centre_rms > centre_tol:
        return False
    if width_free:
        return True
    if flank_rms is None:
        return False
    return flank_rms <= float(tol_cfg["flank_difference_rms_pct_per_h"])


def categorize_run(
    status: str,
    rod_class: str,
    good: bool,
) -> str:
    if status == "accept":
        if good:
            if rod_class == "decline":
                return "accept_on_decline"
            return "good_report"
        return "false_accept"
    if status == "decline":
        if rod_class == "decline":
            return "correct_decline"
        return "unnecessary_decline"
    return "not_reported"


def extract_terminal_fault(
    summary: dict[str, Any],
    summary_path: Path,
    use_filename_fallback: bool = False,
) -> str | None:
    status = summary["outcome"]["status"]
    args = summary["outcome"].get("args") or {}
    if status == "decline" and not use_filename_fallback:
        return args.get("fault")
    trace_name = summary.get("trace")
    if not trace_name and use_filename_fallback:
        trace_name = summary_path.name.replace("_summary.json", "_trace.jsonl")
    if trace_name:
        trace_path = summary_path.parent / trace_name
        if trace_path.exists():
            last_fault = None
            for line in trace_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                step = json.loads(line)
                action = step.get("action") or {}
                if action.get("name") in ("apply_remedy", "decline") and step.get("status") in ("executed", "terminal"):
                    f = (action.get("args") or {}).get("fault")
                    if f:
                        last_fault = f
            return last_fault
    return None


def load_runs(
    runs_dir: Path,
    labels_map: dict[str, dict[str, Any]],
    tol_cfg: dict[str, Any],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    # Only top-level *_summary.json in runs_dir (excludes runs/usage_limit/)
    for f in sorted(runs_dir.glob("*_summary.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        rod_id = s["rod"]["id"]
        if rod_id not in labels_map:
            continue
        rod_info = labels_map[rod_id]
        rod_class = rod_info["class"]
        width_free = bool(s["final_settings"].get("width_free", False))
        good_after = is_measurement_good(s.get("error_after"), s["truth"], width_free, tol_cfg)
        good_before = is_measurement_good(s.get("error_before"), s["truth"], False, tol_cfg)
        status = s["outcome"]["status"]
        cat = categorize_run(status, rod_class, good_after)
        fault = s["rod"].get("fault")
        nf_summary = extract_terminal_fault(s, f, use_filename_fallback=False)
        nf_fallback = extract_terminal_fault(s, f, use_filename_fallback=True)
        remedies_list = s.get("remedies") or []
        roll_backs = int(s.get("roll_backs", 0))
        remedies_kept_net = len(remedies_list) - 2 * roll_backs
        records.append({
            "method": s["method"],
            "rod_id": rod_id,
            "kind": rod_info["kind"],
            "fault": fault,
            "seed": s["rod"]["seed"],
            "repeat": s.get("repeat", 0),
            "class": rod_class,
            "status": status,
            "category": cat,
            "good_after": good_after,
            "good_before": good_before,
            "remedies_raw_len": len(remedies_list),
            "remedies_kept": remedies_kept_net,
            "named_fault_summary": nf_summary,
            "named_fault_fallback": nf_fallback,
            "fault_correct_summary": (
                nf_summary in FAULT_NAMES_CORRECT.get(fault, set())
                if fault is not None and nf_summary is not None
                else False
            ),
            "fault_correct_fallback": (
                nf_fallback in FAULT_NAMES_CORRECT.get(fault, set())
                if fault is not None and nf_fallback is not None
                else False
            ),
            "steps": s["outcome"].get("steps", 0),
            "failed_steps": s["outcome"].get("failed_steps", 0),
        })
    return records


def make_reference_records(
    base_records: list[dict[str, Any]],
    labels_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    by_rod = {r["rod_id"]: r for r in base_records if r["method"] == "script"}
    ref_records: list[dict[str, Any]] = []
    for rod_id, r in sorted(by_rod.items()):
        rod_class = labels_map[rod_id]["class"]
        ref_records.append({
            **r,
            "method": "decline_all",
            "repeat": 0,
            "class": rod_class,
            "status": "decline",
            "category": categorize_run("decline", rod_class, False),
            "remedies_raw_len": 0,
            "remedies_kept": 0,
            "named_fault_summary": None,
            "named_fault_fallback": None,
            "fault_correct_summary": False,
            "fault_correct_fallback": False,
        })
        ref_records.append({
            **r,
            "method": "all_accept",
            "repeat": 0,
            "class": rod_class,
            "status": "accept",
            "category": categorize_run("accept", rod_class, r["good_before"]),
            "remedies_raw_len": 0,
            "remedies_kept": 0,
            "named_fault_summary": None,
            "named_fault_fallback": None,
            "fault_correct_summary": False,
            "fault_correct_fallback": False,
        })
    return ref_records


def compute_single_slice_metrics(runs: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(runs)
    by_class: dict[str, list[dict[str, Any]]] = {c: [] for c in CLASSES}
    for r in runs:
        by_class[r["class"]].append(r)

    class_acc: dict[str, float] = {}
    class_correct: dict[str, int] = {}
    class_total: dict[str, int] = {}
    unnecessary_decline_by_class: dict[str, float] = {}
    not_reported_by_class: dict[str, int] = {}

    for c in CLASSES:
        c_runs = by_class[c]
        class_total[c] = len(c_runs)
        if c in ("accept_clean", "accept_repaired"):
            corr = sum(1 for r in c_runs if r["category"] == "good_report")
            unnec = sum(1 for r in c_runs if r["category"] == "unnecessary_decline")
            unnecessary_decline_by_class[c] = unnec / len(c_runs) if c_runs else 0.0
        else:
            corr = sum(1 for r in c_runs if r["category"] == "correct_decline")
        class_correct[c] = corr
        class_acc[c] = corr / len(c_runs) if c_runs else 0.0
        not_reported_by_class[c] = sum(1 for r in c_runs if r["category"] == "not_reported")

    balanced_acc = sum(class_acc[c] for c in CLASSES) / 3.0
    total_correct = sum(class_correct.values())
    overall_acc = total_correct / total if total else 0.0

    accept_runs = [r for r in runs if r["status"] == "accept"]
    decline_runs = [r for r in runs if r["status"] == "decline"]
    false_accept_count = sum(1 for r in runs if r["category"] == "false_accept")
    false_accept_rate = false_accept_count / len(accept_runs) if accept_runs else None

    coverage = len(accept_runs) / total if total else 0.0
    correct_decline_count = sum(1 for r in runs if r["category"] == "correct_decline")
    abstention_precision = correct_decline_count / len(decline_runs) if decline_runs else None
    abstention_recall = class_acc["decline"]

    remedies_on_clean_accepted = sum(
        1 for r in by_class["accept_clean"]
        if r["status"] == "accept" and r["remedies_kept"] > 0
    )
    remedies_on_clean_any_status = sum(
        1 for r in by_class["accept_clean"]
        if r["remedies_kept"] > 0
    )

    fault_runs = [r for r in runs if r["fault"] is not None]
    fault_correct_summary = sum(1 for r in fault_runs if r["fault_correct_summary"])
    fault_correct_fallback = sum(1 for r in fault_runs if r["fault_correct_fallback"])

    cat_counts = Counter(r["category"] for r in runs)

    return {
        "total_runs": total,
        "class_total": class_total,
        "class_correct": class_correct,
        "class_accuracy": class_acc,
        "balanced_accuracy": balanced_acc,
        "overall_accuracy": overall_acc,
        "false_accept_count": false_accept_count,
        "accept_count": len(accept_runs),
        "false_accept_rate": false_accept_rate,
        "coverage": coverage,
        "correct_decline_count": correct_decline_count,
        "decline_count": len(decline_runs),
        "abstention_precision": abstention_precision,
        "abstention_recall": abstention_recall,
        "unnecessary_decline_by_class": unnecessary_decline_by_class,
        "not_reported_by_class": not_reported_by_class,
        "not_reported_total": sum(not_reported_by_class.values()),
        "remedies_on_clean_accepted": remedies_on_clean_accepted,
        "remedies_on_clean_any": remedies_on_clean_any_status,
        "fault_correct_summary": fault_correct_summary,
        "fault_correct_fallback": fault_correct_fallback,
        "fault_runs_count": len(fault_runs),
        "category_counts": {k: cat_counts.get(k, 0) for k in OUTCOME_CATEGORIES},
    }


def compute_agreement(runs: list[dict[str, Any]]) -> dict[str, Any]:
    by_rod: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in runs:
        by_rod[r["rod_id"]].append(r)

    n_rods = len(by_rod)
    repeats_per_rod = {len(v) for v in by_rod.values()}
    if repeats_per_rod != {3}:
        return {"unanimity_overall": 1.0, "fleiss_kappa": 1.0, "n_rods": n_rods}

    unanimous_overall = 0
    unanimous_by_class: dict[str, int] = {c: 0 for c in CLASSES}
    rods_by_class: dict[str, int] = {c: 0 for c in CLASSES}

    p_i_sum = 0.0
    cat_totals: Counter[str] = Counter()

    for _, r_list in by_rod.items():
        c = r_list[0]["class"]
        rods_by_class[c] += 1
        cats = [x["category"] for x in r_list]
        counts = Counter(cats)
        for k, v in counts.items():
            cat_totals[k] += v
        if len(counts) == 1:
            unanimous_overall += 1
            unanimous_by_class[c] += 1
        p_i = (sum(v * v for v in counts.values()) - 3) / 6.0
        p_i_sum += p_i

    p_bar = p_i_sum / n_rods if n_rods else 1.0
    total_ratings = n_rods * 3
    p_e = sum((cat_totals.get(k, 0) / total_ratings) ** 2 for k in OUTCOME_CATEGORIES)
    kappa = (p_bar - p_e) / (1.0 - p_e) if p_e < 1.0 else 1.0

    return {
        "n_rods": n_rods,
        "unanimous_overall_count": unanimous_overall,
        "unanimity_overall": unanimous_overall / n_rods if n_rods else 0.0,
        "unanimous_by_class_count": unanimous_by_class,
        "rods_by_class": rods_by_class,
        "unanimity_by_class": {
            c: (unanimous_by_class[c] / rods_by_class[c] if rods_by_class[c] else 0.0)
            for c in CLASSES
        },
        "fleiss_kappa": kappa,
        "p_bar": p_bar,
        "p_e": p_e,
    }


def evaluate_dataset(
    runs_dir: Path,
    labels_map: dict[str, dict[str, Any]],
    tol_cfg: dict[str, Any],
    exclude_kinds: set[str] | None = None,
) -> dict[str, Any]:
    filtered_labels = {
        k: v for k, v in labels_map.items()
        if not exclude_kinds or v["kind"] not in exclude_kinds
    }
    raw_runs = load_runs(runs_dir, filtered_labels, tol_cfg)
    ref_runs = make_reference_records(raw_runs, filtered_labels)
    all_runs = raw_runs + ref_runs

    methods = ["script", "remedy_tree", "single_agent", "diagnostician", "decline_all", "all_accept"]
    out: dict[str, Any] = {}
    for m in methods:
        m_runs = [r for r in all_runs if r["method"] == m]
        pooled = compute_single_slice_metrics(m_runs)
        repeats = sorted({r["repeat"] for r in m_runs})
        per_repeat = {rep: compute_single_slice_metrics([r for r in m_runs if r["repeat"] == rep]) for rep in repeats}
        agreement = compute_agreement(m_runs) if len(repeats) == 3 else None

        ranges: dict[str, Any] = {}
        if len(repeats) == 3:
            for k in ("balanced_accuracy", "overall_accuracy", "false_accept_rate", "coverage", "abstention_precision", "abstention_recall"):
                vals = [per_repeat[rep][k] for rep in repeats if per_repeat[rep][k] is not None]
                if vals:
                    ranges[k] = {"mean": sum(vals) / len(vals), "min": min(vals), "max": max(vals), "per_repeat": vals}
            ranges["class_accuracy"] = {}
            for c in CLASSES:
                vals = [per_repeat[rep]["class_accuracy"][c] for rep in repeats]
                ranges["class_accuracy"][c] = {"mean": sum(vals) / len(vals), "min": min(vals), "max": max(vals), "per_repeat": vals}

        out[m] = {
            "pooled": pooled,
            "per_repeat": per_repeat,
            "ranges": ranges,
            "agreement": agreement,
        }
    return out


def main() -> None:
    tol_cfg = load_tolerance_config()
    v3_labels_raw = json.loads((REPO_ROOT / "results/2026-10-23_freeze_v3/labels.json").read_text(encoding="utf-8"))["labels"]
    v4_labels_raw = json.loads((REPO_ROOT / "results/2026-10-25_freeze_v4/labels.json").read_text(encoding="utf-8"))["labels"]

    v3_c3a_labels = json.loads(json.dumps(v3_labels_raw))
    for _, info in v3_c3a_labels.items():
        if info["kind"] == "stage_log_missing":
            info["class"] = "decline"
            info["sequence"] = None

    v3_runs_dir = REPO_ROOT / "results/2026-10-23_freeze_v3/runs"
    v4_runs_dir = REPO_ROOT / "results/2026-10-25_freeze_v4/runs"

    results = {
        "v3_under_v3_labels": evaluate_dataset(v3_runs_dir, v3_labels_raw, tol_cfg),
        "v3_under_c3a_labels": evaluate_dataset(v3_runs_dir, v3_c3a_labels, tol_cfg),
        "v4_under_v4_labels": evaluate_dataset(v4_runs_dir, v4_labels_raw, tol_cfg),
        "v3_unchanged_rows_48": evaluate_dataset(v3_runs_dir, v3_labels_raw, tol_cfg, exclude_kinds={"stage_log_missing"}),
        "v4_unchanged_rows_48": evaluate_dataset(v4_runs_dir, v4_labels_raw, tol_cfg, exclude_kinds={"stage_log_missing"}),
    }

    for key, block in results.items():
        print(f"=== {key} ===")
        for m in ("script", "remedy_tree", "diagnostician", "single_agent", "decline_all", "all_accept"):
            p = block[m]["pooled"]
            print(
                f"  {m:15s}: runs={p['total_runs']:3d} "
                f"bal={p['balanced_accuracy']:.4f} "
                f"clean={p['class_accuracy']['accept_clean']:.4f} "
                f"rep={p['class_accuracy']['accept_repaired']:.4f} "
                f"dec={p['class_accuracy']['decline']:.4f} "
                f"ovr={p['overall_accuracy']:.4f} "
                f"fa={p['false_accept_count']:2d} "
                f"nr={p['not_reported_total']:2d}"
            )


if __name__ == "__main__":
    main()
