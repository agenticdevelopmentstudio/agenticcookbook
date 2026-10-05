
Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Watch started | info | `DirectorySync: FSEvents watch started for "{{rootPath}}"` |
| Watch stopped | info | `DirectorySync: FSEvents watch stopped` |
| Change event received | debug | `DirectorySync: {{changeCount}} changes received, {{affectedDirCount}} directories affected` |
| Excluded path filtered | debug | `DirectorySync: filtered {{count}} excluded paths` |

