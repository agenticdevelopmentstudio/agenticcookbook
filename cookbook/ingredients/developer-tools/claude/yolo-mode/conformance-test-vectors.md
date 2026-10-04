
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| yolo-001 | hook-auto-approves-all | Pipe any JSON to the hook script | stdout contains `"behavior":"allow"`, exit code 0 |
| yolo-002 | toggle-on-installs-hook | Run enable operation and confirm | Hook script exists, is executable; `~/.claude/settings.json` has `hooks.PermissionRequest` |
| yolo-003 | toggle-off-removes-hook | Run disable operation | `hooks.PermissionRequest` removed from `~/.claude/settings.json`; other hooks intact |
| yolo-004 | preserve-existing-hooks | Run enable then disable | `hooks.SessionStart`, `hooks.UserPromptSubmit`, etc. unchanged throughout |
| yolo-005 | status-check | Run status when enabled | Output indicates enabled |
| yolo-006 | status-check | Run status when disabled | Output indicates disabled |
| yolo-007 | idempotent-toggle | Run enable twice | Second invocation reports already enabled, no settings change |
| yolo-008 | warn-before-enable | Run enable | Security warning displayed before confirmation prompt |
| yolo-009 | hook-propagates-to-subagents | Enable, then spawn Agent tool subagent that runs Edit | Edit proceeds without permission prompt |

