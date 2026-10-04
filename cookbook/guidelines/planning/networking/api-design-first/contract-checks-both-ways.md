
- Provider tests **SHOULD** assert that responses conform to the spec schemas.
- Consumers **SHOULD** validate against the same spec (generated client + schema validation) so a contract drift fails a test, not production.

