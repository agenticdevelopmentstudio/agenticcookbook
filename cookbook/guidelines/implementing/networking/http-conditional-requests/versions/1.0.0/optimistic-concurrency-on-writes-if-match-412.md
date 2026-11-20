
- For PUT/PATCH/DELETE on shared, mutable resources, clients **SHOULD** send `If-Match: <etag>` carrying the ETag they last read.
- The server **MUST** apply the change only if the current ETag matches (strong comparison); otherwise it **MUST** reject with `412 Precondition Failed` and make no change. The client refetches, rebases its edit, and retries.
- This is the read-modify-write guard against lost updates: two clients editing the same version cannot both succeed.
- `If-Match: *` requires the resource to exist; `If-None-Match: *` on a write requires it to NOT exist (create-only, guarding against accidental overwrite).
- Mutating endpoints on shared resources **SHOULD** support `If-Match` and **MAY** require it (returning `428 Precondition Required`, RFC 6585) to force callers to opt into concurrency safety.

