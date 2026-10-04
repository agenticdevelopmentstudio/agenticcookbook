
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| term-001 | pty-backed-session | Create a new session | PTY is allocated, shell process is running |
| term-002 | default-shell-env, login-shell-launch | Create session with $SHELL=/bin/zsh | Shell launched as login shell "-zsh" |
| term-003 | default-shell-env | Create session with $SHELL unset | Falls back to /bin/zsh |
| term-004 | term-256color | Create session, inspect child environment | TERM=xterm-256color |
| term-005 | preserve-env-vars | Create session, inspect child environment | HOME, USER, LOGNAME, PATH, LANG, LC_ALL, LC_CTYPE present |
| term-006 | osc7-directory-update | Shell emits OSC 7 with file:///Users/me/projects | `currentWorkingDirectory` updates to /Users/me/projects; git branch detection starts |
| term-007 | osc2-title-update | Shell emits OSC 2 with "my-title" | `terminalTitle` updates to "my-title" |
| term-008 | osc7770-custom-commands | Send OSC 7770 color=#ff0000 | Session dot color set to red |
| term-009 | osc7770-custom-commands | Send OSC 7770 subtitle:task=Building | Custom subtitle "task" = "Building" appears |
| term-010 | osc7770-custom-commands | Send OSC 7770 clear-subtitle:task | Custom subtitle "task" removed |
| term-011 | osc7770-custom-commands | Send OSC 7770 clear-all-subtitles | All custom subtitles removed |
| term-012 | poll-foreground-process, update-foreground-name | Run `sleep 60` in terminal, wait 1.5s | `foregroundProcess` updates to "sleep" |
| term-013 | terminated-on-exit | Type `exit` in shell | Session state transitions to `.terminated` |
| term-014 | async-git-branch, stale-branch-discard | cd to a git repo, then quickly cd to another git repo | Only the second repo's branch is reported (stale result discarded) |
| term-015 | async-git-branch | cd to a non-git directory | `gitBranch` set to nil |
| term-016 | per-window-manager | Open two windows | Each window has its own session manager with independent session lists |
| term-017 | auto-increment-names | Create 3 sessions, delete Session 2, create another | Sessions named "Session 1", "Session 2", "Session 3"; after delete + create: "Session 1", "Session 3", "Session 4" |
| term-018 | add-session-select | Click + button | New session created, selected, terminal view shows shell prompt |
| term-019 | remove-smart-select | With sessions [A, B, C], B selected, remove B | A becomes selected (prefers previous) |
| term-020 | remove-smart-select | With sessions [A, B], A selected, remove A | B becomes selected (falls to next) |
| term-021 | remove-smart-select | With single session [A], remove A | No selection; empty state displayed |
| term-022 | terminate-all-cleanup | Close window with 3 active sessions | All 3 PTYs terminated |
| term-023 | reparent-on-switch | Switch from Session 1 to Session 2 and back | Session 1 scrollback and cursor position preserved |
| term-024 | apply-color-profile | Change color profile while session is active | Colors update immediately; no reparenting; scrollback preserved |
| term-025 | session-row-display | Session in ~/projects on branch main running vim | Row shows: name, "~/projects" with folder icon, "main" with branch icon, "vim" with terminal icon |
| term-026 | row-context-menu | Right-click session row | Context menu shows "Rename" and "Close" |
| term-027 | empty-state-no-sessions | Remove all sessions | Empty state displayed with icon, heading, description, and New Session button |
| term-028 | project-shell-settings | Set defaultShell to /bin/bash, create session | Session launches /bin/bash instead of $SHELL |
| term-029 | project-shell-settings | Enable autoOpenTerminal, open project | Terminal session created automatically on project open |
| term-030 | keyboard-nav-sessions | Focus session list, press Down arrow | Selection moves to next session |
| term-031 | optional-working-dir | Session manager with working directory /tmp, create session | New session shell starts in /tmp |

