
- **should-treat-each-declared-target-as-candidate**: Each independently declared build target or package **SHOULD** be treated as a primary scope group candidate regardless of size: if the build system declares it separately, it is a candidate — one target, one candidate.
- **may-merge-trivial-wrappers**: If a target contains only re-exports of another target with no logic of its own, it **MAY** be merged with the target it wraps — merge trivial wrappers.
- **should-flag-large-monolithic-targets**: A single build target containing 200+ files **SHOULD** be flagged for secondary analysis using the `interface-cohesion` and `dependency-clusters` lenses — split large monolithic targets.
- **should-group-test-targets-with-main-target**: A test target **SHOULD** follow its main target: `AuthTests` belongs with `Auth` — test targets follow their main target.
- **should-not-separate-test-targets**: The analysis **SHOULD NOT** create a separate scope group for test targets unless they test multiple main targets.
- **should-exclude-vendor-directories**: Vendor/third-party directories — `node_modules/`, `Pods/`, `vendor/`, `.build/` — **SHOULD** be excluded: these are external dependencies, not scope groups.
- **should-note-shared-directories**: Directories named `core`, `common`, `shared`, or `util` at the root of a module **SHOULD** be noted, as they often represent deliberate cross-cutting infrastructure.
- **should-not-auto-split-shared-directories**: The analysis **SHOULD NOT** automatically split `core`, `common`, `shared`, or `util` directories.
