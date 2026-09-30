<!-- leaf: ingredients/developer-tools-mcp-tool--logging · source: ingredients/developer-tools/mcp-tool.md -->

# MCP tool

**Rules** (cite as `ingredients/developer-tools-mcp-tool--logging#<slug>`):

- `tool-log-invocation-audit-purposes` SHOULD — A tool SHOULD log each invocation for audit purposes without recording sensitive argument or result values. Redact …

## Logging

Subsystem: `{{server_id}}` | Category: `mcp.tool`

A tool SHOULD log each invocation for audit purposes without recording sensitive argument or result values. Redact secrets and PII before logging.

| Event | Level | Message |
|-------|-------|---------|
| Tool registered | debug | `mcp.tool: registered "{{tool_name}}" (readOnly={{read_only}})` |
| Invocation received | info | `mcp.tool: "{{tool_name}}" invoked by {{caller}}` |
| Argument validation failed | error | `mcp.tool: "{{tool_name}}" rejected — input failed inputSchema validation` |
| Invocation succeeded | info | `mcp.tool: "{{tool_name}}" returned in {{duration}}ms` |
| Tool execution error | error | `mcp.tool: "{{tool_name}}" returned isError — {{reason}}` |
