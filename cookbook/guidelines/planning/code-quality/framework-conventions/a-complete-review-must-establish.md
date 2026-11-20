
- `should-default-to-conventional-units`: whether the conventional units defined the scope groups where the codebase follows its framework
- `should-not-decompose-below-conventional-unit`: whether any conventional unit was decomposed without strong evidence from another lens
- `should-elevate-cross-feature-units`: whether every unit referenced by three or more feature modules is in a shared scope group
- `should-flag-convention-deviations`: whether every convention deviation is noted
- `should-not-legitimize-misplacement`: whether any scope group legitimizes misplaced logic
- `should-treat-lazy-loaded-modules-as-independent`: whether every lazy-loaded module is an independent scope group
- `should-separate-plugin-registry`: whether the plugin registry is a scope group apart from the plugins
- `should-group-mediatr-handlers-by-feature`: whether MediatR request/handler units are grouped by feature domain
- `should-flag-convention-deviations`: For the units the diff adds or changes, the framework convention they follow is identified and any deviation the change introduces is flagged;
- `should-flag-convention-deviations`: a diff that raises no convention question is explicitly cleared.

Scope is the change under review — NOT a whole-codebase inventory.
