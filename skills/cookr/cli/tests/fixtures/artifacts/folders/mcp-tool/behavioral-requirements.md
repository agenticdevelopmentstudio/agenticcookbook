
### Identity and routing

- **unique-routable-name**: A tool MUST have a `name` that is unique within its server and stable across versions. Names SHOULD be 1–128 characters and SHOULD use only ASCII letters, digits, underscore, hyphen, and dot — no spaces or special characters. The model and host route on this name, so it MUST NOT collide with another tool on the same server.
- **precise-description**: A tool MUST carry a `description` written for the model, not for a human reader: it MUST state what the tool does, when to use it, and any preconditions, because the host selects tools by matching the user's intent against these descriptions. A tool MAY also carry an optional human-readable `title` for display.

### Schemas

- **input-schema-required**: A tool MUST declare an `inputSchema` that is a valid JSON Schema object (never `null`) describing its arguments. For a tool with no parameters it MUST use `{ "type": "object", "additionalProperties": false }`. Each parameter SHOULD have a `description`, and required parameters MUST be listed in the schema's `required` array. The schema defaults to JSON Schema draft 2020-12 when no `$schema` field is present.
- **output-schema-for-typed-results**: A tool that returns structured data SHOULD declare an `outputSchema` (a valid JSON Schema object) describing the shape of its result. When an `outputSchema` is declared, the server MUST return a `structuredContent` value conforming to it, and SHOULD also serialize that value into a text `content` block for backward compatibility with clients that do not consume structured content.
- **structured-content-conforms**: When a tool declares an `outputSchema`, its result's `structuredContent` MUST validate against that schema. Clients SHOULD validate it on receipt; a server that cannot produce conforming output MUST return a tool execution error rather than malformed structured content.

### Errors

- **tool-errors-via-iserror**: Failures the model can act on — API failures, input-validation failures, business-logic errors — MUST be reported inside the tool result with `isError: true` and a human-and-model-readable explanation in the `content` array, NOT as a protocol-level failure. This lets the model self-correct and retry with adjusted arguments.
- **protocol-errors-via-jsonrpc**: Failures with the request structure itself — unknown tool name, a malformed `tools/call` request, internal server faults — MUST be returned as standard JSON-RPC errors (e.g. code `-32602`), NOT as a result with `isError: true`. Protocol errors signal the model is unlikely to recover by retrying.

### Annotations

- **behavior-hint-annotations**: A tool SHOULD declare `annotations` that describe its behavior so hosts can apply appropriate trust and confirmation policy: `readOnlyHint` (true if the tool only reads and does not modify its environment; default `false`); `destructiveHint` (true if the tool may delete or overwrite rather than only add — meaningful only when `readOnlyHint` is `false`; default `true`); `idempotentHint` (true if repeating the call with the same arguments has no additional effect — meaningful only when `readOnlyHint` is `false`; default `false`); and `openWorldHint` (true if the tool interacts with an open world of external entities such as the public internet or third-party APIs).
- **annotations-are-untrusted-hints**: Annotations are informational signals, not enforceable guarantees. A server MUST set them accurately, and a client MUST treat annotations from untrusted servers as unverified — they MUST NOT be relied on as a security control, since a buggy or malicious server can misdeclare a destructive tool as read-only.

### Argument safety

- **arguments-untrusted-and-validated**: Tool arguments MUST be treated as untrusted input. The server MUST validate every call's arguments against the declared `inputSchema` before executing, and MUST reject or report (via `isError: true`) input that fails validation. Validation MUST NOT be skipped because the model "should" have produced conforming arguments.
- **authorize-per-call**: When the server is authenticated, every invocation MUST be authorized against the caller's per-request credentials and scopes — there is no implicit per-connection session. State handles passed as arguments MUST be re-authorized on each call; a handle is a name, not a capability.

