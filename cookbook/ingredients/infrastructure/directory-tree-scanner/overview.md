
A directory tree scanner produces the in-memory file tree for a directory subtree in two modes: a full sync that rebuilds the whole tree from the filesystem, and a surgical update that reloads only the children of directories a change event touched. Full sync runs top-level directories in parallel with bounded concurrency; surgical update keeps change handling cheap by never rebuilding what did not change. Use it as the scanning engine of a directory sync coordinator.

### Terminology

| Term | Definition |
|------|-----------|
| File tree node | An in-memory representation of a single file or directory: path, name, metadata, and children |
| Full sync | A complete traversal of the directory subtree that rebuilds the in-memory tree from scratch |
| Surgical update | A targeted reload that only rescans the directories affected by a filesystem change event |
| Package | A directory that the OS treats as a single opaque file (e.g., `.app`, `.playground`, `.catnip-proj`) |

