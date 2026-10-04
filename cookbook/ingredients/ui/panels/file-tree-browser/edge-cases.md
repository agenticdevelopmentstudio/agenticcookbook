
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

