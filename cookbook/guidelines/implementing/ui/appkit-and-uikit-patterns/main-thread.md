
- Touch views, windows, layers that back views, and view-controller state only on the main thread. Mark UI-facing types `@MainActor` and follow [Adopt Swift 6 strict concurrency incrementally](agenticdevelopercookbook://guidelines/implementing/concurrency/swift6-strict-concurrency).
- Do slow work (disk, network, decoding, image processing) off the main thread and hop back only to apply the result.
- Do not block the main thread waiting for another queue or task.

