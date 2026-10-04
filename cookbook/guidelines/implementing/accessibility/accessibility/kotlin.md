
Components MUST respond to these Android accessibility settings:

| Setting | API | Action |
|---------|-----|--------|
| Remove Animations | `animator_duration_scale == 0` | Disable all custom animations |
| Font Scale | `Configuration.fontScale` | Ensure layouts handle 2x font size |
| High Contrast Text | System setting | Ensure text meets WCAG AA contrast ratios |
| Color Inversion | `ACCESSIBILITY_DISPLAY_INVERSION_ENABLED` | Mark media with `importantForAccessibility` |
| TalkBack | `AccessibilityManager` | All elements have `contentDescription` and proper roles |
| Switch Access | `AccessibilityManager` | All interactive elements are focusable and reachable |
| Dark Theme | `Configuration.uiMode` | Full dark theme support |
| Display Size | `displayMetrics.density` | Layouts must not break at larger display sizes |

