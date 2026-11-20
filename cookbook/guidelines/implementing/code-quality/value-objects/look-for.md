
- `should-introduce-value-object-when-criteria-met`: a bare primitive that carries invariants, is validated in more than one place, or is easily confused with a same-shaped primitive; or a value object wrapping a primitive that meets none of these
- `must-validate-at-construction`: a value object that can be constructed invalid, or whose validation runs after construction or outside it
- `should-be-immutable-with-value-equality`: a value object with mutable state, or compared by identity rather than by contents
- `should-keep-value-object-small-and-focused`: a value object that carries more than the single concept it represents
