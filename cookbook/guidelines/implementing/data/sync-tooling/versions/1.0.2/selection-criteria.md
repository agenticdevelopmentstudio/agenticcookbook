
1. **Do you need custom write-path business logic?** If yes: Session Extension (roll your own) or PowerSync. If no: cr-sqlite, ElectricSQL, sqlite-sync, or Turso.

2. **What is your server database?** Postgres only: ElectricSQL or PowerSync. Turso Cloud: Turso. SQLite Cloud or Supabase: sqlite-sync. Anything: Session Extension or cr-sqlite.

3. **Do you need production maturity?** Choose Session Extension, Litestream (for backup), ElectricSQL, or PowerSync. Avoid cr-sqlite, sqlite-sync, and Turso offline writes in production-critical systems.

4. **Is this backup/DR or active sync?** Backup only: Litestream. Active multi-device sync: everything else.

5. **Do you need peer-to-peer (no central server)?** cr-sqlite is the strongest choice. Session Extension with manual changeset exchange also works.

MUST evaluate maturity and support model before committing to a Beta tool in production. Prefer the Session Extension or PowerSync for production systems where stability and custom logic are priorities.

