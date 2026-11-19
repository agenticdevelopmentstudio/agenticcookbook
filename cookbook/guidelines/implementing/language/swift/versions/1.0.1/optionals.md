
- Code MUST model absence with `Optional`, not with sentinel values such as `-1`, `""` or `NSNotFound`.
- Code SHOULD unwrap with `if let`, `guard let`, optional chaining or `??`. Code SHOULD use `guard` for early exit so the main path is not indented.
- Code MUST NOT force-unwrap (`!`) or use `try!` or `as!` except where failure is a programmer error that should crash, and then SHOULD prefer `preconditionFailure` with a message.
- New Swift code MUST NOT declare implicitly unwrapped optionals (`Type!`). The legitimate case is a value injected before first use, such as an outlet; it SHOULD stay `private` and the code SHOULD document the injection point.

