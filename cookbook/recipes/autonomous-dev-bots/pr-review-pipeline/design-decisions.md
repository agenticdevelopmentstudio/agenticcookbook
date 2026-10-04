
**Decision**: Use OpenClaw as the execution platform rather than GitHub Actions or a standalone launchd script.
**Rationale**: OpenClaw is already installed on the execution Mac, provides daemon infrastructure (cron, webhooks, sessions), Claude integration, and conversational control. Avoids building custom daemon management.
**Approved**: yes

**Decision**: Four GitHub Apps (3 phase bots + 1 fix bot) rather than a single bot or GitHub Actions identity.
**Rationale**: Distinct bot personas make PR reviews visually clear — each phase appears as a different reviewer. The fix bot is separate because it writes code while the phase bots are read-only reviewers.
**Approved**: yes

**Decision**: Sequential phase execution (1 → 2 → 3) with short-circuit on rejection.
**Rationale**: Phase 1 fixes content before Phase 2 analyzes it (better to compare clean content). Phase 3 needs findings from both prior phases. Running all phases on content that fails basic structural checks wastes resources.
**Approved**: yes

**Decision**: LLM readability over human readability (no Flesch-Kincaid).
**Rationale**: Cookbook content is consumed by LLMs, not casual human readers. LLM readability means: explicit, unambiguous, no hedging, consistent terminology, self-contained sections. Traditional readability metrics penalize the precision that LLMs need.
**Approved**: yes

**Decision**: Fix preference asked before PR submission, default auto-fix.
**Rationale**: Most contributors want hands-off after submission. Power users who want control can opt into review-each. The choice is per-PR, stored as PR metadata.
**Approved**: yes

**Decision**: Contributor can appeal rejections by commenting on the PR.
**Rationale**: Automated review can be wrong. A simple appeal process (comment → human reviews) prevents valid contributions from being permanently blocked by false positives.
**Approved**: yes

