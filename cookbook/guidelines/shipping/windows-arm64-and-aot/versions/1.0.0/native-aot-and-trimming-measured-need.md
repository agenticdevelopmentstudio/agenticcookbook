
Per make-it-work-make-it-right-make-it-fast and YAGNI, AOT and trimming are last-mile optimizations. Adopt them ONLY when a concrete measurement justifies the added constraints (faster cold start, smaller download, no-runtime self-contained deploy).

- Teams **SHOULD NOT** enable Native AOT or aggressive trimming by default. First make it work and correct; introduce these only after profiling shows startup, size, or deployment is a real bottleneck.
- Before enabling, the team **MUST** record the baseline metric being improved (e.g., cold-start ms, package MB) and re-measure after, so the constraint is paid for by a demonstrated gain.
- Reflection-heavy and dynamic-codegen paths **MUST** be verified: trimming and AOT remove unreferenced code and forbid runtime IL generation, breaking unguarded reflection, runtime serializers, and expression compilation. Use source generators or AOT-safe APIs instead.
- WinRT/CsWinRT interop **MUST** be checked for AOT/trim safety. CsWinRT supplies source-generated vtables and AOT-safe binding (e.g. the `WinRT.GeneratedBindableCustomProperty` attribute) — but every dependent library that touches WinRT interop **MUST** itself be built against an AOT-aware CsWinRT version, or the app is not AOT-compatible (see CsWinRT `aot-trimming.md`).
- Each third-party dependency **MUST** be confirmed trim-compatible (annotated with `IsTrimmable`/feature switches). Trim warnings **MUST NOT** be suppressed blindly; an unverified library can be silently trimmed and fail only at runtime.
- ReadyToRun (R2R) **MAY** be a lower-risk middle ground when only startup matters: it pre-JITs without AOT's full trimming constraints. Prefer it when the measured need is startup latency alone.
- AOT/trimming builds **MUST** be tested per-RID, including `win-arm64`, in CI — a build that passes trim analysis on x64 can still fail at runtime on ARM64.

