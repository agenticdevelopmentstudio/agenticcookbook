
- `should-default-to-conventional-units`: every recommended group in a convention-following codebase matches a conventional unit, or the findings say why not
- `should-not-decompose-below-conventional-unit`: every conventional unit split across groups cites the other lens's evidence for the split
- `should-elevate-cross-feature-units`: every unit shared by three or more features appears under shared conventional units in a shared group
- `should-flag-convention-deviations`: every deviation found is listed under convention violations
- `should-not-legitimize-misplacement`: no recommended group exists only to hold misplaced logic
- `should-treat-lazy-loaded-modules-as-independent`: every lazy-loaded or code-split module is listed with its trigger as an independent group
- `should-separate-plugin-registry`: the plugin registry is a recommended group of its own, apart from the plugins
- `should-group-mediatr-handlers-by-feature`: every MediatR request and handler sits in its feature domain's group, or the findings say why not
