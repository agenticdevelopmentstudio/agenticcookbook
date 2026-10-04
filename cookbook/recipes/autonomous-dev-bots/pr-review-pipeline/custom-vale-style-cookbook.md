
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

