---
id: 792f0b2d-c4b2-440f-9e58-33fa1e30a2c4
title: "Shell scripts"
domain: agenticdevelopercookbook://guidelines/reviewing/code-quality/shell-scripts
type: guideline
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Shell script `main()` functions must only call other functions — no inline logic. Keep scripts composable and testable."
platforms: []
languages:
  - python
tags:
  - language
  - python
  - shell-scripts
depends-on: []
related: []
references:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
  - https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html
  - https://zsh.sourceforge.io/Doc/Release/Options.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - new-module
  - configuration
---

# Shell scripts

Shell script `main()` functions MUST only call other functions — no inline logic. Scripts MUST be kept composable and testable.

## Portability
- The shebang names the shell the script is written for. A `#!/bin/sh` script uses no arrays, `[[ ]]`, process substitution or other extension.
- The script does not rely on zsh-versus-bash differences: unquoted splitting, array indexing or unmatched globs.
- No `set -m`, `fg` or `bg` in a script. Background jobs use `&` and `wait`.
- No logic depends on `set -e` inside a condition, a pipeline, a command substitution or a non-last AND-OR command, where it is ignored. Important commands are checked explicitly.
- Optional variables have a default so `set -u` does not abort. `pipefail` is used only where the shell supports it.
- Every expansion is quoted. There is no `eval` of a built string.
- Cleanup is in a `trap` on `EXIT`, plus `INT` and `TERM` when needed, and it does not trap `KILL` or `STOP`.
- Commands that can hang have a timeout, the exit codes 124 and 137 are handled, and the script checks that `timeout` exists.
## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
| 1.1.0 | 2026-10-09 | Mike Fullerton | Add a portability section: POSIX sh versus bash and zsh, job control, set -e/-u/pipefail caveats, quoting, trap and timeouts |
