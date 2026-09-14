# ARIA Claim Verification Audit

This document contains the itemized forensic audit of all quantitative and qualitative claims made regarding ARIA's performance, benchmark metrics, and structural capabilities.

---

## Claim Verification Registry

| Claim | Status | Evidence Source | Scope | Forensic Audit Notes |
| :--- | :---: | :--- | :--- | :--- |
| **93.39% False-Positive Reduction** | **VERIFIED** | [`evaluation/reports/report.md:L20`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/reports/report.md#L20) | Pinned 10-Task Benchmark | Exact calculation: `(4875 - 322) / 4875 * 100 = 93.3948%`. Baseline had 4,875 FP; ARIA had 322 FP. |
| **"93.39% across 5 repositories"** | **CONTRADICTED** | Previous draft language | Five Qualitative Repos | The quantitative benchmark only evaluated 3 repos (`fastapi`, `requests`, `ARIA`). Claiming it across all 5 is invalid and has been corrected. |
| **4,875 Baseline False Alarms** | **VERIFIED** | [`evaluation/results/results.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/results.json) | Pinned 10-Task Benchmark | Sum of task-by-task baseline file false positives: `853 + 865 + 875 + 29 + 30 + 29 + 749 + 451 + 671 + 323 = 4875`. |
| **322 ARIA False Alarms** | **VERIFIED** | [`evaluation/results/results.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/results.json) | Pinned 10-Task Benchmark | Sum of task-by-task ARIA file false positives: `22 + 29 + 6 + 12 + 9 + 11 + 61 + 67 + 45 + 60 = 322`. |
| **4,553 False Alarms Eliminated** | **VERIFIED** | `evaluation/results/false_positive_analysis.json` | Pinned 10-Task Benchmark | Exact subtraction: `4875 - 322 = 4553`. |
| **FastAPI Core File Count: 3,102** | **VERIFIED** | [`data/architecture/fastapi_fastapi.json:L30`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/data/architecture/fastapi_fastapi.json#L30) | `fastapi/fastapi` Commit `4903347` | `"total_files": 3102` in indexed repository manifest. |
| **FastAPI Core Dependencies: 3,199** | **VERIFIED** | [`data/architecture/fastapi_fastapi.json:L31`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/data/architecture/fastapi_fastapi.json#L31) | `fastapi/fastapi` Commit `4903347` | `"total_dependencies": 3199` in indexed repository manifest. |
| **FastAPI Symbol Count: >200,000** | **CONTRADICTED** | [`data/api_surface/fastapi_fastapi.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/data/api_surface/fastapi_fastapi.json) | `fastapi/fastapi` Commit `4903347` | The JSON file has 202,506 *lines*. At 19 lines per symbol block, actual symbol count is **~10,658 symbols**. Previous draft conflated line count with symbol count. |
| **Stale Ground-Truth Ratio: 27.8%** | **VERIFIED** | [`evaluation/data_quality_report.md:L19`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/data_quality_report.md#L19) | Pinned 10-Task Benchmark | 5 of 18 test files do not exist on disk in pinned commits: `5 / 18 * 100 = 27.777...% ~ 27.8%`. |
| **Interactive P50 Latency: 166.9 ms** | **VERIFIED** | [`evaluation/results/latency.json`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/results/latency.json) | Pinned 10-Task Benchmark | Measured wall-clock latency median across warm ARIA impact analysis runs. |
| **Kubernetes maxRetries: 15** | **VERIFIED** | `pkg/controller/deployment/deployment_controller.go:L67` | `kubernetes/kubernetes` Core | Source declares `const maxRetries = 15`. |
| **PyTorch autograd MAX_DEPTH: 60** | **VERIFIED** | `torch/csrc/autograd/engine.h:L46` | `pytorch/pytorch` Autograd Engine | Source declares `static constexpr int MAX_DEPTH = 60;`. |
| **FastAPI dump_json Rust Fast-Path**| **VERIFIED** | `fastapi/routing.py:L724-745` | `fastapi/routing.py` | Source declares `use_dump_json = response_field is not None and isinstance(response_class, DefaultPlaceholder)`. |
| **LangChain Core Zero-Vendor Deps**| **VERIFIED** | `libs/core/langchain_core/__init__.py:L15` | `langchain_core` Module | Package docstring and pyproject.toml explicitly forbid third-party provider dependencies. |
| **Next.js BaseServer Chokepoint** | **VERIFIED** | `packages/next/src/server/base-server.ts:L180` | `next/server` Runtime Core | Dynamic application requests in NextNodeServer and NextEdgeServer funnel through `BaseServer.handleCatchallRenderRequest`. |

---

## Language & Superlatives Audit

All unverified marketing superlatives have been systematically audited and replaced:
* *"world-class repository intelligence across all codebases"* ➔ **Replaced with:** *"high structural precision in cleanly layered Python, Go, and TypeScript architectures, with documented limitations on dynamic dispatchers."*
* *"zero hallucinations"* ➔ **Replaced with:** *"zero fabricated file paths on physical disk artifacts."*
* *"completely eliminates false positives"* ➔ **Replaced with:** *"reduced false-positive file alerts by 93.39% compared with baseline vector search (322 remaining false positives)."*
* *"insurmountable static barrier"* ➔ **Replaced with:** *"not reliably recoverable from source-only static analysis without runtime trace capture."*
