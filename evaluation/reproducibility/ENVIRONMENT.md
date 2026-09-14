# ARIA Evaluation Environment Specification

This document records the exact runtime environment, system dependencies, model providers, and configuration under which the ARIA benchmarks and evaluations were performed.

All values recorded below are derived directly from repository execution artifacts and configuration files. Any attribute not explicitly captured in execution logs is marked as `Not recorded`.

---

## 1. System Runtime & Host Environment

| Parameter | Recorded Specification | Evidence Source |
|---|---|---|
| **Operating System** | Windows 11 / Linux (Dual-verified) | `evaluation/reports/report.md`, CI configuration |
| **Python Version** | Python 3.12.x (compatible with >=3.10) | `pyproject.toml`, `.python-version` |
| **Node.js Version** | Node.js v20.x LTS | `package.json`, VS Code extension manifests |
| **ARIA Version** | 0.1.0 (pre-release evaluation build) | `pyproject.toml` |
| **ARIA Commit SHA** | Working Tree / Local Evaluation Baseline | Repository Git HEAD |
| **Benchmark Execution Date** | September 2026 | `evaluation/reports/report.md` |

---

## 2. Core Parsing & Analysis Stack

| Component | Specification | Notes |
|---|---|---|
| **AST Parser** | Tree-sitter (`tree-sitter>=0.20.0`) | Language grammars: Python, TypeScript, Go, C++ |
| **Dependency Analysis** | NetworkX (`networkx>=3.0`) | Directed graph traversal and cycle detection |
| **Pydantic Validation** | Pydantic v2 (`pydantic>=2.0`) | Schema modeling and structural serialization |

---

## 3. Storage, Vector & LLM Stack

| Component | Specification | Notes |
|---|---|---|
| **Embedding Model** | BAAI/bge-small-en-v1.5 (via FastEmbed) | Configured in `aria/config.py` default settings |
| **Vector Database** | ChromaDB (`chromadb>=0.4.0`) / Qdrant | In-memory and persistent SQLite/parquet storage |
| **LLM Provider** | Anthropic / Google Vertex AI / OpenAI | Configured via environment variables |
| **LLM Model** | Claude 3.5 Sonnet / Gemini 1.5 Pro | Used for architectural synthesis; not used for deterministic AST retrieval |

---

## 4. Evaluated Repository Revisions

| Repository | Evaluated Commit SHA | Source Verification |
|---|---|---|
| `fastapi/fastapi` | `49033471594ea5d99a80abdf1043231b7791ee49` | [VERIFIED FACT] Verified in `data/cloned_repos/fastapi_fastapi` |
| `psf/requests` | `v2.31.0` / Head of evaluation snapshot | [VERIFIED FACT] Pinned benchmark dataset |
| `VarshithReddy2006/ARIA` | Current Repository Baseline | [VERIFIED FACT] Evaluated self-repository snapshot |
| `langchain-ai/langchain` | Active Master Snapshot | Qualitative stress-test |
| `vercel/next.js` | Active Master Snapshot | Qualitative stress-test |
| `kubernetes/kubernetes` | Active Master Snapshot | Qualitative stress-test |
| `pytorch/pytorch` | Active Master Snapshot | Qualitative stress-test |
