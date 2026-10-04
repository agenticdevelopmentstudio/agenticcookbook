
- Deriving the key from a timestamp or auto-increment — low entropy invites collisions.
- Treating a `409`/`422` from key handling as a transient error and retrying blindly (see `agenticdevelopercookbook://guidelines/implementing/networking/retry-and-resilience`).
- Caching only the status code and not the body, so a replay returns an incomplete response.

