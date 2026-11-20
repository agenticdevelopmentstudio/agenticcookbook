
- `should-place-heavy-os-framework-users-in-platform-group`: whether files importing three or more OS-specific frameworks sit in a platform-specific group
- `should-group-hardware-api-code`: whether hardware API code is grouped together
- `should-mark-hardware-dependent-groups`: whether each hardware API group is marked hardware-dependent
- `should-separate-network-and-persistence`: whether network and persistence files are separated, outside a unified synchronization layer
- `should-identify-sdk-wrapper-groups`: whether each third-party SDK touched by more than 2–3 files has its wrapper/adapter group identified
- `should-not-treat-widespread-dependencies-as-boundaries`: whether dependencies appearing across all groups are treated as cross-cutting, not as boundaries
- `should-identify-introduced-system-dependencies`: a diff that introduces none is explicitly cleared.

Scope is the change under review — NOT a whole-codebase inventory.
