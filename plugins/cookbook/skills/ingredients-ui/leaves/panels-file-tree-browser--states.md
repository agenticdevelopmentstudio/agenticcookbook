<!-- leaf: ingredients-ui/panels-file-tree-browser--states · source: ingredients/ui/panels/file-tree-browser.md -->

# File Tree Browser

## States

| State | Behavior |
|-------|----------|
| Initial load | Top-level entries scanned in parallel, tree populates progressively |
| Directory collapsed | Children not loaded (lazy) |
| Directory expanding | Children loaded on demand, disclosure indicator rotates |
| Directory expanded | Children visible, sorted per dirs-first-alpha-sort |
| File selected | Selection highlight, selection binding updated |
| Syncing | Status bar overlay visible (sync-status-bar) |
| Git status loading | Previous badges remain until new results arrive |
| Empty directory | Expanded directory shows no children |
| Ignore pattern matches | Matching entries hidden from tree |
