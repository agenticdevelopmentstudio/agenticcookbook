---
id: 8238bdf2-432b-4c34-9050-742a1f16d107
title: "Writing comments and docs"
domain: agenticdevelopercookbook://guidelines/implementing/documentation/writing-comments-and-docs
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Comment the why rather than the what, update docs in the same change, write for human and AI readers, and keep the prose plain and free of machine-sounding filler."
platforms: []
tags:
  - documentation
  - writing
  - comments
  - ai
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/code-quality/code-for-the-ai-reader
  - agenticdevelopercookbook://guidelines/reviewing/documentation/docs-match-code
  - agenticdevelopercookbook://principles/explicit-over-implicit
  - agenticdevelopercookbook://principles/principle-of-least-astonishment
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - new-module
  - code-review
---

# Writing comments and docs

Comments and docs are part of the change. This guideline covers what to write, when to write it, who it is for, and how to keep the prose from reading as machine-generated. It builds on `code-for-the-ai-reader`, which covers the code itself, and on the rules the humanize skill uses to spot generated-sounding writing.

## Comment the why, not the what

- A comment SHOULD say what the code cannot: the reason for a choice, a constraint from outside, a trap, or the alternative you rejected and why.
- Do not restate the line below it. `# increment counter` above `counter += 1` adds noise and a second thing to keep in sync.
- If a comment is needed to explain what a block does, first try a clearer name or a smaller function. Comment what is left.
- Name the source of a surprising value: the spec section, the ticket, the measurement.

## Update docs in the same change

- When a change alters behavior, update the comments, docstrings, README sections and instruction files that describe it in that same change. Do not leave a doc update as a follow-up.
- Search the docs for the names you changed, as you would search code.
- New public behavior needs a description where users will look for it. Removed behavior needs its description removed (see `docs-match-code`).

## Write for the AI and human reader

- Both readers need the same things: exact names they can search for, the real command to run, the real path, and a statement of when a rule applies.
- Lead with the point. An agent loads a file partially and a person skims, so put the answer first and the background after.
- Prefer concrete examples with real values over abstract descriptions. Keep each example short enough to be correct.
- Keep one canonical term for each concept, and use it everywhere. A synonym reads as a different thing to a literal-minded reader.
- Say what is true now. Leave out narration of how it got that way.

## Plain-language rules

These are the habits that make prose read as written by a person who knows the subject, distilled from the humanize skill's review rules.

- **Specifics over abstractions.** Name the thing, the number, the file. If you do not know the specific, leave the sentence out rather than invent one. Never make up a statistic, source or quote.
- **Cut throat-clearing.** Do not open by restating the title or announcing what you are about to say, and do not close by summarizing what you just said. Ask of each sentence what it adds.
- **Short ordinary words.** Prefer "use" to "utilize" and "show" to "demonstrate". Avoid stock filler vocabulary and stacked hedges.
- **Do not swap synonyms to disguise a tic.** If a word is vague, rewrite the clause so it is not needed.
- **Verbs over nominalizations.** Write "we decide" rather than "we make a decision".
- **Active voice by default.** Passive is fine when the actor does not matter.
- **Hedge only real uncertainty**, and say what is uncertain. Do not hedge by reflex.
- **Vary rhythm because the content calls for it**, not to hit a quota. Do not break every list into groups of three or end every paragraph on a tidy one-line moral.
- **Punctuation does a job.** Use a comma, colon, parentheses or a new sentence rather than a dash. Do not run clauses together to avoid one.
- **Keep one tense and one register** through a passage.
- **State the premise** behind a claim, or weaken the claim to what you can support.
- **Visible characters only.** Never paste look-alike or invisible Unicode characters into text.

Where the host has the humanize skill, run it over prose you wrote and review its findings. Where it does not, apply these rules by hand.

## Why this matters

Good comments carry the knowledge the code cannot: why it is this way. Docs updated with the change stay true, and plain prose is read, trusted and acted on, where padded or formulaic prose is skimmed and discounted.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
