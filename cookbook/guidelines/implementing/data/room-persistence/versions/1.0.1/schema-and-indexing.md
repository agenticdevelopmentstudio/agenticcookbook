
- Define one `@Entity` per normalized table. Declare relationships with `@ForeignKey` and load them via `@Relation`, not by denormalizing.
- Every `@ForeignKey` column **MUST** be indexed (`@Entity(indices = [Index("owner_id")])`). Room emits a build warning for unindexed foreign keys; treat it as an error to fix.
- Add an `@Index(unique = true)` for natural-key uniqueness instead of relying on app-side checks.

