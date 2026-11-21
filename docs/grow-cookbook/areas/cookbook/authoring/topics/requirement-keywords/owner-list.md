# Owner list: requirement-keywords

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
- **use-rfc-2119-keywords-for-behavioral-requirements** — verdict `unsupported` (claims: use-rfc-2119-keywords-for-behavioral-requirements-prior, keywords-not-required-for-normative-text, qa-consistent-style-explain, tab-keywordless-must-equivalent). Prior text, kept word for word: "Use RFC 2119 keywords for all behavioral requirements:" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "An artifact MUST follow this convention:" (the one change the reviewer accepts)
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
