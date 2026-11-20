
- `should-introduce-value-object-when-criteria-met`: every primitive that meets a criterion is wrapped and none that meets no criterion is, or the code says why not
- `must-validate-at-construction`: every value object rejects invalid input at construction, so each constructed instance is known-valid
- `should-be-immutable-with-value-equality`: every value object is immutable and equal by value, or the code says why not
- `should-keep-value-object-small-and-focused`: every value object is small and represents a single concept, or the code says why not
