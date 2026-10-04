
- **Consumer-driven contracts** — use when you own *both* sides of the interaction (your own services calling each other). The consumer's expectations define the contract; the provider verifies it.
- **Provider / schema contracts** — use for third-party or upstream APIs you consume but do **not** control. Pin to the provider's published schema (e.g. an OpenAPI document at a dated revision) and test that your client tolerates it; you cannot make them run your contract.

