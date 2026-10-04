
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| empty-001 | centered-layout | Render in a 400×400 container | Content is centered |
| empty-002 | icon-and-heading | Provide icon + heading only | Both displayed, no crash |
| empty-003 | optional-action-buttons | Provide 2 action buttons | Both rendered, primary is prominent |
| empty-004 | adaptive-container-fit | Render in 200×150 container | Content fits without scrolling/overflow |
| empty-005 | native-unavailable-view | Build on macOS 14+ | Uses ContentUnavailableView |
| empty-006 | decorative-icon | Enable VoiceOver, navigate to empty state | Icon is not announced, heading is first |

