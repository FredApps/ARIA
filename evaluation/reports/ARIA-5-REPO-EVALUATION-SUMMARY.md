# ARIA Evaluation Summary

**Engine:** ARIA (Autonomous Repository Intelligence & Analysis Engine)
**Evaluation Standard:** Deterministic Evidence-Grounded Structural Analysis
**Scope:** Qualitative 5-Repository Stress Test & Pinned 10-Task Quantitative Benchmark

---

## Executive Summary

Conventional codebase AI tools operate via **structural blindness**: they split source files into arbitrary text chunks, embed them into vectors, and retrieve snippets by cosine similarity. While effective for prose, this approach fails on real-world codebases—flooding developers with thousands of false alarms, hallucinating call relationships, and missing architectural boundaries.

ARIA solves this by building a deterministic, AST-grounded repository intelligence layer combining directed dependency graphs, semantic call graphs, symbol indexing, API surface classification, and in-memory fact lookups.

This document summarizes the core findings from two complementary evaluations:
1. A **Five-Repository Qualitative Stress Test** spanning diverse programming languages and architectural models (`fastapi/fastapi`, `langchain-ai/langchain`, `vercel/next.js`, `kubernetes/kubernetes`, `pytorch/pytorch`).
2. A **Pinned 10-Task Quantitative Benchmark** measuring precision, recall, F1, latency, and false-positive noise reduction against a conventional vector/code-search baseline.

---

## What Was Tested

### 1. Five-Repository Qualitative Stress Test
* **`fastapi/fastapi`** (Python): Coroutine request lifecycle, dependency injection DAG, and Pydantic response serialization.
* **`langchain-ai/langchain`** (Python): Universal `Runnable` execution protocol, LCEL composition, and agent decision loops.
* **`vercel/next.js`** (TypeScript/Rust): Hybrid compilation, App Router React Server Components (RSC) Flight streaming, and central server chokepoints.
* **`kubernetes/kubernetes`** (Go): Distributed level-triggered reconciliation, `client-go` shared informers, and rate-limiting workqueues.
* **`pytorch/pytorch`** (C++/Python/CUDA): C10 Dispatcher operator routing, `TensorImpl` memory layouts, and multithreaded autograd backward execution.

### 2. Pinned 10-Task Quantitative Benchmark
* Evaluated across 10 realistic developer change-impact tasks on pinned commits of `fastapi/fastapi`, `psf/requests`, and `VarshithReddy2006/ARIA`.

---

## Quantitative Benchmark Result

On the pinned 10-task benchmark, ARIA demonstrated a massive reduction in developer noise compared to the conventional search/vector baseline:

* **False-Positive File Alerts:** Reduced from **4,875 to 322 files**—eliminating **4,553 false alarms (-93.39% noise reduction)**.
* **File Retrieval F1 Score:** Increased from **5.3% to 18.0% (+12.8% F1 improvement)**.
* **Caller Identification F1:** Increased from **1.3% to 20.4% (+19.0% F1 improvement)**.
* **Affected Test Identification:** Achieved **36.4% F1** and **69.0% recall** on verified ground-truth test files.
* **Interactive Latency:** Delivered a sub-200ms warm query latency (**P50 = 166.9 ms**).

> *Scope Clarification:* This quantitative result was measured on the pinned 10-task benchmark across FastAPI, Requests, and ARIA; it is not claimed as an aggregate result across all five qualitative repositories.

---

## Five-Repository Stress Test Findings

| Repository | Paradigm | Static Resolution Confidence | Primary Architectural Chokepoint | Primary Static Limitation |
| :--- | :--- | :--- | :--- | :--- |
| `fastapi/fastapi` | Layered Monolith | **High (92%)** | `fastapi/routing.py:get_request_handler` | Dynamic dictionary lookup tables (`ENCODERS_BY_TYPE`) |
| `langchain-ai/langchain` | Functional Protocols | **Moderate (74%)** | `runnables/base.py:Runnable` | Abstract provider model dispatch & non-deterministic tool choice |
| `vercel/next.js` | Compiler/Runtime Hybrid | **Moderate (68%)** | `server/base-server.ts:BaseServer` | Build-time JSON manifests bridging RSC Flight client components |
| `kubernetes/kubernetes` | Distributed State Machine | **High (84%)** | `client-go/tools/cache/shared_informer.go` | Asynchronous Go channel workqueues decoupling event handlers |
| `pytorch/pytorch` | Polyglot Dispatch Engine | **Low / Uncertain (35%)** | `c10/core/TensorImpl.h:TensorImpl` | 64-bit runtime `DispatchKeySet` bitmask routing & dynamic autograd graphs |

---

## Strongest Capabilities

1. **Deterministic False-Positive Suppression:** Pruning >93% of keyword search noise by traversing real AST import and call graphs.
2. **Blast-Radius & Impact Bucketing:** Accurately segmenting affected production files from targeted regression tests in under 200ms.
3. **Architectural Chokepoint Discovery:** Pinpointing single points of failure (e.g. `BaseServer` in Next.js, `TensorImpl` in PyTorch) through graph fan-in and fan-out centrality.
4. **Epistemic Discipline:** Distinguishing verified facts from inferences and dynamic uncertainty, eliminating hallucinated file paths.

---

## Failure Boundaries

ARIA loses fidelity at specific architectural boundaries where static source code analysis is fundamentally insufficient:
1. **Execution-Time Computation Graphs (PyTorch Autograd):** Reverse-mode autograd graphs do not exist in source code; they are dynamically recorded in heap memory during forward execution.
2. **Dynamic Runtime Dispatchers (PyTorch C10):** Operator calls route through dynamic bitmask tables that require runtime device and context state.
3. **Decoupled Concurrency Channels (Kubernetes Workqueues):** Thread-safe asynchronous queues sever direct static call edges between event handlers and worker loops.
4. **Build-Time Manifest Bridges (Next.js):** Client component IDs are strings resolved via build-time compiler manifests rather than static ES6 imports.

---

## Final Conclusion

ARIA is not a chatbot over source files. It is an **autonomous structural repository intelligence system**.

It provides exceptional value when analyzing explicitly connected, statically typed, or dependency-injected codebases, drastically reducing developer cognitive load during refactoring. At the boundaries of dynamic runtime dispatch and execution-time graph creation, ARIA transparently reports uncertainty rather than hallucinating false certainty.

---

## Detailed Reports & Assets
* Full Evaluation Document: [`ARIA-5-REPO-EVALUATION-FINAL.md`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/reports/ARIA-5-REPO-EVALUATION-FINAL.md)
* Claim Verification Audit: [`CLAIM-VERIFICATION.md`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/reports/CLAIM-VERIFICATION.md)
* Case Studies: [`evaluation/case-studies/`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/case-studies/)
* Public Demos: [`evaluation/demos/`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/demos/)
* Reproducibility Runbook: [`evaluation/reproducibility/RUNBOOK.md`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/reproducibility/RUNBOOK.md)
