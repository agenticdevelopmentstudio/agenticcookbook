
Subsystem: `{{bundle_id}}` | Category: `CodeEditorPane`

| Event | Level | Message |
|-------|-------|---------|
| File load started | debug | `CodeEditorPane: loading file "{{path}}"` |
| File load succeeded | debug | `CodeEditorPane: loaded "{{filename}}" ({{bytes}} bytes, language: {{language}})` |
| File load failed (encoding) | debug | `CodeEditorPane: cannot display "{{filename}}" — not valid UTF-8` |
| File load failed (error) | error | `CodeEditorPane: failed to load "{{path}}": {{error}}` |
| Language detected | debug | `CodeEditorPane: detected language "{{language}}" for extension "{{ext}}"` |
| Theme applied | debug | `CodeEditorPane: applied theme "{{theme}}" (appearance: {{light\|dark}})` |
| Content modified | debug | `CodeEditorPane: "{{filename}}" marked as modified` |
| Content reverted to clean | debug | `CodeEditorPane: "{{filename}}" marked as clean (matches saved)` |
| Auto-save triggered | debug | `CodeEditorPane: auto-saving "{{filename}}" before switching to "{{newFilename}}"` |
| Manual save triggered | debug | `CodeEditorPane: manual save "{{filename}}" (Cmd+S)` |
| Save succeeded | debug | `CodeEditorPane: saved "{{filename}}" ({{bytes}} bytes)` |
| Save failed | error | `CodeEditorPane: save failed for "{{path}}": {{error}}` |
| External modification detected | warning | `CodeEditorPane: "{{filename}}" modified externally` |
| File deleted while open | warning | `CodeEditorPane: "{{filename}}" deleted externally while open in editor` |
| Load generation incremented | debug | `CodeEditorPane: loadGeneration incremented to {{generation}} for "{{filename}}"` |
| Placeholder displayed | debug | `CodeEditorPane: showing placeholder — {{reason}}` |
| Editor recreated | debug | `CodeEditorPane: editor recreated (loadGeneration={{generation}})` |
| Large file warning | warning | `CodeEditorPane: "{{filename}}" is {{size}}MB — may impact performance` |

