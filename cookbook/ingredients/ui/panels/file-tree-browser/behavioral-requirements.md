
### Tree display

- **outline-group-hierarchy**: The file tree MUST render using List + OutlineGroup to provide expandable/collapsible directory hierarchy.
- **lazy-child-loading**: The tree MUST use lazy child loading — children MUST be loaded on demand when a directory is expanded, not when the tree is first rendered.
- **parallel-top-level-scan**: Top-level directories MUST be scanned in parallel via OperationQueue for faster initial load.
- **sidebar-list-style**: The tree MUST use `.listStyle(.sidebar)` on Apple platforms.

### Sorting

- **dirs-first-alpha-sort**: Entries MUST be sorted with directories first, then files. Within each group, entries MUST be sorted alphabetically using case-insensitive comparison.

### Filtering and visibility

- **fnmatch-ignore-patterns**: Ignore patterns MUST use POSIX fnmatch() wildcards (`*`, `?`). Entries matching any ignore pattern MUST be hidden from the tree.
- **show-dotfiles**: Hidden files (dotfiles) MUST be shown in the tree.
- **hide-ds-store**: `.DS_Store` files MUST always be hidden regardless of ignore patterns (hardcoded skip).

### Packages

- **package-dir-display**: Directories recognized as packages (e.g., `.catnip-proj` and other registered package extensions) MUST be displayed as single non-expandable items with the package icon.

### Selection

- **single-file-selection**: The tree MUST support single file selection via a selection binding.

### Git status integration

- **git-status-badge**: Each file row MUST display a git status badge when the file has a git status. The badge MUST be right-aligned, use a monospaced font, and be colored per status type. Badge rendering MUST delegate to [git-status-indicator.md](../components/git-status-indicator.md).
- **git-debounce-refresh**: Git status MUST refresh with a 0.5-second debounce after file changes to prevent thrashing.
- **git-background-fetch**: Git status MUST be fetched on a background queue and MUST NOT block the main thread.

### Status bar integration

- **sync-status-bar**: During directory sync operations, a status bar overlay MUST be shown. Display MUST delegate to [status-bar.md](../components/status-bar.md).

### Directory sync lifecycle

- **delegate-directory-sync**: File system monitoring and sync behavior MUST delegate to [directory-sync.md](../../../recipes/infrastructure/directory-sync.md).

