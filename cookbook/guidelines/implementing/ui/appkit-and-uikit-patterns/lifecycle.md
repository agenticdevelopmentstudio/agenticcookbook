
- One-time setup is in the load callbacks; per-appearance work is in the appear callbacks; nothing reads `view` in an initializer.
- Every observer, timer or registration added in one callback is removed in its counterpart.
- Child view controllers are added and removed with the full containment sequence.
- On macOS, window content lives in a view controller, not in the window controller.

