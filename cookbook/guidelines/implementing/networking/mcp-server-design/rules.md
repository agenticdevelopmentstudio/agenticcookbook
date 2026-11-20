
**Spec revision**
- **should-pin-a-dated-spec-revision**: A server SHOULD pin to a dated spec revision.
- **should-default-to-the-stable-revision**: A server SHOULD default to the stable **2025-11-25** revision unless the host requires an older one.
- **should-negotiate-the-revision**: A server SHOULD negotiate the revision during initialization rather than hard-coding it.
- **should-gate-draft-revisions**: A server SHOULD treat any release-candidate or draft revision as a forecast and gate it behind explicit opt-in.

**Choose the right primitive**
- **should-pick-primitives-by-purpose**: A server SHOULD pick each primitive by purpose, not convenience.
- **should-prefer-resources-for-read-only-context**: You **SHOULD** prefer a **resource** for anything read-only that the user or host selects as context.
- **should-prefer-prompts-for-invoked-workflows**: You **SHOULD** prefer a **prompt** for workflows a human explicitly invokes.
- **should-use-tools-only-for-model-chosen-operations**: You **SHOULD** model **tools** for operations the model chooses autonomously — and only those.
- **should-not-expose-read-only-context-as-tools**: A server SHOULD NOT expose read-only context as a tool merely because tools are easier to wire up; that puts routing load on the model and invites accidental invocation.

**Tool design**
- **must-name-and-describe-tools-precisely**: Each tool **MUST** have a precise, action-oriented `name` and a `description` that states what it does, when to use it, and what it returns.
- **should-constrain-tool-names**: Tool names **SHOULD** be 1–128 chars, case-sensitive, and limited to `[A-Za-z0-9_.-]` (no spaces).
- **should-keep-tool-names-unique**: A server SHOULD keep tool names unique within the server.
- **should-use-title-for-display**: A tool SHOULD use the optional `title` for a human-readable display label and keep `name` stable as the machine identifier.
- **should-define-a-strict-input-schema**: A tool SHOULD define a strict `inputSchema` (JSON Schema, defaults to 2020-12).
- **should-close-zero-parameter-schemas**: For zero-parameter tools, the `inputSchema` SHOULD be `{ "type": "object", "additionalProperties": false }`.
- **should-keep-the-tool-surface-small**: A server SHOULD keep the tool surface small: many overlapping tools degrade routing accuracy, so consolidate or parameterize instead.

**Structured output**
- **should-declare-an-output-schema**: A tool **SHOULD** declare an `outputSchema` and return matching `structuredContent`.
- **must-conform-to-the-output-schema**: When `outputSchema` is present, the server **MUST** return `structuredContent` conforming to it; clients **SHOULD** validate it.
  - The schema root is restricted to `type: "object"`.
- **should-also-return-text-json**: For backward compatibility, a tool SHOULD also serialize the structured result as JSON in a `text` content block.
- **must-not-leak-secrets-in-outputs**: A server SHOULD sanitize outputs and MUST NOT leak secrets or internal identifiers the host should not see.

**Error handling**
- **should-use-both-error-channels**: The spec distinguishes two error channels, and a server SHOULD use both correctly (fail-fast at the right layer).
- **should-return-tool-errors-in-the-result**: **Tool execution errors** (API failure, validation, business-logic) SHOULD be returned **in the result** with `isError: true` and an actionable message.
  - The model sees these and can self-correct.
- **should-return-protocol-errors-as-json-rpc**: **Protocol errors** (unknown tool, malformed request) SHOULD be returned as a JSON-RPC `error`.
  - The model usually cannot fix these.
- **should-not-throw-protocol-errors-for-tool-failures**: A server SHOULD NOT throw a protocol error for a recoverable tool failure — the model loses the signal it needs to retry.

**Annotations (untrusted hints)**
- **should-set-annotations**: A server SHOULD set `annotations` to describe tool behavior so hosts can apply policy.
- **must-treat-annotations-as-untrusted**: All are hints with defaults; clients **MUST** treat them as untrusted unless the server is trusted.
- **should-set-annotations-accurately**: You **SHOULD** set these accurately; mislabeling a destructive tool as read-only invites unguarded invocation.
- **must-not-rely-on-annotations-alone**: Annotations inform UI and consent flows; they **MUST NOT** be your only safety control.
  - Validate inputs, enforce access control, and rate-limit on the server.

**Security baseline**
- **must-validate-authorize-rate-limit-and-sanitize**: Servers **MUST** validate all tool inputs, enforce access controls, rate-limit invocations, and sanitize outputs.
- **should-write-for-consent**: A server SHOULD assume a human-in-the-loop may gate invocations, and write descriptions and errors that make consent decisions clear.
