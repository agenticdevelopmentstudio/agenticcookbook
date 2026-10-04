
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

### Catalog entry pattern

```swift
struct PrimaryButtonCatalog: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                Text("PrimaryButton").font(.title)

                Section("Default") {
                    PrimaryButton("Label", action: {})
                }
                Section("Disabled") {
                    PrimaryButton("Label", action: {}).disabled(true)
                }
                Section("Loading") {
                    PrimaryButton("Label", isLoading: true, action: {})
                }
            }
            .padding()
        }
    }
}

#Preview {
    PrimaryButtonCatalog()
}
```

