
- Every call that touches a view, window or view-controller state is on the main thread or in a `@MainActor` context.
- No `DispatchQueue.main.sync` from code that may already be on the main thread, and no blocking wait on another queue from the main thread.
- Slow work runs off the main thread, and only the result is applied on it.

