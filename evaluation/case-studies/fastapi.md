# ARIA Case Study — FastAPI (`fastapi/fastapi`)

## Repository
- **Name:** `fastapi/fastapi`
- **Ecosystem:** Python / ASGI
- **Evaluated Commit:** `49033471594ea5d99a80abdf1043231b7791ee49`
- **Evaluation Role:** Primary Qualitative Case Study & Pinned Quantitative Benchmark Participant

---

## Why This Repository Was Selected
FastAPI represents the modern Python web API standard. It is architecturally characterized by:
1. Declarative routing coupled with Python typing metadata (`typing.Annotated`, Pydantic models).
2. A recursive, compile-time/request-time Dependency Injection (DI) Directed Acyclic Graph (DAG).
3. Tight upstream inheritance from Starlette (`Starlette`, `Route`, `Router`) and serialization through Pydantic v1/v2 compat layers.
4. Moderate file scale (~160 files in core, 10,658 indexed AST symbols) with deep functional interconnectivity.

---

## Architecture Pattern
- **Pattern:** Declarative Layered Web Framework with Hierarchical Dependency Injection.
- **Entry Points:** `fastapi/applications.py:class FastAPI(Starlette)`
- **Routing Engine:** `fastapi/routing.py:class APIRouter` and `class APIRoute(routing.Route)`
- **DI Engine:** `fastapi/dependencies/utils.py:async def solve_dependencies`
- **Data Serialization:** `fastapi/encoders.py:def jsonable_encoder`

```
Client HTTP Request
       │
       ▼
Starlette ASGI Scope Dispatcher
       │
       ▼
fastapi/routing.py : APIRoute.__call__
       │
       ├─► fastapi/dependencies/utils.py : solve_dependencies()
       │        │ (Traverses Dependant tree, validates via Pydantic)
       │        ▼
       ├─► fastapi/routing.py : run_endpoint_function()
       │        │ (Invokes developer async/sync def endpoint)
       │        ▼
       └─► fastapi/routing.py : serialize_response()
                │ (Encodes response model via jsonable_encoder)
                ▼
HTTP Response to Client
```

---

## Developer Question
> *"When a client initiates an HTTP request against a route decorated with multiple sub-dependencies (`Depends(...)`), what is the exact internal lifecycle sequence, which functions validate parameters, and how is the response payload serialized?"*

---

## ARIA Analysis
ARIA parses the abstract syntax trees, symbol references, and import graphs across `fastapi/` to reconstruct the request lifecycle deterministically:
1. **Route Resolution:** `APIRoute.__call__` intercepts the Starlette ASGI request.
2. **Dependency Resolution:** Identifies `solve_dependencies()` (`fastapi/dependencies/utils.py:L586`) as the core graph evaluator. It recursively resolves sub-dependencies stored within `Dependant` AST nodes (`fastapi/dependencies/models.py:L32`).
3. **Execution Chokepoint:** Maps `run_endpoint_function()` (`fastapi/routing.py:L344`) as the bridge executing synchronous endpoints in a threadpool (`anyio.to_thread.run_sync`) or awaiting asynchronous endpoints.
4. **Serialization Pipeline:** Identifies `serialize_response()` (`fastapi/routing.py:L301`) invoking `fastapi/encoders.py:jsonable_encoder` (`L129`) with custom encoder configurations.

---

## Structural Evidence

### Relevant Files
- `fastapi/applications.py`: Core application class initializing routers and middleware stack.
- `fastapi/routing.py`: Route dispatch logic, endpoint execution wrapper, response serialization.
- `fastapi/dependencies/models.py`: Defines `Dependant`, the data structure representing the DI graph.
- `fastapi/dependencies/utils.py`: Dependency graph solver (`solve_dependencies`, `get_param_sub_dependant`).
- `fastapi/encoders.py`: Type coercion and recursive JSON serialization engine.
- `fastapi/params.py`: Marker classes (`Depends`, `Security`, `Query`, `Body`, `Header`).

### Relevant Symbols
- `class FastAPI` (`fastapi/applications.py:L42`)
- `class APIRoute` (`fastapi/routing.py:L1126`)
- `class APIRouter` (`fastapi/routing.py:L2255`)
- `async def serialize_response` (`fastapi/routing.py:L301`)
- `async def run_endpoint_function` (`fastapi/routing.py:L344`)
- `async def solve_dependencies` (`fastapi/dependencies/utils.py:L586`)
- `class Dependant` (`fastapi/dependencies/models.py:L32`)
- `def jsonable_encoder` (`fastapi/encoders.py:L129`)

### Dependency Relationships
- `fastapi.applications` imports `fastapi.routing.APIRouter`
- `fastapi.routing` imports `fastapi.dependencies.utils.solve_dependencies` and `fastapi.encoders.jsonable_encoder`
- `fastapi.dependencies.utils` imports `fastapi.dependencies.models.Dependant`
- `fastapi.params` provides declarations consumed by `fastapi.dependencies.utils`

### Call Relationships
```
APIRoute.get_route_handler()
  └─► route_handler(request: Request)
        ├─► solve_dependencies()
        │     ├─► check_security()
        │     └─► solve_dependencies() [recursive sub-dependencies]
        ├─► run_endpoint_function()
        │     └─► anyio.to_thread.run_sync() [if not is_coroutine]
        └─► serialize_response()
              └─► jsonable_encoder()
```

---

## Change-Impact Scenario
**Simulated Scenario:** Modify the parameter signature or type validation behavior of `jsonable_encoder` in `fastapi/encoders.py`.

- **ARIA Discovery:**
  - Direct callers detected: `fastapi/routing.py:serialize_response`, `fastapi/responses.py`, `fastapi/utils.py`.
  - Transitive impact: Any route returning non-Pydantic raw data or custom classes; response validation pipelines.
  - Affected test discovery: Pins `tests/test_encoders.py`, `tests/test_tutorial/test_response_model/test_tutorial001.py`.
- **Baseline Behavior:**
  - Semantic vector search matches 50+ files mentioning "JSON", "encode", or "response", causing extreme false-positive noise.

---

## Where ARIA Performs Well
1. **Deterministic Call Tracing:** Successfully traces call paths from `APIRoute` down through `solve_dependencies` to leaf parameter extractors.
2. **Symbol Disambiguation:** Differentiates between `fastapi.params.Depends` (the declaration marker) and `fastapi.dependencies.models.Dependant` (the runtime metadata node).
3. **High File Precision:** Achieves 80.0% precision on FastAPI change-impact tasks, stripping out unrelated router documentation and tutorial examples.

---

## Where ARIA Loses Fidelity
1. **Dynamic Dependency Overrides:** `app.dependency_overrides` is a runtime dictionary mutation on `FastAPI`. ARIA sees the dictionary read in `solve_dependencies`, but cannot statically predict which dependency will be replaced during dynamic test injection.
2. **Pydantic v1 vs v2 Dynamic Indirection:** FastAPI conditionally imports from `pydantic.v1` or `pydantic_core` based on environment introspection. ARIA's static AST sees both import branches without execution context.

---

## What This Demonstrates
This case study demonstrates that for clean, typed Python architectures relying on structural compositions and explicit module imports, ARIA's AST and dependency graphs provide pinpoint architectural and change-impact localization, outperforming vector search by over an order of magnitude in precision.

---

## Evidence Classification
- Entry points & AST line numbers: `[VERIFIED FACT]`
- Lifecycle sequence: `[VERIFIED FACT]`
- Static vs dynamic dependency boundaries: `[INFERENCE]`
