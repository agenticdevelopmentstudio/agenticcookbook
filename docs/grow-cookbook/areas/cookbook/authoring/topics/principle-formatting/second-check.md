## google-single-h1
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote appears word for word under "Title phrasing", with "( h1 )" as the only formatting difference.

## md025-single-title
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: MD025 fires on multiple top-level headings. Its fix text asks for a single h1 that is the document's title.

## md041-title-heading
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The rule requires the first line to be a top-level heading, and its rationale treats that heading as the title.

## prompting-explain-why
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote sits under "Add context to improve performance". Its "Less effective: NEVER use ellipses" example supports the comparison with a bare command.

## diataxis-explain-why
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote appears under "Provide context" with only spacing differences.

## adr-motivation-lost
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote says only that decision motivation is hard to track. The "blindly accept or blindly change" reasoning is in the next paragraph of the post ("this person has only two choices: Blindly accept the decision... Blindly change it"), not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST

## skill-only-new-context
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only the first half of the claim. The token-cost part comes from the page's next lines ("Challenge each piece of information... Does this paragraph justify its token cost?"), which the quote leaves out.
- correction: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST

## claude-md-only-what-agent-lacks
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The context is CLAUDE.md, which is loaded every session. The source says "couldn't work out from the code itself", which is slightly narrower than the claim's "for itself".

## cursor-use-a-linter
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is under "What to avoid in rules", with the first phrase in bold.

## smallest-high-signal-set
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says "maximize the likelihood of some desired outcome". The claim's "produce" is a slight simplification but stays within its meaning.

## cursor-start-simple
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim.

## skill-description-what-and-when
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim. The page uses "should", which matches the claim's strength.

## agentskills-metadata-always-loaded
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: In the spec's progressive-disclosure list, only the metadata loads at startup; the body loads on activation and resources load as needed. Calling it the "always-loaded part of a compiled artifact" is the cookbook's own mapping onto that model.

## changelog-latest-first
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is one of Keep a Changelog's guiding principles.

## changelog-entry-per-version
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim, and it says "should", matching the claim.

## changelog-dated
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim, from the guiding principles.

## docs-as-code
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote stops at the colon. The list that follows it on the page (Issue Trackers, Version Control, Plain Text Markup, Code Reviews, Automated Tests) is not in the quote, so the "including code review and automated tests" part is unsupported by the quote itself.
- correction: refuted (quote-found yes, supports-claim partly); trust 66 -> 46; a rule citing it cannot carry MUST

## codex-lint-in-ci
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote follows a "## Code Review Rules" AGENTS.md example, so "review rules" scopes it correctly.

## claude-md-hooks-for-absolutes
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim.

## md043-required-headings
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote supports only enforcing a standard heading structure across files. The wildcard support (`*`, `+`, `?`) that the claim depends on is described further down the page, not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

## json-schema-required
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim. That required fields become tool-decidable follows directly from it.

## markdownlint-custom-rules-frontmatter
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page lists `lines` and `frontMatterLines` as separate params. The claim's comparison and counting uses follow from that.

## vale-metric-formulas
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote says only that metric evaluates formulas over built-in variables. The variable list the claim names (words, sentences, paragraphs, list, heading.h{n}, readability scores) is in the page's Variables table, not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## vale-occurrence
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim.

## vale-script
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is word for word apart from spacing around "Tengo ,". Paragraphs per section is a fair example of "arbitrary logic", and the page's own example script enforces "at most 3 paragraphs per section".

## agentsmd-any-headings
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the FAQ answer to "Are there required fields?". The claim's conclusion that required structure serves authors and tools follows from it.

## claude-md-200-lines
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote reads "Size: target under 200 lines per CLAUDE.md file..." and is guidance ("target"), which the claim correctly calls a target.

## codex-32kib-combined
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim. The page notes the limit is configurable through project_doc_max_bytes, which fits the claim's "by default".

## claude-md-every-line-costs
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim, under "Keep CLAUDE.md short".

## ifscale-density-degrades
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The abstract says the work measures degradation as instruction density increases and reports 68% at 500 instructions.

## lost-in-the-middle
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Verbatim from the abstract.

## ifscale-earlier-instructions
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The abstract reports a "bias towards earlier instructions" but does not tie it to high density, so the claim's "at high instruction density" is not supported. From memory and not checked here: the paper's body says primacy effects peak at moderate density and fade at the highest densities.
- correction: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST

## ms-first-screen
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The quote is under "Put first things first", word for word apart from spacing and emphasis.

## google-opening-sentence
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says "of any paragraph". The claim leaves out that paragraph scope but otherwise matches.
