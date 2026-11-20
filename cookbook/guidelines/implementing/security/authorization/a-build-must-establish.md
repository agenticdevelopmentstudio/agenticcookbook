
- `should-enforce-all-access-control-server-side`: every access control decision is enforced server-side, or the code says why not
- `must-not-use-client-side-checks-as-security-controls`: every action a client-side check hides or disables is also refused by the server
- `must-deny-by-default`: every request that no explicit permission grants is denied, and every new endpoint starts locked down
- `must-request-minimum-scopes`: every endpoint requests only the minimum scopes it needs
- `should-enforce-permission-check-per-endpoint`: every endpoint enforces its own permission check, or the code says why not
- `should-define-roles-with-minimal-permissions`: every role holds only the permissions its holders need, or the code says why
- `should-prefer-fine-grained-permissions-in-roles`: permission checks test fine-grained permissions composed into roles, not monolithic roles, or the code says why
- `must-verify-object-level-access`: every request for a resource by ID verifies the authenticated user has access to that resource
- `must-not-treat-known-id-as-access`: no code path grants access because the caller knows the ID
