<!-- leaf: recipes-autonomous-dev-bots/pr-review-pipeline--part-2 · source: recipes/autonomous-dev-bots/pr-review-pipeline.md -->

# PR Review Pipeline — continued (part 2)

## Execution Platform

### OpenClaw Configuration

- **Trigger**: GitHub webhook configured to POST `pull_request` events to `http://<mac-ip>:18789/hooks/agent`
- **Fallback**: OpenClaw cron job polling `gh pr list --repo agenticdevelopercookbook/cookbook --state open` every 5 minutes
- **Session**: Isolated session per PR review run
- **Model**: Claude Opus for Phase 2 (overlap/scoping requires strong reasoning) and Phase 3 (evaluation). Sonnet for Phase 1 (structural checks are more mechanical).
- **Timeout**: 48 hours max per run
- **Tools**: Shell access to `gh`, `git`, `vale`, `markdownlint-cli2`

### Conversational Control

The pipeline is controllable via chat (any connected channel — Slack, Discord, iMessage):

- "What's the status of PR #42?" → shows current phase, findings so far
- "Re-run review on PR #42" → triggers a fresh pipeline run
- "Show open PRs waiting for my review" → lists PRs that passed all phases and need human approval
- "Approve refactoring on PR #42" → human approves the refactoring proposal, triggers refactoring agent

### External Tools

| Tool | Purpose | Installation |
|------|---------|-------------|
| `gh` | GitHub CLI for PR operations, reviews, comments | `brew install gh` |
| `vale` | Prose linting with custom Cookbook style | `brew install vale` |
| `markdownlint-cli2` | Structural markdown linting | `npm install -g markdownlint-cli2` |
| `gh-token` | GitHub App installation token generation | `gh extension install Link-/gh-token` |

## Custom Vale Style: Cookbook

A custom Vale style (`vale/styles/Cookbook/`) with rules optimized for LLM readability:

| Rule | What it flags |
|------|---------------|
| `VagueTerms.yml` | "appropriate", "suitable", "reasonable", "as needed", "standard", "proper", "adequate" |
| `AmbiguousQuantifiers.yml` | "some", "most", "usually", "often", "sometimes", "generally", "typically", "normally" |
| `Hedging.yml` | "might want to", "consider using", "it may be helpful", "you could", "perhaps", "arguably" |
| `ImplicitReferences.yml` | "as mentioned above", "the usual approach", "handle this correctly", "see above", "as before" |
| `CasualRFC2119.yml` | Lowercase "must", "should", "shall" in requirement sections that are not bolded RFC 2119 keywords |
| `DoubleNegatives.yml` | "must not fail to", "should not avoid", "do not prevent" |
| `AmbiguousPronouns.yml` | "it should", "this must", "that will" at sentence start without clear antecedent in requirement sections |

## LLM Clarity Pass

Beyond Vale's deterministic rules, the LLM clarity pass checks for:

- **Ambiguous antecedents**: pronouns whose referent requires re-reading prior context
- **Implicit assumptions**: statements that assume knowledge not present in the document
- **Terminology drift**: a concept called X in one section and Y in another
- **Section isolation**: can each section be understood without reading the others?
- **Unresolved references**: mentions of concepts not defined or linked
- **Vague quantification in requirements**: "handle multiple items" (how many?) vs "handle 1-1000 items"

## Platform Notes

This pipeline runs on macOS via OpenClaw. It is not platform-portable — it depends on OpenClaw's daemon infrastructure, GitHub App webhooks, and Claude Code CLI availability on the host Mac.

## Design Decisions

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
