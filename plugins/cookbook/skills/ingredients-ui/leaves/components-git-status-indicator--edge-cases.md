<!-- leaf: ingredients-ui/components-git-status-indicator--edge-cases · source: ingredients/ui/components/git-status-indicator.md -->

# Git Status Indicator

## Edge Cases

- **Not a git repo**: No statuses shown, no error.
- **Very large repo (10k+ files)**: `git status` may be slow — timeout protects UI.
- **Rapid file changes**: Debounce git status refresh (0.5s recommended) to prevent thrashing.
- **Submodules**: `--ignore-submodules` flag recommended to avoid deep recursion.
- **Binary files**: Same status handling as text files.
