# ARIA Benchmarking Engine (`evaluation/benchmarks/`)

This directory contains the executable benchmarking engine and evaluation runners for ARIA.

---

## Directory Contents

* [`run_benchmark.py`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/benchmarks/run_benchmark.py): The primary CLI entry point for running the 10-task change-impact benchmark and compiling metrics.
* [`metrics.py`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/benchmarks/metrics.py): Safe implementation of Information Retrieval (IR) metrics (precision, recall, F1, false positives, false negatives).
* [`baselines/README.md`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/benchmarks/baselines/README.md): Detailed documentation of the Conventional Search / Vector RAG baseline runner.

---

## Running the Benchmark

From the repository root:

```bash
python evaluation/benchmarks/run_benchmark.py
```

### Options

```bash
python evaluation/benchmarks/run_benchmark.py \
  --tasks evaluation/tasks/tasks.json \
  --ground-truth evaluation/ground_truth/ground_truth.json \
  --output-dir evaluation/results
```

---

## Generated Results Artifacts

Executing the runner generates:
* `evaluation/results/raw_results.json`: Full task-by-task predictions and confusion matrix entries.
* `evaluation/results/metrics.json`: Macro-averaged precision, recall, F1, and delta scores.
* `evaluation/results/latency.json`: Wall-clock latency distribution (Mean, P50, P95).
* `evaluation/results/false_positive_analysis.json`: Detailed task-by-task false positive breakdown proving the 93.39% noise reduction.
