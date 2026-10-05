
A hierarchical file browser that displays a project's directory structure using OutlineGroup/List with lazy child loading, git status badges, configurable ignore patterns, and SF Symbol icons themed by file type. Serves as the primary navigation sidebar for project-based workflows.

### Terminology

| Term | Definition |
|------|-----------|
| Node | A single entry in the file tree representing a file or directory |
| Lazy loading | Children of a directory are loaded on demand when the user expands it, not upfront |
| Package | A directory that is treated as a single opaque item (e.g., `.catnip-proj`) and is not expandable |
| Ignore pattern | A POSIX fnmatch()-compatible wildcard pattern (supports `*` and `?`) used to hide matching entries |
| Rollup | Aggregation of git statuses from child files to their parent directory |

