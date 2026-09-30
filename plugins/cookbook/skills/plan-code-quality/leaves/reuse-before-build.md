<!-- leaf: plan-code-quality/reuse-before-build · source: guidelines/planning/code-quality/reuse-before-build.md -->

**Rules** (cite as `plan-code-quality/reuse-before-build#<slug>`):

- `you-check-before-writing-custom` MUST — You MUST check these before writing a custom implementation, nearest first:
- `trivial-functionality-you-take-moment-search-ecosystem` SHOULD — For non-trivial functionality you SHOULD take a moment to search the ecosystem — the package registry and code search …
- `you-need-you-prefer-extending-contributing-upstream` SHOULD — If a library you already use *almost* does what you need, you SHOULD prefer extending it or contributing upstream over …
- `you-confirm-candidate-package-actually` MUST — You MUST confirm a candidate package actually exists, is actively maintained, and is genuinely used before adding it. …
- `you-weigh-dependency-against-building` MUST — You MUST weigh the dependency against building it: for trivial functionality, a little copying is better than taking on …

# Search for existing solutions before building

Agents tend to implement from scratch even when a solution already exists — sometimes inside a framework the project is already using. Before building non-trivial functionality, spend a moment to look for what already solves it.

## Look in this order

You MUST check these before writing a custom implementation, nearest first:

1. **The platform / standard library** — the language or OS may already provide it (see native-controls).
2. **Dependencies you already have** — the capability may already live in a library the project uses. Check before adding anything.
3. **Your own and shared codebases** — a sibling project or shared module may already implement it; reuse beats a parallel copy (see dry).
4. **Proven open source** — battle-tested libraries, evaluated per open-source-preference.

## Research before reinventing

- For non-trivial functionality you SHOULD take a moment to search the ecosystem — the package registry and code search (e.g. GitHub) — for prior art before implementing.
- If a library you already use *almost* does what you need, you SHOULD prefer extending it or contributing upstream over building a parallel implementation.

## Verify before adopting

- You MUST confirm a candidate package actually exists, is actively maintained, and is genuinely used before adding it. Do not install a package name an AI suggested without verifying it — hallucinated and typosquatted names ("slopsquatting") are a real supply-chain attack surface.
- You MUST weigh the dependency against building it: for trivial functionality, a little copying is better than taking on a dependency and its supply-chain and maintenance risk (see dependency-security).
