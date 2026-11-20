
- Variants (light/dark, density, brand) **SHOULD** be modeled by swapping the semantic layer's primitive references, leaving component tokens untouched.
- Mode-specific values **SHOULD** be expressed as sets/themes resolved at build or runtime; the component contract stays identical across modes.
- Naming **MUST** be consistent and platform-neutral (`color.action.primary`), so the same identifier resolves on every platform.

