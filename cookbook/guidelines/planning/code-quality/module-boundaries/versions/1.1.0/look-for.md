
- `should-treat-each-declared-target-as-candidate`: declared targets, packages, assemblies, crates or modules in the manifests that are missing from the candidate list, small ones included
- `may-merge-trivial-wrappers`: targets holding only re-exports of another target, and whether merging them was considered
- `should-flag-large-monolithic-targets`: targets with 200+ files, and whether they are flagged for `interface-cohesion` and `dependency-clusters` analysis
- `should-group-test-targets-with-main-target`: test targets placed apart from the main target they test
- `should-not-separate-test-targets`: separate scope groups for test targets that test only one main target
- `should-exclude-vendor-directories`: `node_modules/`, `Pods/`, `vendor/` or `.build/` content counted as scope groups
- `should-note-shared-directories`: `core`, `common`, `shared` or `util` directories at a module root, and whether the findings note them
- `should-not-auto-split-shared-directories`: such directories split apart with no evidence beyond their name
