
A verifier MUST check each of the following items. The recipe PASSES behavioral requirements quality only if every item is satisfied.

- [ ] Every normative statement uses an ALL-CAPS RFC 2119 keyword.
- [ ] No lowercase usage of "must", "should", "may" appears in a normative context.
- [ ] No weaker synonyms ("needs to", "ought to", "has to") substitute for RFC keywords.
- [ ] Each requirement tests a single, discrete behavior — no compound statements.
- [ ] Every MUST requirement can be converted directly into a test case with a clear PASS/FAIL criterion.
- [ ] No requirement references a platform-specific API or framework class unless the recipe is explicitly platform-scoped.
- [ ] All measurable thresholds (sizes, durations, counts, ratios) are expressed as specific numeric values.
- [ ] No requirement uses relative qualifiers ("adequate", "reasonable", "appropriate", "good") without a numeric anchor.
- [ ] SHOULD requirements document or link to a rationale for allowing deviation.
- [ ] No tautological or circular requirements exist.
- [ ] Requirements do not describe internal state or memory layout — only observable behavior.
- [ ] `must-use-keywords-with-defined-semantics`: Each keyword is used with its defined RFC 2119 meaning (MUST absolute, SHOULD with documented deviation, MAY free to include or omit).
- [ ] `must-cite-platform-standard-values`: Where a platform standard defines a value (touch target size, contrast ratio), the requirement cites that value explicitly.
- [ ] `must-use-platform-neutral-terms-for-shared-behavior`: A behavior that is the same across platforms is expressed in platform-neutral terms.
- [ ] `should-give-measurable-values-in-must-requirements`: MUST requirements carry measurable, verifiable values wherever a standard or design decision provides them.
- [ ] `should-document-conditions-for-may-requirements`: MAY requirements document the conditions under which each option is appropriate.
- [ ] `must-describe-required-outcome`: No requirement describes an attempt ("MUST try to") instead of the required outcome.
- [ ] `must-include-specific-values-for-measurable-constraints`: Specific numeric or string values where applicable rather than vague qualifiers.
