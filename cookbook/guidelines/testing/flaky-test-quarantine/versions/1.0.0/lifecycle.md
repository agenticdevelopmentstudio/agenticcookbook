
The lifecycle has five stages. A test MUST move forward through them; it MUST NOT stall in quarantine.

1. **Detect** — Identify flakiness from a signal, not a hunch (see Detection).
2. **Quarantine** — Move the test out of the gating suite into a non-gating bucket. It MUST still execute on every run and report results.
3. **Own** — Assign exactly one owner and a fix deadline at the moment of quarantine.
4. **Fix** — Diagnose and remove the root cause of nondeterminism.
5. **Restore** — Return the test to the gating suite once it is stable, or delete it if the behavior it covered is no longer worth testing.

