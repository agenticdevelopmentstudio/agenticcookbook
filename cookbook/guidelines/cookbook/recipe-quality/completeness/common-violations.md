
- **Empty section with no explanation.** The Accessibility section contains only the heading `## Accessibility` and a single line: "See platform guidelines." The content is not meaningful, and no `NEEDS REVIEW` marker explains what is missing or why.
- **NEEDS REVIEW with no context.** `## States\n\nNEEDS REVIEW` — The marker provides no information about what states are unknown, why they couldn't be determined, or who can resolve the gap. A reviewer reading this cannot act on it.
- **Missing concurrent access edge case.** A recipe for a shared cache component addresses null inputs and boundary values but says nothing about concurrent reads and writes. Concurrent access is directly applicable and its omission is a completeness failure.
- **Test vectors that only cover the happy path.** The Conformance Test Vectors section has eight test vectors, all of which test successful completion. The recipe has four MUST requirements involving error states, none of which have a corresponding test vector.
- **Test vector too vague to produce a PASS/FAIL.** "Test that the button handles errors gracefully." No precondition, no specific action, no measurable outcome. Two testers will reach different conclusions.
- **NEEDS REVIEW as a reminder.** `NEEDS REVIEW: Need to check with design on the hover state colors.` This is a work-in-progress note, not a formal gap declaration. A recipe in this state MUST NOT be submitted for review.
- **No rationale for non-obvious SHOULD.** A requirement states `SHOULD debounce search input by at least 300ms.` The Design Decisions section is empty. The 300ms threshold and the debounce requirement are non-obvious; developers who deviate cannot know whether they are violating a performance constraint or a UX preference.

