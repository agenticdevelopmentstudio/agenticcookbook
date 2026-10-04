
- A tool **SHOULD** declare an `outputSchema` and return matching `structuredContent`. This gives the model and client typed, validatable results.
- When `outputSchema` is present, the server **MUST** return `structuredContent` conforming to it; clients **SHOULD** validate it. The schema root is restricted to `type: "object"`.
- For backward compatibility, also serialize the structured result as JSON in a `text` content block.
- Sanitize outputs and never leak secrets or internal identifiers the host should not see.

