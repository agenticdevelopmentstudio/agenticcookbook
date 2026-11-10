
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| apple-003 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestiOS | Build succeeds, app launches with catalog |
| apple-004 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestMac | Build succeeds, app launches with catalog |
| apple-005 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestWatch | Build succeeds, app launches with catalog |
| apple-006 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestTV | Build succeeds, app launches with catalog |
| apple-007 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestVision | Build succeeds, app launches with catalog |
| apple-012 | os-compilation-conditions | Build Shared/ code for all 5 platforms | No compilation errors from platform-specific API usage |
| apple-013 | entry-point-shows-catalog, catalog-in-shared-dir | Launch any target after adding a component through the adding-component-steps | The catalog lists the component and its entry view displays all spec states |
| apple-014 | catalog-logging-via-shared-logger | Launch LitterboxTestMac and select a component | Logs show `ComponentCatalog: launched with N components` and `ComponentCatalog: selected "ComponentName"` |

