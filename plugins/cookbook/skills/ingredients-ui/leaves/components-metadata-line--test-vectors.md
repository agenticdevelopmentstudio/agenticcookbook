<!-- leaf: ingredients-ui/components-metadata-line--test-vectors · source: ingredients/ui/components/metadata-line.md -->

# Metadata Line

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| meta-001 | icon-and-text-line | icon: "folder", text: "/Users/me/projects" | Icon + text displayed on one line |
| meta-002 | truncation-with-ellipsis | text: very long path, truncation: middle | Displays "..." in middle of path |
| meta-003 | optional-tooltip | Hover over truncated text on macOS | Tooltip shows full text |
| meta-004 | full-text-a11y-label | VoiceOver on truncated text | Full text announced |
