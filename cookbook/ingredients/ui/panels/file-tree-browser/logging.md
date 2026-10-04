
Subsystem: `{{bundle_id}}` | Category: `FileTreeBrowser`

| Event | Level | Message |
|-------|-------|---------|
| Tree load started | debug | `FileTreeBrowser: loading tree for "{{rootPath}}"` |
| Tree load completed | debug | `FileTreeBrowser: loaded {{count}} top-level entries` |
| Directory expanded | debug | `FileTreeBrowser: expanded "{{path}}", {{count}} children` |
| Directory collapsed | debug | `FileTreeBrowser: collapsed "{{path}}"` |
| File selected | debug | `FileTreeBrowser: selected "{{path}}"` |
| Ignore pattern applied | debug | `FileTreeBrowser: hiding "{{path}}" (matched pattern "{{pattern}}")` |
| Scan error | error | `FileTreeBrowser: scan failed for "{{path}}": {{error}}` |
| Symlink cycle detected | warning | `FileTreeBrowser: symlink cycle detected at "{{path}}", skipping` |
| Settings changed | debug | `FileTreeBrowser: settings changed, triggering full resync` |
| Git status refresh | debug | `FileTreeBrowser: git status refresh (debounced)` |

