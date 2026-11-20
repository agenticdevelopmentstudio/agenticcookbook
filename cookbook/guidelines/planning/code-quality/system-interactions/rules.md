
- **should-anchor-groups-on-lifecycle-callbacks**: Files that implement `UIApplicationDelegate`, `AndroidApplication`, or equivalent **SHOULD** be treated as natural scope group anchors — the architectural seams where scope groups plug in.
- **should-treat-each-os-integration-point-as-distinct**: The analysis **SHOULD** treat each OS integration point as a distinct concern and a potential boundary.
  - A file that handles push notification payloads is in the notification scope group.
  - A file that handles URL scheme routing is in the routing/deep-link scope group.
- **should-give-background-code-own-group**: Background execution code **SHOULD** belong in its own scope group.
- **should-not-mix-background-with-foreground-ui**: Code that runs in background contexts **SHOULD NOT** be mixed with foreground UI code.
- **should-group-ipc-with-infrastructure**: IPC code — such as an app extension that communicates with its host app via shared container — is infrastructure-layer code and **SHOULD** be grouped with other infrastructure, not with the feature it serves.
- **should-place-composition-roots-in-bootstrap-group**: A lifecycle callback that dispatches to many subsystems — an `AppDelegate` that calls 15 different services — is a composition root, not a feature, and **SHOULD** belong in an `App` or `Bootstrap` scope group that wires everything together.
