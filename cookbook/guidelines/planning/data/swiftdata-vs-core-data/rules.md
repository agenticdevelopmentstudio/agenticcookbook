
- The choice **MUST** be justified by OS-version floor, model complexity, and migration needs — never by framework novelty.
- New greenfield apps with an iOS 17+ / macOS 14+ floor **SHOULD** use SwiftData.
- Projects requiring deterministic, fully-controlled migrations or schema versioning **SHOULD** use Core Data, whose multi-stage migration tooling is more mature as of 2026.
- Code targeting OS versions below the SwiftData floor **MUST** use Core Data.
- A project **MUST NOT** rewrite a working Core Data stack into SwiftData purely to modernize; migrate only when a concrete need (new model work, concurrency cleanup) justifies the cost.

