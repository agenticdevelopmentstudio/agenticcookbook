
**Build manifests to locate:**

- `Package.swift` (Swift Package Manager) — each `.target()` and `.testTarget()` declaration names an explicit module with a defined source directory
- `build.gradle` / `build.gradle.kts` (Gradle) — top-level `apply plugin:` blocks and subproject includes in `settings.gradle` mark module roots; `implementation`/`api` vs `compileOnly` dependency configurations reveal visibility intent
- `package.json` (Node/npm/yarn) — the `name` field and `exports` map define the public surface; workspaces in a monorepo root list all sub-packages
- `*.csproj` / `*.sln` (MSBuild) — each `.csproj` is a distinct assembly; solution file project references encode the dependency graph
- `Podfile` / `podspec` (CocoaPods) — each podspec is a distributable module boundary
- `MODULE.bazel` / `BUILD` / `BUILD.bazel` (Bazel) — `cc_library`, `swift_library`, `kt_jvm_library` rules define fine-grained build units
- `Cargo.toml` (Rust) — `[workspace]` members and `[lib]`/`[[bin]]` sections define crate boundaries
- `go.mod` (Go) — each module root is a deployable unit; subdirectory `package` declarations name internal groupings

**Directory naming conventions:**

- Directories named `core`, `common`, `shared`, or `util` at the root of a module often represent deliberate cross-cutting infrastructure — note but do not automatically split them
- Directories named after product features (`auth`, `payments`, `checkout`) suggest feature-module organization
- A `modules/` or `packages/` top-level directory almost always signals a monorepo with multiple independent scopes

**Access control declarations:**

- Swift `internal` vs `public` vs `package` keywords on types and functions
- Kotlin `internal` visibility modifier
- TypeScript `export` statements in `index.ts` barrel files
- C# `internal` vs `public` class visibility
- Java package-private (default) vs `public` visibility

