
Each is a deliberate trade-off:

| Scheme | Form | Trade-off |
|--------|------|-----------|
| URI path | `/v2/orders` | Most visible and cacheable; couples version to URL, harder for fine-grained evolution |
| Media-type / header | `Accept: application/vnd.acme.v2+json` | Keeps URLs stable, content-negotiation friendly; less obvious, easy to omit |
| Query param | `/orders?version=2` | Simple; pollutes URLs and caches, easy to forget |
