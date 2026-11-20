
- `must-use-pathlib-not-os-path`: any `import os.path`, `os.path.join`, `os.path.exists` or other `os.path` call
- `must-route-all-path-manipulation-through-pathlib`: paths built or split with string concatenation, f-strings, `split("/")` or `os` functions instead of `Path` operators and methods
