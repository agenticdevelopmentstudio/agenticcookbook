<!-- leaf: ingredients-ui/panels-file-tree-browser--edge-cases · source: ingredients/ui/panels/file-tree-browser.md -->

# File Tree Browser

**Rules** (cite as `ingredients-ui/panels-file-tree-browser--edge-cases#<slug>`):

- `empty-project-directory` SHOULD — Tree SHOULD display an empty state rather than a blank sidebar. MAY delegate to an empty-state component.
- `very-deep-nesting` MUST — Tree MUST remain scrollable and responsive. Indentation SHOULD cap or compress at extreme depths.
- `very-large-directory` SHOULD — Lazy loading (lazy-child-loading) and parallel scanning (parallel-top-level-scan) mitigate load time. The tree SHOULD …
- `permission-denied-on-directory` SHOULD — The directory SHOULD show as non-expandable. An error SHOULD be logged but not surfaced to the user as a modal alert.
- `symlink-loops` MUST — The scanner MUST detect and break symlink cycles to prevent infinite recursion.
- `file-disappears-between-scan-and-display` SHOULD — The tree SHOULD gracefully handle stale entries — remove them on next refresh rather than crash.
- `ignore-pattern-changed-while-tree-is-visible` MUST — Tree MUST fully resync to apply new pattern.

## Edge Cases

- **Empty project directory**: Tree SHOULD display an empty state rather than a blank sidebar. MAY delegate to an empty-state component.
- **Very deep nesting (20+ levels)**: Tree MUST remain scrollable and responsive. Indentation SHOULD cap or compress at extreme depths.
- **Very large directory (10k+ entries)**: Lazy loading (lazy-child-loading) and parallel scanning (parallel-top-level-scan) mitigate load time. The tree SHOULD remain responsive.
- **Permission denied on directory**: The directory SHOULD show as non-expandable. An error SHOULD be logged but not surfaced to the user as a modal alert.
- **Symlink loops**: The scanner MUST detect and break symlink cycles to prevent infinite recursion.
- **File disappears between scan and display**: The tree SHOULD gracefully handle stale entries — remove them on next refresh rather than crash.
- **Ignore pattern changed while tree is visible**: Tree MUST fully resync to apply new pattern.
- **Directory renamed externally**: Directory sync (delegate-directory-sync) handles this — tree updates on next sync cycle.
- **No git repository**: Git status badges not shown, no error. Tree renders without badges.
- **File tree does NOT include a search/filter UI**: This is noted as a future option and is explicitly out of scope for this spec.
