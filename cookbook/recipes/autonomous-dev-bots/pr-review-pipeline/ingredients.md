
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| PR review phase | `agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-review-phase` | Phase 1: structural validation, markdownlint, Vale prose style, LLM clarity pass, completeness, conventions, bounded fix loop | Yes | Max fix iterations (3); Claude Sonnet |
| PR scope phase | `agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-scope-phase` | Phase 2: placement, granularity, overlap detection, ecosystem fit, per-requirement refactoring proposals | Yes | Granularity thresholds (15 MUST requirements, 8 states, 3 requirements); Claude Opus |
| PR evaluate phase | `agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-evaluate-phase` | Phase 3: value and risk scoring, external research, recommendation to the human reviewer | Yes | Claude Opus |
| PR fix agent | `agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-fix-agent` | The single identity that applies automated fixes by commit or suggested change per the contributor's preference | Yes | `fix-preference` (`auto` default or `review`) stored in the PR body |

