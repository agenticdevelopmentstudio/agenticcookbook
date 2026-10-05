
```
Tests/Projects/Apple/              <- XcodeGen Apple Project
├── project.yml
├── TestSharedKit/
├── Sources/{iOS,macOS,watchOS,tvOS,visionOS}/   <- entry point per platform
└── Shared/                        <- compiled into every target
    ├── Components/                <- component implementations
    └── Catalog/                   <- Component Catalog entries

 App entry point -> ComponentCatalogView -> catalog entry -> component in each state
```

Not a visual layout: the diagram shows how the project structure and catalog compose. Navigation layout per platform is defined by the Component Catalog ingredient.

