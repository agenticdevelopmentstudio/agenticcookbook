
Subsystem: `{{bundle_id}}` | Category: `PackageDocument`

| Event | Level | Message |
|-------|-------|---------|
| Document opened (SQLite) | info | `PackageDocument: opened "{{filename}}" (SQLite schema version {{version}})` |
| Document opened (legacy JSON) | info | `PackageDocument: opened "{{filename}}" (legacy JSON format)` |
| Document opened (empty package) | info | `PackageDocument: opened "{{filename}}" (empty package, defaults applied)` |
| Write started | debug | `PackageDocument: write started for "{{filename}}"` |
| Temp database created | debug | `PackageDocument: temp database created at "{{tempPath}}"` |
| Data inserted | debug | `PackageDocument: inserted {{rowCount}} rows into {{tableName}}` |
| Temp database bytes read | debug | `PackageDocument: read {{byteCount}} bytes from temp database` |
| Temp database cleaned up | debug | `PackageDocument: temp database deleted at "{{tempPath}}"` |
| Write completed | debug | `PackageDocument: write completed for "{{filename}}"` |
| Legacy migration triggered | info | `PackageDocument: migrating "{{filename}}" from legacy JSON to SQLite` |
| Schema migration triggered | info | `PackageDocument: migrating "{{filename}}" from schema version {{oldVersion}} to {{newVersion}}` |
| Corrupt database detected | error | `PackageDocument: corrupt database in "{{filename}}": {{error}}` |
| Schema version too new | error | `PackageDocument: "{{filename}}" has schema version {{version}}, app supports up to {{maxVersion}}` |
| Disk full during write | error | `PackageDocument: write failed for "{{filename}}": disk full or I/O error: {{error}}` |
| Temp file cleanup failed | warning | `PackageDocument: failed to delete temp database at "{{tempPath}}": {{error}}` |
| Date parsing failed | error | `PackageDocument: invalid date string "{{dateString}}" in metadata table` |

