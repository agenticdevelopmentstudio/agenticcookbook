
- Frontmatter missing a required field, carrying `domain`, with a `type` other than `guideline`, or with a `triggers` name not in the trigger guide.
- An H1 that differs from the `title`, more than one H1, or a skipped heading level.
- A summary that is not directly under the H1, that needs the body to make sense, or that buries the action a reader takes.
- A bullet in a `rules` part that has no kebab-case name, states no RFC 2119 keyword, or shares its name with another rule.
- A rule that states more than one requirement, mixes in its rationale, cannot be checked, or does not say when it applies.
- A rule whose keyword is stronger than the claims it cites, or a keyword used where nothing requires it or to impose a method.
- A rule with no citation, a citation before its end, an id that is no claim in `research/research.json`, or a claim no verdict names.
- A part without a role, a roled guideline missing a `rules`, `review-focus`, `review-bar` or `build-bar` part, or `routes` or `hosts/` set.
- An example, note or rationale that reads as a requirement, or a rationale part that adds rules of its own.
- A build bar with a missing line for a rule, two lines for one rule, or a line naming something that is not a rule.
- A rule renamed, or a released version's content changed, without a new version.
- A topic that already exists elsewhere in the cookbook written again instead of extended.
- A change history that is not the last section, is missing a column, or has no row for the current version.

