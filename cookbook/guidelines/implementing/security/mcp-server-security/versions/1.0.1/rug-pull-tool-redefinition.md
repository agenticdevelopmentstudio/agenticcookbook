
A server (or a tool it proxies) can present a benign description at approval time and a malicious one later.

- When a host binds user approval to a tool, that approval **SHOULD** be bound to a hash of the tool's full content (name, description, input schema). Any change re-triggers consent.
- The server **SHOULD** version tool definitions and avoid silent semantic changes; changing behavior without a version bump defeats hash-bound approval.
- ACCURACY NOTE: the publicized "MCPoison"/"CurXecute" CVEs were CLIENT-side bugs in an IDE and have been patched. Retain the rug-pull threat class and the hash-bound-approval mitigation; do not cite those CVEs as motivation for server authoring.

