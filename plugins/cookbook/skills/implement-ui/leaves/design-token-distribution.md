<!-- leaf: implement-ui/design-token-distribution · source: guidelines/implementing/ui/design-token-distribution.md -->

**Rules** (cite as `implement-ui/design-token-distribution#<slug>`):

- `file-tokens-json-single-authority-token-values` MUST — The token source (e.g. a W3C Design Tokens JSON file or tokens.json) MUST be the single authority for token values.
- `transform-tool-generate-platform-outputs-style` SHOULD — A transform tool SHOULD generate platform outputs — Style Dictionary is the established choice (use a current released …
- `generated-outputs-not-hand-edited-edits-belong` MUST — Generated outputs MUST NOT be hand-edited. Edits belong in the source; the build regenerates downstream.
- `output-code-generated-committed-published` SHOULD — Each output SHOULD be code-generated, committed (or published as an artifact), and clearly marked "do not edit by hand" …
- `naming-derived-deterministically-from-token` MUST — Naming MUST be derived deterministically from token paths so the same token resolves to a predictable symbol on every …
- `color-surface-primary-exposed-product-code-raw` SHOULD — Semantic/alias tokens (color.surface.primary) SHOULD be exposed to product code; raw/primitive tokens …
- `drift-check-run-ci-regenerate-fail` SHOULD — A drift check SHOULD run in CI: regenerate, then fail if the working tree differs from committed outputs. This …
- `must-not` MUST — maintain parallel hand-written token files per platform — they drift.
- `must-not-2` MUST — let a platform edit propagate "back up" to the source informally; change the source and regenerate.
- `should-not` SHOULD — hardcode raw values (hex colors, pixel literals) in feature code when a token exists.

# Design token distribution

Design tokens have one source of truth. A build step transforms that source into per-platform artifacts so every platform renders the same colors, spacing, and type from identical values. Tokens flow one way — source to platforms — and generated outputs are build artifacts, never hand-edited.

## One-way flow

- The token source (e.g. a [W3C Design Tokens](https://www.designtokens.org/tr/drafts/format/) JSON file or `tokens.json`) **MUST** be the single authority for token values.
- A transform tool **SHOULD** generate platform outputs — [Style Dictionary](https://styledictionary.com/) is the established choice (use a current released version; verify the latest at build time rather than pinning from memory).
- Generated outputs **MUST NOT** be hand-edited. Edits belong in the source; the build regenerates downstream.
- Regenerate on **every** token change, and run generation in CI so drift fails fast (per fail-fast).
- Version the token source. Treat token releases like any other versioned dependency so consumers can pin and upgrade deliberately.

## Per-platform outputs

| Platform | Generated form | Example |
|----------|----------------|---------|
| swift | Swift constants | `Color`, `CGFloat` static lets in an enum/extension |
| kotlin | Compose values | `Color`, `Dp`, `TextStyle` in an `object` |
| typescript / web | CSS custom properties + TS consts | `--color-accent`, exported token map |
| csharp | WinUI `ResourceDictionary` | `<Color x:Key="...">`, `<x:Double x:Key="...">` |

- Each output **SHOULD** be code-generated, committed (or published as an artifact), and clearly marked "do not edit by hand" with a generated-file header.
- Naming **MUST** be derived deterministically from token paths so the same token resolves to a predictable symbol on every platform.
- Semantic/alias tokens (`color.surface.primary`) **SHOULD** be exposed to product code; raw/primitive tokens (`palette.blue.500`) **SHOULD NOT** be referenced directly in features (per explicit-over-implicit).

## Build integration

- Run generation as a checked-in, reproducible step (a package script or task), not a one-off manual command.
- A drift check **SHOULD** run in CI: regenerate, then fail if the working tree differs from committed outputs. This guarantees outputs always match the source.
- Keep the transform configuration in version control alongside the token source.
- Reach for a managed token pipeline or design-tool sync service only when a measured need justifies it (per YAGNI); a local build step covers most projects.

## Anti-patterns

- **MUST NOT** maintain parallel hand-written token files per platform — they drift.
- **MUST NOT** let a platform edit propagate "back up" to the source informally; change the source and regenerate.
- **SHOULD NOT** hardcode raw values (hex colors, pixel literals) in feature code when a token exists.
