
Enable these on greenfield projects; they close gaps `strict` alone leaves open.

| Flag | Effect | Since |
|------|--------|-------|
| `noUncheckedIndexedAccess` | Adds `undefined` to indexed/array element access, forcing a presence check | TS 4.1 |
| `verbatimModuleSyntax` | Emits imports/exports verbatim; non-`type` imports are kept, `type` imports dropped — predictable ESM/CJS interop | TS 5.0 |

- New projects **SHOULD** enable `noUncheckedIndexedAccess` and `verbatimModuleSyntax`.
- With `verbatimModuleSyntax`, type-only imports **MUST** use `import type` / `export type` (or inline `type` modifiers), since the compiler no longer elides them automatically.

