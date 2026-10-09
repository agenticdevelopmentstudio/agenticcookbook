
- Never `rescue Exception`; a bare `rescue` catches `StandardError`, which is the right default. Name the class you handle.
- Do not use the `rescue` modifier (`foo rescue nil`); it hides which error occurred.
- Do not `return` from an `ensure` block; it discards the in-flight exception.
- Raise with `raise`, not `fail`. Define domain errors as subclasses of `StandardError`.

