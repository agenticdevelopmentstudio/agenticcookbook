
- Names **MUST** be searchable as literal strings. Prefer one canonical spelling of a concept over synonyms scattered across the codebase.
- Avoid constructing identifiers at runtime (string-concatenated method names, dynamically generated attributes). An agent grepping for `handle_payment` **SHOULD** find the definition, not a fragment assembled from `"handle_" + verb`.
- Keep call sites discoverable: a function **SHOULD** be reachable by searching for its name, not only through a registry, decorator, or dependency-injection wiring that hides the connection.

