
- State restoration is opt-in. On iOS, the app delegate MUST implement the secure save and restore callbacks (`application(_:shouldSaveSecureApplicationState:)` and `application(_:shouldRestoreSecureApplicationState:)`), MUST assign restoration identifiers to the view controllers to preserve, and MUST encode only the data needed to rebuild each one.
- Code MUST save identifiers and small values, not model objects, and MUST rebuild the screen from the model on restore.
- Saved state SHOULD be versioned, and restoration MUST refuse an incompatible version and fall back to the normal launch UI.

