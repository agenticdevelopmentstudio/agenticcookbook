
- Where the repository already uses XcodeGen (a `project.yml` spec), treat the spec as the source and the generated `.xcodeproj` as an output: regenerate it, do not hand-edit it, and either ignore it in version control or verify in CI that it matches the spec.
- XcodeGen's spec points targets at xcconfig files through its `configFiles` option and at settings through its `settings` key; keep real values in the xcconfig and use the spec for structure.
- Do not introduce a generator into a repository that has none as part of an unrelated change.

