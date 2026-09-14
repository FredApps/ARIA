# ARIA Case Study — Kubernetes (`kubernetes/kubernetes`)

## Repository
- **Name:** `kubernetes/kubernetes`
- **Ecosystem:** Go / Distributed Systems / Cloud Infrastructure
- **Evaluated Commit:** Head / Active Master Branch snapshot
- **Evaluation Role:** Qualitative Architectural Stress Test (Event-Driven Actor Reconciler & Asynchronous Decoupling)

---

## Why This Repository Was Selected
Kubernetes is the reference implementation of large-scale distributed systems in Go:
1. Massive codebase (~4 million lines of Go code).
2. Event-driven controller-runtime reconciliation loops.
3. Decoupled asynchronous pipelines mediated by `client-go` Informers, Reflector threads, DeltaFIFOs, and rate-limiting Workqueues.
4. Extensive use of generated clients, deep copy routines, and OpenAPI specs (`staging/src/k8s.io/`).

---

## Architecture Pattern
- **Pattern:** Distributed Level-Triggered Event Reconciliation Loop with Asynchronous Caching.
- **Informer Mechanism:** `staging/src/k8s.io/client-go/tools/cache/shared_informer.go:SharedIndexInformer`
- **Queue Abstraction:** `staging/src/k8s.io/client-go/util/workqueue/queue.go:RateLimitingInterface`
- **Reconciliation Engine (Example Deployment):** `pkg/controller/deployment/deployment_controller.go:DeploymentController`

```
API Server (etcd Watch)
       │
       ▼
client-go Reflector ──► DeltaFIFO
                            │
                            ▼
               SharedIndexInformer (Local Cache Indexer)
                            │
                            ▼ Resource Event Handler (Add/Update/Delete)
            workqueue.RateLimitingInterface.Add(key)
                            │
                            │  [ASYNC THREAD BOUNDARY]
                            ▼
          worker() ──► processNextWorkItem()
                            │
                            ▼
          DeploymentController.syncDeployment(key)
                            │
     ┌──────────────────────┼──────────────────────┐
     ▼                      ▼                      ▼
Scale Replicas        Rollout Status        Update PodSpec
     │                      │                      │
     └──────────────────────┼──────────────────────┘
                            ▼
                 API Server Mutation Call
```

---

## Developer Question
> *"When a Kubernetes Deployment object is updated in the API server, how does the deployment controller receive this notification, how does it decouple event receipt from reconciliation via workqueues, and what function actually computes replica delta decisions?"*

---

## ARIA Analysis
ARIA navigates the Go package declarations and struct methods:
1. **Event Registration:** Locates `NewDeploymentController` in `pkg/controller/deployment/deployment_controller.go`. Identifies event registration on `dInformer.Informer().AddEventHandler(...)` calling `enqueueDeployment`.
2. **Asynchronous Boundary:** Traces `enqueueDeployment` pushing string keys (`namespace/name`) into `dc.queue.Add(key)`. Recognizes that this is an asynchronous boundary decoupling the Informer thread from workers.
3. **Reconciler Worker Loop:** Identifies `dc.runWorker` calling `dc.processNextWorkItem`, retrieving keys from the queue, and invoking `dc.syncDeployment(ctx, key)`.
4. **Replica Decision Logic:** Maps `syncDeployment` dispatching to `scale` or `rolloutRecreate`/`rolloutRolling` to calculate the ReplicaSet delta.

---

## Structural Evidence

### Relevant Files
- `pkg/controller/deployment/deployment_controller.go`: Core DeploymentController implementation.
- `pkg/controller/deployment/sync.go`: State synchronization and scale evaluation logic.
- `pkg/controller/deployment/rolling.go`: Rolling update strategy implementation.
- `staging/src/k8s.io/client-go/tools/cache/shared_informer.go`: Informer abstraction maintaining local lister caches.
- `staging/src/k8s.io/client-go/util/workqueue/rate_limiting_queue.go`: Workqueue interface decoupling event arrival from processing.

### Relevant Symbols
- `type DeploymentController struct` (`pkg/controller/deployment/deployment_controller.go`)
- `func NewDeploymentController` (`pkg/controller/deployment/deployment_controller.go`)
- `func (dc *DeploymentController) syncDeployment` (`pkg/controller/deployment/sync.go`)
- `func (dc *DeploymentController) processNextWorkItem` (`pkg/controller/deployment/deployment_controller.go`)
- `type RateLimitingInterface interface` (`staging/src/k8s.io/client-go/util/workqueue/rate_limiting_queue.go`)

### Dependency Relationships
- `pkg/controller/deployment` imports `k8s.io/client-go/tools/cache` and `k8s.io/client-go/util/workqueue`
- `pkg/controller/deployment` consumes generated listers from `k8s.io/client-go/listers/apps/v1`

### Call Relationships
```
DeploymentController.Run()
  └─► go wait.Until(dc.worker, time.Second, stopCh)
        └─► dc.processNextWorkItem()
              ├─► dc.queue.Get()
              ├─► dc.syncHandler(key) == dc.syncDeployment(key)
              │     ├─► dc.getReplicaSetsForDeployment()
              │     ├─► dc.scale()
              │     └─► dc.rolloutRolling()
              └─► dc.queue.Done(key)
```

---

## Change-Impact Scenario
**Simulated Scenario:** Modify the rate-limiting backoff algorithm in `staging/src/k8s.io/client-go/util/workqueue/default_rate_limiters.go`.

- **ARIA Discovery:**
  - Identifies that every controller in `pkg/controller/` (Deployment, DaemonSet, StatefulSet, Node, Namespace, Job) initializes queues using this default limiter.
  - Correctly marks all core controller subsystems as transitively impacted.
- **Baseline Vector Search:**
  - Vector search matches rate-limiting documentation, client HTTP rate limiters, and network policy examples, missing the internal controller queue connections.

---

## Where ARIA Performs Well
1. **Go Struct & Interface Mapping:** Reliably maps Go interface implementations (e.g. matching `syncHandler` function pointers to `syncDeployment`).
2. **Controller Topology:** Reconstructs the structural dependency between controllers, Informers, and workqueues.

---

## Where ARIA Loses Fidelity
1. **Asynchronous Workqueue Decoupling:** In Go, pushing a string key into `dc.queue.Add(key)` and popping it in another goroutine (`dc.queue.Get()`) breaks static AST call graph edges. The connection between `enqueueDeployment` and `syncDeployment` is semantic, not a direct call.
2. **Dynamic Generation & Staging Repositories:** Kubernetes heavily relies on code generators (`k8s.io/code-generator`) and symlinked/vendored `staging/src/k8s.io/` directories, which require specific workspace resolution rules.

---

## What This Demonstrates
ARIA effectively maps Go interfaces, struct fields, and package topologies across a multi-million-line codebase. However, asynchronous concurrency boundaries (channels, queues, goroutines) represent a classic static-analysis discontinuity where call-graph tracing requires high-level architectural understanding.

---

## Evidence Classification
- Controller struct definitions and methods: `[VERIFIED FACT]`
- Informer and workqueue pattern topology: `[VERIFIED FACT]`
- Asynchronous queue call-graph severance: `[INFERENCE]`
