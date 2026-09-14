"""Transparent, reproducible evaluation metrics for repository intelligence benchmarks.

Handles zero denominators safely, preserves unrounded intermediate calculations,
and computes standard Information Retrieval (IR) metrics:
- Precision: TP / (TP + FP)
- Recall: TP / (TP + FN)
- F1 Score: 2 * Precision * Recall / (Precision + Recall)
"""

from typing import Dict, Any, List, Set


def safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two numbers, returning 0.0 if denominator is 0."""
    return (numerator / denominator) if denominator != 0 else 0.0


def calculate_precision(tp: int, fp: int) -> float:
    """Precision = TP / (TP + FP)"""
    return safe_divide(float(tp), float(tp + fp))


def calculate_recall(tp: int, fn: int) -> float:
    """Recall = TP / (TP + FN)"""
    return safe_divide(float(tp), float(tp + fn))


def calculate_f1(precision: float, recall: float) -> float:
    """F1 = 2 * P * R / (P + R)"""
    return safe_divide(2.0 * precision * recall, precision + recall)


def calculate_noise_reduction(baseline_fp: int, aria_fp: int) -> float:
    """Calculate percentage reduction in false-positive alerts."""
    diff = baseline_fp - aria_fp
    return safe_divide(float(diff) * 100.0, float(baseline_fp))


def calculate_metrics(
    predicted: List[str] | Set[str], ground_truth: List[str] | Set[str]
) -> Dict[str, Any]:
    """Calculate TP, FP, FN, Precision, Recall, and F1 score safely."""
    pred_set = set(predicted)
    gt_set = set(ground_truth)

    tp_set = pred_set.intersection(gt_set)
    fp_set = pred_set.difference(gt_set)
    fn_set = gt_set.difference(pred_set)

    tp = len(tp_set)
    fp = len(fp_set)
    fn = len(fn_set)

    precision = calculate_precision(tp, fp)
    recall = calculate_recall(tp, fn)
    f1 = calculate_f1(precision, recall)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tp_items": sorted(list(tp_set)),
        "fp_items": sorted(list(fp_set)),
        "fn_items": sorted(list(fn_set)),
    }


def aggregate_macro_metrics(
    task_results: List[Dict[str, Any]], key: str
) -> Dict[str, float]:
    """Computes macro-averaged metrics across a collection of task evaluations."""
    if not task_results:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "total_fp": 0}

    total_precision = 0.0
    total_recall = 0.0
    total_f1 = 0.0
    total_fp = 0

    n = len(task_results)
    for res in task_results:
        metric_dict = res.get(key, {})
        total_precision += metric_dict.get("precision", 0.0)
        total_recall += metric_dict.get("recall", 0.0)
        total_f1 += metric_dict.get("f1", 0.0)
        total_fp += metric_dict.get("fp", 0)

    return {
        "precision": total_precision / n,
        "recall": total_recall / n,
        "f1": total_f1 / n,
        "total_fp": total_fp,
    }
