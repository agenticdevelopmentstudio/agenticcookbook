
Subsystem: `{{bundle_id}}` | Category: `PackageDocument`

| Event | Level | Message |
|-------|-------|---------|
| Document opened (SQLite) | info | `PackageDocument: opened "{{filename}}" (SQLite schema version {{version}})` |
| Document opened (legacy JSON) | info | `PackageDocument: opened "{{filename}}" (legacy JSON format)` |
| Document opened (empty package) | info | `PackageDocument: opened "{{filename}}" (empty package, defaults applied)` |
| Document created | info | `PackageDocument: created new document "{{filename}}"` |
| Write started | debug | `PackageDocument: write started for "{{filename}}"` |
| Temp database created | debug | `PackageDocument: temp database created at "{{tempPath}}"` |
| Data inserted | debug | `PackageDocument: inserted {{rowCount}} rows into {{tableName}}` |
| Temp database bytes read | debug | `PackageDocument: read {{byteCount}} bytes from temp database` |
| Temp database cleaned up | debug | `PackageDocument: temp database deleted at "{{tempPath}}"` |
| Write completed | debug | `PackageDocument: write completed for "{{filename}}"` |
| Legacy migration triggered | info | `PackageDocument: migrating "{{filename}}" from legacy JSON to SQLite` |
| Schema migration triggered | info | `PackageDocument: migrating "{{filename}}" from schema version {{oldVersion}} to {{newVersion}}` |
| Session URLs saved | debug | `PackageDocument: saved {{count}} open document URLs for session restoration` |
| Session restoration started | info | `PackageDocument: restoring {{count}} documents from previous session` |
| Session restoration failed for URL | warning | `PackageDocument: failed to restore document at "{{url}}": {{error}}` |
| Corrupt database detected | error | `PackageDocument: corrupt database in "{{filename}}": {{error}}` |
| Schema version too new | error | `PackageDocument: "{{filename}}" has schema version {{version}}, app supports up to {{maxVersion}}` |
| Disk full during write | error | `PackageDocument: write failed for "{{filename}}": disk full or I/O error: {{error}}` |
| SQLite open failed | error | `PackageDocument: cannot open database at "{{path}}": {{error}}` |
| SQL exec failed | error | `PackageDocument: exec failed: {{sql}} — {{error}}` |
| Temp file cleanup failed | warning | `PackageDocument: failed to delete temp database at "{{tempPath}}": {{error}}` |
| Date parsing failed | error | `PackageDocument: invalid date string "{{dateString}}" in metadata table` |

