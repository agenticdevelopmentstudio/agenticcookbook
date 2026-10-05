
### Catalog behavior

- **catalog-root-view**: Each app's entry point MUST display a `ComponentCatalogView` as its root view.
- **adaptive-navigation**: `ComponentCatalogView` MUST use `NavigationSplitView` on macOS, iPadOS, and visionOS, and `NavigationStack` on iPhone, watchOS, and tvOS.
- **navigable-component-list**: The catalog MUST list all implemented components by name. Selecting a component MUST navigate to its catalog entry view.
- **all-states-per-component**: Each catalog entry view MUST display the component in every state defined in its spec (default, pressed, disabled, focused, loading, etc.), each in its own labeled section.
- **preview-per-entry**: Each catalog entry view MUST include a `#Preview` block.

### Adding a component

- **adding-component-steps**: When adding a new component, the implementer MUST:
  1. Read the component spec from `ui/`
  2. Implement the component in `Shared/Components/`
  3. Create a catalog entry view in `Shared/Catalog/` showing all states
  4. Register the entry in `ComponentCatalogView`
  5. Build all five targets to verify cross-platform compatibility

