
- `should-treat-each-declared-target-as-candidate`: every declared module in the manifests appears among the declared modules and candidates, or the findings say why not
- `may-merge-trivial-wrappers`: every merged wrapper target is shown to hold only re-exports of the target it joins
- `should-flag-large-monolithic-targets`: every target with 200+ files is listed under anomalies for `interface-cohesion` and `dependency-clusters` analysis
- `should-group-test-targets-with-main-target`: every test target sits with its main target, or the findings say why not
- `should-not-separate-test-targets`: no test target is its own candidate unless it tests multiple main targets
- `should-exclude-vendor-directories`: no vendor or third-party directory appears among the candidates
- `should-note-shared-directories`: every `core`, `common`, `shared` or `util` directory at a module root is named in the findings
- `should-not-auto-split-shared-directories`: no such directory is split without stated evidence
