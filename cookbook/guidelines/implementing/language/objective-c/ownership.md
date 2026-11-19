
- Every object property has an explicit `strong`, `weak` or `copy` attribute. Flag `assign` on an object property.
- `NSString`, collection and block properties that a caller could hand a mutable value to are `copy`.
- Delegates and back-references are `weak`.
- No manual `retain`, `release` or `autorelease` in an ARC file, and no per-file `-fno-objc-arc` without a written reason.
- A name starting with `alloc`, `new`, `copy` or `mutableCopy` is only used for methods that return an owned object.

