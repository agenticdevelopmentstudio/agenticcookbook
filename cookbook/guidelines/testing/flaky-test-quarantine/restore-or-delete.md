
- A test returns to the gating suite only after the root cause is fixed and it has run green enough times to clear the flip-rate threshold.
- Masking a failure with a retry, an increased timeout, or a loosened assertion is NOT a fix and MUST NOT qualify a test for restoration.
- If the covered behavior no longer warrants a test, the test SHOULD be deleted outright rather than left quarantined.

