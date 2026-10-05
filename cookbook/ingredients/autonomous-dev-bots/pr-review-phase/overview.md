
The PR review phase is Phase 1 of the cookbook PR review pipeline, run by the Cookbook Review Bot (`@cookbook-review-bot[bot]`). It checks a contributed artifact for structural validity, prose quality, content completeness, and convention compliance, fixes what it can in a bounded loop, and rejects what it cannot. It reads the PR content and posts a GitHub PR review (Approve or Request Changes).

### Custom Vale Style: Cookbook

A custom Vale style (`vale/styles/Cookbook/`) with rules optimized for LLM readability:

| Rule | What it flags |
|------|---------------|
| `VagueTerms.yml` | "appropriate", "suitable", "reasonable", "as needed", "standard", "proper", "adequate" |
| `AmbiguousQuantifiers.yml` | "some", "most", "usually", "often", "sometimes", "generally", "typically", "normally" |
| `Hedging.yml` | "might want to", "consider using", "it may be helpful", "you could", "perhaps", "arguably" |
| `ImplicitReferences.yml` | "as mentioned above", "the usual approach", "handle this correctly", "see above", "as before" |
| `CasualRFC2119.yml` | Lowercase "must", "should", "shall" in requirement sections that are not bolded RFC 2119 keywords |
| `DoubleNegatives.yml` | "must not fail to", "should not avoid", "do not prevent" |
| `AmbiguousPronouns.yml` | "it should", "this must", "that will" at sentence start without clear antecedent in requirement sections |

### LLM Clarity Pass

Beyond Vale's deterministic rules, the LLM clarity pass checks for:

- **Ambiguous antecedents**: pronouns whose referent requires re-reading prior context
- **Implicit assumptions**: statements that assume knowledge not present in the document
- **Terminology drift**: a concept called X in one section and Y in another
- **Section isolation**: can each section be understood without reading the others?
- **Unresolved references**: mentions of concepts not defined or linked
- **Vague quantification in requirements**: "handle multiple items" (how many?) vs "handle 1-1000 items"

