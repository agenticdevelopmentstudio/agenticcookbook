
- `should-avoid-runtime-constructed-identifiers`, `should-find-definition-by-grep`: An agent grepping for a name finds the definition only when the name is written out whole, not assembled from fragments.
- `should-minimize-hidden-runtime-behavior`: These force an agent (and a human) to simulate the runtime to predict behavior.
- `should-prefer-explicit-types-and-names`: Explicit types and verbose, intention-revealing names are a deliberate **semantic investment**: they encode meaning the agent would otherwise have to reconstruct from context it may not have loaded.
- `should-prefer-explicit-control-flow`: Surprising behavior costs both audiences — see `principle-of-least-astonishment`.
- `must-not-maximize-machine-legibility-at-all-costs`, `should-favor-locality-of-related-behavior`, `should-judge-dry-per-case`: This guidance is in genuine tension with some human-readability norms. Very short files and aggressive file-splitting can aid humans but scatter related behavior an agent must assemble from many sources.
- `should-judge-dry-per-case`: Heavy DRY and deep indirection trade duplication for hidden coupling. A small, explicit repetition is often easier for both readers than a clever abstraction three layers deep.
- `should-not-cite-agent-readership-as-statistic`: The claim "agents now read code more than humans do" is a **plausible direction of travel, not a measured fact**.
