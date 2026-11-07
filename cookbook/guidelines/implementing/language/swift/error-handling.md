
- A function that can fail MUST be marked `throws`, and each call site MUST be marked `try`. Errors are values of a type that conforms to `Error`; related failures SHOULD be modeled as an `enum`.
- Handle an error with `do`/`catch`, code SHOULD convert it to an optional with `try?` only when the reason does not matter, and let it propagate when the caller is better placed to decide.
- A `do`/`catch` MUST be exhaustive or sit in a throwing function. A `catch` that matches every case of an enum by switch gets a compile error if a case is added later; code SHOULD prefer that to a catch-all that hides new cases.
- Code SHOULD use `defer` for cleanup that must run on every exit, such as closing a file. Deferred blocks run in reverse order of appearance and cannot exit their scope.
- Most functions SHOULD throw plain `Error`. Code SHOULD use typed throws (`throws(MyError)`) only where the error type is a stable, closed set: embedded code that avoids boxing, an error that is an internal detail of a library, or code that forwards the errors of a generic closure parameter.

