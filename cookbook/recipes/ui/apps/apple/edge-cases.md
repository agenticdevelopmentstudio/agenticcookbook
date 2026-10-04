
- **No components implemented yet**: Catalog SHOULD show an empty state message (e.g., "No components yet") rather than a blank screen.
- **Component only valid on some platforms**: Use `#if os(...)` around the catalog entry registration. The catalog on excluded platforms SHOULD NOT show that component.
- **XcodeGen not installed**: Build commands SHOULD fail with a clear error. Prerequisites section documents the install step.
- **visionOS SDK not installed**: The visionOS target will fail to build. This is acceptable — the other four targets SHOULD still build independently.

