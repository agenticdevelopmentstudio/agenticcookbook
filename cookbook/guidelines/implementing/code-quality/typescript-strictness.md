---
id: 5662987f-fd56-4a3a-a519-672187207745
title: "TypeScript strictness configuration"
domain: agenticdevelopercookbook://guidelines/implementing/code-quality/typescript-strictness
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Set strict: true on every new TypeScript project and adopt the stricter index/module flags incrementally."
platforms:
  - typescript
tags:
  - typescript
  - type-safety
  - config
depends-on: []
related:
  - agenticdevelopercookbook://principles/fail-fast
  - agenticdevelopercookbook://principles/explicit-over-implicit
references:
  - https://www.typescriptlang.org/tsconfig/strict.html
  - https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html
  - https://www.typescriptlang.org/tsconfig/verbatimModuleSyntax.html
  - https://github.com/microsoft/TypeScript/issues/63293
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - new-module
---

# TypeScript strictness configuration

A type checker that admits `any` and unchecked access is a linter, not a safety net. Configure `tsconfig.json` so the compiler catches the errors it is capable of catching, and adopt the stricter flags deliberately rather than all at once.

## Baseline (table stakes)

- New TypeScript projects **MUST** set `"strict": true` in `tsconfig.json` `compilerOptions`. This enables the strict family as a unit (`strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictBindCallApply`, `useUnknownInCatchVariables`, and others).
- Code **MUST NOT** silence the checker with project-wide `// @ts-nocheck`, blanket `any`, or `skipLibCheck` used to hide first-party errors. Use a narrowly-scoped `// @ts-expect-error` (with a reason) for the rare unavoidable case so the suppression fails loudly if the underlying type later changes.
- Disabling individual strict-family flags (e.g. `"strictNullChecks": false`) **SHOULD** be treated as a temporary migration state, recorded in code with a tracking reference — not a permanent posture.

## Recommended near-defaults

Enable these on greenfield projects; they close gaps `strict` alone leaves open.

| Flag | Effect | Since |
|------|--------|-------|
| `noUncheckedIndexedAccess` | Adds `undefined` to indexed/array element access, forcing a presence check | TS 4.1 |
| `verbatimModuleSyntax` | Emits imports/exports verbatim; non-`type` imports are kept, `type` imports dropped — predictable ESM/CJS interop | TS 5.0 |

- New projects **SHOULD** enable `noUncheckedIndexedAccess` and `verbatimModuleSyntax`.
- With `verbatimModuleSyntax`, type-only imports **MUST** use `import type` / `export type` (or inline `type` modifiers), since the compiler no longer elides them automatically.

## Optional, situational flags

- `exactOptionalPropertyTypes` (TS 4.4) — distinguishes a missing property from one explicitly set to `undefined`. Enable when modeling APIs where "absent" and "present but undefined" differ. It adds real friction with loosely-typed third-party shapes, so it is **opt-in**, not a baseline.
- `erasableSyntaxOnly` (TS 5.8) — errors on TypeScript constructs that emit runtime code (`enum`, `namespace` with runtime members, parameter properties). Enable it when files are run via native type-stripping (Node.js `--experimental-strip-types`/stable type stripping, Bun, Deno, or in-browser transforms) so the source contains no non-erasable syntax. Pair it with `verbatimModuleSyntax`.

## Adopt incrementally on existing code

The stricter flags surface real defects but generate large error volumes on legacy code. Per `agenticdevelopercookbook://principles/small-reversible-decisions`:

- Turn on `strict` first; land that as its own change.
- Enable one stricter flag at a time (`noUncheckedIndexedAccess`, then `exactOptionalPropertyTypes`, etc.), fixing the fallout before moving on.
- Agents **SHOULD NOT** enable every flag in a single sweep on an established codebase — small, reviewable diffs keep each step reversible.

## FORECAST — not yet relied upon as shipped

Treat the following as roadmap/proposed behavior. Do **not** write configs or guidance that assume it as current.

- The **native Go compiler ("tsgo", "Project Corsa")** and the **TypeScript 7.0** line are a proposed reimplementation targeting large build speedups. As of this writing, confirm actual release state against the official [TypeScript blog](https://devblogs.microsoft.com/typescript/) and [microsoft/typescript-go](https://github.com/microsoft/typescript-go) before depending on it.
- "**strict by default**" and the **removal of legacy module/target modes** (e.g. dropping `node10` resolution, raising the minimum target) are PLANNED breaking changes discussed for the 6.0/7.0 line. Until you have verified them in shipped release notes, **MUST** keep setting `"strict": true` explicitly rather than relying on an implicit default.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
