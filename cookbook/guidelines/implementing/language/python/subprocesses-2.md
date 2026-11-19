
- No `shell=True` with a string that includes a variable. Arguments are a list.
- `check=True` is set, or the return code is handled in the next lines.
- Any call that can hang has a `timeout`.
- Output capture does not combine `capture_output` with explicit `stdout` or `stderr`.
- A custom `env` starts from `os.environ` unless a clean environment is the point.

