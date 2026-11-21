# Write brief: requirement-keywords

Today is 2026-11-21.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/cookbook/authoring/topics/requirement-keywords/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/skills/cookr/cli /private/tmp/claude-501/-Users-mfullerton-Development-projects-myagenticteams-teamtesting--claude-worktrees-devteam-scope-specialists/42c82725-9e4b-4ae4-aed3-3ac87a841295/scratchpad/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/tbd/compliance/artifact-formatting/guideline-formatting.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- gf-rfc-keywords: unsupported (claims: gf-rfc-keywords-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, oasis-should-use-rfc2119, keywords-make-requirements-easy-to-spot)
- gf-rfc-keywords-bold-or-uppercase: contradicted (claims: gf-rfc-keywords-bold-or-uppercase-prior, uppercase-only-meaning, lowercase-has-normal-english-meaning, bcp14-boilerplate, oasis-uppercase-only)
- use-rfc-2119-keywords-for-behavioral-requirements: unsupported (claims: use-rfc-2119-keywords-for-behavioral-requirements-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, tab-keywordless-must-equivalent)
- must-is-absolute-requirement: supported (claims: rfc2119-must-absolute-requirement, rfc2119-must-not-absolute-prohibition, iso-shall-requirement)
- should-is-recommendation: supported (claims: rfc2119-should-recommendation, rfc2119-should-not-recommendation, iso-should-preferred)
- may-is-optional-behavior: supported (claims: rfc2119-may-truly-optional, iso-may-permission)
- rule-uses-rfc-2119-keywords: unsupported (claims: rule-uses-rfc-2119-keywords-prior, keywords-not-required-for-normative-text, oasis-should-use-rfc2119, infra-core-subset)
- follow-must-address-should-checks: supported (claims: rfc2119-must-absolute-requirement, rfc2119-should-recommendation, qa-indicate-levels, qa-conformance-classes-by-level)
- approve-on-zero-fail: supported (claims: vale-only-errors-nonzero, eslint-error-for-ci, markdownlint-cli2-exit-codes, github-check-fails-on-error, bikeshed-die-on, bikeshed-die-on-default-fatal)
- keywords-meaningful-only-in-uppercase: new (claims: uppercase-only-meaning, lowercase-has-normal-english-meaning, oasis-uppercase-only, oasis-case-change-is-material, infra-willful-violation, infra-lowercase-equivalent, bikeshed-lowercase-for-readability)
- lowercase-keyword-in-rule-text-flagged: new (claims: sperberg-mcqueen-lowercase-misuse, fantasai-lowercase-misuse-is-editorial-error, oasis-case-change-is-material, bikeshed-accidental-2119, caceres-respec-defaults-bcp14, lint-unmarked-keyword-usage, eslint-warn-for-uncertain)
- state-the-keyword-interpretation: new (claims: state-the-interpretation, bcp14-boilerplate, idnits-boilerplate-check, respec-conformance-boilerplate, respec-warns-missing-conformance)
- state-how-keywordless-text-is-read: new (claims: qa-consistent-style-explain, keywords-not-required-for-normative-text, infra-no-keywords-in-non-normative, tab-keywordless-must-equivalent)
- no-keywords-in-non-normative-text: new (claims: qa-no-normative-language-in-informative, w3c-mos-no-keywords-informative, infra-lowercase-equivalent, etsi-requirements-only-normative, bikeshed-accidental-2119)
- keyword-sets-finding-severity: new (claims: rfc2119-must-absolute-requirement, rfc2119-should-recommendation, rfc2119-may-truly-optional, qa-conformance-classes-by-level, sarif-error-level, sarif-warning-level, sarif-note-level, eslint-warn-for-uncertain, markdownlint-error-or-warning, respec-lint-severity, bikeshed-error-levels)
- warn-findings-do-not-block: new (claims: vale-only-errors-nonzero, vale-minalertlevel-ci, eslint-warn-no-exit-code, eslint-max-warnings, markdownlint-cli2-exit-codes, github-check-fails-on-error, github-ruleset-blocks-merge, bikeshed-die-on-default-fatal)
- one-keyword-per-requirement: new (claims: qa-subject-keyword-operation, w3c-wiki-active-form)
- use-core-keyword-subset: new (claims: infra-core-subset, plainlanguage-must-not-shall)
- no-mixed-case-negation-or-may-not: new (claims: idnits-mixed-case-not, idnits-may-not, oasis-may-not-not-keyword, iso-no-may-not)
- one-keyword-set-never-mixed: new (claims: oasis-never-mix-keyword-sets, iso-no-must-for-shall, plainlanguage-must-not-shall, oasis-iso-keywords-by-definition, sperberg-mcqueen-iso-avoids-nonstandard-senses)
- keywords-only-where-required: new (claims: keywords-used-sparingly, sperberg-mcqueen-focus-attention, keywords-make-requirements-easy-to-spot, w3c-mos-uppercase-em, tab-drop-formatting-requirement, fantasai-styling-requirement)

Second-check corrections, refuted (criteria 3 applies to these claims):
- bcp14-boilerplate: refuted (quote-found yes, supports-claim partly); trust 88 -> 68; a rule citing it cannot carry MUST
- bikeshed-lowercase-for-readability: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- eslint-warn-for-uncertain: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- state-the-interpretation: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST
- idnits-boilerplate-check: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST; dropped 1 citation(s) lacking the quote; independence single -> single
- qa-consistent-style-explain: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- etsi-requirements-only-normative: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- sarif-warning-level: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- respec-lint-severity: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- vale-minalertlevel-ci: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- eslint-warn-no-exit-code: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- markdownlint-cli2-exit-codes: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- github-ruleset-blocks-merge: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- bikeshed-die-on-default-fatal: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- plainlanguage-must-not-shall: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **gf-rfc-keywords** — verdict `unsupported` (claims: gf-rfc-keywords-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, oasis-should-use-rfc2119, keywords-make-requirements-easy-to-spot). Prior text, kept word for word: "Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels."
  - against: Using the keywords is not required: normative text does not need them, and much normative text without them is still normative.
  - against: Specifications convey conformance requirements in different styles (RFC 2119 keywords, imperative voice, descriptive assertions); a specification must use a consistent style and tell readers which styles it uses and how to distinguish them.
  - against: OASIS says work products that become specifications should use RFC 2119 keywords: a recommendation, not a requirement.
  - against: RFC 2119 keywords make conformance requirements easy to spot, and are usually given distinctive formatting such as uppercase or bold.
- **gf-rfc-keywords-bold-or-uppercase** — verdict `contradicted` (claims: gf-rfc-keywords-bold-or-uppercase-prior, uppercase-only-meaning, lowercase-has-normal-english-meaning, bcp14-boilerplate, oasis-uppercase-only). Prior text, kept word for word: "Keywords MUST be bold or uppercase when used normatively."
  - against: Only the UPPERCASE forms of the keywords carry the defined BCP 14 meanings.
  - against: When the words are not capitalized they have their normal English meanings and BCP 14 does not apply to them.
  - against: A document that follows BCP 14 states near its beginning a boilerplate that names the keywords and says they carry the BCP 14 meaning only in all capitals.
  - against: OASIS writes RFC 2119 keywords in UPPERCASE; in lowercase they have only normal English meaning and state no requirement.
- **use-rfc-2119-keywords-for-behavioral-requirements** — verdict `unsupported` (claims: use-rfc-2119-keywords-for-behavioral-requirements-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, tab-keywordless-must-equivalent). Prior text, kept word for word: "Use RFC 2119 keywords for all behavioral requirements:" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Using the keywords is not required: normative text does not need them, and much normative text without them is still normative.
  - against: Specifications convey conformance requirements in different styles (RFC 2119 keywords, imperative voice, descriptive assertions); a specification must use a consistent style and tell readers which styles it uses and how to distinguish them.
  - against: Specifications state many requirements without any keyword, through 'is' statements and algorithm steps that are MUST-equivalent, so a keyword-only reading misses them.
- **rule-uses-rfc-2119-keywords** — verdict `unsupported` (claims: rule-uses-rfc-2119-keywords-prior, keywords-not-required-for-normative-text, oasis-should-use-rfc2119, infra-core-subset). Prior text, kept word for word: "**Use RFC 2119 keywords** for requirements — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY."
  - against: Using the keywords is not required: normative text does not need them, and much normative text without them is still normative.
  - against: OASIS says work products that become specifications should use RFC 2119 keywords: a recommendation, not a requirement.
  - against: WHATWG Infra encourages documents to limit themselves to must, must not, should and may.

## Open questions

- Case convention: follow RFC 8174 (only all-capital keywords carry meaning) or WHATWG Infra's willful violation (lowercase keywords carry the same meaning and are preferred for legibility); the sources support either if declared, and the owner chooses one.
- Whether skipping a SHOULD requires a documented reason (follow-must-address-should-checks) or only that the implications be understood and weighed (RFC 2119's wording); RFC 2119 does not require documentation.
- Whether warnings ever block /approve-artifact (an ESLint --max-warnings style threshold) or never do; the tools make a warning threshold optional and default to warnings not blocking.
- Whether rules restrict themselves to the five keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY (as Infra encourages) or also admit SHALL, REQUIRED, RECOMMENDED and OPTIONAL as BCP 14 defines them.
- Whether a lowercase keyword found in rule text is reported as a WARN (as Bikeshed's opt-in accidental-2119 lint and ReSpec's warnings do) or a FAIL.
- Whether lint-artifact's GF-03 level 'WARN if missing' stays a warning; the sources support a keyword as SHOULD, which maps to a warning, but the owner decides.
- Whether keywords are additionally styled (bold, or the W3C Manual of Style's em with class rfc2119) for readability; no source makes styling carry the meaning, and a W3C editor recommends dropping the formatting requirement.
