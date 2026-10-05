
The PR fix agent is the Cookbook Fix Bot (`@cookbook-fix-bot[bot]`): the single identity that writes to a contribution during the pipeline. It applies structural fixes from Phase 1 and refactoring proposals approved by the human reviewer from Phase 2, either committing directly or posting GitHub suggested changes, according to a preference the contributor states before submitting the PR. The three phase bots stay read-only reviewers.

### Contributor Preference

The `/contribute-to-cookbook` skill asks the contributor before PR submission whether fixes should be applied automatically or reviewed one by one, and records the answer in the PR body as an HTML comment (`<!-- fix-preference: auto -->` or `<!-- fix-preference: review -->`).

