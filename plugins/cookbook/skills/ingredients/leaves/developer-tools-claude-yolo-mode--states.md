<!-- leaf: ingredients/developer-tools-claude-yolo-mode--states · source: ingredients/developer-tools/claude/yolo-mode.md -->

# Yolo Mode (Permission Bypass Hook)

## States

| State | How to detect | Behavior |
|-------|---------------|----------|
| Enabled | `hooks.PermissionRequest` exists in `~/.claude/settings.json` with `yolo-approve-all.sh` | All permission prompts auto-approved |
| Disabled | `hooks.PermissionRequest` absent or does not reference `yolo-approve-all.sh` | Normal permission prompts shown |
