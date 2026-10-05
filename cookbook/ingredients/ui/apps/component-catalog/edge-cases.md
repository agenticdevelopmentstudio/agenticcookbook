
- **No components implemented yet**: Catalog SHOULD show an empty state message (e.g., "No components yet") rather than a blank screen.
- **Component only valid on some platforms**: Use `#if os(...)` around the catalog entry registration. The catalog on excluded platforms SHOULD NOT show that component.

