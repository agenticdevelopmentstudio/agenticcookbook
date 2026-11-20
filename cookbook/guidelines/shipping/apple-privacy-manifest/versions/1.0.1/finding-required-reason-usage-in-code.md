
- Search the source and dependencies for the trigger symbols, e.g. `cc-grep` (or `grep -rE`) for: `contentModificationDate|creationDate|attributesOfItem|systemUptime|volumeAvailableCapacity|statfs|UserDefaults|NSUserDefaults`.
- Inspect compiled SDKs: a manifest's reasons must cover transitively linked binaries, so scan vendored `.framework`/`.xcframework` symbols, not just first-party Swift.
- After a clean Archive build, confer the **Privacy Report** in Xcode's Organizer (or `xcrun` privacy tooling) to aggregate manifests across the app and its bundles, and reconcile gaps before submitting.

