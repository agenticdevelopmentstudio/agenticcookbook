---
id: e0c6916b-4c1c-49f6-9111-69eb0ee64d2d
title: "Separate server state from client state"
domain: agenticdevelopercookbook://guidelines/planning/ui/state-management
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Keep remote server state in a query/cache layer and UI client state in lightweight local state; never hand-cache server data in a global store."
platforms:
  - web
  - typescript
tags:
  - web
  - state
  - architecture
depends-on: []
related:
  - agenticdevelopercookbook://principles/separation-of-concerns
  - agenticdevelopercookbook://principles/manage-complexity-through-boundaries
references:
  - https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ui-implementation
---

# Separate server state from client state

Application state is not one thing. **Server state** (remote, asynchronous, cacheable, can go stale without your code touching it) and **client state** (UI toggles, modals, form drafts) have different lifecycles and MUST be managed by different mechanisms. Conflating them — typically by copying fetched data into a global client store — is the most common state-management mistake in web UIs.

This guideline covers *data* state ownership. For PRESENTATION states (loading / empty / error / content rendering), see the UI state-design guideline.

## The two kinds of state

| Property | Server state | Client state |
|----------|--------------|--------------|
| Owner | A remote system you don't control | This client session |
| Lifecycle | Can go stale, change behind your back | Changes only when the user/app changes it |
| Sync | Asynchronous, may fail, may be slow | Synchronous, always available |
| Examples | User profile, product list, search results | Open modal, selected tab, theme toggle, unsaved form input |
| Needs | Caching, dedup, refetch, invalidation | Read/write, occasionally shared across components |

## Requirements

- **separate-server-and-client**: Server state and client state MUST be managed by separate mechanisms. Do not store fetched server data in the same construct used for UI toggles.
- **no-hand-cached-server-state**: Server data SHOULD NOT be hand-cached in a global client store (e.g., copying a fetch result into Redux/Zustand and manually keeping it fresh). This is a named anti-pattern: you end up reimplementing caching, deduplication, and invalidation by hand, and the copy drifts from the source of truth.
- **query-layer-for-server-state**: Server state SHOULD live in a dedicated query/cache layer that provides caching, request deduplication, background refetching, and mutation-with-invalidation. The server, not your store, remains the source of truth.
- **local-state-for-client-state**: Client state SHOULD use the lightest mechanism that works — component-local state first, lifting state up when genuinely shared, and a small global store only when many distant components need the same value.
- **context-for-slow-changing-config**: Framework context (e.g., React Context) SHOULD carry slow-changing, app-wide configuration (theme, locale, authenticated user, feature flags) — NOT high-frequency or rapidly-mutating state, because every context value change re-renders all consumers.

## How to choose a mechanism (decision order)

1. **Is it server data?** Put it in a query/cache layer. Cache key = the request identity. Read from the cache; mutate, then invalidate the affected keys to trigger refetch. Do not mirror it elsewhere.
2. **Does only one component need it?** Use component-local state.
3. **Do a few nearby components need it?** Lift the state to the nearest common ancestor and pass it down.
4. **Do many distant components need it?** Use a small client store scoped to that concern.
5. **Is it app-wide config that rarely changes?** Use context.

## Example libraries (not mandates)

These are deliberate, swappable choices — name the role, not the brand. Libraries in this space churn; treat the pattern as durable and the tool as an implementation detail.

- **Server-state / query layer**: TanStack Query (formerly React Query) is a common choice and provides caching, dedup, background refetch, and mutation + invalidation. SWR and RTK Query fill the same role. The framework-agnostic lesson is "use a query cache," not "use this package."
- **Client store**: Zustand and Jotai are lightweight options; Redux Toolkit suits larger apps with structured updates. Reach for one only when local state and lifting genuinely fall short (see YAGNI).
- **Config context**: the framework's built-in context API.

## Anti-patterns to flag in review

- Fetching in a `useEffect` and writing the result into a global store, then manually refetching on focus/interval — that is reimplementing a query cache poorly.
- A single "app state" store that mixes the user list (server) with `isSidebarOpen` (client).
- Putting frequently-changing values in React Context and triggering app-wide re-renders.
- Treating the client store as the source of truth for data that actually lives on the server.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
