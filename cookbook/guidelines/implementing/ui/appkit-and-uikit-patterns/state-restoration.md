
- State restoration is opt-in. On iOS, the app delegate implements the secure save and restore callbacks (`application(_:shouldSaveSecureApplicationState:)` and `application(_:shouldRestoreSecureApplicationState:)`), assigns restoration identifiers to the view controllers to preserve, and encodes only the data needed to rebuild each one.
- Save identifiers and small values, not model objects. Rebuild the screen from the model on restore.
- Version the saved state and refuse to restore from an incompatible version, then fall back to the normal launch UI.

