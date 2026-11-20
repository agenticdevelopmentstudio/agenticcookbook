
A verifier MUST check each of the following items. The recipe PASSES completeness only if every item is satisfied.

- [ ] Every required section contains meaningful body content or a properly formatted `NEEDS REVIEW` marker.
- [ ] Every `NEEDS REVIEW` marker identifies what is missing, why it couldn't be determined, and who can resolve it.
- [ ] No section uses `NEEDS REVIEW` as a placeholder for future authoring.
- [ ] The Edge Cases section addresses null/empty input, boundary values, concurrent access (or explains inapplicability), error states, and offline/disconnected state (or explains inapplicability).
- [ ] Each edge case entry states the condition, the expected behavior, and its normative level (MUST/SHOULD).
- [ ] Every MUST requirement in Behavioral Requirements has at least one corresponding numbered test vector.
- [ ] Every test vector specifies a precondition, an action, and a concrete measurable expected outcome.
- [ ] Test vectors cover failure modes, not only the happy path.
- [ ] SHOULD requirements without test vectors have documented rationale for the omission.
- [ ] The Design Decisions section explains any non-obvious MUST constraint.
- [ ] The Design Decisions section is non-empty if any SHOULD requirement exists.

