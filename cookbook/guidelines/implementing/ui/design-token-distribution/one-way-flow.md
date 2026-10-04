
- The token source (e.g. a [W3C Design Tokens](https://www.designtokens.org/tr/drafts/format/) JSON file or `tokens.json`) **MUST** be the single authority for token values.
- A transform tool **SHOULD** generate platform outputs — [Style Dictionary](https://styledictionary.com/) is the established choice (use a current released version; verify the latest at build time rather than pinning from memory).
- Generated outputs **MUST NOT** be hand-edited. Edits belong in the source; the build regenerates downstream.
- Regenerate on **every** token change, and run generation in CI so drift fails fast (per fail-fast).
- Version the token source. Treat token releases like any other versioned dependency so consumers can pin and upgrade deliberately.

