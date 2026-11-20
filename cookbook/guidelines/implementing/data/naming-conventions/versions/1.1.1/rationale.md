
- `must-use-snake-case-identifiers`: SQL is case-insensitive for identifiers, so `CamelCase` creates false visual distinctions (`UnderValue` and `Undervalue` are identical to the engine). Underscores are unambiguous, readable across tools, and work well for non-native English speakers.
- `must-name-primary-keys-table-id`: Self-documenting PKs make JOIN bugs immediately visible.
- `should-quote-english-word-identifiers`: SQLite adds new keywords over time.

