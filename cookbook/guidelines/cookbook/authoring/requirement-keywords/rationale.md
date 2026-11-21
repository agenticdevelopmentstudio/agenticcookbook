
- `must-is-absolute-requirement`, `should-is-recommendation`, `may-is-optional-behavior`: RFC 2119 defines the three levels, and ISO/IEC Directives Part 2 draws the same lines with 'shall', 'should' and 'may'.
- `keywords-meaningful-only-in-uppercase`, `lowercase-keyword-in-rule-text-flagged`: RFC 8174 gives the defined meaning to the uppercase forms only; in lowercase the words are ordinary English, so a stray lowercase keyword is either an editorial error or a hidden requirement.
- `state-the-keyword-interpretation`, `state-how-keywordless-text-is-read`: RFC 7322 asks a document to cite RFC 2119 or give its own interpretation, and the W3C QA Framework asks a specification to say which requirement styles it uses.
- `no-keywords-in-non-normative-text`: the W3C QA Framework, the W3C Manual of Style, WHATWG Infra and ETSI keep requirement language out of informative text.
- `keyword-sets-finding-severity`, `warn-findings-do-not-block`, `approve-on-zero-fail`: Vale, ESLint, markdownlint, SARIF, Bikeshed and GitHub code scanning all separate errors from warnings, and by default only errors fail a run.
- `one-keyword-per-requirement`, `use-core-keyword-subset`, `no-mixed-case-negation-or-may-not`, `one-keyword-set-never-mixed`: the W3C QA Framework, WHATWG Infra, IETF idnits, OASIS and ISO/IEC each narrow the forms a requirement can take so that it reads one way.
- `keywords-only-where-required`: RFC 2119 asks for the keywords to be used sparingly, so that the ones that appear stand out.

