
Choose a database strategy: **fresh provision** (blank DB + run migrations + seed) is simplest and works anywhere; **copy-on-write branching** (e.g. Neon/PlanetScale-style branches, or a snapshot restore) is faster when the engine supports it natively.
