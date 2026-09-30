<!-- leaf: implement-code-quality/typescript-strictness · source: guidelines/implementing/code-quality/typescript-strictness.md -->

**Rules** (cite as `implement-code-quality/typescript-strictness#<slug>`):

- `new-typescript-projects-set-strict-true-tsconfig` MUST — New TypeScript projects MUST set "strict": true in tsconfig.json compilerOptions. This enables the strict family as a …
- `code-not-silence-checker-project-wide` MUST — Code MUST NOT silence the checker with project-wide // @ts-nocheck, blanket any, or skipLibCheck used to hide …
- `flags-strictnullchecks-false-treated-temporary-migration-state` SHOULD — Disabling individual strict-family flags (e.g. "strictNullChecks": false) SHOULD be treated as a temporary migration …
- `new-projects-enable-nouncheckedindexedaccess-verbatimmodulesyntax` SHOULD — New projects SHOULD enable noUncheckedIndexedAccess and verbatimModuleSyntax.
- `type-only-imports-use-import-type-export` MUST — With verbatimModuleSyntax, type-only imports MUST use import type / export type (or inline type modifiers), since the …
- `agents-not-enable-flag-single-sweep` SHOULD — Agents SHOULD NOT enable every flag in a single sweep on an established codebase — small, reviewable diffs keep each …
- `shipped-release-notes-keep-setting-strict-true` MUST — "strict by default" and the removal of legacy module/target modes (e.g. dropping node10 resolution, raising the minimum …

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
