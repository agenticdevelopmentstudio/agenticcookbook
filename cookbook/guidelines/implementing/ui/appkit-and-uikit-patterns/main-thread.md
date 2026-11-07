
- Code MUST touch views, windows, layers that back views, and view-controller state only on the main thread. UI-facing types SHOULD be marked `@MainActor`, following [Adopt Swift 6 strict concurrency incrementally](agenticdevelopercookbook://guidelines/implementing/concurrency/swift6-strict-concurrency).
- Slow work (disk, network, decoding, image processing) MUST run off the main thread and hop back only to apply the result.
- Code MUST NOT block the main thread waiting for another queue or task.

