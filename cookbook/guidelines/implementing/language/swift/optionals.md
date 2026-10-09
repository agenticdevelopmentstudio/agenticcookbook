
- Model absence with `Optional`, not with sentinel values such as `-1`, `""` or `NSNotFound`.
- Unwrap with `if let`, `guard let`, optional chaining or `??`. Use `guard` for early exit so the main path is not indented.
- Do not force-unwrap (`!`) or use `try!` or `as!` except where failure is a programmer error that should crash, and then prefer `preconditionFailure` with a message.
- Do not declare implicitly unwrapped optionals (`Type!`) in new Swift code. The legitimate case is a value injected before first use, such as an outlet; keep it `private` and document the injection point.

