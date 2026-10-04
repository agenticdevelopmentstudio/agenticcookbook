
When a contributor submits a PR to the cookbook (via `/contribute-to-cookbook` or manually), this pipeline runs automatically:

1. **Phase 1: Review** — structural validation, prose quality, content completeness, convention compliance. Fixes what it can (up to 3 iterations), rejects what it cannot.
2. **Phase 2: Refactoring & Scoping** — placement analysis, granularity assessment, overlap detection against all cookbook content, refactoring proposals.
3. **Phase 3: Evaluate** — value scoring, risk assessment, ecosystem research, recommendation to human reviewer.

Phases run **sequentially**. If a phase rejects, subsequent phases do not run. Each phase posts a GitHub PR review (Approve or Request Changes) under its own bot identity.

The PR is unmergeable until all three phase bots approve AND a human reviewer approves.

