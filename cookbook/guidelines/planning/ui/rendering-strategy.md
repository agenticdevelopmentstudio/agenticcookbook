---
id: f35cf9c3-7488-4192-93fb-12d95f7244e5
title: "Choose a rendering strategy per route, minimize client JS"
domain: agenticdevelopercookbook://guidelines/planning/ui/rendering-strategy
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pick a rendering strategy per route to minimize how much JavaScript reaches the client and when, treating it as an architecture decision not a framework mandate."
platforms:
  - web
  - typescript
tags:
  - web
  - performance
  - architecture
depends-on: []
related:
  - agenticdevelopercookbook://principles/simplicity
  - agenticdevelopercookbook://principles/meta-principle-optimize-for-change
  - agenticdevelopercookbook://guidelines/implementing/ui/core-web-vitals
references:
  - https://react.dev/reference/rsc/server-components
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ui-implementation
  - performance-optimization
---

# Choose a rendering strategy per route, minimize client JS

The amount of JavaScript that reaches the client — and *when* it arrives — is the primary lever on Interaction to Next Paint (INP) and Largest Contentful Paint (LCP). There is no single winning strategy: the industry has converged on hybrid, per-route rendering. Choose the strategy per route based on that route's job, and default to shipping less client JS.

## Core principle

- The decision variable is **how much JavaScript reaches the client, and when**. Frame rendering as an architecture-selection decision, not a framework choice.
- You **SHOULD** select a rendering strategy **per route**, not one strategy for the whole app. A marketing landing page and a logged-in dashboard have different constraints.
- You **MUST NOT** mandate a framework to satisfy this guideline. The same per-route reasoning applies to React, Svelte/SvelteKit, Vue/Nuxt, Astro, SolidStart, Qwik, and others.
- Note: INP replaced FID as a Core Web Vital on 2024-03-12. Optimize for INP and LCP; do **not** target FID.

## Strategy selection by route type

| Route type | Recommended strategy | Why |
|---|---|---|
| Content-heavy, mostly static (docs, blog, marketing) | Static generation (SSG) + islands | Near-zero client JS; hydrate only interactive islands |
| Dynamic but cacheable | SSR with caching / ISR-style revalidation | Fresh HTML, cheap to serve, fast LCP |
| Personalized / data-driven app pages | Streaming SSR with Suspense | First paint streams while data resolves; lower TTFB-to-content |
| Highly interactive, slow-startup-dominated | Resumability (e.g. Qwik) or aggressive code-splitting | Avoids large hydration cost at startup |
| Behind auth, no SEO need | Client-side render (SPA) only if SSR adds no value | Simplicity when crawlability and first-paint don't matter |

- You **SHOULD** prefer islands/partial hydration for pages that are mostly content with a few interactive widgets.
- You **SHOULD** use streaming SSR (Suspense boundaries) for app pages that depend on slow data, so the shell paints before data resolves.
- You **MUST** measure the client JS bytes per route (initial + hydration) and treat regressions as defects, not cosmetics.

## React Server Components (React-specific note)

React Server Components (RSC) are the default for new high-performance **React** apps — but they are not a universal web requirement and apply only when you have already chosen React.

- RSC is only usable **through a framework**. As of 2026: the **Next.js App Router is the mature, production-proven** RSC implementation. **React Router v7 RSC support is newer and less stable** — treat it as evolving, and pin to a tested release before relying on it.
- RSC moves component work to the server so component code and its dependencies do **not** ship to the client; you **SHOULD** keep `"use client"` boundaries small and push interactivity to leaf components.
- RSC adds **real complexity**: a server/client boundary you must reason about, serialization constraints on props, and **framework lock-in**. Adopt it deliberately, not reflexively.
- You **MUST NOT** introduce RSC to a non-React stack or to a React app where the server/client split adds no measurable benefit — that violates simplicity.

## Decision hygiene

- You **SHOULD** record the chosen strategy per route (e.g. in the route's plan or a routing manifest) with a one-line rationale, so the decision is reversible and auditable.
- You **SHOULD** keep strategies swappable: avoid coupling business logic to a rendering mode so a route can move from SSR to SSG (or vice versa) as requirements change.
- You **MUST** validate the choice against real metrics (INP, LCP, TTFB, JS transfer size) on representative routes before locking it in.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
