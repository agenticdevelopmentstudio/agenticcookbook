
Apply these in order; the first matching row decides.

| If the project... | Choose |
|---|---|
| Must support iOS/iPadOS below 17 (or macOS below 14) | **Core Data** — SwiftData requires iOS 17 / macOS 14+ |
| Shares the store with an Objective-C target or extension | **Core Data** |
| Needs custom multi-stage migrations, model versioning UI, or a large/complex object graph at scale | **Core Data** |
| Needs CloudKit **public** database sync | **Core Data** — SwiftData supports private CloudKit only |
| Is a new app targeting iOS 17+ / macOS 14+ with a straightforward model | **SwiftData** |

When no row above forces Core Data, **SHOULD** default to SwiftData for new code.

