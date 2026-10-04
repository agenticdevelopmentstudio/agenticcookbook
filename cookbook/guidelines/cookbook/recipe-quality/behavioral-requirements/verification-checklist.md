
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

