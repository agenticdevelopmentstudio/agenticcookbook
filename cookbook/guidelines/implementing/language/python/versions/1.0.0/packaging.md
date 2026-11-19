
- A project that is installed or imported by other code MUST declare itself in `pyproject.toml`. The file has a `[build-system]` table (`requires` and `build-backend`) and a `[project]` table with `name`, `version` (or `dynamic`), `description`, `readme`, `requires-python`, `license` (an SPDX expression), and `dependencies`.
- Put optional extras in `[project.optional-dependencies]` and command-line entry points in `[project.scripts]`. Do not write a `setup.py` for a new project.
- Declare `requires-python` to match the oldest interpreter you test.
- A single-file script that has dependencies SHOULD carry inline script metadata (PEP 723): a `# /// script` comment block with `requires-python` and `dependencies`, so a runner can build its environment.
- A typed library ships a `py.typed` marker file in the package (PEP 561) so type checkers use its annotations.

