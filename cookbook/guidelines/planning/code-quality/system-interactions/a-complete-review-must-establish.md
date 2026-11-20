
- `should-anchor-groups-on-lifecycle-callbacks`: whether lifecycle callback implementations serve as scope group anchors
- `should-treat-each-os-integration-point-as-distinct`: whether each OS integration point is treated as a distinct concern
- `should-give-background-code-own-group`: whether background execution code has its own scope group
- `should-not-mix-background-with-foreground-ui`: whether any background-context code is mixed with foreground UI code
- `should-group-ipc-with-infrastructure`: whether IPC code is grouped with infrastructure rather than the feature it serves
- `should-place-composition-roots-in-bootstrap-group`: whether every composition root sits in an `App` or `Bootstrap` group
- `should-treat-each-os-integration-point-as-distinct`: Every OS lifecycle hook, IPC mechanism, background-execution path, or notification/deep-link handler the diff introduces or changes is identified and traced;
- `should-treat-each-os-integration-point-as-distinct`: a diff that introduces none is explicitly cleared.

Scope is the change under review — NOT a whole-codebase inventory.
