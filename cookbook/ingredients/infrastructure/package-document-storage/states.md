
| State | Behavior |
|-------|----------|
| New document | Empty model with default values; first save creates the package directory with a fresh SQLite database |
| Existing SQLite document | Read from SQLite database in the package; schema version checked against current version |
| Legacy JSON document | JSON file detected in the package; model populated from JSON; next save migrates to SQLite format |
| Corrupt database | SQLite open or query fails; document reports an error to the user and does not load |
| Missing database file | Neither SQLite nor JSON found in the package directory; treated as new empty document |
| Schema version mismatch (older) | Database `user_version` is lower than current; migration logic upgrades the schema on next save |
| Schema version mismatch (newer) | Database `user_version` is higher than current app version; document reports a version error and refuses to load |
| Writing | Model serialized to a temporary SQLite database, wrapped in a FileWrapper, and written to the package |

