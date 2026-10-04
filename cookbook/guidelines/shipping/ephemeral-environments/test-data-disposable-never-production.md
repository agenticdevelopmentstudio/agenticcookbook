
- Seed each environment with synthetic or anonymized fixtures (per *test-data-management*). Production PII MUST NOT be copied into a preview.
- Choose a database strategy: **fresh provision** (blank DB + run migrations + seed) is simplest and works anywhere; **copy-on-write branching** (e.g. Neon/PlanetScale-style branches, or a snapshot restore) is faster when the engine supports it natively. Pick fresh-provision by default and adopt branching only when spin-up latency is a measured bottleneck (per *yagni*).

