
- **Component added on one platform only**: When a component is registered under `#if os(...)`, the project MUST still build for the other four targets, and the catalog on the excluded platforms MUST omit it.
- **Missing visionOS SDK with new components**: Adding a component while the visionOS SDK is absent MUST NOT block building and verifying the other four targets.
- **Empty `Shared/Catalog/`**: With no catalog entries, every target MUST still build and show the catalog's empty state rather than a blank screen.

