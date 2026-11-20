
- `should-enforce-all-access-control-server-side`: whether all access control is enforced server-side
- `must-not-use-client-side-checks-as-security-controls`: whether any client-side check is used as a security control
- `must-deny-by-default`: whether a request that no explicit permission grants is denied, and every new endpoint starts locked down
- `must-request-minimum-scopes`: whether every endpoint requests minimum scopes
- `should-enforce-permission-check-per-endpoint`: whether each endpoint enforces its own permission check
- `should-define-roles-with-minimal-permissions`: whether roles are defined with minimal permissions
- `should-prefer-fine-grained-permissions-in-roles`: whether fine-grained permissions composed into roles are used over monolithic role checks
- `must-verify-object-level-access`: whether the server verifies, for every request, that the authenticated user has access to the specific resource ID requested
- `must-not-treat-known-id-as-access`: whether any code grants access because the caller knows the ID
