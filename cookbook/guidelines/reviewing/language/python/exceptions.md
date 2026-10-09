
- No bare `except:`. Broad `except Exception` appears only at a process boundary and logs.
- Translated errors use `raise ... from ...`.
- `try` bodies are short. No `return`, `break` or `continue` in `finally`.
- New error classes derive from `Exception` and end in `Error`.

