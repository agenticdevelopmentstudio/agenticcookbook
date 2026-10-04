
- Use **OpenAPI 3.1.x** as the baseline (full JSON Schema 2020-12 alignment). See https://spec.openapis.org/oas/v3.1.0.
- OpenAPI **3.2.0** was published in September 2025 (adds streaming media types, the `query` HTTP method, `additionalOperations`, and a richer Tag Object). Adopt it **only** when your toolchain — generators, linters, mock servers — fully supports it; otherwise stay on 3.1.x. Verify tool support before relying on 3.2-only features.
- Always state the `openapi:` version explicitly in the document; **MUST NOT** leave it implicit or mixed across files.

