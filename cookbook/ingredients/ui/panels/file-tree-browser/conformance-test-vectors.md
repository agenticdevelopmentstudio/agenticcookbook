
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ftb-001 | outline-group-hierarchy | Render tree with nested directories | OutlineGroup renders expandable hierarchy |
| ftb-002 | lazy-child-loading | Expand a collapsed directory | Children loaded at expand time, not before |
| ftb-003 | dirs-first-alpha-sort | Directory with mixed files and subdirs | Subdirs listed first, then files, both alphabetical case-insensitive |
| ftb-004 | fnmatch-ignore-patterns | Ignore pattern `*.log`, directory contains `debug.log` | `debug.log` not visible in tree |
| ftb-005 | fnmatch-ignore-patterns | Ignore pattern `temp?`, directory contains `temp1` and `temp12` | `temp1` hidden, `temp12` visible |
| ftb-006 | show-dotfiles | Directory contains `.env` and `.gitignore` | Both dotfiles visible in tree |
| ftb-007 | hide-ds-store | Directory contains `.DS_Store` | `.DS_Store` not visible in tree |
| ftb-008 | package-dir-display | Directory contains `MyPlugin.catnip-proj` | Shown as non-expandable item with `shippingbox.fill` icon |
| ftb-009 | single-file-selection | Tap/click a file row | Selection binding updates to that file |
| ftb-010 | git-status-badge | File has git status "modified" | Orange "M" badge right-aligned in row |
| ftb-011 | git-debounce-refresh | Three file changes within 0.3s | Git status refreshes once after 0.5s debounce, not three times |
| ftb-012 | dirs-first-alpha-sort | Entries: `zebra/`, `alpha.txt`, `beta/`, `gamma.txt` | Order: `beta/`, `zebra/`, `alpha.txt`, `gamma.txt` |
| ftb-013 | parallel-top-level-scan | Root directory with 5 top-level subdirectories | All 5 scanned in parallel (up to maxScanWorkers) |
| ftb-014 | row-accessible-label, voiceover-row-announce | VoiceOver focus on a modified Swift file | Announces "App.swift, file, Modified" |
| ftb-015 | keyboard-tree-nav | Focus on collapsed directory, press Right arrow | Directory expands |

