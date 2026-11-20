
- **should-look-for-existing-solution**: Before building non-trivial functionality, you **SHOULD** spend a moment to look for what already solves it.
- **must-check-existing-solutions-nearest-first**: You **MUST** check these before writing a custom implementation, nearest first:
  1. **The platform / standard library** — the language or OS may already provide it (see native-controls).
  2. **Dependencies you already have** — the capability may already live in a library the project uses.
  3. **Your own and shared codebases** — a sibling project or shared module may already implement it (see dry).
  4. **Proven open source** — battle-tested libraries, evaluated per open-source-preference.
- **should-check-dependencies-before-adding**: You **SHOULD** check the dependencies you already have before adding anything.
- **should-search-ecosystem-for-prior-art**: For non-trivial functionality you **SHOULD** take a moment to search the ecosystem — the package registry and code search (e.g. GitHub) — for prior art before implementing.
- **should-prefer-extending-existing-library**: If a library you already use *almost* does what you need, you **SHOULD** prefer extending it or contributing upstream over building a parallel implementation.
- **must-verify-candidate-package**: You **MUST** confirm a candidate package actually exists, is actively maintained, and is genuinely used before adding it.
- **should-not-install-unverified-ai-suggested-package**: You **SHOULD NOT** install a package name an AI suggested without verifying it.
- **must-weigh-dependency-against-building**: You **MUST** weigh the dependency against building it: for trivial functionality, a little copying is better than taking on a dependency and its supply-chain and maintenance risk (see dependency-security).
