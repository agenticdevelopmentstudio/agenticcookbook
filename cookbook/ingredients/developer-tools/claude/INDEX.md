# Claude Developer Tools Ingredients

Atomic specs for Claude Code automation and workflow patterns.

| File | Description |
|------|-------------|
| [yolo-mode.md](yolo-mode.md) | Toggleable PermissionRequest hook that auto-approves all Claude Code tool calls |
| [rule-audit.md](rule-audit.md) | Read-only audit of Claude Code rule files that inventories them, measures per-turn context cost, and detects duplication, ungated rules, and mandatory external reads |
| [rule-optimizer.md](rule-optimizer.md) | Proposes and, on explicit user confirmation, applies context-reduction strategies to Claude Code rule files |
| [rule-validation-report.md](rule-validation-report.md) | Verifies behavioral preservation and lint results for optimized rules, measures the reduction, and writes the before/after report file |
