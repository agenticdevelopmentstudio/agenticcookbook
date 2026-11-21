# requirement-keywords: research agent run

The research team could not run (`team_probe.py researchteam`: `ok: false`,
"missing distributions: PyYAML, aiohttp, mcp, websockets"), so the research
ran as one fresh Opus Agent with the `research` prompt as `write_brief.py
prompt research` printed it, on 2026-11-21. Its reply, verbatim:

---

I wrote both research files, but the exact validate command does not print `Research passed.`. It exits 2 with `requirement-keywords: not an artifact source folder (no artifact.json)`. The folder has no `artifact.json` yet, and I was not allowed to create one.

To check the content anyway, I ran the same validator's research checks on the folder directly, inline, with the folder gate and rule-citation checks bypassed. They came back with no findings: claim fields, citations, trust, independence, verdicts, and the four headings in order. Every claim appears in at least one verdict. I also checked each quote against the fetched source text. All matched, apart from line wraps, `&gt;` quote markers in the mailing-list archive, and string joins in the idnits source.

**Files**
- /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords/research/research.json
- /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/requirement-keywords/research/research.md

**Claims per question** (74 in total)

| Question | Claims |
|---|---|
| best-practices | 21 (includes the 4 `-prior` claims) |
| known-solutions | 24 |
| platform-guidelines | 18 |
| experts-view | 11 |

**Verdicts**
- gf-rfc-keywords: unsupported (sources support SHOULD). Claims: gf-rfc-keywords-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, oasis-should-use-rfc2119, keywords-make-requirements-easy-to-spot
- gf-rfc-keywords-bold-or-uppercase: contradicted (bold contradicted; uppercase alone supported). Claims: gf-rfc-keywords-bold-or-uppercase-prior, uppercase-only-meaning, lowercase-has-normal-english-meaning, bcp14-boilerplate, oasis-uppercase-only
- use-rfc-2119-keywords-for-behavioral-requirements: unsupported (SHOULD; a finding against conventions.md, noted in research.md). Claims: use-rfc-2119-keywords-for-behavioral-requirements-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, tab-keywordless-must-equivalent
- must-is-absolute-requirement: supported. Claims: rfc2119-must-absolute-requirement, rfc2119-must-not-absolute-prohibition, iso-shall-requirement
- should-is-recommendation: supported. Claims: rfc2119-should-recommendation, rfc2119-should-not-recommendation, iso-should-preferred
- may-is-optional-behavior: supported. Claims: rfc2119-may-truly-optional, iso-may-permission
- rule-uses-rfc-2119-keywords: unsupported (SHOULD). Claims: rule-uses-rfc-2119-keywords-prior, keywords-not-required-for-normative-text, oasis-should-use-rfc2119, infra-core-subset
- follow-must-address-should-checks: supported. RFC 2119 does not require the "documented reason", so it is an open question. Claims: rfc2119-must-absolute-requirement, rfc2119-should-recommendation, qa-indicate-levels, qa-conformance-classes-by-level
- approve-on-zero-fail: supported. Claims: vale-only-errors-nonzero, eslint-error-for-ci, markdownlint-cli2-exit-codes, github-check-fails-on-error, bikeshed-die-on, bikeshed-die-on-default-fatal
- keywords-meaningful-only-in-uppercase: new, MUST (question 5). Claims: uppercase-only-meaning, lowercase-has-normal-english-meaning, oasis-uppercase-only, oasis-case-change-is-material, infra-willful-violation, infra-lowercase-equivalent, bikeshed-lowercase-for-readability
- lowercase-keyword-in-rule-text-flagged: new, SHOULD, reported as a warning (question 5). Claims: sperberg-mcqueen-lowercase-misuse, fantasai-lowercase-misuse-is-editorial-error, oasis-case-change-is-material, bikeshed-accidental-2119, caceres-respec-defaults-bcp14, lint-unmarked-keyword-usage, eslint-warn-for-uncertain
- state-the-keyword-interpretation: new, MUST. Claims: state-the-interpretation, bcp14-boilerplate, idnits-boilerplate-check, respec-conformance-boilerplate, respec-warns-missing-conformance
- state-how-keywordless-text-is-read: new, MUST. Claims: qa-consistent-style-explain, keywords-not-required-for-normative-text, infra-no-keywords-in-non-normative, tab-keywordless-must-equivalent
- no-keywords-in-non-normative-text: new, SHOULD NOT. Claims: qa-no-normative-language-in-informative, w3c-mos-no-keywords-informative, infra-lowercase-equivalent, etsi-requirements-only-normative, bikeshed-accidental-2119
- keyword-sets-finding-severity: new, SHOULD (question 6). MUST and MUST NOT give FAIL, SHOULD and SHOULD NOT give WARN, MAY gives no finding; this mapping is inferred, since no source states it. Claims: rfc2119-must-absolute-requirement, rfc2119-should-recommendation, rfc2119-may-truly-optional, qa-conformance-classes-by-level, sarif-error-level, sarif-warning-level, sarif-note-level, eslint-warn-for-uncertain, markdownlint-error-or-warning, respec-lint-severity, bikeshed-error-levels
- warn-findings-do-not-block: new, SHOULD (question 6). Claims: vale-only-errors-nonzero, vale-minalertlevel-ci, eslint-warn-no-exit-code, eslint-max-warnings, markdownlint-cli2-exit-codes, github-check-fails-on-error, github-ruleset-blocks-merge, bikeshed-die-on-default-fatal
- one-keyword-per-requirement: new, SHOULD. Claims: qa-subject-keyword-operation, w3c-wiki-active-form
- use-core-keyword-subset: new, SHOULD. Claims: infra-core-subset, plainlanguage-must-not-shall
- no-mixed-case-negation-or-may-not: new, SHOULD NOT. Claims: idnits-mixed-case-not, idnits-may-not, oasis-may-not-not-keyword, iso-no-may-not
- one-keyword-set-never-mixed: new, SHOULD. Claims: oasis-never-mix-keyword-sets, iso-no-must-for-shall, plainlanguage-must-not-shall, oasis-iso-keywords-by-definition, sperberg-mcqueen-iso-avoids-nonstandard-senses
- keywords-only-where-required: new, SHOULD. Claims: keywords-used-sparingly, sperberg-mcqueen-focus-attention, keywords-make-requirements-easy-to-spot, w3c-mos-uppercase-em, tab-drop-formatting-requirement, fantasai-styling-requirement

**Other things to know**
- **Open questions:** research.json records 7, one per owner decision. The main ones are uppercase-only (RFC 8174) versus WHATWG's lowercase convention, whether a warning can ever block approval, and whether GF-03 stays at WARN.
- **Limitations:**
  - The current ISO Directives returned 403, so Annex H is quoted from the 2004 edition in a mailing-list archive.
  - W3C pubrules and specberus were not fetched.
- **Cleanup:** I deleted my temporary scratchpad helpers (`h2t.py` and the `rk/` source cache).
- **Repo state:** nothing was committed. The repo also holds other sessions' uncommitted work I did not touch: staged cookbook-formatting files, and untracked guideline-formatting, activity-triggers, guideline-formatting and ingredient-formatting topic directories.
