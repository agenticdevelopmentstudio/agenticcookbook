
- Resolve tokens at a single boundary: a CSS custom-property scope (`:root[data-theme]`,
  `@media (prefers-color-scheme)`), a SwiftUI `Environment`/asset catalog, a Compose
  `MaterialTheme`/`CompositionLocal`, or a WinUI `ResourceDictionary` theme dictionary.
- Theme switching **MUST** be a single state change (swap the set), not per-component conditionals.
- Every semantic token **MUST** be defined in every theme. A missing key is a defect — fail fast in a
  build/test check rather than falling back silently.

