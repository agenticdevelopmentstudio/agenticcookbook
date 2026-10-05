
- **Empty workspace (no entries)**: Both sidebar sections show empty. Detail pane shows welcome empty state with add buttons. The window MUST NOT crash or display broken layout.
- **Directory entry points to non-existent path**: Entry SHOULD display with a warning indicator (e.g., exclamation mark badge). Coordinator SHOULD NOT be created for a missing path. Entry SHOULD remain in the list to allow the user to remove it.
- **Project entry points to non-existent .catnip-proj**: Entry SHOULD display with a warning indicator. Double-tap SHOULD show an error rather than crash.
- **Very long project/directory name**: Sidebar rows SHOULD truncate with ellipsis. Full path shown in tooltip.
- **Many entries (50+)**: Sidebar MUST scroll. Performance MUST remain acceptable with lazy list rendering.
- **Directory entry discovers zero projects**: DisclosureGroup expands but shows no children. SHOULD display a subtle "No projects found" message within the group.

