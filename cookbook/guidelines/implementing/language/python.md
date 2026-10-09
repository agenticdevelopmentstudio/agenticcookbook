---
id: 929e96cb-2900-4386-ad4a-1a67a0568480
title: "Python"
domain: agenticdevelopercookbook://guidelines/implementing/language/python
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Package Python with pyproject.toml, type it, run subprocesses without a shell, use pathlib, raise and chain specific exceptions, and run untrusted-directory scripts in isolated mode."
platforms:
  - macos
  - linux
  - windows
languages:
  - python
tags:
  - language
  - python
  - packaging
  - pyproject
  - subprocess
  - pathlib
  - exceptions
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/code-quality/type-hints
  - agenticdevelopercookbook://guidelines/implementing/code-quality/shell-scripts
  - agenticdevelopercookbook://guidelines/implementing/language/ruby
  - agenticdevelopercookbook://guidelines/reviewing/language/python
  - agenticdevelopercookbook://principles/explicit-over-implicit
  - agenticdevelopercookbook://principles/fail-fast
references:
  - https://docs.python.org/3/library/subprocess.html
  - https://docs.python.org/3/using/cmdline.html
  - https://docs.python.org/3/library/pathlib.html
  - https://docs.python.org/3/tutorial/errors.html
  - https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
  - https://peps.python.org/pep-0723/
  - https://peps.python.org/pep-0561/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - new-module
  - refactor
  - error-handling
  - security-review
---

# Python

Python code in this cookbook's projects follows the rules below. Typing details, including the minimum Python version a script must run on, are in [Type hints](agenticdevelopercookbook://guidelines/implementing/code-quality/type-hints); this guideline does not repeat them.

## Packaging

- A project that is installed or imported by other code MUST declare itself in `pyproject.toml`. The file has a `[build-system]` table (`requires` and `build-backend`) and a `[project]` table with `name`, `version` (or `dynamic`), `description`, `readme`, `requires-python`, `license` (an SPDX expression), and `dependencies`.
- Put optional extras in `[project.optional-dependencies]` and command-line entry points in `[project.scripts]`. Do not write a `setup.py` for a new project.
- Declare `requires-python` to match the oldest interpreter you test.
- A single-file script that has dependencies SHOULD carry inline script metadata (PEP 723): a `# /// script` comment block with `requires-python` and `dependencies`, so a runner can build its environment.
- A typed library ships a `py.typed` marker file in the package (PEP 561) so type checkers use its annotations.

## Typing

- Annotate every function signature and every public attribute. Run a type checker in strict mode in CI (for mypy, `--strict`, which includes `--disallow-untyped-defs`).
- Do not silence a checker with a blanket `# type: ignore`; ignore one error code and say why.

## Subprocesses

- Run external programs with `subprocess.run`, passing the command as a list: `subprocess.run(["git", "status"], check=True)`.
- Never use `shell=True` with a string that contains any value you did not write yourself. A list of arguments never reaches a shell, so there is nothing to escape. If a shell is truly required, quote each interpolated value with `shlex.quote`.
- Pass `check=True` so a non-zero exit raises `CalledProcessError`, or inspect `returncode` on purpose.
- Pass `timeout=` for any command that could hang. On expiry the child is killed and `TimeoutExpired` is raised.
- Use `capture_output=True` with `text=True` to read output. Do not combine `capture_output` with explicit `stdout` or `stderr` arguments.
- The `env` argument replaces the inherited environment. Build it from `os.environ` plus your changes unless you want a clean one.

## Paths

- Use `pathlib.Path`, not string concatenation or `os.path`. Join with `/`, read and write with `read_text` and `write_text`, and always pass `encoding="utf-8"`.
- Create directories with `mkdir(parents=True, exist_ok=True)` and search with `glob` and `rglob`.
- `Path.resolve()` is the only method that collapses `..` and symlinks. Resolve a path before you test whether it lies under a root.

## Exceptions

- Catch the narrowest exception that you can handle. Never write a bare `except:`, and do not catch `Exception` except at a process boundary that logs and exits.
- Define your own errors as subclasses of `Exception`, named with the suffix `Error`.
- When you translate an exception, chain it: `raise ConfigError("...") from err`. Use `from None` only to hide an implementation detail on purpose.
- Keep the `try` body small. Put code that runs only on success in `else`, and cleanup in `finally`.
- Never `return`, `break` or `continue` out of a `finally` block; the 3.14 interpreter warns about it (PEP 765).
- Add context to an in-flight exception with `add_note()` instead of wrapping it where you have nothing to add.

## Untrusted directories

- A script run from a directory you do not control can import a file planted next to it. Start it with `python -I` (isolated mode), which ignores the script directory, the user site-packages directory and every `PYTHON*` environment variable.
- Isolated mode implies `-E -P -s`. Be aware that `-m` puts the current directory on `sys.path`, so do not use `-m` from an untrusted working directory.
- Never run an interpreter inside a directory of downloaded files. Run it from your own directory and pass the downloaded path as an argument.

## Why this matters

Most Python incidents come from a few habits: a shell string built from input, a path compared as text, an exception swallowed too broadly, and an interpreter that imports from the directory it was started in. Writing the safe form each time costs a few characters and removes whole classes of failure.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
