
AI-generated code is a known source of this fragility: agents readily encode incidental behavior (parsing a specific error string, asserting on response-field order, sleeping a fixed time) as if it were guaranteed.

- Code **SHOULD NOT** depend on any behavior the provider has not explicitly promised.
- Reviewers **SHOULD** flag: assertions on exact error message text, reliance on response/iteration ordering, hard-coded timing/sleep assumptions, and parsing of free-form provider strings.
- Tests **SHOULD** assert on documented contract (status code, typed error category, declared fields) rather than incidental output.
- When a dependency on unspecified behavior is genuinely unavoidable, the code **SHOULD** isolate it behind an adapter and document the assumption so the coupling is greppable and reversible.

