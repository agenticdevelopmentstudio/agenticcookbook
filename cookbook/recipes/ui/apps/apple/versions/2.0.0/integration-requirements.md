
- **shared-source-directory**: A `Shared/` directory MUST be added as a source directory to all targets. It contains:
  - `Shared/Components/` — component implementations from `ui/` specs
  - `Shared/Catalog/` — catalog views showing all states per component
- **os-compilation-conditions**: Platform-specific adaptations within shared code MUST use `#if os(...)` compilation conditions.
- **entry-point-shows-catalog**: Each platform's app entry point (the file under `Sources/{platform}/`) MUST present the Component Catalog's `ComponentCatalogView` as its root view.
- **catalog-in-shared-dir**: The catalog implementation MUST live in `Shared/Catalog/` and component implementations in `Shared/Components/`, so all five targets compile the same catalog source.
- **catalog-logging-via-shared-logger**: Catalog events MUST be logged through the `logging` ingredient with category `ComponentCatalog`.

