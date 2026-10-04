
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| apple-001 | xcodegen-project | Run `xcodegen generate` in project dir | `LitterboxTests.xcodeproj` is created |
| apple-002 | five-platform-targets | Open generated project | 5 app targets exist with correct names and platforms |
| apple-003 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestiOS | Build succeeds, app launches with catalog |
| apple-004 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestMac | Build succeeds, app launches with catalog |
| apple-005 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestWatch | Build succeeds, app launches with catalog |
| apple-006 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestTV | Build succeeds, app launches with catalog |
| apple-007 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestVision | Build succeeds, app launches with catalog |
| apple-008 | adaptive-navigation | Run LitterboxTestMac | Root view is NavigationSplitView |
| apple-009 | adaptive-navigation | Run LitterboxTestiOS on iPhone | Root view is NavigationStack |
| apple-010 | navigable-component-list | Launch any target with components registered | Catalog lists all components, selecting one navigates to detail |
| apple-011 | all-states-per-component | View a catalog entry | All states from spec are displayed in labeled sections |
| apple-012 | os-compilation-conditions | Build Shared/ code for all 5 platforms | No compilation errors from platform-specific API usage |

