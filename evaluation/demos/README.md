# ARIA Developer Demos & Interactive Walkthroughs

## Overview
This directory contains end-to-end developer walkthroughs demonstrating how ARIA analyzes complex real-world codebases. Unlike generic LLM chat interfaces that ingest raw text files into context windows, ARIA constructs structural graph representations of codebases—traversing AST definitions, symbol tables, dependency imports, and call graphs to answer technical engineering questions with verified evidence.

---

## Demo Scenarios

| Demo Scenario | Repository | Ecosystem | Architectural Pattern Highlighted | Static Analysis Boundary Explored |
|---|---|---|---|---|
| [FastAPI Dependency Resolution](fastapi-dependency-resolution.md) | `fastapi/fastapi` | Python / ASGI | Hierarchical Dependency Injection DAG | Dynamic `dependency_overrides` |
| [LangChain Runnable Execution](langchain-runnable-execution.md) | `langchain-ai/langchain` | Python / AI | LCEL Composable Pipeline & Operator Overloading | Dynamic Tool/Model Ingestion |
| [Next.js Request Flow](nextjs-request-flow.md) | `vercel/next.js` | TypeScript / Rust | BaseServer Core & RSC Flight Streaming | Compile-Time Generated Manifests |
| [Kubernetes Controller Flow](kubernetes-controller-flow.md) | `kubernetes/kubernetes` | Go / Distributed | Reconciler Loop & Informer Cache Indexing | Asynchronous Workqueue Boundary |
| [PyTorch Operator Dispatch](pytorch-dispatch.md) | `pytorch/pytorch` | C++ / CUDA / Python | C10 Central Operator Dispatcher & ATen | Dynamic Bitmask Dispatch & Heap Autograd DAG |

---

## Demo Structure

Each demo follows a consistent developer-facing anatomy:
1. **Developer Question:** A real-world architectural or change-impact question.
2. **Structural Pipeline:** Step-by-step trace through ARIA's analysis engine:
   ```
   Developer Question
           │
           ▼
   Structural Context Query
           │
           ▼
   Symbol & AST Discovery
           │
           ▼
   Dependency & Call Graph Traversal
           │
           ▼
   Change Impact & Test Pinning
           │
           ▼
   Evidence-Backed Answer
   ```
3. **Verified Code References:** Exact file paths, symbol names, and line numbers verified against indexed ASTs.
4. **Boundary & Fidelity Analysis:** Honest accounting of where static analysis stops and runtime behavior begins.
