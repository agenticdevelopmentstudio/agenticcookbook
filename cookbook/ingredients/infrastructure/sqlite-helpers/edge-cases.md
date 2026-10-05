
- **Missing data**: A query that is expected to return a row but returns none throws `.missingData` rather than a default value.
- **Invalid date string**: A date column that does not parse as ISO 8601 throws `.invalidDate` rather than substituting a fallback date.
- **Null binding**: A `.null` binding writes SQL NULL, not the string "null".
- **Handle not closed on error**: A thrown error MUST NOT leak an open database handle; the helper closes it on every exit path.

