
- Gates **MUST** fail only on correctness or stated requirements (broken build, failing test, violated contract). They **MUST NOT** block on style nitpicks an autoformatter or optional linter can handle non-blockingly.
- An adversarial reviewer or "find the gaps" check **SHOULD** be told to flag only gaps affecting correctness or the stated spec; chasing every speculative finding drives over-engineering.

