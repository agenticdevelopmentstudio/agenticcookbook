
1. **Lifecycle callback implementations are natural scope group anchors.** Files that implement `UIApplicationDelegate`, `AndroidApplication`, or equivalent are the entry points of the application — they are architectural seams where scope groups plug in.
2. **Each OS integration point is a potential boundary.** A file that handles push notification payloads is in the notification scope group. A file that handles URL scheme routing is in the routing/deep-link scope group. Treat each OS integration point as a distinct concern.
3. **Background execution code belongs in its own scope group.** Background tasks have distinct lifecycle, resource, and testing constraints. Code that runs in background contexts should not be mixed with foreground UI code.
4. **IPC code is infrastructure.** An app extension that communicates with its host app via shared container is infrastructure-layer code — it should be grouped with other infrastructure, not with the feature it serves.
5. **Lifecycle callbacks that dispatch to many subsystems are composition roots.** An `AppDelegate` that calls 15 different services is a composition root, not a feature — it belongs in an `App` or `Bootstrap` scope group that wires everything together.

