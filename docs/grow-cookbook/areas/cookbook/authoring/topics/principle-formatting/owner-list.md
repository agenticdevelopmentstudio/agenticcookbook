# Owner list: principle-formatting

For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **pf-title-heading** — verdict `unsupported` (claims: pf-title-heading-prior, md041-frontmatter-title-satisfies, md025-frontmatter-title-counts, markdownlint-custom-rules-frontmatter). Prior text, kept word for word: "The first H1 heading MUST match the frontmatter `title` field exactly."
  - against: By default MD041 accepts a front-matter title in place of a first-line H1, so it does not by itself check that an H1 matches the front-matter title.
  - against: With default settings MD025 treats a front-matter title as the H1 and reports any later H1, so a compiled document carrying both a front-matter title and a `# Title` trips it unless front_matter_title is set to an empty string.
  - against: markdownlint custom rules receive the document's lines and its front-matter lines separately, so a custom rule can compare the H1 with the front-matter title or count body lines.
- **pf-statement** — verdict `unsupported` (claims: pf-statement-prior, lead-with-main-point, ms-lead-with-most-important, google-opening-sentence, pep-abstract-short, google-paragraph-length, vale-metric-formulas). Prior text, kept word for word: "A concise statement paragraph MUST appear immediately after the H1 heading. This is the principle's core idea — typically 1-3 sentences."
  - against: Start content with its most important piece of information (the inverted pyramid), so a reader who stops early still gets the main point.
  - against: Microsoft's style guide says to get to the point fast: lead with what matters most and front-load keywords.
  - against: Google's technical-writing course treats the opening sentence as the most important, since busy readers may skip what follows.
  - against: A structured document opens with a short abstract of the issue it addresses; PEP 1 says each PEP should have one of about 200 words.
  - against: Readers welcome paragraphs of three to five sentences and avoid ones of more than about seven.
  - against: Vale's metric check evaluates formulas over built-in counts (words, sentences, paragraphs, lists, headings by level, readability scores), document-wide or per scoped block, so it can bound a statement's sentence count or a body's word count.
- **pf-change-history** — verdict `unsupported` (claims: pf-change-history-prior, changelog-entry-per-version, changelog-dated, md043-required-headings). Prior text, kept word for word: "The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary."
  - against: A change history should have an entry for every version.
  - against: Each version in a change history shows its release date.
  - against: markdownlint MD043 enforces a required heading structure across a set of files, with wildcards for optional sections, so it can require a final `## Change History` heading.
- **pf-brevity** — verdict `unsupported` (claims: pf-brevity-prior, claude-md-200-lines, skill-body-500-lines, agentskills-progressive-disclosure, cursor-rules-500-lines, codex-32kib-combined, copilot-two-pages, ifscale-density-degrades, chroma-context-rot, lost-in-the-middle, context-finite-resource, minimal-not-short, claude-md-line-gets-lost, ms-be-brief, adr-short-record, diataxis-keep-bounded, md013-measures-line-width). Prior text, kept word for word: "Principles SHOULD be concise. The body (excluding frontmatter and Change History) SHOULD NOT exceed ~50 lines. Principles are philosophical anchors, not exhaustive guides — detailed guidance belongs in guidelines."
  - against: Anthropic's Claude Code guidance targets under 200 lines per always-loaded CLAUDE.md file, because longer files consume more context and reduce adherence.
  - against: Anthropic recommends keeping an on-demand SKILL.md body under 500 lines, splitting longer content into separate files.
  - against: The Agent Skills specification loads metadata (~100 tokens) for every skill at startup and the body (under 5000 tokens recommended) only on activation, and moves detailed reference material to separate files.
  - against: Cursor's rule guidance keeps each rule under 500 lines and splits large rules into composable ones.
  - against: OpenAI Codex stops adding instruction files once their combined size reaches 32 KiB by default, so an always-loaded set has a hard total budget.
  - against: GitHub's published prompt for generating Copilot repository instructions limits them to two pages.
  - against: Instruction-following accuracy falls as instruction density grows; even the best frontier models reach only 68% accuracy at 500 simultaneous instructions.
  - against: Across 18 models, performance grows less reliable as input length grows, even on simple tasks.
  - against: Language models use information at the start or end of a long context best and degrade significantly for information in the middle, even long-context models.
  - against: Anthropic's context-engineering guidance treats context as a finite resource with diminishing returns, because recall falls as context grows (context rot).
  - against: Minimal context does not mean short: an instruction still needs enough information up front for the agent to adhere, which is where a hard length cap can hurt.
  - against: When an agent keeps ignoring an instruction that is in its file, emphasis does not fix it: the file has grown long enough that the line gets lost, or the rule belongs in enforcement.
  - against: Microsoft's style guide says to be brief: give just enough to decide confidently and prune every excess word.
  - against: Michael Nygard's architecture decision record, a close analogue of a short principle document, is meant to be one or two pages long.
  - against: Diataxis keeps explanation closely bounded: instruction and technical description belong elsewhere, and letting them in harms the explanation and hides them from their proper place.
  - against: markdownlint's length rule MD013 measures the width of each line, not the length of a document, so a body-length cap needs a custom rule or another tool.
- **roles-vocabulary** — verdict `unsupported` (claims: roles-vocabulary-prior). Prior text, kept word for word: "A part may carry a `role` in `artifact.json`: `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **roles-every-part-roled** — verdict `unsupported` (claims: roles-every-part-roled-prior). Prior text, kept word for word: "A roled artifact gives every other part a role, names each rule in its `rules` parts (`- **kebab-name**: … MUST|SHOULD|MAY …`), and sets no `routes` and no `hosts/`."
- **roles-principle-skill-names** — verdict `unsupported` (claims: roles-principle-skill-names-prior). Prior text, kept word for word: "`principles/t`, which has no use case, keeps its type: `principle-t` and `reviewing-principle-t`." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
- **roles-principle-routing** — verdict `unsupported` (claims: roles-principle-routing-prior). Prior text, kept word for word: "Each skill has its own description and routes under its own use case, with the artifact's own use case below it (`coding/reviewing/planning/data`; a principle's `coding/reviewing/principles`)." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.

## Open questions

- Which length figure the principle rule should name: the research supports no ~50-line per-principle cap; it supports a budget for everything always loaded (Claude Code's under-200-lines-per-file target) and an on-demand body bound (SKILL.md under 500 lines / under 5000 tokens). Whether principles are always loaded together (then the cap is the shared budget divided across the cookbook's principles, about 45 today) or load on demand as compiled skills (then the skill bound applies) is the owner's to decide.
- Whether pf-frontmatter-complete's field list should match conventions.md's Field Definitions table, which marks approved-by and approved-date as required (written by /approve-artifact, not linted) while the draft list omits them.
- Whether pf-title-heading keeps its exact-match MUST as an internal consistency check (tool-decidable) although no outside source requires it, or is restated as the single-title practice the sources support.
- Whether pf-statement and pf-change-history stay MUST as definitions of the artifact type (internal design) or drop to the SHOULD their outside sources support.
- How a principle's actionable bullets relate to Diataxis, which keeps instruction out of explanation: whether a principle is an explanation page with a short action list, or a separate artifact kind for which Diataxis is not the model.
