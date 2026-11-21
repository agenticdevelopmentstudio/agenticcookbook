## uppercase-only-meaning
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 8174 Abstract says this word for word.

## lowercase-has-normal-english-meaning
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 8174 Section 2 says this word for word.

## bcp14-boilerplate
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is only the boilerplate text. The claim's point that a document states it "near its beginning" is not in the quote; RFC 8174 says that in a separate sentence ("should incorporate this phrase near the beginning").
- correction: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST

## oasis-uppercase-only
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The OASIS keyword guidance page says this word for word.

## oasis-case-change-is-material
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The only differences are spaces around the bracketed "[RFC 2119]".

## infra-willful-violation
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: In Infra §2.1, "This" follows the sentence giving the keywords equivalent meaning in lowercase. §2.2 repeats that §2.1 is a willful violation of RFC 8174.

## infra-lowercase-equivalent
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Infra §2.1 says this word for word.

## bikeshed-lowercase-for-readability
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only the readability and lowercase point. The page's previous sentence says requirements combine "descriptive assertions and RFC 2119 terminology", but that sentence is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST

## sperberg-mcqueen-lowercase-misuse
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source is about claims that every "must" and "may" is a conformance use. He says he never saw such a claim survive inspection, which is at least as strong as the claim's "rarely".

## fantasai-lowercase-misuse-is-editorial-error
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "Such instances" refers to the ordinary-sense uses of must and may in the message being quoted. The author's view is hedged with "Afaict".

## bikeshed-accidental-2119
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The only differences are spaces around the parenthesised list. "default: off" is what makes the lint opt-in.

## caceres-respec-defaults-bcp14
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is Marcos Caceres's reply on spec-prod; "IIRC" hedges the warning part.

## lint-unmarked-keyword-usage
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Caceres's message quotes this text from Tab Atkins's plan for Bikeshed (issue #2564), so the proposal is Atkins's, not Caceres's.

## eslint-warn-for-uncertain
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only the uncertain or false-positive use. The page's "introducing a new rule that will eventually be set to error" clause is not in the quote, and the page lists a third use the claim leaves out (flagging non-error issues).
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## state-the-interpretation
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: RFC 7322 (the RFC Style Guide) scopes the rule to "IETF documents" and RFCs. The claim applies it to any document.
- correction: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST

## idnits-boilerplate-check
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- citation 2: lacks-quote
- result: refuted
- note: The quote is a fragment of a message in the idnits source. The split the claim describes (error with no reference, warning with only the boilerplate off) comes from the code around it (`sectionerr` vs `sectionwarn`), not from the quote. The author-tools page is only an upload form.
- correction: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST; dropped 1 citation(s) lacking the quote; independence single -> single

## respec-conformance-boilerplate
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The ReSpec docs say this word for word.

## respec-warns-missing-conformance
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The ReSpec docs say this word for word.

## qa-consistent-style-explain
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote supports only "tell readers what styles are used". The duty to "use a consistent style" and explain "how to distinguish them" is in Requirement 7's title, which the quote leaves out.
- correction: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST

## keywords-not-required-for-normative-text
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 8174 says this word for word.

## infra-no-keywords-in-non-normative
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The claim text matches the quote, though the claim id ("no keywords") describes something different from the claim text.

## tab-keywordless-must-equivalent
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is Tab Atkins on spec-prod (signed ~TJ). It is one editor's argument, not a standard.

## qa-no-normative-language-in-informative
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source is the QA Framework's Techniques text under Requirement 7.

## w3c-mos-no-keywords-informative
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Manual of Style says this word for word.

## etsi-requirements-only-normative
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only the first half. The "avoid shall/must ... in informative deliverables (TR, EG, SR, GR)" part is in the page's next sentence, which is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST

## rfc2119-must-absolute-requirement
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 2119 §1 says this word for word.

## rfc2119-should-recommendation
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 2119 §3 says this word for word.

## rfc2119-may-truly-optional
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 2119 §5 opens with this sentence.

## qa-conformance-classes-by-level
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The only differences are spaces around the brackets in "[HTTP11]".

## sarif-error-level
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the SARIF 2.1.0 result.level definition. The only differences are spacing around the colon.

## sarif-warning-level
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote says only "a problem was found". "Below error" has to be inferred from the separate error definition ("serious problem"), which the quote does not include.
- correction: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST

## sarif-note-level
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The SARIF result.level definition says this word for word.

## markdownlint-error-or-warning
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The markdownlint README says this word for word.

## respec-lint-severity
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only the true, "warn" and false values. The red and yellow banners are in the page's next sentence, which is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## bikeshed-error-levels
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Bikeshed docs say this word for word.

## vale-only-errors-nonzero
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the `level` row of the rule-keys table on the Vale styles page.

## vale-minalertlevel-ci
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is about the `--minAlertLevel` command-line override and says error-level alerts are "run" in CI. It does not say MinAlertLevel controls which levels are reported, or that errors "fail CI". The page says those things elsewhere.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## eslint-warn-no-exit-code
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only "warn". The claim's "error makes the exit code 1" is in the next list item ("exit code is 1 when triggered"), which is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST

## eslint-max-warnings
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The ESLint CLI docs say this word for word.

## markdownlint-cli2-exit-codes
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only exit code 0. The README's next line has exit 1 for errors, but it is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## github-check-fails-on-error
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GitHub's docs say this word for word, and add that the default can be overridden in repository settings.

## github-ruleset-blocks-merge
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is only one condition from a list. The words that rulesets "prevent pull requests from being merged" are in the sentence before it, which is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## bikeshed-die-on-default-fatal
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: "Defaults to 'fatal'" on its own does not say what defaults. The surrounding `--die-on` text, where each level includes all previous levels, is what supports the claim, and it is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## qa-subject-keyword-operation
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The QA Framework says this word for word.

## w3c-wiki-active-form
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is one contributor's view on a W3C wiki page ("my understanding of the gap"), not formal guidance.

## infra-core-subset
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Infra §2.1 says this word for word.

## plainlanguage-must-not-shall
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers only "use must not shall". The Justice Canada passage ("Drafters should not use 'must' and 'shall' together...") is further down the page and not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST

## idnits-mixed-case-not
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the `bad["MUST not"]` message in the idnits source. The only differences are from string concatenation in the code.

## idnits-may-not
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the `bad["MAY NOT"]` message in the idnits source. The only differences are from string concatenation in the code.

## oasis-may-not-not-keyword
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The OASIS page says this word for word.

## iso-no-may-not
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source is an ISO/IEC Directives Part 2 Annex H excerpt attached to a 2011 IETF list post, so it is an old edition. The current ISO/IEC Directives Part 2 would be a better source.

## oasis-never-mix-keyword-sets
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The OASIS page says this word for word.

## iso-no-must-for-shall
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the same 2011 Annex H excerpt, so the edition is old. The current ISO/IEC Directives Part 2 would be a better source.

## oasis-iso-keywords-by-definition
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The OASIS page says this word for word.

## sperberg-mcqueen-iso-avoids-nonstandard-senses
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is Sperberg-McQueen's message (0018), which fantasai also quotes in 0019.

## keywords-used-sparingly
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 2119 §6 says this word for word.

## sperberg-mcqueen-focus-attention
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: In the source, "it" refers to the special-styling convention for the keywords.

## keywords-make-requirements-easy-to-spot
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both parts of the quote, on either side of the ellipsis, appear in the QA Framework's Requirement 7 Techniques text, with only spacing differences around the brackets.

## w3c-mos-uppercase-em
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Manual of Style says this word for word.

## tab-drop-formatting-requirement
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is Tab Atkins (signed ~TJ) on spec-prod, 2023-05-30.

## fantasai-styling-requirement
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is fantasai's opening message in the thread (she signs 0019 as CSSWG editor). The message ends the sentence with "to make it lowercase small-caps".
