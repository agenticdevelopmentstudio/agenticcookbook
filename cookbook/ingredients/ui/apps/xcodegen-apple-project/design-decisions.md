
**Decision**: Generate the Xcode project from `project.yml` with XcodeGen instead of checking in an `.xcodeproj`.
**Rationale**: The generated project is reproducible and diffable; only the declarative file is reviewed (single source of truth).
**Approved**: pending

**Decision**: The visionOS target MAY fail to build when its SDK is missing; the other four targets still build independently.
**Rationale**: A missing optional SDK should not block work on the other platforms.
**Approved**: pending

