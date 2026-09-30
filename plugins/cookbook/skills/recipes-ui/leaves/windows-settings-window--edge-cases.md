<!-- leaf: recipes-ui/windows-settings-window--edge-cases · source: recipes/ui/windows/settings-window.md -->

# Settings Window

**Rules** (cite as `recipes-ui/windows-settings-window--edge-cases#<slug>`):

- `no-categories-defined` SHOULD — The window SHOULD display an empty state message rather than crashing.
- `category-with-no-settings` SHOULD — The content panel SHOULD show a message like "No settings available" rather than a blank panel.
- `extremely-long-category-name` SHOULD — Sidebar SHOULD truncate with ellipsis rather than expanding width.
- `many-settings-in-one-category` SHOULD — Content panel scrolls (content-vertical-scroll); performance SHOULD remain smooth with 50+ settings.
- `rapid-category-switching` MUST — Content panel MUST update without flicker or stale content.

## Edge Cases

- **No categories defined**: The window SHOULD display an empty state message rather than crashing.
- **Category with no settings**: The content panel SHOULD show a message like "No settings available" rather than a blank panel.
- **Extremely long category name**: Sidebar SHOULD truncate with ellipsis rather than expanding width.
- **Many settings in one category**: Content panel scrolls (content-vertical-scroll); performance SHOULD remain smooth with 50+ settings.
- **Rapid category switching**: Content panel MUST update without flicker or stale content.
