# ARIA Evaluated Repositories Specification

This document defines the exact repository targets, commit hashes, clone sources, and evaluation roles for both the quantitative benchmark and the qualitative structural stress tests.

---

## 1. Quantitative 10-Task Benchmark Repositories

These three repositories constitute the pinned benchmark dataset evaluated in `evaluation/tasks/tasks.json` and reported in `evaluation/results/metrics.json`.

| Repository | Pinned Commit SHA / Tag | Role in Quantitative Benchmark | Tasks Assigned |
|---|---|---|---|
| [`fastapi/fastapi`](https://github.com/fastapi/fastapi) | `49033471594ea5d99a80abdf1043231b7791ee49` | Core routing, dependency injection DAG, response serialization tasks | `fastapi-task-001`, `fastapi-task-002`, `fastapi-task-003`, `fastapi-task-004` |
| [`psf/requests`](https://github.com/psf/requests) | `v2.31.0` / `b4112e3` (snapshot) | Synchronous HTTP client, adapter pipeline, session cookies | `requests-task-001`, `requests-task-002`, `requests-task-003` |
| [`VarshithReddy2006/ARIA`](https://github.com/VarshithReddy2006/ARIA) | Repository Evaluation Baseline | Self-reflection benchmark: AST parser, symbol graph, indexing pipeline | `aria-task-001`, `aria-task-002`, `aria-task-003` |

---

## 2. Five-Repository Qualitative Stress Test Repositories

These five repositories were analyzed to stress-test ARIA's structural reasoning across differing architectural patterns, scale, and language ecosystems.

| Repository | Cloned Revision / Tag | Primary Languages | Architectural Pattern Evaluated |
|---|---|---|---|
| [`fastapi/fastapi`](https://github.com/fastapi/fastapi) | `49033471594ea5d99a80abdf1043231b7791ee49` | Python | Hierarchical Dependency Injection DAG, Declarative ASGI Routing |
| [`langchain-ai/langchain`](https://github.com/langchain-ai/langchain) | Active Monorepo Snapshot | Python | Composable Pipeline (LCEL), Operator Overloading (`|`), Monorepo |
| [`vercel/next.js`](https://github.com/vercel/next.js) | Active Master Snapshot | TypeScript, Rust, Node.js | Full-Stack Hybrid Runtime, BaseServer Core, RSC Flight Streaming |
| [`kubernetes/kubernetes`](https://github.com/kubernetes/kubernetes) | Active Master Snapshot | Go | Event-Driven Reconciler Loops, Informer Cache Indexing, Workqueues |
| [`pytorch/pytorch`](https://github.com/pytorch/pytorch) | Active Master Snapshot | C++, Python, CUDA | Central C10 Bitmask Dispatcher, Ephemeral Dynamic Autograd DAGs |

---

## 3. Ground-Truth Data Quality Note
As documented in [`evaluation/ground_truth/README.md`](../ground_truth/README.md), the benchmark includes annotations marking stale ground-truth entries (such as test files that do not exist in the evaluated snapshot). ARIA provides dual-mode metric evaluation (`RAW` vs `VALID-GT`) to ensure transparency.
