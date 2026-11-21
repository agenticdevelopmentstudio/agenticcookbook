
- **Start from the frontmatter.** Fill every required field, set `type: guideline`, give the artifact a new UUID as its `id`, and leave `domain` out. Leave `approved-by` and `approved-date` as `""` until approval stamps them. Set `triggers` to names from `guide/introduction/trigger-guide.md`, or `[]` when none fits.
- **Write the H1 and the summary next.** Copy the frontmatter `title` into the H1 word for word, then write the summary statement directly under it: the action a reader takes, first, in a paragraph that stands without the rest of the doc.
- **Lay out the parts in order.** Use the headings `## Rules`, `## How to keep the rules`, `## Examples`, `## What a reviewer looks for`, `## A complete review must establish`, `## A build must establish`, `## Rationale`, `## References` and `## Change History`. Give each a role with `cookr roles set` after `cookr convert`; the intro and the history carry none.
- **Write one rule to a bullet.** Name it in kebab-case, state one requirement with one RFC 2119 keyword in uppercase, say when it applies, and end it with its citation. Keep the why for the rationale part.
- **Pick the keyword from the evidence.** A rule is no stronger than the weakest claim it cites. Use MUST only where the cited claims say must; a claim that says should carries SHOULD.
- **Cite the claim, at the end.** Write `(claim: <id>)` or `(claims: <id>, <id>)` as the bullet's last text, with nothing after it, not even a full stop. Every id is a claim in `research/research.json` that some verdict names.
- **Indent what continues a rule.** A rule that needs a second paragraph, a table or a code block indents those lines under its bullet, so they stay part of it, and the citation still ends the last line.
- **Write the build bar from the rules.** Give it exactly one line per named rule, `` - `rule-name`: … ``, and no line naming anything else.
- **Keep names once they ship.** A rule's name is how other docs and reviews link to it; rename it only by a new version, and never number rules by position.
- **Let the tools check it.** Run `cookr roles check <folder>` for unnamed, duplicate and uncited rules and citations not at the end, and `cookr validate` for the frontmatter, links, research and the index.
- **Record each version.** Add a row per version to the change history table, with the date and a summary a reader can follow. Let `cookr bump <folder> --summary "..."` write the version, the `modified` date and the row.

