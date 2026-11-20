
The host's model selects tools from their `name` and `description` alone, so these are load-bearing.

- Each tool **MUST** have a precise, action-oriented `name` and a `description` that states what it does, when to use it, and what it returns.
- Tool names **SHOULD** be 1–128 chars, case-sensitive, and limited to `[A-Za-z0-9_.-]` (no spaces). Keep them unique within the server.
- Use the optional `title` for a human-readable display label; keep `name` stable as the machine identifier.
- Define a strict `inputSchema` (JSON Schema, defaults to 2020-12). For zero-parameter tools, use `{ "type": "object", "additionalProperties": false }`.
- Keep the tool surface small. Many overlapping tools degrade routing accuracy; consolidate or parameterize instead.

