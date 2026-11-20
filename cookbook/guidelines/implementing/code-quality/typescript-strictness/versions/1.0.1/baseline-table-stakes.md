
- New TypeScript projects **MUST** set `"strict": true` in `tsconfig.json` `compilerOptions`. This enables the strict family as a unit (`strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictBindCallApply`, `useUnknownInCatchVariables`, and others).
- Code **MUST NOT** silence the checker with project-wide `// @ts-nocheck`, blanket `any`, or `skipLibCheck` used to hide first-party errors. Use a narrowly-scoped `// @ts-expect-error` (with a reason) for the rare unavoidable case so the suppression fails loudly if the underlying type later changes.
- Disabling individual strict-family flags (e.g. `"strictNullChecks": false`) **SHOULD** be treated as a temporary migration state, recorded in code with a tracking reference — not a permanent posture.

