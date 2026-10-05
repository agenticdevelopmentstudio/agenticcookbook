
An autonomous dev bot that reviews pull requests to the Agentic Developer Cookbook. Three sequential phases — Review, Refactoring & Scoping, Evaluate — each run by a distinct GitHub App bot persona. The pipeline runs on OpenClaw, triggered by GitHub webhooks, and posts structured PR reviews that gate merging.

When a contributor submits a PR to the cookbook (via `/contribute-to-cookbook` or manually), this pipeline runs automatically:

1. **Phase 1: Review** — structural validation, prose quality, content completeness, convention compliance. Fixes what it can (up to 3 iterations), rejects what it cannot.
2. **Phase 2: Refactoring & Scoping** — placement analysis, granularity assessment, overlap detection against all cookbook content, refactoring proposals.
3. **Phase 3: Evaluate** — value scoring, risk assessment, ecosystem research, recommendation to human reviewer.

Phases run **sequentially**. If a phase rejects, subsequent phases do not run. Each phase posts a GitHub PR review (Approve or Request Changes) under its own bot identity.

The PR is unmergeable until all three phase bots approve AND a human reviewer approves.

The recipe composes four ingredients: one per phase, plus the fix agent that applies automated fixes. The trigger, sequencing, rejection and appeal behavior, and the execution platform belong to the recipe because they span the ingredients.

### Pipeline Outcomes

| Outcome | Description | Next action |
|---------|-------------|-------------|
| Accept | Passes all phases, high value | Human reviewer approves, PR is mergeable |
| Accept with refactoring | Has value, needs structural changes | Refactoring agent applies changes, pipeline reruns |
| Partial accept | Some parts valuable, others not | Proposal extracts good parts, rejects rest. Human decides. |
| Reject | No parts meet the bar | Detailed per-section rationale posted. Contributor can appeal. |
| Reject with appeal | Contributor disputes rejection | Human reviewer evaluates the appeal |

### GitHub Apps

Four GitHub App identities are required:

| App | Purpose | Posts as |
|-----|---------|---------|
| Cookbook Review Bot | Phase 1: structural, prose, completeness, conventions | `@cookbook-review-bot[bot]` |
| Cookbook Scope Bot | Phase 2: placement, granularity, overlap, ecosystem fit | `@cookbook-scope-bot[bot]` |
| Cookbook Eval Bot | Phase 3: value, risk, recommendation | `@cookbook-eval-bot[bot]` |
| Cookbook Fix Bot | Refactoring agent: applies all automated fixes | `@cookbook-fix-bot[bot]` |

Each app requires:
- `checks:write` permission (to create check runs)
- `pull_requests:write` permission (to post reviews and suggested changes)
- `contents:write` permission (Fix Bot only — to push commits)
- Private key PEM stored on the execution Mac
- Installation tokens generated per run via `gh-token` extension

### Execution Platform

#### OpenClaw Configuration

- **Trigger**: GitHub webhook configured to POST `pull_request` events to `http://<mac-ip>:18789/hooks/agent`
- **Fallback**: OpenClaw cron job polling `gh pr list --repo agenticdevelopercookbook/cookbook --state open` every 5 minutes
- **Session**: Isolated session per PR review run
- **Model**: Claude Opus for Phase 2 (overlap/scoping requires strong reasoning) and Phase 3 (evaluation). Sonnet for Phase 1 (structural checks are more mechanical).
- **Timeout**: 48 hours max per run
- **Tools**: Shell access to `gh`, `git`, `vale`, `markdownlint-cli2`

#### Conversational Control

The pipeline is controllable via chat (any connected channel — Slack, Discord, iMessage):

- "What's the status of PR #42?" → shows current phase, findings so far
- "Re-run review on PR #42" → triggers a fresh pipeline run
- "Show open PRs waiting for my review" → lists PRs that passed all phases and need human approval
- "Approve refactoring on PR #42" → human approves the refactoring proposal, triggers refactoring agent

#### External Tools

| Tool | Purpose | Installation |
|------|---------|-------------|
| `gh` | GitHub CLI for PR operations, reviews, comments | `brew install gh` |
| `vale` | Prose linting with custom Cookbook style | `brew install vale` |
| `markdownlint-cli2` | Structural markdown linting | `npm install -g markdownlint-cli2` |
| `gh-token` | GitHub App installation token generation | `gh extension install Link-/gh-token` |

### Logging

Subsystem: `pr-review-pipeline` | Category: `Pipeline`

Pipeline-level events are listed here. The fix iteration event is in the PR review phase ingredient and the fix bot commit event is in the PR fix agent ingredient.

| Event | Level | Message |
|-------|-------|---------|
| Pipeline started | info | `Pipeline: started for PR #{{pr_number}} on {{repo}}` |
| Phase completed | info | `Pipeline: phase {{phase}} completed — {{result}}` |
| Phase short-circuited | info | `Pipeline: skipping phase {{phase}} — prior phase rejected` |
| Fix bot committed | info | `Pipeline: fix bot pushed commit {{sha}} for PR #{{pr_number}}` |
| Rate limit hit | warning | `Pipeline: GitHub API rate limited — retrying in {{seconds}}s` |
| Pipeline failed | error | `Pipeline: failed for PR #{{pr_number}} — {{error}}` |

### Sections that do not apply

The original recipe recorded Appearance, States, and Accessibility as not applicable because the pipeline is automated with no visual UI: its state is tracked through GitHub PR status checks and bot comments, and it interacts through GitHub's PR interface, whose accessible rendering of plain-markdown bot comments is inherited. Each ingredient states this in its own Appearance, States, and Accessibility sections.

