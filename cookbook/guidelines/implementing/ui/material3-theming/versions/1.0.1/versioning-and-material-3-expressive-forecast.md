
- Pin the dependency, e.g. `androidx.compose.material3:material3:1.4.x` (stable line as of mid-2026), via the Compose BOM where possible.
- **Material 3 Expressive is NOT stable** (FORECAST). Its APIs (`ExperimentalMaterial3ExpressiveApi`) were removed from the stable 1.4.x line; using Expressive components requires an alpha artifact (e.g. `1.5.0-alphaXX`), and mixing alpha and stable material3 artifacts breaks builds.
- **MUST NOT** blanket-adopt Expressive in production. Default to stable M3 color roles; adopt Expressive only behind a flag, on a pinned alpha, when a concrete UX need justifies the instability.

