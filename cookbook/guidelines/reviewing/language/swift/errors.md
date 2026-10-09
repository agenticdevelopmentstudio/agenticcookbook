
- Failing functions are `throws` and every call is marked `try`. Related failures are an enum that conforms to `Error`.
- `try?` is used only where the reason for failure is irrelevant, and a swallowed error is not hiding a real problem.
- Cleanup that must always run is in `defer`.
- Typed throws appear only where the closed error set is part of the design.

