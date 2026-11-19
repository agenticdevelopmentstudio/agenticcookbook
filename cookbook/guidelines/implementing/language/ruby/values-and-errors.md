
- Records are `Data.define` unless mutation is required.
- No `rescue Exception`, no `rescue` modifier, no `return` inside `ensure`. Errors are raised with `raise` and rescued by name.

