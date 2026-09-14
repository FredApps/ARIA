# ARIA Evaluation & Benchmark Suite

Welcome to the public evaluation, benchmark, and reproducibility package for **ARIA** (Autonomous Repository Intelligence & Analysis Engine).

This directory contains everything required to inspect, audit, and reproduce ARIA's evaluation results across both **quantitative change-impact benchmarks** and **qualitative multi-repository architectural stress tests**.

---

## Overview

Software repositories are not flat text collections—they are directed dependency graphs, abstract syntax trees, and typed interface contracts. Standard retrieval-augmented generation (RAG) models index source code as raw unstructured chunks, leading to severe retrieval noise, hallucinated call paths, and broken context boundaries.

ARIA approaches repository intelligence structurally:
- Parsing syntax trees via Tree-sitter.
- Extracting typed symbols, functions, classes, and interfaces.
- Constructing physical file import graphs and logical call hierarchies.
- Providing deterministic graph traversal for change impact, caller resolution, and test pinning.

This evaluation package provides transparent, verifiable evidence measuring ARIA's structural analysis against conventional search baselines.

---

## Evaluation Design

The evaluation package separates empirical evidence into two distinct, rigorous tracks:

```
ARIA Evaluation Package
        │
        ├─► Track A: Quantitative 10-Task Benchmark (Pinned Repositories)
        │            • Repositories: FastAPI, Requests, ARIA
        │            • Scope: 10 Change-Impact Tasks
        │            • Focus: File precision, recall, F1, caller resolution, false positives
        │            • Baseline: Chroma Vector RAG / Text Search
        │
        └─► Track B: Five-Repository Qualitative Stress Test
                     • Repositories: FastAPI, LangChain, Next.js, Kubernetes, PyTorch
                     • Scope: Architectural patterns, frameworks, and language paradigms
                     • Focus: Request lifecycles, dispatcher logic, async boundaries
                     • Policy: Architectural case studies (NOT a quantitative benchmark)
```

### Track A: Quantitative 10-Task Benchmark
- **Scope:** 10 change-impact simulation tasks across three repositories (`fastapi/fastapi`, `psf/requests`, `VarshithReddy2006/ARIA`).
- **Baseline:** Conventional chunked vector search / text retrieval baseline utilizing ChromaDB and BAAI/bge-small-en-v1.5 embeddings.
- **Metrics:** Information retrieval metrics (Precision, Recall, F1) across affected files, callers, and affected test suites.

### Track B: Five-Repository Structural Stress Test
- **Scope:** Deep architectural analysis across five distinct software ecosystems:
  1. `fastapi/fastapi` (Python ASGI, Declarative Dependency Injection)
  2. `langchain-ai/langchain` (Python Composable LCEL, Operator Overloading)
  3. `vercel/next.js` (TypeScript/Rust Monorepo, RSC Flight Streaming)
  4. `kubernetes/kubernetes` (Go Distributed System, Reconcilers, Workqueues)
  5. `pytorch/pytorch` (C++/CUDA Polyglot, C10 Dispatcher, Autograd DAGs)
- **Nature:** Thorough qualitative architectural case studies verifying AST symbol mapping and identifying where source-only static analysis meets runtime boundaries.

> [!IMPORTANT]
> **Quantitative Scope Policy:** The quantitative result—including the 93.39% reduction in false-positive file alerts—is strictly specific to the pinned 10-task benchmark covering FastAPI, Requests, and ARIA. It is **never** presented as a claim across all five qualitative stress-test repositories.

---

## Repositories Under Evaluation

| Repository | Ecosystem | Evaluated Revision | Evaluation Track | Primary Pattern |
|---|---|---|---|---|
| [`fastapi/fastapi`](https://github.com/fastapi/fastapi) | Python / ASGI | `49033471594ea5d99a80abdf1043231b7791ee49` | Both (Track A & B) | Hierarchical Dependency Injection DAG |
| [`psf/requests`](https://github.com/psf/requests) | Python / HTTP | `v2.31.0` snapshot | Track A (Quantitative) | Synchronous HTTP Client & Adapters |
| [`VarshithReddy2006/ARIA`](https://github.com/VarshithReddy2006/ARIA) | Python / AST Engine | Baseline snapshot | Track A (Quantitative) | AST Parser, Symbol Index, Dependency Graph |
| [`langchain-ai/langchain`](https://github.com/langchain-ai/langchain) | Python / AI | Active Master snapshot | Track B (Qualitative) | Composable LCEL Pipeline & Dynamic Tools |
| [`vercel/next.js`](https://github.com/vercel/next.js) | TypeScript / Rust | Active Master snapshot | Track B (Qualitative) | Full-Stack Hybrid Runtime & BaseServer |
| [`kubernetes/kubernetes`](https://github.com/kubernetes/kubernetes) | Go / Cloud | Active Master snapshot | Track B (Qualitative) | Reconciler Loop & Concurrency Workqueue |
| [`pytorch/pytorch`](https://github.com/pytorch/pytorch) | C++ / CUDA / Python | Active Master snapshot | Track B (Qualitative) | C10 Central Bitmask Dispatcher & Autograd |

---

## Benchmark Metrics & Quantitative Summary

On the pinned 10-task benchmark covering `fastapi/fastapi`, `psf/requests`, and `VarshithReddy2006/ARIA`:

| Evaluation Metric | Baseline (Chroma Vector RAG) | ARIA Structural Engine | Performance Delta |
|---|---|---|---|
| **File Retrieval Precision** | 0.028 (2.8%) | **0.106 (10.6%)** | **+7.8% absolute** ($3.8\times$ improvement) |
| **File Retrieval Recall** | **0.917 (91.7%)** | 0.717 (71.7%) | -20.0% absolute (deterministic boundary) |
| **File Retrieval F1 Score** | 0.053 (5.3%) | **0.180 (18.0%)** | **+12.8% absolute** ($3.4\times$ improvement) |
| **Caller Resolution F1** | 0.013 (1.3%) | **0.204 (20.4%)** | **+19.0% absolute** ($15.7\times$ improvement) |
| **Affected Tests F1 (Raw / Valid-GT)** | 0.062 (6.2%) | **0.285 (28.5%) / 0.364 (36.4%)** | **+22.3% / +30.2% absolute** |
| **False-Positive File Alerts** | 4,875 alerts | **322 alerts** | **-4,553 alerts (93.39% noise reduction)** |
| **P50 Latency (ms)** | 235.7 ms | **166.9 ms** | **$1.4\times$ faster response** (sub-200ms warm SLA) |

> [!NOTE]
> Detailed per-task metrics and raw latency breakdowns are located in [`results/metrics.json`](results/metrics.json), [`results/latency.json`](results/latency.json), and [`results/false_positive_analysis.json`](results/false_positive_analysis.json).

---

## Reproducibility

Every quantitative result and structural claim is reproducible using the provided runbook and tools:
- **Runbook:** [`reproducibility/RUNBOOK.md`](reproducibility/RUNBOOK.md) (Complete setup, command execution, and verification guide).
- **Environment:** [`reproducibility/ENVIRONMENT.md`](reproducibility/ENVIRONMENT.md) (Python, Node, Tree-sitter, and OS versions).
- **Repository Hashes:** [`reproducibility/REPOSITORIES.md`](reproducibility/REPOSITORIES.md) (Pinned Git commit SHAs).
- **Runner:** [`benchmarks/run_benchmark.py`](benchmarks/run_benchmark.py) (Reproducible benchmark runner CLI).
- **Verification Command:**
  ```bash
  python evaluation/benchmarks/run_benchmark.py --verify-only
  ```

---

## Key Findings

1. **Massive False-Positive Reduction:** In change-impact analysis, standard semantic search floods context windows with hundreds of loosely related files (e.g. documentation, tutorials, utilities). By constraining search through explicit AST import trees and call graphs, ARIA eliminated 4,553 irrelevant file alerts (a **93.39% reduction** from 4,875 down to 322).
2. **Caller Resolution Breakthrough:** Vector search achieved only 1.3% Caller Resolution F1 across tasks because text chunk embeddings lack call-site semantics. ARIA achieved a **20.4% Caller Resolution F1** (+19.0% absolute improvement) using multi-stage AST semantic resolution.
3. **Sub-second Structural Graph Queries:** Once indexed, graph traversals on in-memory NetworkX directed graphs complete in milliseconds, yielding an interactive warm P50 latency of **166.9 ms** (P95: 451.6 ms) compared to 235.7 ms for the baseline.

---

## Known Limitations & Failure Boundaries

ARIA does not claim omniscient repository understanding. Source-only static analysis exhibits well-defined structural boundaries:

1. **Runtime Operator Dispatch:** In systems like PyTorch (`c10::Dispatcher`), operator execution targets are resolved at runtime via 64-bit bitmasks (`DispatchKeySet`) evaluating dynamic tensor properties. Static AST analysis cannot resolve which kernel will execute.
2. **Ephemeral Dynamic Graphs:** Dynamic computation graphs (such as PyTorch autograd DAGs) are instantiated in C++ heap memory during forward execution. They have no static existence in source code.
3. **Asynchronous Concurrency Boundaries:** In event-driven architectures like Kubernetes, pushing a string key into a workqueue (`queue.Add(key)`) and popping it in another goroutine (`queue.Get()`) severs static AST call-graph edges. The connection is semantic, not syntactic.
4. **Compile-Time Generated Manifests:** Frameworks like Next.js rely on build-time compiler artifacts (`app-paths-manifest.json`) generated by Turbopack/webpack. If these files are not present in source control, static routing resolution is impaired.
5. **Dynamic Tool & Model Ingestion:** In LangChain, agents dynamically configuring tools or selecting LLMs from runtime environment variables exceed deterministic static analysis.

---

## Case Studies

In-depth technical analyses investigating how ARIA models diverse architectures:
- [**FastAPI Case Study**](case-studies/fastapi.md): Declarative routing and hierarchical dependency injection.
- [**LangChain Case Study**](case-studies/langchain.md): LCEL pipelining, operator overloading, and runnable composition.
- [**Next.js Case Study**](case-studies/nextjs.md): Full-stack monorepo, BaseServer routing, and React Flight streaming.
- [**Kubernetes Case Study**](case-studies/kubernetes.md): Informer cache indexing, rate-limiting workqueues, and reconciler loops.
- [**PyTorch Case Study**](case-studies/pytorch.md): C10 dispatcher bitmasks, pybind11 glue, and ATen native kernels.

---

## Demo Scenarios

Step-by-step developer walkthroughs showing how ARIA resolves real-world questions:
- [**FastAPI Dependency Resolution**](demos/fastapi-dependency-resolution.md): Tracing the complete request lifecycle and DI DAG.
- [**LangChain Runnable Execution**](demos/langchain-runnable-execution.md): Tracing LCEL `|` operator composition and config flow.
- [**Next.js Request Flow**](demos/nextjs-request-flow.md): Tracing request handling and RSC Flight serialization.
- [**Kubernetes Controller Flow**](demos/kubernetes-controller-flow.md): Tracing Informer event delivery through workqueue workers.
- [**PyTorch Dispatch**](demos/pytorch-dispatch.md): Tracing `tensor.add()` from Python to ATen C++ SIMD kernels.

---

## Evidence Policy

This evaluation adheres to strict evidence governance:
- Every factual claim is tagged as `[VERIFIED FACT]`, `[INFERENCE]`, `[UNCERTAIN]`, or `[UNRESOLVED]`.
- All quantitative claims are cross-checked in [`reports/CLAIM-VERIFICATION.md`](reports/CLAIM-VERIFICATION.md).
- Stale benchmark ground truth is retained and documented in [`ground_truth/ground_truth.json`](ground_truth/ground_truth.json).
- Marketing superlatives ("world-class", "zero hallucinations", "100% accurate") are explicitly prohibited.
