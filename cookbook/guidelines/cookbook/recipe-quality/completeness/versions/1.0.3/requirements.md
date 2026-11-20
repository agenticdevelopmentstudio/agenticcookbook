
### Section Content

- Every required section MUST contain meaningful content. A section with only a heading and no body content is NOT permitted.
- If a section cannot be filled because the information is unavailable or the concern is not yet analyzed, the section MUST be marked with `NEEDS REVIEW` followed by an explanation that:
  1. States specifically what information is missing (not just "to be completed").
  2. Explains why it could not be determined during recipe creation.
  3. Identifies who or what could resolve the gap (e.g., "requires review of accessibility audit results" or "pending confirmation from the iOS team").
- `NEEDS REVIEW` markers MUST NOT be stacked — multiple gaps in one section MUST each have their own labeled marker explaining the specific gap.
- A `NEEDS REVIEW` marker MUST NOT be used as a placeholder for content the author intends to add later. It is a formal gap declaration, not a reminder note.

### Edge Cases Coverage

- The Edge Cases section MUST address each of the following categories that are applicable to the recipe's domain:
  - **Null and empty input**: What happens when required inputs are null, empty string, zero, or an empty collection?
  - **Boundary values**: What happens at the minimum and maximum valid values for any constrained input?
  - **Concurrent access**: If the component can be accessed or mutated from multiple threads or sessions simultaneously, what is the defined behavior?
  - **Error states**: What happens when a dependency (network, database, file system) is unavailable or returns an error?
  - **Offline or disconnected state**: If the component operates over a network, what happens when connectivity is lost mid-operation?
- If a category is not applicable to the recipe's domain, the recipe MUST include a brief statement explaining why (e.g., "Concurrent access: this component is single-threaded and access is serialized by the main queue.").
- Edge cases MUST NOT be limited to the happy path and one error case. The Edge Cases section MUST reflect deliberate analysis of failure modes, not a minimal token response.
- Each edge case entry MUST state the input or condition, the expected behavior, and whether the behavior is a MUST or SHOULD.

### Conformance Test Vectors

- The Conformance Test Vectors section MUST include at least one test vector for every MUST requirement in the Behavioral Requirements section. No MUST requirement MAY be left without a corresponding test vector.
- Each test vector MUST specify: the precondition or input, the action taken, and the expected observable outcome. Outcome descriptions MUST be concrete enough that two independent testers reach the same PASS/FAIL conclusion.
- Test vectors MUST NOT be limited to happy-path scenarios. Each MUST requirement that involves a failure mode MUST have a test vector that exercises that failure.
- SHOULD requirements SHOULD have test vectors. When SHOULD requirements do not have test vectors, the omission MUST be documented with a rationale.
- Test vectors MUST be numbered or labeled so that individual vectors can be referenced in bug reports and review comments.

### Design Decisions

- If the recipe's Behavioral Requirements section contains any non-obvious constraint — one that a competent developer reading the code would not immediately understand the rationale for — the Design Decisions section MUST explain it.
- The Design Decisions section MUST NOT be empty if any SHOULD requirement exists, because every SHOULD implies a permissible deviation and the rationale for the default MUST be explained.

