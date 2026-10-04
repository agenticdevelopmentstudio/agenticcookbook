
- **hook-auto-approves-all**: The PermissionRequest hook MUST return `{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}` for every permission prompt, unconditionally.
- **hook-propagates-to-subagents**: The hook MUST be installed in `~/.claude/settings.json` (user scope) so that all sessions and subagents inherit it.
- **toggle-on-installs-hook**: Enabling yolo mode MUST create the hook script at `~/.claude/hooks/yolo-approve-all.sh`, make it executable, and add the `PermissionRequest` entry to `~/.claude/settings.json` under `hooks`.
- **toggle-off-removes-hook**: Disabling yolo mode MUST remove the `PermissionRequest` key from `hooks` in `~/.claude/settings.json`. It SHOULD leave the hook script on disk (harmless, avoids recreation).
- **preserve-existing-hooks**: Toggling on or off MUST NOT modify any other hook entries in `settings.json` (e.g., `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `Stop`, `SessionEnd`).
- **warn-before-enable**: Enabling MUST display a security warning and require explicit user confirmation before proceeding.
- **status-check**: The skill MUST be able to report whether yolo mode is currently active by inspecting the `PermissionRequest` key in `~/.claude/settings.json`.
- **idempotent-toggle**: Enabling when already enabled, or disabling when already disabled, SHOULD print a message and stop without modifying files.

