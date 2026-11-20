
- `should-treat-each-declared-target-as-candidate`: A 3-file Swift target is still a distinct module.
- `should-flag-large-monolithic-targets`: A single build target containing 200+ files likely conflates multiple concerns.
- `should-treat-each-declared-target-as-candidate`, `may-merge-trivial-wrappers`, `should-flag-large-monolithic-targets`, `should-group-test-targets-with-main-target`, `should-not-separate-test-targets`, `should-exclude-vendor-directories`: these are the rules to apply to the declared build targets and packages, each of which starts as a primary scope group candidate.
