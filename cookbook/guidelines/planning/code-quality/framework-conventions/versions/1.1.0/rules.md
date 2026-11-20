
- **should-default-to-conventional-units**: When the codebase follows framework conventions, those conventions **SHOULD** define the scope groups — framework-conventional units are the default scope group.
- **should-not-decompose-below-conventional-unit**: The analysis **SHOULD NOT** decompose below the conventional unit without strong evidence from other lenses.
- **should-elevate-cross-feature-units**: A ViewModel or service referenced by three or more feature modules is no longer feature-local and **SHOULD** be placed in a shared scope group — cross-feature sharing elevates to its own scope group.
- **should-flag-convention-deviations**: When a codebase violates framework conventions — for example logic placed in the wrong layer (business logic in a view) — the analysis **SHOULD** note the deviation — deviations are flagged, not respected.
- **should-not-legitimize-misplacement**: The analysis **SHOULD NOT** create a scope group that legitimizes a misplacement.
- **should-treat-lazy-loaded-modules-as-independent**: Any module configured for lazy loading in Angular, Next.js dynamic imports, or Webpack code splitting **SHOULD** be treated as an independent scope group — lazy-loaded modules are independent scope groups.
- **should-separate-plugin-registry**: The registry that loads and wires plugins **SHOULD** be a separate scope group from the plugins themselves — plugin/extension registries are composition roots.
- **should-group-mediatr-handlers-by-feature**: MediatR `Query`/`Command` + `Handler` units **SHOULD** be grouped by feature domain.
