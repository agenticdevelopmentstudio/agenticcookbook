# Phase 2 batch 13 report

Four principles, each converted from a single intro (statement plus bullets) to roled parts. In every
topic the statement paragraph stays in `intro`, the bullets become the `rules` part, and the three bar parts
are new. None of these principles had an RFC 2119 keyword, so every rule is promoted. No topic had text
written for a reviewer, so all three bar parts are **authored** in every topic.

## Where principles differ from the brief

- **A colon lead-in has to map to its rules, and those rules or their rationale must hold its words.** In
  `tight-feedback-loops` the statement was "The speed of your feedback loop is the speed of your learning:",
  ending in a colon and introducing the bullets. `cookr roles lossless` reads it as a bare lead-in, so it
  cannot map to `intro`. It refuses that mapping with "a lead-in maps to the rules it introduced". It must map
  to its rules, and the rules or their rationale must hold its content words (speed, loop, learning). A
  lead-in may name more than three rules. The fix was a `rationale` part giving the statement as the reason
  for all four rules. The intro keeps the statement too, ending in a period, because `pf-statement` and
  `GF-01` require one after the H1.
- **Bullets with no keyword.** All the bullets are imperatives or plain statements. Each one became SHOULD
  (or SHOULD NOT, or MAY), because none says "never" or "always".
- `approve.py`, `roles check` and `bump` worked on principles without any changes. `bump` writes a
  `versions/<old>/` snapshot inside the folder, and it is committed with that folder.

## cookbook/principles/suppress-unsupported-confidence

**promoted** (6 rules):
- "Score a claim by its evidence, not by how certain it sounds." → `should-score-claims-by-evidence`: "A claim SHOULD be scored by its evidence, not by how certain it sounds."
- "Words like "proven" or "scientists confirm" without a supporting citation lower trust, not raise it." → `should-lower-trust-for-uncited-certainty`: "Words like "proven" or "scientists confirm" without a supporting citation SHOULD lower trust, not raise it."
- "Surfacing a popular-but-unsupported claim and scoring it low is useful; presenting it as true is not." → split in two:
  - `may-surface-unsupported-claims-scored-low`: "A popular-but-unsupported claim MAY be surfaced and scored low; doing so is useful." ("is useful" was read as a permission, MAY. It could be read as SHOULD, so a judge should check it.)
  - `should-not-present-unsupported-claims-as-true`: "A popular-but-unsupported claim SHOULD NOT be presented as true."
- "Match stated confidence to the strength and independence of the sources." → `should-match-confidence-to-sources`: "Stated confidence SHOULD match the strength and independence of the sources."
- "Urgency and emotional framing are signals to scrutinize harder, not to believe." → `should-scrutinize-urgency-and-emotion`: "Urgency and emotional framing SHOULD be treated as signals to scrutinize harder, not to believe."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/tight-feedback-loops

**promoted** (4 rules):
- "Optimize test suite runtime — slow tests do not get run" → `should-optimize-test-suite-runtime`: "Test suite runtime SHOULD be optimized — slow tests do not get run."
- "Deploy small changes frequently" → `should-deploy-small-changes-frequently`: "Small changes SHOULD be deployed frequently."
- "Get real user feedback as early as possible" → `should-get-real-user-feedback-early`: "Real user feedback SHOULD be gotten as early as possible."
- "Automate everything between commit and production observation" → `should-automate-commit-to-observation`: "Everything between commit and production observation SHOULD be automated."

The lead-in "The speed of your feedback loop is the speed of your learning:" maps to all four rules. A
`rationale` part carries its text as their reason (see above), and the intro keeps it as the statement.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/type-precedes-method

**promoted** (5 rules):
- "Classify the topic's type (medical, technical, legal, financial, news, consumer, …) before searching." → `should-classify-topic-type-before-searching`: "SHOULD classify the topic's type (medical, technical, legal, financial, news, consumer, …) before searching."
- "The type — not the user's wording or urgency — selects which sources count as authoritative." → `should-select-authoritative-sources-by-type`: "The type — not the user's wording or urgency — SHOULD select which sources count as authoritative."
- "The type sets the evidence bar: a treatment claim and a recipe claim are not held to the same standard." → `should-set-evidence-bar-by-type`: "The type SHOULD set the evidence bar: a treatment claim and a recipe claim are not held to the same standard."
- "A method that fits one type (web consensus for a recipe) is wrong for another (clinical trials for a treatment)." → `should-not-carry-method-across-types`: "A method that fits one type (web consensus for a recipe) is wrong for another (clinical trials for a treatment), and SHOULD NOT be carried over to it."
- "When a topic spans types, classify each claim by the type it asserts." → `should-classify-each-claim-by-its-type`: "When a topic spans types, SHOULD classify each claim by the type it asserts."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/yagni

**promoted** (3 rules):
- "Before adding a parameter, config option, or extension point, confirm a current requirement demands it" → `should-confirm-requirement-before-adding-extension-points`: "Before adding a parameter, config option, or extension point, SHOULD confirm a current requirement demands it."
- "Delete dead code and unused abstractions — they are not "free" to keep around" → `should-delete-dead-code-and-unused-abstractions`: "SHOULD delete dead code and unused abstractions — they are not "free" to keep around."
- "When someone says "we might need this later," treat that as a reason to wait, not a reason to build" → `should-treat-might-need-later-as-reason-to-wait`: "When someone says "we might need this later," SHOULD treat that as a reason to wait, not a reason to build."

The statement paragraph, including its reasoning sentences, stays in `intro` as written.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.
