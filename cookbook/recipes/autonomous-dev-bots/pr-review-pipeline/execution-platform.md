
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

