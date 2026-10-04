
### Status types

- **supported-statuses**: The component MUST support these git statuses:

  | Status | Character | Color | Priority |
  |--------|-----------|-------|----------|
  | Modified | M | Orange | 5 |
  | Added | A | Green | 4 |
  | Deleted | D | Red | 3 |
  | Renamed | R | Blue | 2 |
  | Untracked | ? | Green | 1 |
  | Conflicted | U | Purple | 6 (highest) |
  | Ignored | ! | Gray | 0 (lowest) |

### Display

- **character-badge-display**: The status MUST be displayable as a single monospaced character badge with the associated color.
- **bold-monospaced-font**: The badge MUST use a bold, caption-sized monospaced font for the character.
- **optional-text-label**: The badge MAY additionally show a text label (e.g., "Modified") in inspector/detail contexts.

### Directory rollup

- **directory-rollup**: When displaying status for a directory, the component MUST aggregate child file statuses by selecting the highest-priority status. For example, a directory containing both modified (5) and untracked (1) files MUST show modified (5).
- **ancestor-propagation**: The rollup MUST propagate through all ancestor directories up to the root.

### Git status parsing

- **porcelain-parsing**: Status SHOULD be parsed from `git status --porcelain=v1` output (XY format).
- **handle-renames**: Parsing MUST handle renamed files (format: `R  old -> new`) by using the new path.
- **command-timeout**: The git command MUST have a timeout (5 seconds recommended) to prevent hanging on large repos.
- **discard-stale-results**: Stale results MUST be discarded — use request ID tracking to ignore out-of-order responses.

