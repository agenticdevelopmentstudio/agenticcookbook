
- Define `inputSchema` with explicit `type`, `required`, `enum`, `pattern`, `minLength`/`maxLength`, and numeric bounds; the root **MUST** be `type: object`.
- Validate with a JSON Schema 2020-12 validator at the handler boundary and **MUST** reject unknown properties (`additionalProperties: false`) unless a field is intentionally open.
- Implementations **MUST NOT** auto-dereference external `$ref` URIs and **SHOULD** bound schema depth and total validation time to prevent schema-driven DoS.
- A passing schema check proves shape, not safety — it does **not** neutralize malicious instructions embedded in syntactically valid strings.

