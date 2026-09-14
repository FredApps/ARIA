# ARIA Reproducibility Suite

## Overview
This directory contains everything required to audit, verify, and reproduce ARIA's evaluation results and benchmarks.

ARIA enforces an evidence-first, zero-fabrication standard:
- Quantitative claims are pinned to verifiable benchmark runs with machine-readable metrics.
- Qualitative stress-test findings are linked to specific code locations in pinned repository revisions.
- Stale or ambiguous ground truth is preserved and documented rather than silently erased.

---

## Reproducibility Index

| Document | Description |
|---|---|
| [ENVIRONMENT.md](ENVIRONMENT.md) | Verified software versions, runtime environments, models, and dependencies used during evaluation. |
| [REPOSITORIES.md](REPOSITORIES.md) | Pinned Git commit SHAs, URLs, and evaluation scopes for all analyzed repositories. |
| [RUNBOOK.md](RUNBOOK.md) | Complete step-by-step developer guide for running benchmarks, inspecting metrics, and reproducing findings. |

---

## Quick Start
To run the automated verification suite checking all benchmark datasets, ground truth, and metric calculations:

```bash
# Run the benchmark runner against precomputed outputs
python evaluation/benchmarks/run_benchmark.py --verify-only

# Run test suite verifying JSON integrity and mathematical consistency
pytest tests/test_evaluation_integrity.py -v
```
