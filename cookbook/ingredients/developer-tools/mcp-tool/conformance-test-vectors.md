
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| mcp-tool-001 | unique-routable-name, precise-description | Send `tools/list` | Tool appears once with a unique name and a non-empty, intent-describing `description` |
| mcp-tool-002 | input-schema-required | Inspect the tool's `inputSchema` | A valid JSON Schema object (not `null`); a no-parameter tool uses `{ "type": "object", "additionalProperties": false }` |
| mcp-tool-003 | input-schema-required | Call the tool with an argument that violates the schema | Server rejects it (protocol error) or returns a result with `isError: true`; the handler does not run on invalid input |
| mcp-tool-004 | output-schema-for-typed-results, structured-content-conforms | Call a tool that declares an `outputSchema` with valid arguments | Result includes a `structuredContent` value that validates against `outputSchema`, plus a serialized text `content` block |
| mcp-tool-005 | tool-errors-via-iserror | Call the tool with a future-date-required field set to a past date | Result has `isError: true` and a `content` block explaining the failure; no JSON-RPC error |
| mcp-tool-006 | protocol-errors-via-jsonrpc | Send `tools/call` for a name that does not exist | JSON-RPC error (e.g. code `-32602`, "Unknown tool"); not a result with `isError: true` |
| mcp-tool-007 | behavior-hint-annotations | Inspect the tool's `annotations` | `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` present and consistent with the tool's actual effect |
| mcp-tool-008 | annotations-are-untrusted-hints | Client receives a tool from an untrusted server marked `readOnlyHint: true` | Client does not rely on the hint to skip confirmation for a non-read operation |
| mcp-tool-009 | arguments-untrusted-and-validated | Call the tool with extra, malformed, or injection-style argument values | Arguments are schema-validated before execution; non-conforming input is rejected or reported via `isError: true` |
| mcp-tool-010 | authorize-per-call | Call an authenticated tool with credentials lacking the required scope | Call is denied per request; authorization is not inferred from a prior call on the same connection |

