# Integrate: requirement-keywords

## Lossless

New topic: its text was never in the cookbook at the base commit (it came from tbd/compliance/, which owner-list.md carries word for word), so `cookr roles lossless` has no base text to check.

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped to 1.0.1; /add-artifact approved it (lint 24 pass, 0 fail).

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'gf-rfc-keywords' cites 'gf-rfc-keywords-prior', which the research rules unsupported
- rule 'gf-rfc-keywords-bold-or-uppercase' cites 'gf-rfc-keywords-bold-or-uppercase-prior', which the research rules contradicted
- rule 'use-rfc-2119-keywords-for-behavioral-requirements' cites 'use-rfc-2119-keywords-for-behavioral-requirements-prior', which the research rules unsupported
- rule 'rule-uses-rfc-2119-keywords' cites 'rule-uses-rfc-2119-keywords-prior', which the research rules unsupported

Open questions from the owner list:

- Case convention: follow RFC 8174 (only all-capital keywords carry meaning) or WHATWG Infra's willful violation (lowercase keywords carry the same meaning and are preferred for legibility); the sources support either if declared, and the owner chooses one.
- Whether skipping a SHOULD requires a documented reason (follow-must-address-should-checks) or only that the implications be understood and weighed (RFC 2119's wording); RFC 2119 does not require documentation.
- Whether warnings ever block /approve-artifact (an ESLint --max-warnings style threshold) or never do; the tools make a warning threshold optional and default to warnings not blocking.
- Whether rules restrict themselves to the five keywords MUST, MUST NOT, SHOULD, SHOULD NOT, MAY (as Infra encourages) or also admit SHALL, REQUIRED, RECOMMENDED and OPTIONAL as BCP 14 defines them.
- Whether a lowercase keyword found in rule text is reported as a WARN (as Bikeshed's opt-in accidental-2119 lint and ReSpec's warnings do) or a FAIL.
- Whether lint-artifact's GF-03 level 'WARN if missing' stays a warning; the sources support a keyword as SHOULD, which maps to a warning, but the owner decides.
- Whether keywords are additionally styled (bold, or the W3C Manual of Style's em with class rfc2119) for readability; no source makes styling carry the meaning, and a W3C editor recommends dropping the formatting requirement.

Notes:

- gf-rfc-keywords-bold-or-uppercase (kept word for word, research contradicted) lets a keyword count when bold or uppercase, while keywords-meaningful-only-in-uppercase gives meaning to UPPERCASE only. conventions.md now says to write keywords in UPPERCASE, which satisfies both, but whether a bold lowercase "must" is a requirement stays open.

## Owner rulings

- 2026-11-23, keyword case: only the UPPERCASE form of a keyword carries meaning (RFC 8174), and bold adds none. `gf-rfc-keywords-bold-or-uppercase` is renamed `gf-rfc-keywords-uppercase`, reads "Keywords MUST be written in UPPERCASE when used normatively; bold adds no meaning", and cites the research claims that support it instead of its contradicted prior text. This settles the case-convention question (RFC 8174, not Infra's willful violation) and the styling question (styling is not required and never carries meaning) on the owner list, and the note on a bold lowercase "must".

integrated: 2026-11-21
