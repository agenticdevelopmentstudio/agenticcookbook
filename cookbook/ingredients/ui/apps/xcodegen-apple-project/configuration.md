
| Option | Type | Default | Description |
|---|---|---|---|
| `name` | string | `LitterboxTests` | Generated project name |
| `bundleIdPrefix` | string | `com.litterbox.test` | Prefix for every target bundle ID |
| `deploymentTarget` | map | iOS 17.0, macOS 14.0, watchOS 10.0, tvOS 17.0, visionOS 1.0 | Minimum OS versions, also applied to TestSharedKit |
| `outputDirectory` | path | `Tests/Projects/Apple/` | Where the project is generated |

### project.yml

```yaml
name: LitterboxTests
settings:
  base:
    GENERATE_INFOPLIST_FILE: YES
options:
  bundleIdPrefix: com.litterbox.test
  deploymentTarget:
    iOS: "17.0"
    macOS: "14.0"
    watchOS: "10.0"
    tvOS: "17.0"
    visionOS: "1.0"
packages:
  TestSharedKit:
    path: TestSharedKit
targets:
  LitterboxTestiOS:
    type: application
    platform: iOS
    sources:
      - Sources/iOS
      - Shared
    dependencies:
      - package: TestSharedKit
  LitterboxTestMac:
    type: application
    platform: macOS
    sources:
      - Sources/macOS
      - Shared
    dependencies:
      - package: TestSharedKit
  LitterboxTestWatch:
    type: application
    platform: watchOS
    sources:
      - Sources/watchOS
      - Shared
    dependencies:
      - package: TestSharedKit
  LitterboxTestTV:
    type: application
    platform: tvOS
    sources:
      - Sources/tvOS
      - Shared
    dependencies:
      - package: TestSharedKit
  LitterboxTestVision:
    type: application
    platform: visionOS
    sources:
      - Sources/visionOS
      - Shared
    dependencies:
      - package: TestSharedKit
```

### Source file layout

```
Tests/Projects/Apple/
├── project.yml
├── TestSharedKit/
│   ├── Package.swift
│   └── Sources/
│       └── TestSharedKit/
│           └── ComponentCatalog.swift
├── Sources/
│   ├── iOS/
│   │   └── LitterboxTestiOSApp.swift
│   ├── macOS/
│   │   └── LitterboxTestMacApp.swift
│   ├── watchOS/
│   │   └── LitterboxTestWatchApp.swift
│   ├── tvOS/
│   │   └── LitterboxTestTVApp.swift
│   └── visionOS/
│       └── LitterboxTestVisionApp.swift
└── Shared/
    ├── Components/          ← component implementations from ui/ specs
    └── Catalog/             ← catalog entry views showing all states
```

