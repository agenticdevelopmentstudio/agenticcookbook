
| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Component registry | `Shared/Components/` implementations | Component Catalog entries | one-way | Entries registered in `ComponentCatalogView` |
| Platform conditions | Compilation (`#if os(...)`) | Catalog registration | one-way | Entries for unsupported platforms are excluded at compile time |
| Deployment versions | `project.yml` | TestSharedKit and all targets | one-way | One version table applied to every target and the package |

