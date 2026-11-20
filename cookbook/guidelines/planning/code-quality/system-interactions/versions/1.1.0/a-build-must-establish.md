
- `should-anchor-groups-on-lifecycle-callbacks`: every lifecycle callback file in the findings is named as an anchor of a recommended group
- `should-treat-each-os-integration-point-as-distinct`: every OS integration point in the findings maps to its own concern, such as the notification or routing/deep-link group, or the findings say why not
- `should-give-background-code-own-group`: every background execution mechanism's files sit in a background scope group, or the findings say why not
- `should-not-mix-background-with-foreground-ui`: no recommended group mixes background-context code with foreground UI code
- `should-group-ipc-with-infrastructure`: every IPC mechanism's files sit in an infrastructure group, not a feature group
- `should-place-composition-roots-in-bootstrap-group`: every lifecycle callback dispatching to many subsystems sits in an `App` or `Bootstrap` group, and is listed as a lifecycle anomaly when it should be decomposed
