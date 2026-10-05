
- **Single rule, already optimal**: One rule file under 50 lines, no duplication, has globs, clean MUST NOTs. The optimizer MUST report "No optimizations proposed."
- **Overly broad globs**: A rule with `globs: **` is treated as ungated and the optimizer suggests narrowing.
- **Very large single rule (500+ lines)**: The optimizer SHOULD propose splitting into a minimal always-on section plus one or more skills, identifying natural section boundaries.
- **User declines all optimizations**: The optimizer proposes changes, the user declines everything. The pipeline MUST proceed to the report with a record of the proposals and the decision to decline.

