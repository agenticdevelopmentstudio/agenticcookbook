
- **placement-analysis**: Phase 2 MUST verify the recipe is in the correct directory for its type and that the domain identifier matches the file path.
- **granularity-check**: Phase 2 MUST assess whether the recipe covers exactly one coherent concept. Flag recipes with more than 15 MUST requirements or more than 8 states as potentially too broad. Flag recipes with fewer than 3 requirements as potentially too narrow.
- **overlap-detection**: Phase 2 MUST compare the new/changed content against ALL existing cookbook content (principles, guidelines, and recipes) for conceptual overlap. This includes: identical or near-identical requirement names, duplicate behavioral descriptions, redefinition of concepts that have their own specs.
- **ecosystem-fit**: Phase 2 MUST check whether existing recipes should reference the new content (backlinks), whether new terminology conflicts with established terms, and whether relevant guidelines are referenced.
- **refactoring-proposal**: When overlap or scope issues are found, Phase 2 MUST produce a concrete refactoring proposal specifying exact changes: which requirements to move, merge, or split, and which files are affected.
- **granular-assessment**: Refactoring proposals MUST be per-requirement/section, not per-recipe. A recipe with 10 parts where 2 are valuable MUST have a proposal that extracts those 2.

