
- Use `pathlib.Path`, not string concatenation or `os.path`. Join with `/`, read and write with `read_text` and `write_text`, and always pass `encoding="utf-8"`.
- Create directories with `mkdir(parents=True, exist_ok=True)` and search with `glob` and `rglob`.
- `Path.resolve()` is the only method that collapses `..` and symlinks. Resolve a path before you test whether it lies under a root.

