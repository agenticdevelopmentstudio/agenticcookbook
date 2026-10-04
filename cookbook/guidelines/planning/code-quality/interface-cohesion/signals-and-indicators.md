
**Public and exported declarations to locate:**

- Swift `public` / `open` classes, structs, protocols, and typealiases. Pay special attention to protocol + extension pairs — the extension often lives in a separate file but is inseparable from the protocol definition.
- Kotlin `interface` declarations in the same package as their primary implementors. `sealed class` hierarchies — the sealed parent and all its subclasses form a single interface unit.
- TypeScript `export` statements at the top level, particularly in `index.ts` barrel files that re-export from multiple implementation files. The barrel and everything it re-exports constitute one interface surface.
- C# `interface` definitions paired with their `abstract class` base implementations. `partial class` declarations spread across files — all partials of the same class belong together.
- Java `interface` + `abstract class` + primary implementation triads are a common pattern; treat them as one unit.

**Shared type usage:**

- Types that appear in the parameter or return position of multiple files' public functions — these types are load-bearing for the interface and belong with it.
- DTOs, request/response models, and error types that are defined in one file and consumed across many — they define a shared contract.
- Protocol/interface conformance declarations: a file that declares `extension Foo: BarProtocol` is coupled to both `Foo` and `BarProtocol`.

**Co-export patterns:**

- Barrel files (`index.ts`, `__init__.py`, `Public.swift`) that gather exports from multiple files — the barrel signals that those files are intended to be consumed together.
- Umbrella headers in C/Objective-C that include multiple sub-headers — the umbrella defines the public interface boundary.
- Re-export declarations (`export { A } from './a'; export { B } from './b'`) that assemble a unified API from parts.

**Versioned interfaces:**

- Files with version suffixes (`AuthServiceV2.swift`, `PaymentApiV3.kt`) paired with adapter or migration shims — these are part of the same interface evolution and belong together.

