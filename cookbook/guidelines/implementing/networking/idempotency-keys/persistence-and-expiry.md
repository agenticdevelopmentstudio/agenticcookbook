
- Persist key records durably (database or shared cache), not in per-process memory — a retry can land on any instance.
- **MUST** set a TTL on each record (24 hours is a common default). After expiry the same key value is treated as new. Keep the TTL longer than the client's maximum retry window.
- Only finalize (persist as replayable) once the side effect has committed. Recording the key before the operation succeeds risks replaying a response for work that never happened.

