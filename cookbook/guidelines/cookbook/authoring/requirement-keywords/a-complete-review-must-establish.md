
- Every requirement uses an RFC 2119 keyword in uppercase, in the form subject, keyword, operation
- MUST and MUST NOT are treated as absolute, SHOULD and SHOULD NOT as recommendations weighed before deviating, and MAY as truly optional
- The keyword interpretation is stated near the beginning of the document
- No keyword appears in examples, notes or other informative text
- One keyword set is used throughout; no 'MUST not' and no 'MAY NOT'
- Lint findings take their severity from the keyword, and approval needs zero FAIL findings
- Every MUST rule is kept, with no exception: `gf-rfc-keywords`, `gf-rfc-keywords-bold-or-uppercase`, `use-rfc-2119-keywords-for-behavioral-requirements`, `rule-uses-rfc-2119-keywords`, `must-is-absolute-requirement`, `should-is-recommendation`, `may-is-optional-behavior`, `follow-must-address-should-checks`, `approve-on-zero-fail`, `keywords-meaningful-only-in-uppercase`
- Every SHOULD rule is kept, or the change says why not: `lowercase-keyword-in-rule-text-flagged`, `state-the-keyword-interpretation`, `state-how-keywordless-text-is-read`, `no-keywords-in-non-normative-text`, `keyword-sets-finding-severity`, `warn-findings-do-not-block`, `one-keyword-per-requirement`, `use-core-keyword-subset`, `no-mixed-case-negation-or-may-not`, `one-keyword-set-never-mixed`, `keywords-only-where-required`

A review passes when it establishes every item above.

