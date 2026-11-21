
- Start from the frontmatter block in `guide/introduction/conventions.md`, set `type: principle`, and write a `summary` that names the idea and the decisions it applies to.
- Write the H1 as the frontmatter `title`, word for word, and use no other level-1 heading anywhere in the body.
- Write the statement first, typically in one to three sentences, as the paragraph a reader who stops there still acts on. Put the reason the principle holds in it or in the bullet it explains.
- Write each bullet as a full sentence naming a concrete action, most important first. When a bullet needs a procedure, a table or a worked case, link the guideline that holds it instead of copying it in.
- Before adding a bullet, ask whether the agent already gets this right without it. Leave out common conventions the agent knows and anything a linter already checks.
- When the principle loads on every task, count it with the others that do, not alone, and measure that total against the hosts' own limits.
- Let tools decide what they can: run `cookr validate` for the frontmatter, the type, the roles and the citations, and a markdownlint or Vale rule for headings and counts. Keep the reviewer for whether the statement holds the core idea and whether the bullets are actionable.
- For a roled principle, give every part but the intro and the history one role with `cookr roles set`, then run `cookr roles check` to confirm the census and the four skills.
- Record each new version with `cookr bump <folder> --summary "<what changed>"`, which adds the dated row to the Change History.

