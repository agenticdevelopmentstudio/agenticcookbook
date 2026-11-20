
- **should-shape-boundaries-to-target-architecture**: SHOULD deliberately shape team and agent boundaries to match the architecture you want, then let the system grow into them (the "inverse Conway maneuver").
- **should-treat-agent-assignment-as-architecture**: Agent assignment SHOULD be treated as an architectural decision, not just a scheduling one.
- **should-optimize-real-coordination-paths**: SHOULD optimize the real coordination paths — who actually coordinates with whom (shared context, handoffs, review loops) — not nominal reporting lines or agent labels.
- **should-treat-inverse-maneuver-as-lens**: SHOULD treat the inverse maneuver as a lens, not a deterministic law: aligning boundaries makes a target architecture *easier*; it does not guarantee it.
- **should-verify-emergent-structure**: SHOULD verify the emergent structure against the intended design rather than assuming alignment.
- **should-assign-agents-along-desired-seams**: SHOULD assign agents along the seams you want in the code: give each module or bounded context to one agent (or one tightly-coordinating cluster).
- **should-watch-for-high-bandwidth-handoffs**: SHOULD watch for high-bandwidth handoffs: where two agents must exchange large, frequently-changing context to make progress, expect a tight coupling to appear at that boundary in the output.
- **should-restructure-assignment-not-prompt**: If that coupling is undesirable, SHOULD restructure the assignment, not just the prompt.
- **should-repartition-when-architecture-changes**: SHOULD re-partition when the architecture should change: because boundaries are sticky, a desired architectural shift usually requires reshaping who builds what — see [adc.principle.meta-principle-optimize-for-change](cookbook:aadd048b-da52-415d-949f-45160b970381).
