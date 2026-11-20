
A verifier MUST check each of the following items. The recipe PASSES cross-recipe consistency only if every item is satisfied.

- [ ] All terms for shared concepts match the terminology used in sibling recipes.
- [ ] No synonym for an established term is introduced without a documented justification in Design Decisions.
- [ ] Section depth (number of behavioral requirements, states, edge cases) is comparable to sibling recipes of similar complexity, or a documented rationale explains the disparity.
- [ ] All tags use the family's established tag vocabulary — no freeform or ad-hoc tags not used by siblings.
- [ ] Platform identifiers use the cookbook's canonical casing and naming.
- [ ] The `author` field format matches the convention established in the family.
- [ ] All cross-references link the sibling's UUID (`[<rdid>](cookbook:<uuid>)` in text), not filenames or titles.
- [ ] Cross-reference link formatting is consistent with siblings (formatted links vs. bare UUIDs).
- [ ] All cross-reference links resolve to existing recipes in the cookbook (`cookr validate`).
- [ ] Existing related recipes have been updated to include a reference back to this recipe where appropriate.

