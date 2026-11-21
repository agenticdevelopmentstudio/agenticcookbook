
This part is informative: it describes one way to keep the rules above.

- **Start from the frontmatter.** Fill every required field, set `type: guideline`, give the artifact a new UUID as its `id`, and leave `domain` out. Leave `approved-by` and `approved-date` as `""` until approval stamps them. Set `triggers` to names from `guide/introduction/trigger-guide.md`, or `[]` when none fits.
- **Write the H1 and the summary next.** Copy the frontmatter `title` into the H1 word for word, then write the summary statement directly under it: the action a reader takes, first, in a paragraph that stands without the rest of the doc.
- **Say what conforming means, and what the guideline covers.** After the summary, one paragraph names the normative part and how its keywords are read; another states the scope as a plain description, leaving every requirement to the rules.
- **Lay out the parts in order.** The headings are `## Rules`, `## How to keep the rules`, `## Examples`, `## What a reviewer looks for`, `## A complete review must establish`, `## A build must establish`, `## Rationale`, `## References` and `## Change History`. `cookr roles set` gives each a role after `cookr convert`; the intro and the history carry none. Each informative part opens with a sentence saying it is informative.
- **Write one rule to a bullet.** Name it in kebab-case, state one requirement with one RFC 2119 keyword in uppercase, and end it with its citation. A rule's subject usually says where it applies; an `**Applies when:**` line says so when the subject alone does not. The why goes in the rationale part.
- **Choose the keyword from the evidence.** A rule reads truest at the strength of the weakest claim it cites: a claim that says must supports a MUST, and a claim that says should, or that a second check found only partly supported, supports a SHOULD.
- **Cite the claim, at the end.** Write `(claim: <id>)` or `(claims: <id>, <id>)` as the bullet's last text, with nothing after it, not even a full stop. Every id is a claim in `research/research.json` that some verdict names.
- **Indent what continues a rule.** A rule that needs a second paragraph, a table or a code block indents those lines under its bullet, so they stay part of it, and the citation still ends the last line.
- **Write the build bar from the rules.** It has exactly one line per named rule, `` - `rule-name`: … ``, and no line naming anything else.
- **Keep names once they ship.** A rule's name is how other docs and reviews link to it; a rename comes only with a new version, and rules are never numbered by position.
- **Let the tools check it.** `cookr roles check <folder>` reports unnamed, duplicate and uncited rules and citations not at the end, and `cookr validate` checks the frontmatter, links, research and the index.
- **Record each version.** `cookr bump <folder> --summary "..."` writes the version, the `modified` date and a row of the change history table, with the date and a summary a reader can follow.

