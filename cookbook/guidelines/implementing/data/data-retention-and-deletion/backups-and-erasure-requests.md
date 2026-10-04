
- Backups and immutable logs **SHOULD** be excluded from immediate cascade; instead **document the lag** — deleted data persists until the backup rotates out of its retention window.
- Define and publish a backup retention/purge policy so the maximum lag between an erasure request and full physical removal is bounded and known.
- For an erasure request, suppress the data from active systems immediately and rely on backup rotation for residual copies; **MUST NOT** restore deleted records from an old backup without re-applying pending deletions.

