---
id: ea5ccc72-7b6e-4aa8-a599-40837f722f38
title: "Modern CSS layout and Baseline-driven adoption"
domain: agenticdevelopercookbook://guidelines/implementing/ui/modern-css
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Adopt modern interoperable CSS features (container queries, @layer, :has(), subgrid, nesting, view transitions) gated on Baseline status with fallbacks."
platforms:
  - web
tags:
  - web
  - css
  - ui
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/ui/layout
  - agenticdevelopercookbook://guidelines/implementing/ui/theming
references:
  - https://web.dev/baseline
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - ui-implementation
---

# Modern CSS layout and Baseline-driven adoption

A cohort of CSS features is now interoperable across modern browsers and can replace JavaScript hacks, viewport-only media queries, and specificity battles. Decide what to ship using the **Baseline** maturity model, not ad-hoc browser checks.

## Decide adoption with Baseline

[Baseline](https://web.dev/baseline) classifies each feature by interoperability across the two most recent major versions of Chrome, Edge, Firefox, and Safari:

- **Newly available** — interoperable across all core browsers as of a recent date. Usable, but older still-in-use versions may lack it.
- **Widely available** — Newly available plus 30 months elapsed. Treat as safe for general production with no fallback.

Requirements:

- Adoption of a CSS feature **MUST** be gated on its Baseline status, not on a single browser's support or anecdotal "Can I Use" glances.
- **Widely available** features **MAY** be used without a fallback.
- **Newly available** features **SHOULD** be used only with a documented fallback or progressive enhancement, because pre-cutoff browser versions still receiving traffic may not support them.
- Pin any Baseline claim to a date — statuses advance over time. Verify against MDN or the Baseline data before assuming current status.

## Feature cohort and current Baseline status

Statuses below are accurate as of 2026-06-09; re-verify before relying on them.

| Feature | What it replaces | Baseline status |
|---|---|---|
| Container queries (`@container`, size) | Viewport `@media` for component-level responsiveness | Newly available (Feb 2023) |
| `:has()` relational selector | JS-driven conditional/parent styling | Newly available (Dec 2023) |
| `@layer` cascade layers | Specificity wars; taming third-party CSS | Newly available |
| Subgrid (`grid-template-*: subgrid`) | Nested grid alignment hacks | Newly available (Sep 2023) |
| Native CSS nesting | Sass/Less just for nesting | Newly available (Aug 2023) |
| Same-document View Transitions | JS animation libs for state changes | Newly available (Oct 2025) |
| Cross-document View Transitions (MPA) | JS route-transition libs | NOT Baseline — no Firefox support |

## Layout and structure

- Author component responsiveness with **container queries** keyed to the component's own size: wrap the component in a query container (`container-type: inline-size`) and use `@container`, so the component adapts wherever it is placed.
- Use **viewport media queries** only for genuinely page-level concerns (overall page shell, print, `prefers-*` user preferences).
- Use **subgrid** to align nested items to an ancestor grid's tracks. Provide a non-subgrid fallback (explicit tracks) only if you target pre-cutoff versions.
- Prefer **logical properties** (`margin-inline`, `inset-block`) over physical ones for internationalization-ready layout.

## Cascade control

- Define an explicit **`@layer`** order (e.g. `@layer reset, base, components, utilities`) so cascade precedence is by layer, not by escalating specificity. Import third-party CSS into a low-priority layer to keep it overridable without `!important`.
- Use **`:has()`** to drive conditional styling from descendant or sibling state instead of toggling classes in JavaScript (e.g. `form:has(:invalid)`, `.card:has(> img)`).
- Use **native nesting** for co-locating related rules; do not nest deeply — flat, shallow rules stay readable and greppable.

## Motion and transitions

- Use the **same-document View Transitions API** (`document.startViewTransition`) for animated state/route changes in SPAs. It is Newly available, so it **MUST** degrade gracefully: when unsupported, the DOM update still applies, just without animation. Feature-detect with `if (document.startViewTransition) { ... } else { /* apply update directly */ }`.
- **Cross-document (MPA) View Transitions are a FORECAST for full interoperability** — they ship in Chromium and Safari but not Firefox as of this writing, so they are NOT Baseline. Use them as pure progressive enhancement only; never make navigation depend on them.
- Respect `prefers-reduced-motion: reduce` and disable or shorten transitions accordingly.

## Anti-patterns

- Do not reach for a CSS-in-JS runtime or a JS animation library when an interoperable native CSS feature covers the need.
- Do not escalate specificity or use `!important` to win the cascade — reach for `@layer` instead.
- Do not gate a feature solely on `caniuse` percentages without checking Baseline tier and whether your traffic includes pre-cutoff versions.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
