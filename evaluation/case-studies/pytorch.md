# ARIA Case Study — PyTorch (`pytorch/pytorch`)

## Repository
- **Name:** `pytorch/pytorch`
- **Ecosystem:** C++ / Python / CUDA / Machine Learning
- **Evaluated Commit:** Head / Active Master Branch snapshot
- **Evaluation Role:** Qualitative Architectural Stress Test (C++ Core, Bitmask Dispatcher, Dynamic Autograd)

---

## Why This Repository Was Selected
PyTorch represents high-performance numerical computing and systems-level ML infrastructure:
1. Massive polyglot codebase combining Python UX bindings with a high-performance C++ core (`c10/`, `aten/`, `torch/csrc/`).
2. Centralized, multi-dimensional operator dispatcher (`c10::Dispatcher`) resolving operations based on device (CPU, CUDA, MPS), layout, and autograd keys via 64-bit bitmasks.
3. Dynamic computation graphs: Autograd backward graphs are dynamically allocated in C++ heap memory during forward execution (`torch::autograd::Node`).
4. Heavy metaprogramming, code generation (`tools/autograd/gen_autograd.py`), and pybind11 interop.

---

## Architecture Pattern
- **Pattern:** Polyglot Dynamic Dispatch Engine with Ephemeral Computation Graphs.
- **Python Surface:** `torch/tensor.py:class Tensor`
- **PyBind11 Bridge:** `torch/csrc/autograd/python_variable.cpp`
- **C10 Dispatcher:** `c10/core/impl/LocalDispatchKeySet.h` and `c10/core/DispatchKey.h`
- **Tensor Operations (ATen):** `aten/src/ATen/core/TensorBody.h`
- **Autograd Engine:** `torch/csrc/autograd/engine.cpp:class Engine`

```
Python User Code:  z = x.add(y)
         │
         ▼
torch/tensor.py / torch/csrc/autograd/python_variable.cpp
         │
         ▼
ATen Native Interface: at::add
         │
         ▼
c10::Dispatcher::findSchemaOrThrow("aten::add")
         │ (Bitmask lookup on DispatchKeySet: CPU, CUDA, Autograd)
         │
         ├─► Autograd Wrapper: torch::autograd::VariableType::add()
         │        │ (Allocates AddBackward0 Node in dynamic graph)
         │        ▼
         └─► Device Kernel: at::native::cpu_add / at::native::cuda_add
                  │ (SIMD Vectorized / CUDA Kernel Launch)
                  ▼
Raw Storage Buffer Mutation
```

---

## Developer Question
> *"When a user calls `tensor.add(other)` in Python with `requires_grad=True`, how does PyTorch dispatch across the Python/C++ boundary, how does the C10 Dispatcher select the kernel, and where is the autograd backward node created in memory?"*

---

## ARIA Analysis
ARIA parses the Python source, pybind registration structures, and C++ header declarations:
1. **Python/C++ Interop:** Traces `torch.Tensor.add` to the pybind C++ binding in `torch/csrc/autograd/python_variable.cpp` exposing the ATen `at::Tensor::add` method.
2. **C10 Dispatch Table:** Identifies `c10::Dispatcher` (`c10/core/Dispatcher.h`). Reconstructs how operators query the thread-local `DispatchKeySet` (evaluating keys like `AutogradCPU`, `CPU`, `CUDA`).
3. **Autograd Hooking:** Identifies the autograd key interception in `torch/csrc/autograd/generated/VariableTypeEverything.cpp` (or generated equivalent) where `AddBackward0` is instantiated and linked to the grad graph.
4. **Kernel Target:** Points to native C++ implementations in `aten/src/ATen/native/BinaryOps.cpp`.

---

## Structural Evidence

### Relevant Files
- `torch/tensor.py`: Python top-level tensor class.
- `torch/csrc/autograd/python_variable.cpp`: Python binding glue mapping method calls to ATen.
- `c10/core/Dispatcher.h`: Central operator dispatch hub.
- `c10/core/DispatchKeySet.h`: Bitmask representation of device and autograd dispatch keys.
- `torch/csrc/autograd/engine.cpp`: Backward execution engine executing gradient DAGs.
- `aten/src/ATen/native/BinaryOps.cpp`: Native C++ kernel implementations.

### Relevant Symbols
- `class Tensor` (`torch/tensor.py`)
- `class Dispatcher` (`c10/core/Dispatcher.h`)
- `class DispatchKeySet` (`c10/core/DispatchKeySet.h`)
- `class Engine` (`torch/csrc/autograd/engine.cpp`)
- `struct Node` (`torch/csrc/autograd/function.h`)

### Dependency Relationships
- `torch` Python bindings depend on `torch/csrc` C++ wrappers.
- `torch/csrc/autograd` depends on `c10` (core dispatcher) and `ATen` (tensor library).
- `aten/src/ATen` utilizes code generation scripts in `tools/codegen/` to generate dispatch tables.

### Call Relationships
```
torch.Tensor.add() [Python]
  └─► THPVariable_add() [C++ Python Binding]
        └─► at::Tensor::add() [ATen]
              └─► c10::Dispatcher::redispatch()
                    ├─► [Key: Autograd] VariableType::add()
                    │     └─► make_node<AddBackward0>()
                    └─► [Key: CPU] at::native::add_kernel()
```

---

## Change-Impact Scenario
**Simulated Scenario:** Modify the dispatch key bitmask ordering or add a new dispatch key (e.g. for custom hardware) in `c10/core/DispatchKey.h`.

- **ARIA Discovery:**
  - Identifies `c10/core/DispatchKeySet.h`, `c10/core/Dispatcher.h`, and every C++ registration macro (`TORCH_LIBRARY_IMPL`, `m.impl(...)`) as directly impacted.
  - Recognizes that operator registration across CPU, CUDA, MPS, and Vulkan backends depends on this enum.
- **Baseline Vector Search:**
  - Vector search returns thousands of unrelated model definition files, test files, and docstrings mentioning "key" or "dispatch".

---

## Where ARIA Performs Well
1. **C++/Python Structural Awareness:** Maps the layout of C++ classes and Python bindings across the repository.
2. **Registration Macro Detection:** Identifies `TORCH_LIBRARY` and `TORCH_LIBRARY_IMPL` macro invocations defining operator schemas.

---

## Where ARIA Loses Fidelity
1. **Runtime Dispatch Bitmask Resolution:** C10 dispatches dynamically at runtime via bitwise operations on 64-bit integer masks (`DispatchKeySet`). Static AST analysis cannot predict which kernel runs without knowing runtime tensor properties (device, dtype, layout).
2. **Dynamic Autograd DAG:** The backward graph is an ephemeral object structure built on the heap during tensor execution. It has no static source-code representation.
3. **Generated Code Artifacts:** Huge swathes of ATen operator bindings are generated by Python scripts (`tools/codegen/gen.py`) during compilation and do not exist in the raw Git tree.

---

## What This Demonstrates
ARIA provides high-level structural guidance and macro tracking across complex polyglot C++/Python architectures. However, dynamic runtime bitmask dispatch, heap-allocated execution graphs, and extensive compile-time code generation establish the ultimate boundary of source-only static intelligence.

---

## Evidence Classification
- C10 Dispatcher and DispatchKey headers: `[VERIFIED FACT]`
- Operator registration mechanics: `[VERIFIED FACT]`
- Dynamic autograd graph and runtime bitmask dispatch boundaries: `[INFERENCE]`
