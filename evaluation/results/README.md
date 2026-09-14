# ARIA Benchmark Results (`evaluation/results/`)

This directory contains the machine-readable benchmark outputs and empirical measurements for ARIA.

---

## Artifact Inventory

* [`metrics.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/metrics.json): Macro-averaged Information Retrieval metrics (Precision, Recall, F1, Caller F1, Test F1) comparing Baseline vs ARIA RAW vs ARIA VALID-GT.
* [`false_positive_analysis.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/false_positive_analysis.json): Task-by-task and aggregate false-positive alert counts proving the 4,553 false alarm reduction (-93.39%).
* [`latency.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/latency.json): Latency distribution profile (Mean, P50, P95) for Baseline vs ARIA.
* [`results.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/results.json): Full per-task confusion matrix data and prediction arrays.
* [`results.csv`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/results.csv): Tabular summary formatted for spreadsheet inspection.
* [`incremental_benchmarks.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/incremental_benchmarks.json): Incremental re-indexing latency and memory benchmarks across 1-file, 3-file, and 10-file diffs.

---

## Benchmark Summary

| Metric | Conventional Search / Vector RAG | ARIA RAW | ARIA VALID-GT | Delta |
| :--- | :--- | :--- | :--- | :--- |
| **File Precision** | 2.8% | **10.6%** | **10.6%** | **+7.8%** |
| **File Recall** | 91.7% | 71.7% | 71.7% | Deterministic Boundary |
| **File F1 Score** | 5.3% | **18.0%** | **18.0%** | **+12.8%** |
| **Caller Resolution F1** | 1.3% | **20.4%** | **20.4%** | **+19.0%** |
| **Affected Tests F1 (HIGH Tier)** | 6.2% | **28.5%** | **36.4%** | **+22.3% / +30.2%** |
| **False-Positive File Alerts** | 4,875 files | **322 files** | **322 files** | **-4,553 false alarms (-93.39%)** |
| **P50 Latency** | 235.7 ms | **166.9 ms** | **166.9 ms** | **Sub-200ms interactive SLA** |
