
- `should-introduce-value-object-when-criteria-met`: each value object the build adds wraps a primitive that meets a stated criterion, and each such primitive the build handles is wrapped, or the build says why not
- `must-validate-at-construction`: constructing each value object from invalid input fails at construction
- `should-be-immutable-with-value-equality`: each value object the build adds has no mutating member and two with the same contents compare equal, or the build says why not
- `should-keep-value-object-small-and-focused`: each value object the build adds holds only its single concept, or the build says why not
