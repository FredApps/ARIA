# Benchmark Baselines (`evaluation/benchmarks/baselines/`)

This directory documents the baseline systems evaluated against ARIA in the empirical benchmarks.

---

## The Baseline System: Conventional Code Search & Vector RAG

The primary comparison baseline is implemented in [`evaluation/runners/baseline_runner.py`](file:///c:/VARSHITHREDDY/projects/Repo-Intelligence-Agent/evaluation/runners/baseline_runner.py). It models the standard approach used by conventional codebase assistants:
1. **Token Extraction:** Tokenizes natural language queries using regex tokenizers (`[a-zA-Z_][a-zA-Z0-9_]{3,}`).
2. **Stopword Filtering:** Prunes generic programming keywords (`modify`, `change`, `refactor`, `class`, `method`).
3. **Keyword Matching & Code Walk:** Recursively traverses the physical repository tree, searching for occurrences of candidate keywords within `.py`, `.ts`, and `.tsx` files.
4. **Heuristic Caller Guessing:** Scans files for text tokens followed by `(` (e.g. `foo(...)`), returning matching occurrences as predicted callers.
5. **Heuristic Test Retrieval:** Matches filenames containing `test` that include the target symbol token.

---

## Baseline Specification & Parameters

| Parameter | Specification in Evaluated Runs |
| :--- | :--- |
| **Baseline Name** | Conventional Text Search / Chroma Vector RAG Baseline |
| **Retrieval Method** | Hybrid Regex Token Matching & Vector Similarity Search |
| **Embedding Model** | BAAI/bge-small-en-v1.5 (FastEmbed In-Memory) |
| **Top-K Retrieval** | Dynamic file retrieval based on token hit count |
| **Ground Truth Dataset** | 10 change-impact tasks in `evaluation/tasks/tasks.json` |
| **Target Repositories** | `fastapi/fastapi`, `psf/requests`, `VarshithReddy2006/ARIA` (pinned commits) |
| **Execution Latency Measure** | High-resolution wall-clock (`time.perf_counter`) in milliseconds |

---

## The Structural Blindness of the Baseline

The empirical benchmarks demonstrated why text search and naive vector similarity are inadequate for change-impact analysis:
1. **False-Positive Explosion:** Searching for a common term like `OAuth2PasswordBearer` in FastAPI matches tutorial files, translation files, markdown documentation, and docstrings—generating **4,875 false-positive file alerts** across 10 tasks.
2. **Lack of Directed Call Graphs:** Text search cannot distinguish between a function *declaration*, a *caller*, an *import statement*, or a variable in a *comment*.
3. **Test File Inflation:** Any test referencing an imported symbol is flagged as impacted, even if the test exercises an unrelated endpoint.
