
Each independently declared build target or package is a primary scope group candidate. Apply these rules:

1. **One target, one candidate.** If the build system declares it separately, treat it as a candidate scope group regardless of size. A 3-file Swift target is still a distinct module.
2. **Merge trivial wrappers.** If a target contains only re-exports of another target with no logic of its own, it may belong with the target it wraps.
3. **Split large monolithic targets.** A single build target containing 200+ files likely conflates multiple concerns. Flag for secondary analysis using `interface-cohesion` and `dependency-clusters` lenses.
4. **Test targets follow their main target.** `AuthTests` belongs with `Auth` — do not create a separate scope group for test targets unless they test multiple main targets.
5. **Vendor/third-party directories are excluded.** `node_modules/`, `Pods/`, `vendor/`, `.build/` — these are external dependencies, not scope groups.

