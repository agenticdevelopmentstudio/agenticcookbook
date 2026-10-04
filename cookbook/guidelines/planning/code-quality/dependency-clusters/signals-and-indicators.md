
**Import statement forms by platform:**

- Swift: `import ModuleName` at file top; `@_implementationOnly import` for private dependencies; within a module, `import class ModuleName.TypeName` for targeted imports
- Kotlin: `import com.example.package.ClassName` statements; star imports (`import com.example.package.*`) suggest tight coupling to an entire package
- TypeScript/JavaScript: `import { A, B } from './relative/path'` for internal; `import { C } from 'npm-package'` for external. Relative paths (starting with `./` or `../`) are internal; bare specifiers are external.
- C#: `using Namespace.Sub;` directives — internal vs external determined by namespace prefix matching the project's root namespace
- Java: `import com.example.*` — internal vs external by package prefix
- C/C++: `#include "local.h"` (quoted — local/internal) vs `#include <system.h>` (angle bracket — system/external)
- Go: import paths — module-local paths share the module prefix from `go.mod`; external paths reference a different module

**Coupling metrics to compute:**

- **Internal coupling:** count of import relationships between files within a candidate group
- **External coupling:** count of import relationships from files in the candidate group to files outside it
- **Coupling ratio:** internal / (internal + external). Ratios above 0.6 indicate a cohesive cluster; below 0.3 indicates a loosely coupled file that may not belong.
- **Fan-in:** number of files that import a given file — high fan-in files are likely shared infrastructure or cross-cutting concerns (see `cross-cutting-detection`)
- **Fan-out:** number of files a given file imports — high fan-out files are often orchestrators or aggregators

**Dependency direction:**

- Identify the direction of dependencies: do files in directory A import files in directory B, or vice versa? Unidirectional dependency flows suggest a layered architecture where the two directories belong in separate scope groups.
- Bidirectional dependencies (A imports B and B imports A) indicate either tight cohesion (same scope group) or a design problem (circular dependency that should be resolved).

**Circular dependencies:**

- Note any import cycles — these are candidates for refactoring, but in the short term they force the cyclic files into the same scope group since they cannot be independently deployed.

