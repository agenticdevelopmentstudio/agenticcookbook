<!-- leaf: ingredients-ui/components-status-bar--edge-cases · source: ingredients/ui/components/status-bar.md -->

# Status Bar

**Rules** (cite as `ingredients-ui/components-status-bar--edge-cases#<slug>`):

- `rapid-show-hide` SHOULD — If the operation completes before the appear animation finishes, the bar SHOULD reverse smoothly (not jump).

## Edge Cases

- **Rapid show/hide**: If the operation completes before the appear animation finishes, the bar SHOULD reverse smoothly (not jump).
- **Very long status text**: Truncate with ellipsis on one line.
- **Multiple overlapping operations**: Show the most recent status text. Bar stays visible until all operations complete.
