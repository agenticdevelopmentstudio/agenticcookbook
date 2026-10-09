
- A property that applies to every project is in `Directory.Build.props`, not repeated in each project.
- The `Directory.Build.props` file name has exact casing.
- CI sets `ContinuousIntegrationBuild`. Output folders use `BaseOutputPath`, not `OutDir`.

