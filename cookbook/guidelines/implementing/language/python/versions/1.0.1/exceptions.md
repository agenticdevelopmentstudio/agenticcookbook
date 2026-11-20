
- Catch the narrowest exception that you can handle. Never write a bare `except:`, and do not catch `Exception` except at a process boundary that logs and exits.
- Define your own errors as subclasses of `Exception`, named with the suffix `Error`.
- When you translate an exception, chain it: `raise ConfigError("...") from err`. Use `from None` only to hide an implementation detail on purpose.
- Keep the `try` body small. Put code that runs only on success in `else`, and cleanup in `finally`.
- Never `return`, `break` or `continue` out of a `finally` block; the 3.14 interpreter warns about it (PEP 765).
- Add context to an in-flight exception with `add_note()` instead of wrapping it where you have nothing to add.

