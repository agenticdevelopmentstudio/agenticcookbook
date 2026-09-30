<!-- leaf: recipes-ui/apps-apple--edge-cases · source: recipes/ui/apps/apple.md -->

# Apple Test App Suite

**Rules** (cite as `recipes-ui/apps-apple--edge-cases#<slug>`):

- `no-components-implemented-yet` SHOULD — Catalog SHOULD show an empty state message (e.g., "No components yet") rather than a blank screen.
- `component-only-valid-on-some-platforms` SHOULD — Use #if os(...) around the catalog entry registration. The catalog on excluded platforms SHOULD NOT show that component.
- `xcodegen-not-installed` SHOULD — Build commands SHOULD fail with a clear error. Prerequisites section documents the install step.
- `visionos-sdk-not-installed` SHOULD — The visionOS target will fail to build. This is acceptable — the other four targets SHOULD still build independently.

## Edge Cases

- **No components implemented yet**: Catalog SHOULD show an empty state message (e.g., "No components yet") rather than a blank screen.
- **Component only valid on some platforms**: Use `#if os(...)` around the catalog entry registration. The catalog on excluded platforms SHOULD NOT show that component.
- **XcodeGen not installed**: Build commands SHOULD fail with a clear error. Prerequisites section documents the install step.
- **visionOS SDK not installed**: The visionOS target will fail to build. This is acceptable — the other four targets SHOULD still build independently.
