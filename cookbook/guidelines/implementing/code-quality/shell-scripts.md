---
id: e9e60a7e-4e15-40e7-b730-fc2e311df1af
title: "Shell scripts"
domain: agenticdevelopercookbook://guidelines/implementing/code-quality/shell-scripts
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
- Declare the shell in the shebang and write to that shell's rules. `#!/bin/sh` means POSIX `sh`: no arrays, no `[[ ]]`, no `local` assumptions, no process substitution. Use `#!/usr/bin/env bash` (or zsh) only when you need those features, and then do not call the script with `sh`.
- Zsh is not a superset of bash by default. Word splitting of an unquoted variable is off unless `SH_WORD_SPLIT` is set (it is on only in `sh` and `ksh` emulation), arrays are one-based unless `KSH_ARRAYS` is set, and a glob with no match is an error (`NOMATCH`) rather than the literal text. Quote every expansion and use `setopt`-independent forms so the script behaves the same under either.
- `set -m` turns on job control, which POSIX makes the default only for interactive shells. A script does not need it and must not depend on it. Start background work with `&` and collect it with `wait`; never rely on `fg` or `bg` in a script.
- `set -e` is not a general error handler. It is ignored for pipeline elements other than the overall result, inside command substitutions' subshells, in the condition of `if`, `while`, `until` and `elif`, after `!`, and for every command of an AND-OR list except the last. Check the commands that matter explicitly with `|| exit` or an `if`.
- `set -u` fails the expansion of an unset parameter (the special parameters `@` and `*` excepted). Give optional values a default with `${name:-default}`.
- `set -o pipefail` exists in the current POSIX edition. The pipeline's status becomes that of the rightmost command that failed, using the setting in effect when the pipeline began. Older `sh` implementations may lack it, so test for it or avoid it in `#!/bin/sh` scripts.
- Quote every expansion: `"$var"`, `"$@"`. Single quotes keep text literal; double quotes keep everything except `$`, backquote and backslash. The characters that need quoting to be literal are `& ; < > ( ) $` backquote, backslash, quotes, space, tab and newline. Never build a command in a string and run it with `eval`.
- Use `trap` for cleanup. `trap 'cleanup' EXIT` runs when the shell exits; trap `INT` and `TERM` too if the script must clean up on a signal. A non-interactive shell cannot trap or reset a signal that was ignored on entry, `KILL` and `STOP` cannot be trapped, a subshell resets its traps to the default, and a trap action waits until the foreground command finishes.
- Put a time limit on any command that can hang with `timeout [options] duration command [arg]...` (GNU coreutils). It exits 124 when the command timed out, 125 when `timeout` itself failed, 126 when the command could not be run, 127 when it was not found, and 137 when the command was killed. Use `-k` to send a follow-up kill, and note that `timeout` is not part of POSIX and may be absent on macOS; check for it, or do the work in Python.
## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
| 1.1.0 | 2026-10-09 | Mike Fullerton | Add a portability section: POSIX sh versus bash and zsh, job control, set -e/-u/pipefail caveats, quoting, trap and timeouts |
