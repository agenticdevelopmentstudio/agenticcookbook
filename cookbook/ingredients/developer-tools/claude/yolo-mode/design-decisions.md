
- **PermissionRequest hook over PreToolUse**: PermissionRequest fires specifically on permission dialogs. PreToolUse fires on every tool call and requires returning `permissionDecision` — more complex, but also works in headless mode. We chose PermissionRequest for simplicity since the primary use case is interactive sessions.
- **User-level scope only**: The hook is installed in `~/.claude/settings.json` (not project-level) because permission bypass is a personal environment choice, not a project setting that should be committed to a repo.
- **Leave hook script on disk after disable**: Deleting the script saves nothing meaningful and means it must be recreated on next enable. Leaving it avoids unnecessary file I/O.
- **Remove entire PermissionRequest key on disable**: Simpler than surgically removing a single entry. Custom PermissionRequest hooks are rare enough that this trade-off is acceptable.

