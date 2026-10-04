
- **primitive-by-purpose**: Each capability **MUST** use the primitive that matches its purpose — *resources* for read-only context the client/user selects, *prompts* for user-initiated templated workflows, *tools* for model-controlled actions with side effects. Reviewer **MUST** reject a tool that only returns static data (should be a resource).
- **no-overlap**: The same data **SHOULD NOT** be exposed redundantly across primitives without a stated reason.

