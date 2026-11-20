
- `should-use-single-project-msix`: the app is packaged from its own project with the single-project MSIX model, not a separate packaging project
- `must-declare-capabilities-minimally`: every capability in `Package.appxmanifest` is one the app uses; an unused capability breaks it
- `must-sign-with-trusted-certificate`: the signing step uses a certificate trusted on the sideloading machines
- `must-use-four-part-monotonic-version`: the package version has four parts (`Major.Minor.Build.Revision`) and is higher than the last release
