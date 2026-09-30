<!-- leaf: ingredients/developer-tools-claude-yolo-mode--edge-cases · source: ingredients/developer-tools/claude/yolo-mode.md -->

# Yolo Mode (Permission Bypass Hook)

## Edge Cases

- **settings.json does not exist**: The skill should create it with the hooks entry. This is unlikely in practice — Claude Code creates this file on first run.
- **hooks key does not exist**: The skill should create the `hooks` object and add `PermissionRequest` to it.
- **Malformed settings.json**: If the file is not valid JSON, the skill should warn the user and stop without modifying it.
- **Hook script deleted but settings entry remains**: The hook will fail silently (command not found). The status operation should check both the settings entry and script existence.
- **Multiple PermissionRequest entries**: If someone manually added other PermissionRequest hooks, the disable operation removes the entire `PermissionRequest` key. This is acceptable — custom PermissionRequest hooks are rare and the user can re-add them.
- **Session restart needed**: Hook changes may not take effect in the current session. The skill should note this in the enable confirmation.
