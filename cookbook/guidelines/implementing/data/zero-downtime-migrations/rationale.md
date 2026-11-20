
- `must-be-compatible-with-running-version`, `must-not-ship-schema-and-code-together`, `must-keep-old-shape-one-deploy-cycle`: During a rolling deploy, both the old app version (N-1) and the new one (N) run against the *same* schema simultaneously.
- `should-bound-ddl-lock-wait`, `must-set-lock-timeout`, `should-retry-lock-timeout-aborts`: A blocking DDL statement that waits on a lock will queue *behind* it every subsequent query on that table — the app appears frozen.
- `should-confirm-engine-lock-behavior`: Note: exact lock behavior and which `ALTER TABLE` operations rewrite the table vary by database engine and version. The Postgres examples here are illustrative.
