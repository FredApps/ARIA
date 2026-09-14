# ARIA Evaluation Tasks (`evaluation/tasks/`)

This directory contains the machine-readable task dataset used for the **ARIA 10-Task Quantitative Change-Impact Benchmark**.

---

## Task Dataset Overview

The benchmark tasks are defined in [`tasks.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/tasks/tasks.json). Each task represents a realistic engineering refactoring or bugfix request targeting a specific component in a pinned repository commit.

### Target Repositories Covered
1. **`fastapi/fastapi`** (Commit `49033471594ea5d99a80abdf1043231b7791ee49`)
   - 3 Change-Impact Tasks (`task-01`, `task-02`, `task-03`)
2. **`psf/requests`** (Commit `5460f467b02e49471c0fd6cfc9ca0adab6351f98`)
   - 3 Change-Impact Tasks (`task-04`, `task-05`, `task-06`)
3. **`VarshithReddy2006/ARIA`** (Commit `bbc81833baa1b2c6c01a63528bf270a653281729`)
   - 4 Change-Impact Tasks (`task-07`, `task-08`, `task-09`, `task-10`)

---

## Task Schema

Each entry in `tasks.json` adheres to the following specification:

```json
{
  "task_id": "string",
  "repository": "owner/name",
  "revision": "git-commit-sha",
  "change_description": "Natural language refactoring instruction",
  "ground_truth_files": ["list", "of", "production", "files"],
  "ground_truth_symbols": ["list", "of", "symbols"],
  "ground_truth_callers": ["list", "of", "callers"],
  "ground_truth_dependencies": ["list", "of", "dependencies"],
  "ground_truth_tests": ["list", "of", "test", "files"],
  "ground_truth_api_surfaces": ["list", "of", "routes", "or", "apis"],
  "ground_truth_risk": "low | medium | high | extreme"
}
```

---

## Tasks Summary Table

| Task ID | Repository | Target Area | Risk | Expected Files | Expected Callers | Expected Tests |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `task-01-fastapi-oauth2` | `fastapi/fastapi` | `fastapi/security/oauth2.py:OAuth2PasswordBearer` | High | 4 | 2 | 3 |
| `task-02-fastapi-serialize-response` | `fastapi/fastapi` | `fastapi/routing.py:serialize_response` | Extreme | 3 | 2 | 2 |
| `task-03-fastapi-status-codes` | `fastapi/fastapi` | `fastapi/status.py:HTTP_404_NOT_FOUND` | Low | 2 | 0 | 1 |
| `task-04-requests-session-send` | `psf/requests` | `requests/sessions.py:Session.send` | High | 3 | 4 | 2 |
| `task-05-requests-adapters-ssl` | `psf/requests` | `requests/adapters.py:HTTPAdapter.cert_verify` | Medium | 2 | 2 | 2 |
| `task-06-requests-models-response` | `psf/requests` | `requests/models.py:Response.content` | Medium | 3 | 2 | 1 |
| `task-07-aria-symbol-schema` | `VarshithReddy2006/ARIA` | `models/symbol.py:Symbol` | Medium | 4 | 2 | 2 |
| `task-08-aria-call-graph-blast-radius` | `VarshithReddy2006/ARIA` | `services/call_graph_service.py:get_blast_radius`| High | 3 | 2 | 2 |
| `task-09-aria-api-surface-status` | `VarshithReddy2006/ARIA` | `models/api_surface.py:ApiStatus` | Medium | 4 | 2 | 1 |
| `task-10-aria-impact-engine-bucketing` | `VarshithReddy2006/ARIA` | `services/impact_analysis_service.py:bucketing` | Medium | 3 | 1 | 2 |

---

## Evaluation Dataset Integrity Notice

Ground truth test files were audited against physical disk snapshots in [`evaluation/data_quality_report.md`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/data_quality_report.md).
- **Production Files:** 26 / 26 files (100.0%) exist on physical disk and are verified `VALID`.
- **Test Files:** 13 / 18 files (72.2%) exist on physical disk (`VALID`). 5 / 18 files (27.8%) are legacy stale paths (e.g. `tests/test_response_model.py` instead of the actual `tests/test_tutorial/test_response_model/test_tutorial001.py`).
- Benchmark metrics are reported in both **RAW** (historical unmodified ground truth) and **VALID-GT** (excluding non-existent files) modes.
