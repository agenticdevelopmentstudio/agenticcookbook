
- `should-use-single-project-msix`: the package is built with the single-project MSIX model, or the project says why not
- `must-declare-capabilities-minimally`: `Package.appxmanifest` lists only capabilities the app uses
- `must-sign-with-trusted-certificate`: the built package is signed with a trusted certificate
- `must-use-four-part-monotonic-version`: the package version is `Major.Minor.Build.Revision` and exceeds every earlier release's
