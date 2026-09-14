# ARIA Ground Truth Dataset (`evaluation/ground_truth/`)

This directory contains the verified, audited ground-truth dataset ([`ground_truth.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/ground_truth/ground_truth.json)) for the 10-task change-impact benchmark.

---

## Provenance & Audit Standard

Ground truth must never be fabricated to make an AI system look favorable.

In this repository:
1. **Separation of Concerns:** Ground truth definitions are decoupled from model prediction outputs.
2. **Physical Disk Verification:** An exhaustive audit ([`evaluation/data_quality_report.md`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/data_quality_report.md)) scanned all 26 production files and 18 test files against the pinned git revisions.
3. **Audit Finding:**
   - **Production Ground Truth:** 26 / 26 files (100.0%) verified `VALID` on disk.
   - **Test Ground Truth:** 13 / 18 files (72.2%) verified `VALID` on disk.
   - **Stale Paths:** 5 / 18 test files (27.8%) do not physically exist on disk in the evaluated commits due to outdated benchmark naming conventions.

---

## Dual-Mode Evaluation Policy

To preserve scientific reproducibility without polluting developer metrics:
* **RAW Mode:**
  - Evaluates recall and precision strictly against the unmodified historical `tasks.json` ground truth.
  - Stale/non-existent test files count as automatic false negatives, preserving historical comparability across earlier milestones.
* **VALID-GT Mode:**
  - Excludes the 5 non-existent test files from the denominator, evaluating performance strictly against the 13 physically verifiable test files.
  - Gives developers an unpolluted assessment of true predictive precision and recall.

---

## Audited Stale Entries Registry

| Task ID | Specified Ground Truth Test | Real Disk Status | Actual Location on Disk |
| :--- | :--- | :--- | :--- |
| `task-02-fastapi-serialize-response` | `tests/test_response_model.py` | `DOES NOT EXIST` | `tests/test_tutorial/test_response_model/test_tutorial001.py` |
| `task-03-fastapi-status-codes` | `tests/test_status_codes.py` | `DOES NOT EXIST` | `tests/test_response_change_status_code.py` |
| `task-04-requests-session-send` | `tests/test_sessions.py` | `DOES NOT EXIST` | Consolidated in `tests/test_requests.py` |
| `task-08-aria-call-graph-blast-radius` | `tests/test_call_graph.py` | `DOES NOT EXIST` | `tests/test_call_graph_service.py` |
| `task-09-aria-api-surface-status` | `tests/test_api_surface.py` | `DOES NOT EXIST` | `tests/test_api_surface_service.py` |
