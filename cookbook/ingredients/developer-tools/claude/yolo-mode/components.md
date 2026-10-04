
### Hook Script

**Path:** `~/.claude/hooks/yolo-approve-all.sh`

```bash
#!/bin/bash
echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}'
exit 0
```

The script:
- Receives permission request JSON on stdin (ignored — approves unconditionally)
- Returns the PermissionRequest hook-specific output with `"behavior": "allow"`
- Exits with code 0 (success — action proceeds)

### Settings.json Hook Entry

**Location:** `~/.claude/settings.json` → `hooks.PermissionRequest`

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/yolo-approve-all.sh"
          }
        ]
      }
    ]
  }
}
```

- **matcher**: Empty string matches all tool types
- **type**: `command` — executes a shell script
- **command**: Uses `$HOME` for portability across environments

### Scope

| Scope | Affected? | Why |
|-------|-----------|-----|
| Current session | Yes | Hook fires on every permission prompt in the active session |
| Subagents (Agent tool) | Yes | Subagents read the same `~/.claude/settings.json` |
| Plan mode transitions | Yes | Hooks persist across mode changes (unlike the CLI flag) |
| New sessions | Yes | Hook is in user-level settings, applies to all future sessions |
| Headless mode (`-p`) | No | `PermissionRequest` does not fire in non-interactive mode — use `PreToolUse` with `permissionDecision` instead |
| Other users | No | User-level `~/.claude/settings.json` is per-user |
| Project-level overrides | No | Only installed at user scope; project `.claude/settings.json` is not modified |

### Commands

An implementation MUST provide these operations:

| Operation | Effect |
|-----------|--------|
| Enable | Show warning, confirm, install hook script and settings entry |
| Disable | Remove `PermissionRequest` from settings, print confirmation |
| Status | Check settings and report whether yolo mode is active |

