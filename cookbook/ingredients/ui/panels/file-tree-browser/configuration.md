
This ingredient has no configurable options.

### Project Settings

| Setting | Type | Default | Constraints | Description |
|---------|------|---------|-------------|-------------|
| `ignorePatterns` | `[String]` | `[]` | POSIX fnmatch() wildcards | Wildcard patterns to hide from the tree |
| `maxScanWorkers` | `Int` | `3` | 1-8 | Maximum parallel scan concurrency for top-level directory scanning |

- **per-project-settings**: Both settings MUST be configured per-project.
- **setting-change-resync**: Changing either setting MUST trigger a full resync of the file tree.

