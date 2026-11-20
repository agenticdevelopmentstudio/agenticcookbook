
- You **SHOULD** assert specific values explicitly when the test verifies behavior or computation; a snapshot obscures *which* field mattered and why.
- You **SHOULD** reserve snapshots for output that is verbose, structurally stable, and tedious to assert by hand (serialized DOM, generated config, formatted reports).
- You **SHOULD** delete obsolete snapshots promptly (`--ci` reports them); a stale snapshot is dead weight that misleads future readers (`design-for-deletion`).

