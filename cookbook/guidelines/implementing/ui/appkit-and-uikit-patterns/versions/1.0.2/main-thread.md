
- Code MUST touch views, windows, layers that back views, and view-controller state only on the main thread. UI-facing types SHOULD be marked `@MainActor`, following Adopt Swift 6 strict concurrency incrementally ([adc.guideline.implementing.concurrency.swift6-strict-concurrency](cookbook:344b69da-c901-4650-b49d-c2df0234103b)).
- Slow work (disk, network, decoding, image processing) MUST run off the main thread and hop back only to apply the result.
- Code MUST NOT block the main thread waiting for another queue or task.

