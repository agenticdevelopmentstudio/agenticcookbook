
- Tool results flow back into model context — **SHOULD** validate against `outputSchema` and strip or label untrusted fetched content so it is not read as instructions.
- Log validation failures and authorization denials with the tool name and caller identity (not raw argument payloads); **MUST NOT** log secrets or full tokens.
- Return structured, non-leaky errors on rejection — fail closed, surface a stable error code, and **MUST NOT** echo internal paths or stack traces.

