# ARIA Benchmark & Reproducibility Runbook

This runbook provides complete, step-by-step instructions for installing ARIA, preparing evaluation targets, executing the benchmark runner, and validating evaluation results.

---

## 1. How do I install ARIA?

Clone the repository and set up a virtual environment with Python 3.10+:

```bash
# Clone the repository
git clone https://github.com/VarshithReddy2006/ARIA.git
cd ARIA

# Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies in editable mode
pip install -e .

# Install development and benchmark evaluation dependencies
pip install pytest networkx tree-sitter fastembed chromadb
```

---

## 2. How do I prepare benchmark repositories?

Benchmark target repositories are placed inside `data/cloned_repos/`:

```bash
# Prepare the data directory
mkdir -p data/cloned_repos

# Clone FastAPI at pinned commit SHA
git clone https://github.com/fastapi/fastapi.git data/cloned_repos/fastapi_fastapi
git -C data/cloned_repos/fastapi_fastapi checkout 49033471594ea5d99a80abdf1043231b7791ee49

# Clone Requests at v2.31.0
git clone https://github.com/psf/requests.git data/cloned_repos/psf_requests
git -C data/cloned_repos/psf_requests checkout v2.31.0
```

---

## 3. How do I select a repository revision?

Always check out the exact commit SHA or tag specified in [`REPOSITORIES.md`](REPOSITORIES.md) before running tasks or re-indexing:

```bash
git -C data/cloned_repos/<repo_dir> checkout <commit_sha>
```

---

## 4. How do I run one task?

You can execute a single benchmark task using the benchmark CLI runner:

```bash
# Run a specific task by task_id
python evaluation/benchmarks/run_benchmark.py --task-id fastapi-task-001
```

---

## 5. How do I run the full benchmark?

To execute the entire 10-task quantitative benchmark:

```bash
# Run all tasks defined in evaluation/tasks/tasks.json
python evaluation/benchmarks/run_benchmark.py

# Run in verification mode (validates precomputed metrics against ground truth)
python evaluation/benchmarks/run_benchmark.py --verify-only
```

---

## 6. Where are results written?

Benchmark outputs are written directly to `evaluation/results/`:
- `evaluation/results/metrics.json`: Macro-averaged and task-level precision, recall, and F1 scores.
- `evaluation/results/latency.json`: Execution latency distributions (P50, Mean, P95).
- `evaluation/results/false_positive_analysis.json`: Task-by-task and aggregate false-positive alert counts.
- `evaluation/results/benchmark-report.md`: Human-readable markdown summary report.

---

## 7. How are metrics calculated?

Metrics are computed via [`evaluation/benchmarks/metrics.py`](../benchmarks/metrics.py):
- **Precision:** $\text{TP} / (\text{TP} + \text{FP})$
- **Recall:** $\text{TP} / (\text{TP} + \text{FN})$
- **F1 Score:** $2 \times (\text{Precision} \times \text{Recall}) / (\text{Precision} + \text{Recall})$

Zero denominators return `0.0` safely. Calculations use floating-point math and are rounded to 4 decimal places for reporting.

---

## 8. How are stale ground-truth entries handled?

As documented in [`evaluation/ground_truth/README.md`](../ground_truth/README.md), several expected test files in the baseline benchmark do not exist on disk at the evaluated commit.
- By default, the benchmark runner evaluates against `RAW` ground truth (preserving the exact historical benchmark figures).
- Passing `--valid-gt-only` filters out stale ground truth to calculate clean metrics.

---

## 9. How do I reproduce the five-repository qualitative analysis?

1. Review the detailed case studies in [`evaluation/case-studies/`](../case-studies/):
   - `fastapi.md`, `langchain.md`, `nextjs.md`, `kubernetes.md`, `pytorch.md`
2. Walk through the interactive demos in [`evaluation/demos/`](../demos/):
   - `fastapi-dependency-resolution.md`, `langchain-runnable-execution.md`, `nextjs-request-flow.md`, `kubernetes-controller-flow.md`, `pytorch-dispatch.md`
3. Index each repository target with ARIA's parser to verify symbol locations and line numbers:
   ```bash
   aria index --repo-path data/cloned_repos/fastapi_fastapi
   ```

---

## 10. What environment variables are required?

Copy `.env.example` to `.env` if using live LLM synthesis features:
```bash
# Optional: only required for live LLM response generation
ANTHROPIC_API_KEY=your_key_here
# or
OPENAI_API_KEY=your_key_here
```
Note: **No API keys are required** to run Tree-sitter AST parsing, graph traversal, or metric verification.

---

## 11. What external API keys are required?

Zero external API keys are required for core AST parsing, dependency graph traversal, call-graph construction, or benchmark metric calculation. The structural intelligence engine operates fully offline and locally.

---

## 12. What cannot currently be reproduced automatically?

1. **Live External LLM Responses:** Live responses from proprietary LLMs (Claude, GPT-4) vary slightly across non-zero temperatures and provider model updates.
2. **Ephemeral C++ Runtime Dispatch:** In PyTorch, runtime operator dispatch decisions are mediated by runtime bitmasks in memory, which cannot be statically reproduced without compiling and running PyTorch C++ binaries.
3. **Generated Monorepo Build Manifests:** Next.js and Kubernetes generated client manifests require running their respective build tools (`pnpm build`, `make`) to create on-disk manifest JSON files.
