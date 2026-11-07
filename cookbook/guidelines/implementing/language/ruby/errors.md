
- Code MUST NOT `rescue Exception`; a bare `rescue` catches `StandardError`, which is the right default. Code SHOULD name the class it handles.
- Code MUST NOT use the `rescue` modifier (`foo rescue nil`); it hides which error occurred.
- Code MUST NOT `return` from an `ensure` block; it discards the in-flight exception.
- Code SHOULD raise with `raise`, not `fail`, and SHOULD define domain errors as subclasses of `StandardError`.

