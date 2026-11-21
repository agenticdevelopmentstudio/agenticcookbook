---
id: 456f23bd-4523-47e8-9541-073ac046f2ad
title: Requirement Keywords
type: guideline
version: 1.0.0
status: draft
language: en
created: 2026-11-21
modified: 2026-11-21
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "How cookbook rules use RFC 2119 keywords: what MUST, SHOULD and MAY mean, case, where keywords belong, and how a keyword sets a lint finding's severity."
platforms: []
tags:
  - authoring
  - requirement-keywords
  - rfc-2119
  - lint-severity
depends-on: []
related: []
references:
  - https://www.rfc-editor.org/rfc/rfc2119.txt
  - https://www.rfc-editor.org/rfc/rfc8174.txt
  - https://www.rfc-editor.org/rfc/rfc7322.txt
  - https://www.w3.org/TR/qaframe-spec/
  - https://www.w3.org/guide/manual-of-style/
  - https://www.w3.org/wiki/RfcKeywords
  - https://infra.spec.whatwg.org/
  - https://www.oasis-open.org/?p=3585
  - https://portal.etsi.org/Services/editHelp/Search/FAQs/Requirements
  - https://respec.org/docs/
  - https://speced.github.io/bikeshed/
  - https://raw.githubusercontent.com/ietf-tools/idnits/main/idnits
  - https://vale.sh/docs/styles
  - https://eslint.org/docs/latest/use/configure/rules
  - https://eslint.org/docs/latest/use/command-line-interface
  - https://github.com/DavidAnson/markdownlint
  - https://github.com/DavidAnson/markdownlint-cli2
  - https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/sarif-v2.1.0-errata01-os-complete.html
  - https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/triaging-code-scanning-alerts-in-pull-requests
triggers:
  - recipe-authoring
---

# Requirement Keywords

Cookbook rules state their obligation with the requirement keywords of RFC 2119 and RFC 8174 (BCP 14). The keyword says how firm a rule is, so it decides how a builder follows the rule, how a reviewer judges it, and how severe a lint finding against it is.

## Rules

- **gf-rfc-keywords**: Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels. (claim: gf-rfc-keywords-prior)
- **gf-rfc-keywords-bold-or-uppercase**: Keywords MUST be bold or uppercase when used normatively. (claim: gf-rfc-keywords-bold-or-uppercase-prior)
- **use-rfc-2119-keywords-for-behavioral-requirements**: An artifact MUST follow this convention: Use RFC 2119 keywords for all behavioral requirements: (claim: use-rfc-2119-keywords-for-behavioral-requirements-prior)
- **rule-uses-rfc-2119-keywords**: **Use RFC 2119 keywords** for requirements — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY. (claim: rule-uses-rfc-2119-keywords-prior)
- **must-is-absolute-requirement**: A rule's MUST MUST be read as an absolute requirement and its MUST NOT as an absolute prohibition: no deviation from either is permitted. (claims: rfc2119-must-absolute-requirement, rfc2119-must-not-absolute-prohibition, iso-shall-requirement)
- **should-is-recommendation**: A rule's SHOULD MUST be read as a recommendation, a preferred but not required course, and its SHOULD NOT as a negative recommendation, a deprecated but not prohibited one: valid reasons to deviate may exist, but the full implications MUST be understood and carefully weighed before deviating. (claims: rfc2119-should-recommendation, rfc2119-should-not-recommendation, iso-should-preferred)
- **may-is-optional-behavior**: A rule's MAY MUST be read as marking an item that is truly optional: a course of action permitted, not required. (claims: rfc2119-may-truly-optional, iso-may-permission)
- **follow-must-address-should-checks**: A builder or reviewer MUST follow every MUST check, and MUST address every SHOULD check unless there is a documented reason to skip it. (claims: rfc2119-must-absolute-requirement, rfc2119-should-recommendation, qa-indicate-levels, qa-conformance-classes-by-level)
- **approve-on-zero-fail**: `/approve-artifact` MUST run `/lint-artifact` on a cookbook artifact and stamp the frontmatter with approval metadata only when it passes with zero FAIL findings; when it fails, it MUST report the issues and MUST NOT approve. (claims: vale-only-errors-nonzero, eslint-error-for-ci, github-check-fails-on-error, bikeshed-die-on)
- **keywords-meaningful-only-in-uppercase**: Where the cookbook follows BCP 14 as RFC 8174 states it, only the UPPERCASE form of a keyword MUST be read as carrying its defined meaning; the same word not capitalized has its normal English meaning and states no requirement, so changing a keyword's case is a material change to the requirement. A document that declares a different convention, as WHATWG Infra's willful violation of RFC 8174 gives the lowercase forms the same meaning, is read by its declaration. (claims: uppercase-only-meaning, lowercase-has-normal-english-meaning, oasis-uppercase-only, oasis-case-change-is-material, infra-willful-violation, infra-lowercase-equivalent)
- **lowercase-keyword-in-rule-text-flagged**: Where only UPPERCASE keywords carry meaning, the linter SHOULD flag a keyword word written in lowercase in a named rule's text for manual review, since a document rarely avoids every ordinary-sense use, a keyword used in its ordinary sense is an editorial error to reword, and fixing it by changing its case changes the requirement. (claims: sperberg-mcqueen-lowercase-misuse, fantasai-lowercase-misuse-is-editorial-error, oasis-case-change-is-material, bikeshed-accidental-2119, caceres-respec-defaults-bcp14, lint-unmarked-keyword-usage, eslint-warn-for-uncertain)
- **state-the-keyword-interpretation**: A document that uses the keywords SHOULD state their interpretation near its beginning, either by citing RFC 2119 with the BCP 14 boilerplate, which names the keywords and says they carry that meaning only in all capitals, or by specifying its own interpretation, as Bikeshed's generated conformance text declares its keywords are not in uppercase; a linter SHOULD warn when keywords are present and that statement is missing. (claims: state-the-interpretation, bcp14-boilerplate, idnits-boilerplate-check, respec-conformance-boilerplate, respec-warns-missing-conformance, bikeshed-lowercase-for-readability)
- **state-how-keywordless-text-is-read**: A document SHOULD state its requirements in one consistent style and tell readers which styles it uses and how to tell them apart, because normative text does not need a keyword: an 'is' statement or an algorithm step can be MUST-equivalent, and everything outside assertions, diagrams, examples and notes can be normative. (claims: qa-consistent-style-explain, keywords-not-required-for-normative-text, infra-no-keywords-in-non-normative, tab-keywordless-must-equivalent)
- **no-keywords-in-non-normative-text**: Informative content, such as examples, notes and sections marked informative, SHOULD NOT use the keywords in any case; requirements belong only in normative text, and a linter MAY flag a keyword found in a non-normative section. (claims: qa-no-normative-language-in-informative, w3c-mos-no-keywords-informative, infra-lowercase-equivalent, etsi-requirements-only-normative, bikeshed-accidental-2119)
- **keyword-sets-finding-severity**: By default a lint check SHOULD take its finding's severity from the keyword of the rule it checks: a broken MUST or MUST NOT is a FAIL, the analogue of an error, a serious problem; a missed SHOULD or SHOULD NOT is a WARN, a problem below error; a MAY gives no finding beyond, at most, a note of an opportunity to improve. The level stays configurable per check. (claims: rfc2119-must-absolute-requirement, rfc2119-should-recommendation, rfc2119-may-truly-optional, qa-conformance-classes-by-level, sarif-error-level, sarif-warning-level, sarif-note-level, eslint-warn-for-uncertain, markdownlint-error-or-warning, respec-lint-severity, bikeshed-error-levels)
- **warn-findings-do-not-block**: By default WARN findings SHOULD NOT fail a lint run or block approval; only FAIL findings do, and a threshold that makes warnings block is an opt-in setting. (claims: vale-only-errors-nonzero, vale-minalertlevel-ci, eslint-warn-no-exit-code, eslint-max-warnings, markdownlint-cli2-exit-codes, github-check-fails-on-error, github-ruleset-blocks-merge, bikeshed-die-on-default-fatal)
- **one-keyword-per-requirement**: Each requirement SHOULD take the form subject, one keyword, operation, in the active form 'X MUST do Y' rather than the passive 'X MUST be Y'. (claims: qa-subject-keyword-operation, w3c-wiki-active-form)
- **use-core-keyword-subset**: Rules SHOULD limit themselves to MUST, MUST NOT, SHOULD and MAY, preferring MUST over SHALL. (claims: infra-core-subset, plainlanguage-must-not-shall)
- **no-mixed-case-negation-or-may-not**: A rule SHOULD NOT pair an uppercase keyword with a lowercase not, as in 'MUST not', and SHOULD NOT write MAY NOT, which is not a keyword and cannot express a prohibition; a prohibition is written MUST NOT. (claims: idnits-mixed-case-not, idnits-may-not, oasis-may-not-not-keyword, iso-no-may-not)
- **one-keyword-set-never-mixed**: An artifact SHOULD use one keyword set, the RFC 2119 set or the ISO/IEC verbal forms, and never mix the two, nor use must and shall together; the ISO/IEC forms are keywords by definition rather than typography, and work without capitals only because those verbs are never used in non-standard senses. (claims: oasis-never-mix-keyword-sets, iso-no-must-for-shall, plainlanguage-must-not-shall, oasis-iso-keywords-by-definition, sperberg-mcqueen-iso-avoids-nonstandard-senses)
- **keywords-only-where-required**: Keywords SHOULD be used with care and sparingly, only where a requirement actually needs one, so that marking them distinctly keeps conformance requirements easy to spot and helps readers focus on what is and is not a requirement. Sources differ on formatting beyond case: the W3C Manual of Style asks for an em element with the rfc2119 class, and a spec editor recommends dropping that requirement. (claims: keywords-used-sparingly, sperberg-mcqueen-focus-attention, keywords-make-requirements-easy-to-spot, w3c-mos-uppercase-em, tab-drop-formatting-requirement, fantasai-styling-requirement)

## Reading a keyword

| Keyword | Meaning | Lint finding when broken |
|---------|---------|--------------------------|
| MUST | Absolute requirement | FAIL |
| MUST NOT | Absolute prohibition | FAIL |
| SHOULD | Recommendation; deviate only after weighing the implications | WARN |
| SHOULD NOT | Negative recommendation; do it only after weighing the implications | WARN |
| MAY | Truly optional | none, at most a note |

## Writing a requirement

1. Name the subject: the artifact, builder, reviewer or check the rule binds.
2. Pick one keyword, in uppercase.
3. Name the operation as an active verb.
4. Keep the keyword out of examples, notes and rationale.

## Examples

Good: "A migration MUST record its schema version."

Weak, passive: "The schema version MUST be recorded."

Wrong, mixed-case negation: "A migration MUST not drop a column."

Wrong, not a keyword: "A client MAY NOT retry."

## What a reviewer looks for

Checks that every requirement carries one uppercase keyword in the form subject, keyword, operation, read as RFC 2119 defines it; that the keyword interpretation is stated; that keywords stay out of informative text; that only one keyword set is used, with no 'MUST not' or 'MAY NOT'; and that lint severity and approval follow the keyword: FAIL for MUST, WARN for SHOULD, and approval only at zero FAIL.

## A complete review must establish

- Every requirement uses an RFC 2119 keyword in uppercase, in the form subject, keyword, operation
- MUST and MUST NOT are treated as absolute, SHOULD and SHOULD NOT as recommendations weighed before deviating, and MAY as truly optional
- The keyword interpretation is stated near the beginning of the document
- No keyword appears in examples, notes or other informative text
- One keyword set is used throughout; no 'MUST not' and no 'MAY NOT'
- Lint findings take their severity from the keyword, and approval needs zero FAIL findings
- Every MUST rule is kept, with no exception: `gf-rfc-keywords`, `gf-rfc-keywords-bold-or-uppercase`, `use-rfc-2119-keywords-for-behavioral-requirements`, `rule-uses-rfc-2119-keywords`, `must-is-absolute-requirement`, `should-is-recommendation`, `may-is-optional-behavior`, `follow-must-address-should-checks`, `approve-on-zero-fail`, `keywords-meaningful-only-in-uppercase`
- Every SHOULD rule is kept, or the change says why not: `lowercase-keyword-in-rule-text-flagged`, `state-the-keyword-interpretation`, `state-how-keywordless-text-is-read`, `no-keywords-in-non-normative-text`, `keyword-sets-finding-severity`, `warn-findings-do-not-block`, `one-keyword-per-requirement`, `use-core-keyword-subset`, `no-mixed-case-negation-or-may-not`, `one-keyword-set-never-mixed`, `keywords-only-where-required`

A review passes when it establishes every item above.

## A build must establish

- `gf-rfc-keywords`: every requirement in the guideline uses one of MUST, MUST NOT, SHOULD, SHOULD NOT or MAY
- `gf-rfc-keywords-bold-or-uppercase`: every keyword used normatively is bold or uppercase
- `use-rfc-2119-keywords-for-behavioral-requirements`: every behavioral requirement uses an RFC 2119 keyword
- `rule-uses-rfc-2119-keywords`: every rule states its requirement with MUST, MUST NOT, SHOULD, SHOULD NOT or MAY
- `must-is-absolute-requirement`: every MUST is followed and every MUST NOT avoided, with no deviation
- `should-is-recommendation`: every deviation from a SHOULD or SHOULD NOT was made only after its implications were weighed
- `may-is-optional-behavior`: no MAY item is treated as required
- `follow-must-address-should-checks`: every MUST check is followed, and every SHOULD check is addressed or skipped with a documented reason
- `approve-on-zero-fail`: approval metadata is stamped only after `/lint-artifact` reports zero FAIL findings, and a failing run reports its issues without approving
- `keywords-meaningful-only-in-uppercase`: every keyword meant to carry its BCP 14 meaning is uppercase, unless the document declares another convention
- `lowercase-keyword-in-rule-text-flagged`: the linter flags a lowercase keyword word in a named rule's text for review
- `state-the-keyword-interpretation`: the document states its keyword interpretation near its beginning
- `state-how-keywordless-text-is-read`: the document says which requirement styles it uses and how to tell them apart
- `no-keywords-in-non-normative-text`: no keyword appears in examples, notes or informative sections
- `keyword-sets-finding-severity`: each lint check's default severity follows its rule's keyword: FAIL for MUST, WARN for SHOULD, at most a note for MAY
- `warn-findings-do-not-block`: by default a run with only WARN findings neither fails nor blocks approval
- `one-keyword-per-requirement`: each requirement has one keyword in the form subject, keyword, operation, written actively
- `use-core-keyword-subset`: rules use MUST, MUST NOT, SHOULD and MAY, and MUST rather than SHALL
- `no-mixed-case-negation-or-may-not`: no rule writes 'MUST not' or 'MAY NOT'
- `one-keyword-set-never-mixed`: the artifact uses one keyword set and never mixes must and shall
- `keywords-only-where-required`: keywords appear only where a requirement needs one

## Rationale

- `must-is-absolute-requirement`, `should-is-recommendation`, `may-is-optional-behavior`: RFC 2119 defines the three levels, and ISO/IEC Directives Part 2 draws the same lines with shall, should and may.
- `keywords-meaningful-only-in-uppercase`, `lowercase-keyword-in-rule-text-flagged`: RFC 8174 gives the defined meaning to the uppercase forms only; in lowercase the words are ordinary English, so a stray lowercase keyword is either an editorial error or a hidden requirement.
- `state-the-keyword-interpretation`, `state-how-keywordless-text-is-read`: RFC 7322 asks a document to cite RFC 2119 or give its own interpretation, and the W3C QA Framework asks a specification to say which requirement styles it uses.
- `no-keywords-in-non-normative-text`: the W3C QA Framework, the W3C Manual of Style, WHATWG Infra and ETSI keep requirement language out of informative text.
- `keyword-sets-finding-severity`, `warn-findings-do-not-block`, `approve-on-zero-fail`: Vale, ESLint, markdownlint, SARIF, Bikeshed and GitHub code scanning all separate errors from warnings, and by default only errors fail a run.
- `one-keyword-per-requirement`, `use-core-keyword-subset`, `no-mixed-case-negation-or-may-not`, `one-keyword-set-never-mixed`: the W3C QA Framework, WHATWG Infra, IETF idnits, OASIS and ISO/IEC each narrow the forms a requirement can take so that it reads one way.
- `keywords-only-where-required`: RFC 2119 asks for the keywords to be used sparingly, so that the ones that appear stand out.

## References

- [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119.txt)
- [RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174.txt)
- [RFC 7322: RFC Style Guide](https://www.rfc-editor.org/rfc/rfc7322.txt)
- [W3C QA Framework: Specification Guidelines](https://www.w3.org/TR/qaframe-spec/)
- [W3C Manual of Style](https://www.w3.org/guide/manual-of-style/)
- [W3C wiki: RfcKeywords](https://www.w3.org/wiki/RfcKeywords)
- [WHATWG Infra Standard](https://infra.spec.whatwg.org/)
- [OASIS: Keywords in OASIS specifications](https://www.oasis-open.org/?p=3585)
- [ETSI: Requirements FAQ](https://portal.etsi.org/Services/editHelp/Search/FAQs/Requirements)
- [ReSpec documentation](https://respec.org/docs/)
- [Bikeshed documentation](https://speced.github.io/bikeshed/)
- [IETF idnits](https://raw.githubusercontent.com/ietf-tools/idnits/main/idnits)
- [Vale styles](https://vale.sh/docs/styles)
- [ESLint: Configure rules](https://eslint.org/docs/latest/use/configure/rules)
- [ESLint: Command line interface](https://eslint.org/docs/latest/use/command-line-interface)
- [markdownlint](https://github.com/DavidAnson/markdownlint)
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
- [SARIF v2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/sarif-v2.1.0-errata01-os-complete.html)
- [GitHub: Triaging code scanning alerts in pull requests](https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/triaging-code-scanning-alerts-in-pull-requests)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-21 | Mike Fullerton | Initial version |
