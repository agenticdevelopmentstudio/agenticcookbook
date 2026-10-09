---
id: d7079751-71c5-49a6-9c1d-505921e4cee9
title: "Python"
domain: agenticdevelopercookbook://guidelines/reviewing/language/python
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review Python for pyproject packaging, strict typing, shell-free subprocess calls, pathlib use, specific chained exceptions and isolated mode on untrusted directories."
platforms:
  - macos
  - linux
  - windows
languages:
  - python
tags:
  - language
  - python
  - review
  - subprocess
  - exceptions
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/language/python
  - agenticdevelopercookbook://guidelines/reviewing/code-quality/type-hints
  - agenticdevelopercookbook://guidelines/reviewing/code-quality/shell-scripts
references:
  - https://docs.python.org/3/library/subprocess.html
  - https://docs.python.org/3/using/cmdline.html
  - https://docs.python.org/3/library/pathlib.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
  - security-review
---

# Python

Review changed Python against [Python](agenticdevelopercookbook://guidelines/implementing/language/python).

## Packaging

- Installable code is described in `pyproject.toml` with a build system, `requires-python` and declared dependencies. No new `setup.py`.
- A script with third-party imports carries inline script metadata or a documented environment.
- A typed library includes `py.typed`.

## Typing

- Every new signature is annotated and the strict type check passes.
- Each `# type: ignore` names one error code and has a reason.

## Subprocesses

- No `shell=True` with a string that includes a variable. Arguments are a list.
- `check=True` is set, or the return code is handled in the next lines.
- Any call that can hang has a `timeout`.
- Output capture does not combine `capture_output` with explicit `stdout` or `stderr`.
- A custom `env` starts from `os.environ` unless a clean environment is the point.

## Paths

- Paths are `pathlib.Path` objects. Every `read_text` and `write_text` passes an encoding.
- A containment check resolves the path first.

## Exceptions

- No bare `except:`. Broad `except Exception` appears only at a process boundary and logs.
- Translated errors use `raise ... from ...`.
- `try` bodies are short. No `return`, `break` or `continue` in `finally`.
- New error classes derive from `Exception` and end in `Error`.

## Untrusted directories

- A script that runs in a directory the user does not control is invoked with `-I`, and does not use `-m` there.

## Why this matters

Each item is a place where an unsafe form and the safe form compile identically. Only a reviewer who looks for them will see the difference.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
