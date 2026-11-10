
**Decision**: Use OpenClaw as the execution platform rather than GitHub Actions or a standalone launchd script.
**Rationale**: OpenClaw is already installed on the execution Mac, provides daemon infrastructure (cron, webhooks, sessions), Claude integration, and conversational control. Avoids building custom daemon management.
**Approved**: yes

**Decision**: Four GitHub Apps (3 phase bots + 1 fix bot) rather than a single bot or GitHub Actions identity.
**Rationale**: Distinct bot personas make PR reviews visually clear — each phase appears as a different reviewer. The fix bot is separate because it writes code while the phase bots are read-only reviewers.
**Approved**: yes

**Decision**: Sequential phase execution (1 → 2 → 3) with short-circuit on rejection.
**Rationale**: Phase 1 fixes content before Phase 2 analyzes it (better to compare clean content). Phase 3 needs findings from both prior phases. Running all phases on content that fails basic structural checks wastes resources.
**Approved**: yes

**Decision**: Contributor can appeal rejections by commenting on the PR.
**Rationale**: Automated review can be wrong. A simple appeal process (comment → human reviews) prevents valid contributions from being permanently blocked by false positives.
**Approved**: yes

**Decision**: LLM readability over human readability (no Flesch-Kincaid), and fix preference asked before PR submission with a default of auto-fix.
**Rationale**: These two decisions apply to a single ingredient each and are recorded in full in the PR review phase ingredient (LLM readability) and the PR fix agent ingredient (fix preference).
**Approved**: yes

