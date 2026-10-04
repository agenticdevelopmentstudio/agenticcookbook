
- `exactOptionalPropertyTypes` (TS 4.4) — distinguishes a missing property from one explicitly set to `undefined`. Enable when modeling APIs where "absent" and "present but undefined" differ. It adds real friction with loosely-typed third-party shapes, so it is **opt-in**, not a baseline.
- `erasableSyntaxOnly` (TS 5.8) — errors on TypeScript constructs that emit runtime code (`enum`, `namespace` with runtime members, parameter properties). Enable it when files are run via native type-stripping (Node.js `--experimental-strip-types`/stable type stripping, Bun, Deno, or in-browser transforms) so the source contains no non-erasable syntax. Pair it with `verbatimModuleSyntax`.

