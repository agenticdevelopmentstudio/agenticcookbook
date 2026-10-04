
A verifier MUST check each of the following items. The recipe PASSES source fidelity only if every item is satisfied.

- [ ] Every normative requirement can be traced to observable source code behavior or a cited test case.
- [ ] No requirement describes behavior that does not exist in the source code.
- [ ] All known workarounds, hacks, or non-obvious behavioral patterns in the source are documented in Design Decisions or as inline notes.
- [ ] Sections covering concerns not implemented in the source are marked `NEEDS REVIEW: Not implemented in source` rather than containing invented requirements.
- [ ] `NEEDS REVIEW` markers are used only for genuine gaps — not as a substitute for analysis.
- [ ] Error handling requirements accurately reflect what the code does on failure, not what it should do.
- [ ] No aspirational or "best practice" behavior is presented as a normative MUST requirement without being traceable to the source.
- [ ] Technical debt affecting behavioral correctness is documented in Design Decisions.
- [ ] Any "Recommended Improvements" content is clearly separated from normative requirements and is not written using RFC keywords.

