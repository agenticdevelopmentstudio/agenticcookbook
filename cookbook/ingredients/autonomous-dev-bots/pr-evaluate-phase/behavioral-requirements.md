
- **value-scoring**: Phase 3 MUST score the contribution on: novelty (fills a gap), demand signal (multiple projects would use this), quality (how clean was the Phase 1/2 pass), completeness (platform coverage, test vector thoroughness), ecosystem integration (quality of depends-on/related links).
- **risk-scoring**: Phase 3 MUST assess: breaking changes to existing content, conflicts with engineering principles, scope appropriateness for the cookbook, contributor track record (first-time vs established).
- **external-research**: Phase 3 MUST research beyond the repo: search GitHub for similar patterns, check platform SDK documentation to see if the concept is built-in, assess whether the pattern is well-established or novel.
- **recommendation**: Phase 3 MUST produce a structured recommendation: value (HIGH/MEDIUM/LOW), confidence (HIGH/MEDIUM/LOW), recommendation (ACCEPT/ACCEPT WITH REFACTORING/PARTIAL ACCEPT/REJECT), with per-section rationale.
- **human-escalation**: Phase 3 MUST post its recommendation as a PR review. The human reviewer makes the final decision — Phase 3 recommends but never merges.

