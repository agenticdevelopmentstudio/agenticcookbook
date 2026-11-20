
| Artifact | Generated from spec | Why |
|----------|--------------------|-----|
| Typed client | `openapi-generator`, `openapi-typescript`, etc. | Callers stay in sync with the contract |
| Server stubs / route validation | server generators or request-validation middleware | Implementation cannot drift silently |
| Mock server | Prism, or generator mocks | Consumers integrate before the backend exists |
| Docs | Redoc, Scalar, Swagger UI | Human + agent reference, always current |

