
WinUI 3 controls expose [UI Automation](https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-uiautomationoverview) patterns automatically. Set `AutomationProperties.Name` on interactive elements that lack visible text labels.

- Use `AutomationProperties.LabeledBy` for form fields
- Use `AutomationProperties.LiveSetting` for dynamic content regions
- High contrast support is automatic when using `ThemeResource` — never hard-code colors
- Test with [Accessibility Insights for Windows](https://accessibilityinsights.io/)
- Keyboard navigation: all interactive elements must be reachable via Tab, actionable via Enter/Space

Components MUST respond to these Windows accessibility settings:

| Setting | API / Detection | Action |
|---------|----------------|--------|
| High Contrast | `AccessibilitySettings.HighContrast` | Automatic via ThemeResource — verify custom visuals adapt |
| Animations Disabled | `UISettings.AnimationsEnabled` | Disable all custom animations and transitions |
| Text Scaling | `UISettings.TextScaleFactor` | Layouts must not break up to 225% text scale |
| Color Filters | System setting | Ensure UI is usable with color vision deficiency filters |
| Narrator | UI Automation tree | All elements have Name, Role, and appropriate patterns |
| Keyboard Navigation | Focus management | All interactive elements reachable via Tab, actionable via Enter/Space |
| Dark Theme | `Application.RequestedTheme` | Full dark theme support via ThemeResource |
| Caret Browsing | System setting | Non-interactive text should be navigable |

