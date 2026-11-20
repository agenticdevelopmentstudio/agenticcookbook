
- Store filterable attributes (tenant, source, document type, timestamp, access scope) as ordinary columns alongside the vector, and filter on them in the same query.
- For multi-tenant or access-controlled data, the tenant/permission filter **MUST** be applied at query time — never rely on the LLM to ignore retrieved context it should not see (fail-fast, security).

