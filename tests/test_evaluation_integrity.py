"""
test_evaluation_integrity.py
Automated integrity test suite for ARIA's public evaluation package.

Verifies:
1. All evaluation JSON files exist and are syntactically valid JSON.
2. Schema consistency and 1:1 parity between tasks and ground truth.
3. No duplicate task IDs or invalid repository identifiers.
4. Benchmark metrics and reduction calculations (4,875 -> 322 = 93.39% reduction).
5. Safe mathematical properties of metrics (precision, recall, F1).
"""

import json
from pathlib import Path
import pytest

from evaluation.benchmarks.metrics import (
    calculate_precision,
    calculate_recall,
    calculate_f1,
    calculate_noise_reduction,
    safe_divide,
)

EVAL_DIR = Path(__file__).resolve().parent.parent / "evaluation"


@pytest.fixture
def tasks_data():
    tasks_file = EVAL_DIR / "tasks" / "tasks.json"
    assert tasks_file.exists(), f"Missing tasks file: {tasks_file}"
    with open(tasks_file, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def ground_truth_data():
    gt_file = EVAL_DIR / "ground_truth" / "ground_truth.json"
    assert gt_file.exists(), f"Missing ground truth file: {gt_file}"
    with open(gt_file, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def metrics_data():
    metrics_file = EVAL_DIR / "results" / "metrics.json"
    assert metrics_file.exists(), f"Missing metrics file: {metrics_file}"
    with open(metrics_file, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def false_positive_data():
    fp_file = EVAL_DIR / "results" / "false_positive_analysis.json"
    assert fp_file.exists(), f"Missing false positive file: {fp_file}"
    with open(fp_file, "r", encoding="utf-8") as f:
        return json.load(f)


def test_tasks_json_schema(tasks_data):
    """Verify tasks.json structure, uniqueness, and fields."""
    assert isinstance(tasks_data, list), "tasks.json should be a JSON array"
    assert len(tasks_data) == 10, f"Expected 10 tasks, found {len(tasks_data)}"

    seen_ids = set()
    valid_repos = {"fastapi/fastapi", "psf/requests", "VarshithReddy2006/ARIA"}

    for task in tasks_data:
        assert "task_id" in task
        assert "repository" in task
        assert "change_description" in task
        assert "ground_truth_files" in task

        # Check uniqueness
        tid = task["task_id"]
        assert tid not in seen_ids, f"Duplicate task_id detected: {tid}"
        seen_ids.add(tid)

        # Check repo identifier
        assert task["repository"] in valid_repos, (
            f"Unexpected repo: {task['repository']}"
        )


def test_ground_truth_parity(tasks_data, ground_truth_data):
    """Verify 1:1 correspondence between tasks.json and ground_truth.json."""
    assert isinstance(ground_truth_data, list), (
        "ground_truth.json should be a JSON array"
    )
    assert len(ground_truth_data) == len(tasks_data)

    task_ids = [t["task_id"] for t in tasks_data]
    gt_ids = [gt["task_id"] for gt in ground_truth_data]

    assert task_ids == gt_ids, (
        "Task IDs in tasks.json and ground_truth.json must match exactly"
    )

    for gt in ground_truth_data:
        assert "validation_status" in gt
        assert gt["validation_status"] in {"VERIFIED", "PARTIAL", "STALE", "UNRESOLVED"}
        assert "ground_truth" in gt
        assert "files" in gt["ground_truth"]


def test_noise_reduction_calculation():
    """Verify exact mathematical derivation of the 93.39% false-positive noise reduction."""
    baseline_fp = 4875
    aria_fp = 322
    difference = baseline_fp - aria_fp
    assert difference == 4553

    reduction_pct = (difference / baseline_fp) * 100.0
    # Expected: 93.39487179...
    assert round(reduction_pct, 2) == 93.39

    calc_reduction = calculate_noise_reduction(baseline_fp, aria_fp)
    assert round(calc_reduction, 2) == 93.39


def test_false_positive_analysis_integrity(false_positive_data):
    """Verify that false_positive_analysis.json matches the audited totals."""
    summary = false_positive_data["aggregate"]
    assert summary["baseline_total_false_positives"] == 4875
    assert summary["aria_total_false_positives"] == 322
    assert summary["total_false_alarms_removed"] == 4553
    assert summary["overall_noise_reduction_percentage"] == 93.39

    # Verify task sum equals aggregate
    tasks = false_positive_data["per_task"]
    assert len(tasks) == 10

    sum_baseline = sum(t["baseline_false_positives"] for t in tasks)
    sum_aria = sum(t["aria_false_positives"] for t in tasks)

    assert sum_baseline == 4875
    assert sum_aria == 322


def test_metrics_json_internal_consistency(metrics_data):
    """Verify that metrics.json contains valid deltas and values."""
    assert metrics_data["tasks_count"] == 10
    assert "fastapi/fastapi" in metrics_data["repositories_evaluated"]

    # Check baseline & ARIA false-positive alerts
    baseline = metrics_data["metrics"]["baseline"]
    aria_raw = metrics_data["metrics"]["aria_raw"]
    deltas = metrics_data["deltas_vs_baseline"]

    assert baseline["false_positive_file_alerts"] == 4875
    assert aria_raw["false_positive_file_alerts"] == 322
    assert deltas["false_alarms_eliminated"] == 4553
    assert deltas["noise_reduction_percentage"] == 93.39


def test_metric_functions_edge_cases():
    """Verify safe mathematical behavior of metrics (zero division, empty sets)."""
    assert safe_divide(0, 0) == 0.0
    assert safe_divide(10, 0) == 0.0
    assert safe_divide(10, 2) == 5.0

    # Zero TP
    assert calculate_precision(0, 10) == 0.0
    assert calculate_recall(0, 10) == 0.0
    assert calculate_f1(0.0, 0.0) == 0.0

    # Perfect scores
    assert calculate_precision(10, 0) == 1.0
    assert calculate_recall(10, 0) == 1.0
    assert calculate_f1(1.0, 1.0) == 1.0

    # Non-trivial calculation
    p = calculate_precision(4, 1)  # 4 / 5 = 0.8
    r = calculate_recall(4, 1)  # 4 / 5 = 0.8
    assert p == 0.8
    assert r == 0.8
    assert round(calculate_f1(p, r), 4) == 0.8000
