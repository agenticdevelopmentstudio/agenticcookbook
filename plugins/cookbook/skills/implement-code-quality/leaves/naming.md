<!-- leaf: implement-code-quality/naming · source: guidelines/implementing/code-quality/naming.md -->

**Rules** (cite as `implement-code-quality/naming#<slug>`):

- `fields-constants-namespaces-use-pascalcase` MUST — Types, methods, properties, public fields, constants, namespaces MUST use PascalCase
- `parameters-local-variables-use-camelcase` MUST — Parameters and local variables MUST use camelCase
- `private-instance-fields-use-camelcase-underscore-prefix` MUST — Private instance fields MUST use _camelCase (underscore prefix)
- `async-methods-have-async-suffix-saveasync` MUST — Async methods MUST have the Async suffix (e.g., SaveAsync)
- `constants-use-pascalcase-screaming-snake` MUST — Constants MUST use PascalCase, not SCREAMING_SNAKE_CASE

# Naming

Use .NET's established casing conventions consistently: `PascalCase` for public symbols, `camelCase` for locals, and `_camelCase` for private fields.

- Types, methods, properties, public fields, constants, namespaces MUST use `PascalCase`
- Parameters and local variables MUST use `camelCase`
- Private instance fields MUST use `_camelCase` (underscore prefix)
- `I` prefix for interfaces (e.g., `IDisposable`)
- Async methods MUST have the `Async` suffix (e.g., `SaveAsync`)
- Constants MUST use `PascalCase`, not `SCREAMING_SNAKE_CASE`
- Use `var` when the type is apparent from the right side of the assignment
