<!-- leaf: ingredients-ui/components-git-status-indicator--test-vectors · source: ingredients/ui/components/git-status-indicator.md -->

# Git Status Indicator

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| git-001 | supported-statuses | File status: modified | Orange "M" badge |
| git-002 | supported-statuses | File status: conflicted | Purple "U" badge |
| git-003 | directory-rollup | Directory with modified + untracked children | Shows modified (priority 5 > 1) |
| git-004 | directory-rollup | Directory with conflicted + modified children | Shows conflicted (priority 6 > 5) |
| git-005 | ancestor-propagation | Deeply nested modified file | All ancestor dirs show modified |
| git-006 | handle-renames | Porcelain output: `R  old.txt -> new.txt` | Status applied to new.txt path |
| git-007 | command-timeout | Git hangs for 6 seconds | Command terminated, no crash |
| git-008 | differentiate-without-color | Grayscale display | Characters (M, A, D, etc.) still distinguish statuses |
