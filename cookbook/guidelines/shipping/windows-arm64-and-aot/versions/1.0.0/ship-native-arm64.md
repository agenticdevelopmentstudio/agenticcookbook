
- Apps targeting Windows on ARM **SHOULD** publish a native `win-arm64` build. An `AnyCPU` or `win-x64` binary runs only under x64 emulation, with measurably slower startup, sluggish UI, and higher power draw (see the ARM overview reference).
- Builds **MUST NOT** rely on x64 emulation as the shipping plan for ARM hardware when native ARM64 is achievable; emulation is a compatibility fallback, not a target.
- Distribution **SHOULD** ship multi-arch (both `win-x64` and `win-arm64`) so one artifact set covers all Windows hardware — MSIX bundles or per-RID installers selected by the host architecture.
- Every native dependency (C/C++ runtimes, P/Invoke targets, NuGet packages with native assets) **MUST** provide an ARM64 variant; a single x64-only native dependency forces the whole process into emulation. Audit `runtimes/` folders before shipping.
- Arm64EC **MAY** be used for incremental migration of a large native codebase, letting ARM64 and emulated x64 code coexist in one process while modules are ported. Mark this as a transitional state, not an end goal.

