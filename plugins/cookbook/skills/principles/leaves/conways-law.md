<!-- leaf: principles/conways-law · source: principles/conways-law.md -->

# Conway's Law

Any system tends to reproduce the communication structure of the people — or agents — that designed it. Module boundaries follow the seams along which builders coordinate, not the seams a clean design would prefer. The actionable corollary (the "inverse Conway maneuver") is to deliberately shape team and agent boundaries to match the architecture you want, then let the system grow into them.

For a multi-agent dev system this is direct: how you partition work across specialist and platform agents imprints on the generated module boundaries. **Agent assignment is therefore an architectural decision, not just a scheduling one.**

- **Communication patterns drive the effect — not org charts.** What matters is who actually coordinates with whom (shared context, handoffs, review loops), not nominal reporting lines or agent labels. Optimize the real coordination paths.
- **Treat the inverse maneuver as a lens, not a deterministic law.** Aligning boundaries makes a target architecture *easier*; it does not guarantee it. Verify the emergent structure against the intended design rather than assuming alignment.
- **Assign agents along the seams you want in the code.** Give each module or bounded context to one agent (or one tightly-coordinating cluster). Splitting a single coherent module across loosely-coupled agents tends to fracture it; forcing unrelated concerns onto one agent tends to fuse them.
- **Watch for high-bandwidth handoffs.** Where two agents must exchange large, frequently-changing context to make progress, expect a tight coupling to appear at that boundary in the output. If that coupling is undesirable, restructure the assignment, not just the prompt.
- **Re-partition when the architecture should change.** Because boundaries are sticky, a desired architectural shift usually requires reshaping who builds what — see `agenticdevelopercookbook://principles/meta-principle-optimize-for-change`.
