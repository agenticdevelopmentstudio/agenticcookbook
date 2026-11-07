
- Projects SHOULD turn on central versions with a `Directory.Packages.props` at the root containing `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>` and one `<PackageVersion Include="..." Version="..." />` per package. Project files then use `<PackageReference Include="..." />` with no `Version`.
- Only the nearest `Directory.Packages.props` applies. A nested one MUST import its parent explicitly with `GetPathOfFileAbove`.
- `VersionOverride` on one reference MUST be used only for a documented exception, and a project MAY set `CentralPackageVersionOverrideEnabled` to `false` to forbid it. `CentralPackageTransitivePinningEnabled` pins transitive versions, and `GlobalPackageReference` adds a package (an analyzer, for example) to every project.

