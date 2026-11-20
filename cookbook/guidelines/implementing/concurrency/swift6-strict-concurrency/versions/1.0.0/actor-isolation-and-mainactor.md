
- Use `actor` to protect mutable state; its members are isolated and accessed with `await` from outside.
- Annotate UI types and view models that touch UIKit/AppKit/SwiftUI state with `@MainActor`. UI updates **MUST** run on the main actor.
- A function that is `nonisolated` **MUST NOT** access actor-isolated state synchronously.

