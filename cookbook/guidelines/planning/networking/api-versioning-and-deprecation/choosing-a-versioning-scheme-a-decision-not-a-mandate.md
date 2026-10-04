
Pick ONE scheme and apply it consistently across the whole surface. Each is a deliberate trade-off:

| Scheme | Form | Trade-off |
|--------|------|-----------|
| URI path | `/v2/orders` | Most visible and cacheable; couples version to URL, harder for fine-grained evolution |
| Media-type / header | `Accept: application/vnd.acme.v2+json` | Keeps URLs stable, content-negotiation friendly; less obvious, easy to omit |
| Query param | `/orders?version=2` | Simple; pollutes URLs and caches, easy to forget |

- You **MUST NOT** mix schemes within one API.
- You **SHOULD** version at a coarse grain (major version per breaking batch), not per endpoint or per field.
- Unversioned requests **SHOULD** resolve to a documented, pinned default version rather than "latest", so default behavior cannot shift under a client.

