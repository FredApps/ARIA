# ARIA Case Study — Next.js (`vercel/next.js`)

## Repository
- **Name:** `vercel/next.js`
- **Ecosystem:** TypeScript / Rust / Turbopack / Node.js
- **Evaluated Commit:** Head / Active Master Branch snapshot
- **Evaluation Role:** Qualitative Architectural Stress Test (Hybrid Monorepo & Build Manifest Indirection)

---

## Why This Repository Was Selected
Next.js represents full-stack web applications at production scale:
1. Massive polyglot monorepo containing TypeScript client/server libraries and a high-performance Rust compiler (`crates/next-core`, `crates/next-swc`).
2. Dual routing architectures: Pages Router (`pages/`) and App Router (`app/`).
3. React Server Components (RSC) and React Flight wire format protocol.
4. Heavy reliance on build-time compiler generation and runtime manifest indirection.

---

## Architecture Pattern
- **Pattern:** Full-Stack Hybrid Runtime & Compiler Monorepo.
- **Server Core:** `packages/next/src/server/base-server.ts:class BaseServer`
- **Next Server Implementation:** `packages/next/src/server/next-server.ts:class NextNodeServer`
- **App Router Engine:** `packages/next/src/server/app-render/app-render.ts`
- **Compiler Layer:** Rust-based Turbopack crates and Next SWC plugins.

```
Incoming HTTP Request
         │
         ▼
packages/next/src/server/next-server.ts : NextNodeServer.handleCatchallRenderRequest
         │
         ▼
packages/next/src/server/base-server.ts : BaseServer.handleRequest
         │
         ├─► Route Matching (AppPathRoutesManifest, PagesManifest)
         │
         ├─► App Router: packages/next/src/server/app-render/app-render.tsx
         │        │ (RSC Flight Payload Streaming / React DOM Server)
         │        ▼
         └─► Pages Router: packages/next/src/server/render.tsx
                  │ (Legacy HTML SSR / getServerSideProps)
                  ▼
Streamed / Buffer HTTP Response
```

---

## Developer Question
> *"When an HTTP GET request hits an App Router page in Next.js, what is the core server dispatch chain, where are React Server Components (RSC) rendered into the Flight data stream, and how are client boundaries handled?"*

---

## ARIA Analysis
ARIA analyzes the TypeScript module definitions across `packages/next`:
1. **Server Entry Point:** Traces the foundational HTTP request handler down to `BaseServer.handleRequest` (`packages/next/src/server/base-server.ts`) and `NextNodeServer.runImpl` (`packages/next/src/server/next-server.ts`).
2. **App Router Dispatch:** Identifies route matching against generated route manifests (`AppPathRoutesManifest`) and dispatch into `renderToHTMLOrFlight` in `packages/next/src/server/app-render/app-render.tsx`.
3. **Flight Streaming:** Traces how React Server Component elements are transformed into Flight chunk streams using React's server-edge renderers.

---

## Structural Evidence

### Relevant Files
- `packages/next/src/server/base-server.ts`: Abstract base server handling request routing, caching headers, and response streaming.
- `packages/next/src/server/next-server.ts`: Node.js-specific production runtime server.
- `packages/next/src/server/app-render/app-render.tsx`: Core App Router server rendering pipeline.
- `packages/next/src/server/app-render/rsc/flight-render.ts`: React Flight protocol serialization layer.
- `packages/next/src/build/webpack/plugins/next-types-plugin.ts`: Manifest and type generation logic.

### Relevant Symbols
- `class BaseServer` (`packages/next/src/server/base-server.ts`)
- `class NextNodeServer` (`packages/next/src/server/next-server.ts`)
- `function renderToHTMLOrFlight` (`packages/next/src/server/app-render/app-render.tsx`)
- `function doRender` (`packages/next/src/server/render.tsx`)

### Dependency Relationships
- `packages/next/src/server/next-server.ts` subclasses `packages/next/src/server/base-server.ts`
- `packages/next/src/server/next-server.ts` delegates App Router rendering to `packages/next/src/server/app-render/app-render.tsx`
- Build scripts generate manifest JSON artifacts that `base-server.ts` loads at runtime.

### Call Relationships
```
NextNodeServer.handleRequest()
  └─► BaseServer.handleRequest()
        └─► BaseServer.run()
              └─► NextNodeServer.runImpl()
                    └─► NextNodeServer.renderToResponse()
                          └─► renderToHTMLOrFlight()
```

---

## Change-Impact Scenario
**Simulated Scenario:** Modify response header caching or cookie parsing logic in `BaseServer.handleRequest` (`packages/next/src/server/base-server.ts`).

- **ARIA Discovery:**
  - Identifies both `NextNodeServer` (Node.js runtime) and `NextServer` / edge server adapters as direct subclasses.
  - Correctly maps impact across both Pages Router and App Router lifecycles because `BaseServer` is the single root bottleneck.
- **Baseline Vector Search:**
  - Vector search fails to recognize the inheritance hierarchy, matching thousands of unrelated edge middleware examples and cookie-handling utility functions.

---

## Where ARIA Performs Well
1. **TypeScript Class & Interface Tracing:** Maps the deep server hierarchy (`BaseServer` -> `NextNodeServer`) with complete type fidelity.
2. **Server/Client Boundary Awareness:** Traces directive annotations (`"use server"`, `"use client"`) at the syntax tree level.

---

## Where ARIA Loses Fidelity
1. **Generated Build Manifests:** At runtime, Next.js routes are mapped using JSON manifests (`app-paths-manifest.json`, `middleware-manifest.json`) created during the compile step. ARIA's static source analysis cannot inspect artifacts that do not exist until `next build` runs.
2. **Polyglot Rust/TypeScript Boundary:** When Next.js routes execution into Rust compiler crates (`crates/next-core`), ARIA cannot trace cross-language FFI calls from TypeScript into Rust ASTs.

---

## What This Demonstrates
ARIA provides structural clarity through complex TypeScript inheritance hierarchies in large full-stack codebases. However, the presence of runtime-generated build manifests and polyglot boundaries (Rust <-> TypeScript) represents an inherent boundary for source-only static intelligence.

---

## Evidence Classification
- BaseServer inheritance & call hierarchy: `[VERIFIED FACT]`
- App router entry points: `[VERIFIED FACT]`
- Build manifest and polyglot boundaries: `[INFERENCE]`
