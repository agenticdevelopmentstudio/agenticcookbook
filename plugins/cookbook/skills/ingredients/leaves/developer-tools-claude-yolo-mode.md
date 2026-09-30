<!-- leaf: ingredients/developer-tools-claude-yolo-mode · source: ingredients/developer-tools/claude/yolo-mode.md -->

**Rules** (cite as `ingredients/developer-tools-claude-yolo-mode#<slug>`):

- `hook-auto-approves-all` MUST
- `hook-propagates-to-subagents` MUST
- `toggle-on-installs-hook` MUST
- `toggle-off-removes-hook` MUST
- `preserve-existing-hooks` MUST
- `warn-before-enable` MUST
- `status-check` MUST
- `idempotent-toggle` SHOULD
- `implementation-provide-operations` MUST — An implementation MUST provide these operations:

# Yolo Mode (Permission Bypass Hook)

## Overview

A toggleable `PermissionRequest` hook that auto-approves all Claude Code tool calls without user confirmation. This is a workaround for `--dangerously-skip-permissions` being broken in Claude Code v2.1.x, where the flag fails to propagate to subagents ([anthropics/claude-code#40241](https://github.com/anthropics/claude-code/issues/40241)) and silently stops working after exiting Plan Mode ([anthropics/claude-code#40136](https://github.com/anthropics/claude-code/issues/40136)).

Unlike the CLI flag, the hook approach works because hooks are inherited by subagents (they read the same `settings.json`) and persist across mode transitions.

## Security Warning

```
╔══════════════════════════════════════════════════╗
║                                                  ║
║           ☠  HERE BE DRAGONS  ☠                  ║
║                                                  ║
║  Yolo mode auto-approves ALL permission prompts  ║
║  with zero safety checks.                        ║
║                                                  ║
║  This means Claude can:                          ║
║    • Run any shell command                       ║
║    • Edit or delete any file                     ║
║    • Push to any remote                          ║
║    • Do anything — without asking                ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

This recipe provides the same security posture as `--dangerously-skip-permissions`: **none**. It is intended for trusted local development environments where the user is actively monitoring Claude's output. It offers no protection against prompt injection, destructive commands, or unintended side effects.

**Do not use this in:**
- Shared CI/CD environments
- Production systems
- Environments with access to sensitive credentials or infrastructure
- Sessions where untrusted content (PRs, issues, external files) will be processed

## Behavioral Requirements

- **hook-auto-approves-all**: The PermissionRequest hook MUST return `{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}` for every permission prompt, unconditionally.
- **hook-propagates-to-subagents**: The hook MUST be installed in `~/.claude/settings.json` (user scope) so that all sessions and subagents inherit it.
- **toggle-on-installs-hook**: Enabling yolo mode MUST create the hook script at `~/.claude/hooks/yolo-approve-all.sh`, make it executable, and add the `PermissionRequest` entry to `~/.claude/settings.json` under `hooks`.
- **toggle-off-removes-hook**: Disabling yolo mode MUST remove the `PermissionRequest` key from `hooks` in `~/.claude/settings.json`. It SHOULD leave the hook script on disk (harmless, avoids recreation).
- **preserve-existing-hooks**: Toggling on or off MUST NOT modify any other hook entries in `settings.json` (e.g., `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `Stop`, `SessionEnd`).
- **warn-before-enable**: Enabling MUST display a security warning and require explicit user confirmation before proceeding.
- **status-check**: The skill MUST be able to report whether yolo mode is currently active by inspecting the `PermissionRequest` key in `~/.claude/settings.json`.
- **idempotent-toggle**: Enabling when already enabled, or disabling when already disabled, SHOULD print a message and stop without modifying files.

## Components

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

## Configuration

This ingredient has no configurable options.

## Localization

| String Key | Default (en) | Context |
|-----------|-------------|---------|
| yolo.warning.title | HERE BE DRAGONS | Warning box header |
| yolo.enabled | Yolo mode enabled. All permission prompts will be auto-approved. | Enable confirmation |
| yolo.disabled | Yolo mode disabled. Permission prompts restored. | Disable confirmation |
| yolo.status.on | Yolo mode is ON. All permission prompts are auto-approved. | Status when enabled |
| yolo.status.off | Yolo mode is OFF. Normal permission prompts are active. | Status when disabled |
| yolo.already.enabled | Yolo mode is already enabled. | Idempotent enable |
| yolo.already.disabled | Yolo mode is already disabled. | Idempotent disable |

## Privacy

- **Data collected**: None
- **Storage**: Hook script stored at `~/.claude/hooks/yolo-approve-all.sh`; configuration in `~/.claude/settings.json`
- **Transmission**: No data leaves the device
- **Retention**: Persists until the disable operation is run

## Platform Notes

- **macOS/Linux**: Hook script uses `#!/bin/bash` shebang and `chmod +x`. Works on any POSIX system with bash.
- **Windows**: Hook script requires Git Bash, WSL, or another bash-compatible shell. The `$HOME` variable in the settings command path resolves correctly in these environments. Native PowerShell is not supported.

## Design Decisions

- **PermissionRequest hook over PreToolUse**: PermissionRequest fires specifically on permission dialogs. PreToolUse fires on every tool call and requires returning `permissionDecision` — more complex, but also works in headless mode. We chose PermissionRequest for simplicity since the primary use case is interactive sessions.
- **User-level scope only**: The hook is installed in `~/.claude/settings.json` (not project-level) because permission bypass is a personal environment choice, not a project setting that should be committed to a repo.
- **Leave hook script on disk after disable**: Deleting the script saves nothing meaningful and means it must be recreated on next enable. Leaving it avoids unnecessary file I/O.
- **Remove entire PermissionRequest key on disable**: Simpler than surgically removing a single entry. Custom PermissionRequest hooks are rare enough that this trade-off is acceptable.
