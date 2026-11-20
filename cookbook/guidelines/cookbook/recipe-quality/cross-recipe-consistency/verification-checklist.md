
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
- [ ] `must-use-canonical-glossary-terms`: Every term a cookbook-level glossary or guideline defines is used in its canonical form, or Design Decisions explains the deviation.
- [ ] `must-name-differing-concepts-distinctly`: Concepts that differ between siblings carry distinct, consistent names, not context-dependent uses of one word.
- [ ] `no-incoherent-depth-standard`: No recipe sets a depth standard so far above or below its siblings that the group is incoherent to a first-time reader.
- [ ] `must-keep-starting-version-consistent`: A new recipe's starting version follows the family convention (`1.0.0` or `0.1.0`).
