
- `should-enforce-all-access-control-server-side`: an access decision made only in the client, with no matching server check
- `must-not-use-client-side-checks-as-security-controls`: a hidden button or disabled field relied on to stop an action the server would still perform breaks it
- `must-deny-by-default`: an endpoint or permission check that lets a request through when no explicit permission grants it, or a new endpoint that ships open
- `must-request-minimum-scopes`: an endpoint requesting scopes broader than it needs breaks it
- `should-enforce-permission-check-per-endpoint`: an endpoint with no permission check of its own, relying on a gateway or a caller to have checked
- `should-define-roles-with-minimal-permissions`: a role granting permissions its holders do not need
- `should-prefer-fine-grained-permissions-in-roles`: code checking a role name (`if user.isAdmin`) where a fine-grained permission composed into roles would serve
- `must-verify-object-level-access`: a handler that loads a resource by the requested ID without checking the authenticated user may access that resource breaks it
- `must-not-treat-known-id-as-access`: access granted because the caller supplied a valid or guessable ID breaks it
