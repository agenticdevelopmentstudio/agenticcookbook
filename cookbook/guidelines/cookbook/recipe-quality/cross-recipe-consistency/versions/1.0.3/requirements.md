
### Terminology

- Sibling recipes (recipes that share the same parent node in the cookbook component tree) MUST use consistent terminology for shared concepts. If one recipe calls the authenticated user a "user", all siblings MUST do the same. Introducing "account", "member", "principal", or "identity" for the same concept in a sibling recipe is a consistency violation.
- When a term is established in an earlier recipe in a family, subsequent sibling recipes MUST adopt it without modification. Authors MUST NOT introduce synonyms for existing terms.
- Where terminology is defined in a cookbook-level glossary or guideline, recipes MUST use the canonical term. Deviating from canonical terminology requires an explicit note in Design Decisions explaining why the deviation is justified.
- Concepts that differ between siblings (e.g., "guest user" vs. "authenticated user") MUST be distinguished using distinct, consistent names — not context-dependent uses of the same word.

### Structural Depth and Detail

- Sibling recipes of comparable complexity SHOULD have comparable section depth. A recipe with 3 behavioral requirements and a sibling of similar functional complexity with 20 behavioral requirements is a consistency signal that one or both recipes are incorrectly scoped.
- "Comparable complexity" is defined by the number of distinct behaviors the component supports, the number of states it can occupy, and the number of error conditions it must handle — not by its visual simplicity.
- When a depth disparity between siblings exists, it MUST be explained. Either the simpler recipe is incomplete (a completeness failure), or the more detailed recipe is over-specified (an authoring quality issue), or the complexity difference is genuinely warranted and SHOULD be noted in Design Decisions.
- No recipe in a sibling group MAY set a depth standard so far above or below the others that it makes the group incoherent to a first-time reader.

### Frontmatter Conventions

- All recipes in a family MUST use the same tag vocabulary. If one recipe in a family uses the tag `form-validation`, all siblings addressing the same concept MUST use `form-validation` — not `validation`, `input-validation`, or `forms`.
- Platform identifiers in the `platforms` field MUST use the cookbook's canonical platform names. A recipe MUST NOT list `iOS` when siblings list `ios`, or `TypeScript` when siblings list `typescript`.
- The `author` field format MUST be consistent across a family (e.g., if siblings use `Given Family`, a new recipe MUST not use `family, given` or an email address).
- `version` fields across a sibling family are independent — each recipe is versioned individually — but the starting version for new recipes MUST be consistent (all start at `1.0.0` or all start at `0.1.0`, as established by the family convention).

### Cross-References

- When a recipe references a sibling recipe in its `related` field or within its body, the reference MUST use the sibling's canonical `domain` URI, not its filename, title, or a freeform description.
- Cross-references in the body text MUST be formatted consistently: if one sibling uses `[Button Recipe](agenticdevelopercookbook://recipes/ui/button)`, all siblings MUST use the same link format — not bare URIs in some and formatted links in others.
- Cross-references MUST be verified at review time to ensure the target recipe exists and the domain URI is correct. Broken cross-references are a consistency failure.
- When a new recipe is added that is relevant to an existing recipe, the existing recipe's `related` field SHOULD be updated to include the new entry. Unidirectional cross-references are acceptable but bidirectional is preferred.

