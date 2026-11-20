
### Terminology

- **must-use-consistent-sibling-terminology**: Sibling recipes (recipes that share the same parent node in the cookbook component tree) MUST use consistent terminology for shared concepts. If one recipe calls the authenticated user a "user", all siblings MUST do the same. Introducing "account", "member", "principal", or "identity" for the same concept in a sibling recipe is a consistency violation.
- **must-adopt-established-terms**: When a term is established in an earlier recipe in a family, subsequent sibling recipes MUST adopt it without modification. Authors MUST NOT introduce synonyms for existing terms.
- **must-use-canonical-glossary-terms**: Where terminology is defined in a cookbook-level glossary or guideline, recipes MUST use the canonical term. Deviating from canonical terminology requires an explicit note in Design Decisions explaining why the deviation is justified.
- **must-name-differing-concepts-distinctly**: Concepts that differ between siblings (e.g., "guest user" vs. "authenticated user") MUST be distinguished using distinct, consistent names — not context-dependent uses of the same word.

### Structural Depth and Detail

- **should-match-sibling-section-depth**: Sibling recipes of comparable complexity SHOULD have comparable section depth. A recipe with 3 behavioral requirements and a sibling of similar functional complexity with 20 behavioral requirements is a consistency signal that one or both recipes are incorrectly scoped.
  - "Comparable complexity" is defined by the number of distinct behaviors the component supports, the number of states it can occupy, and the number of error conditions it must handle — not by its visual simplicity.
- **must-explain-depth-disparity**: When a depth disparity between siblings exists, it MUST be explained. Either the simpler recipe is incomplete (a completeness failure), or the more detailed recipe is over-specified (an authoring quality issue), or the complexity difference is genuinely warranted and SHOULD be noted in Design Decisions.
- **no-incoherent-depth-standard**: No recipe in a sibling group MAY set a depth standard so far above or below the others that it makes the group incoherent to a first-time reader.

### Frontmatter Conventions

- **must-use-family-tag-vocabulary**: All recipes in a family MUST use the same tag vocabulary. If one recipe in a family uses the tag `form-validation`, all siblings addressing the same concept MUST use `form-validation` — not `validation`, `input-validation`, or `forms`.
- **must-use-canonical-platform-names**: Platform identifiers in the `platforms` field MUST use the cookbook's canonical platform names. A recipe MUST NOT list `iOS` when siblings list `ios`, or `TypeScript` when siblings list `typescript`.
- **must-keep-author-format-consistent**: The `author` field format MUST be consistent across a family (e.g., if siblings use `Given Family`, a new recipe MUST not use `family, given` or an email address).
- **must-keep-starting-version-consistent**: `version` fields across a sibling family are independent — each recipe is versioned individually — but the starting version for new recipes MUST be consistent (all start at `1.0.0` or all start at `0.1.0`, as established by the family convention).

### Cross-References

- **must-reference-siblings-by-uuid**: When a recipe references a sibling recipe in its `related` field or within its body, the reference MUST use the sibling's UUID (in `related`) or an in-text `[<rdid>](cookbook:<uuid>)` link, not its filename, title, or a freeform description.
- **must-format-cross-references-consistently**: Cross-references in the body text MUST be formatted consistently: if one sibling uses `[adc.recipe.ui.button](cookbook:<uuid>)`, all siblings MUST use the same link format — not bare UUIDs in some and formatted links in others.
- **must-verify-cross-references-resolve**: Cross-references MUST be verified at review time to ensure the target recipe exists and the link resolves (`cookr validate`). Broken cross-references are a consistency failure.
- **should-update-existing-related-fields**: When a new recipe is added that is relevant to an existing recipe, the existing recipe's `related` field SHOULD be updated to include the new entry. Unidirectional cross-references are acceptable but bidirectional is preferred.

