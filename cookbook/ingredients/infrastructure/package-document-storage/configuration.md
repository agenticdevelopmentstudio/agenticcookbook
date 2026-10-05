
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `databaseFileName` | string | (required, per document type) | Name of the SQLite file inside the package (e.g., `project.db`) |
| `legacyJSONFileName` | string | (none) | Name of the legacy JSON file read as a fallback (e.g., `data.json`) |
| `currentSchemaVersion` | integer | (required) | Highest `PRAGMA user_version` this app version supports |

