
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| PR review phase | [adc.ingredient.autonomous-dev-bots.pr-review-phase](cookbook:32eb5fa7-31ba-49d2-8223-a530d8cc7092) | Phase 1: structural validation, markdownlint, Vale prose style, LLM clarity pass, completeness, conventions, bounded fix loop | Yes | Max fix iterations (3); Claude Sonnet |
| PR scope phase | [adc.ingredient.autonomous-dev-bots.pr-scope-phase](cookbook:63c5a406-6356-417f-b549-b97e40385ba5) | Phase 2: placement, granularity, overlap detection, ecosystem fit, per-requirement refactoring proposals | Yes | Granularity thresholds (15 MUST requirements, 8 states, 3 requirements); Claude Opus |
| PR evaluate phase | [adc.ingredient.autonomous-dev-bots.pr-evaluate-phase](cookbook:f48198bb-f5ad-49dd-9342-945af89a3ab4) | Phase 3: value and risk scoring, external research, recommendation to the human reviewer | Yes | Claude Opus |
| PR fix agent | [adc.ingredient.autonomous-dev-bots.pr-fix-agent](cookbook:fe3522f2-1b94-494e-8136-c8a5eea876cf) | The single identity that applies automated fixes by commit or suggested change per the contributor's preference | Yes | `fix-preference` (`auto` default or `review`) stored in the PR body |

