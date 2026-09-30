<!-- leaf: ship-general/windows-arm64-and-aot · source: guidelines/shipping/windows-arm64-and-aot.md -->

**Rules** (cite as `ship-general/windows-arm64-and-aot#<slug>`):

- `targeting-windows-arm-publish-native-win-arm64` SHOULD — Apps targeting Windows on ARM SHOULD publish a native win-arm64 build. An AnyCPU or win-x64 binary runs only under x64 …
- `builds-not-rely-x64-emulation-shipping` MUST — Builds MUST NOT rely on x64 emulation as the shipping plan for ARM hardware when native ARM64 is achievable; emulation …
- `distribution-ship-multi-arch-both` SHOULD — Distribution SHOULD ship multi-arch (both win-x64 and win-arm64) so one artifact set covers all Windows hardware — MSIX …
- `packages-native-assets-provide-arm64-variant-single` MUST — Every native dependency (C/C++ runtimes, P/Invoke targets, NuGet packages with native assets) MUST provide an ARM64 …
- `arm64ec-used-incremental-migration-large` MAY — Arm64EC MAY be used for incremental migration of a large native codebase, letting ARM64 and emulated x64 code coexist …
- `teams-not-enable-native-aot-aggressive` SHOULD — Teams SHOULD NOT enable Native AOT or aggressive trimming by default. First make it work and correct; introduce these …
- `before-enabling-team-record-baseline-metric-being` MUST — Before enabling, the team MUST record the baseline metric being improved (e.g., cold-start ms, package MB) and …
- `dynamic-codegen-paths-verified-trimming-aot-remove` MUST — Reflection-heavy and dynamic-codegen paths MUST be verified: trimming and AOT remove unreferenced code and forbid …
- `winrt-cswinrt-interop-checked-aot-trim-safety` MUST — WinRT/CsWinRT interop MUST be checked for AOT/trim safety. CsWinRT supplies source-generated vtables and AOT-safe …
- `third-party-dependency-confirmed-trim-compatible-annotated` MUST — Each third-party dependency MUST be confirmed trim-compatible (annotated with IsTrimmable/feature switches). Trim …
- `readytorun-r2r-lower-risk-middle-ground` MAY — ReadyToRun (R2R) MAY be a lower-risk middle ground when only startup matters: it pre-JITs without AOT's full trimming …
- `aot-trimming-builds-tested-per-rid-including` MUST — AOT/trimming builds MUST be tested per-RID, including win-arm64, in CI — a build that passes trim analysis on x64 can …

# Windows ARM64 and Native AOT

Windows on ARM runs unmodified x64 apps under emulation, but a native ARM64 build starts faster, runs more responsively, and uses less battery. Ship native ARM64 and package multi-arch. Treat Native AOT and trimming as optimizations gated on a concrete, measured need — not as defaults.

## Ship native ARM64

- Apps targeting Windows on ARM **SHOULD** publish a native `win-arm64` build. An `AnyCPU` or `win-x64` binary runs only under x64 emulation, with measurably slower startup, sluggish UI, and higher power draw (see the ARM overview reference).
- Builds **MUST NOT** rely on x64 emulation as the shipping plan for ARM hardware when native ARM64 is achievable; emulation is a compatibility fallback, not a target.
- Distribution **SHOULD** ship multi-arch (both `win-x64` and `win-arm64`) so one artifact set covers all Windows hardware — MSIX bundles or per-RID installers selected by the host architecture.
- Every native dependency (C/C++ runtimes, P/Invoke targets, NuGet packages with native assets) **MUST** provide an ARM64 variant; a single x64-only native dependency forces the whole process into emulation. Audit `runtimes/` folders before shipping.
- Arm64EC **MAY** be used for incremental migration of a large native codebase, letting ARM64 and emulated x64 code coexist in one process while modules are ported. Mark this as a transitional state, not an end goal.

## Native AOT and trimming (MEASURED-NEED)

Per make-it-work-make-it-right-make-it-fast and YAGNI, AOT and trimming are last-mile optimizations. Adopt them ONLY when a concrete measurement justifies the added constraints (faster cold start, smaller download, no-runtime self-contained deploy).

- Teams **SHOULD NOT** enable Native AOT or aggressive trimming by default. First make it work and correct; introduce these only after profiling shows startup, size, or deployment is a real bottleneck.
- Before enabling, the team **MUST** record the baseline metric being improved (e.g., cold-start ms, package MB) and re-measure after, so the constraint is paid for by a demonstrated gain.
- Reflection-heavy and dynamic-codegen paths **MUST** be verified: trimming and AOT remove unreferenced code and forbid runtime IL generation, breaking unguarded reflection, runtime serializers, and expression compilation. Use source generators or AOT-safe APIs instead.
- WinRT/CsWinRT interop **MUST** be checked for AOT/trim safety. CsWinRT supplies source-generated vtables and AOT-safe binding (e.g. the `WinRT.GeneratedBindableCustomProperty` attribute) — but every dependent library that touches WinRT interop **MUST** itself be built against an AOT-aware CsWinRT version, or the app is not AOT-compatible (see CsWinRT `aot-trimming.md`).
- Each third-party dependency **MUST** be confirmed trim-compatible (annotated with `IsTrimmable`/feature switches). Trim warnings **MUST NOT** be suppressed blindly; an unverified library can be silently trimmed and fail only at runtime.
- ReadyToRun (R2R) **MAY** be a lower-risk middle ground when only startup matters: it pre-JITs without AOT's full trimming constraints. Prefer it when the measured need is startup latency alone.
- AOT/trimming builds **MUST** be tested per-RID, including `win-arm64`, in CI — a build that passes trim analysis on x64 can still fail at runtime on ARM64.

## FORECAST

ARM64 tooling, CsWinRT AOT coverage, and WinUI/UWP-on-.NET AOT support evolve release-over-release. Pin to the .NET and CsWinRT versions you build against and re-verify AOT/trim compatibility on each upgrade rather than assuming prior results hold.
