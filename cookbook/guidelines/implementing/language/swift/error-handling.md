
- Mark a function that can fail `throws`, and mark each call site `try`. Errors are values of a type that conforms to `Error`; model related failures as an `enum`.
- Handle an error with `do`/`catch`, convert it to an optional with `try?` only when the reason does not matter, and let it propagate when the caller is better placed to decide.
- A `do`/`catch` must be exhaustive or sit in a throwing function. A `catch` that matches every case of an enum by switch gets a compile error if a case is added later; prefer that to a catch-all that hides new cases.
- Use `defer` for cleanup that must run on every exit, such as closing a file. Deferred blocks run in reverse order of appearance and cannot exit their scope.
- Most functions should throw plain `Error`. Use typed throws (`throws(MyError)`) only where the error type is a stable, closed set: embedded code that avoids boxing, an error that is an internal detail of a library, or code that forwards the errors of a generic closure parameter.

