
- Build with ARC (`-fobjc-arc`). Do not call `retain`, `release` or `autorelease` by hand in an ARC file, and do not mix manual reference counting into a target by file-level flags without a written reason.
- Declare object properties with an explicit ownership attribute: `strong` for owned objects, `weak` for back-references and delegates, `copy` for `NSString`, `NSArray`, `NSDictionary` and block properties whose mutable subclasses a caller could pass in.
- Ownership qualifiers on variables are `__strong` (the default), `__weak`, `__unsafe_unretained` and `__autoreleasing`. Reach for `__unsafe_unretained` only where the compiler cannot express the lifetime, and say why in a comment.
- Method families decide ownership of a returned object. A method whose name begins with `alloc`, `new`, `copy` or `mutableCopy` returns a retained object that the caller owns; any other name returns an object the caller does not own. Name your own methods with that rule in mind, because ARC applies it to them too.
- Break retain cycles in blocks. A block that captures `self` and is stored on `self` MUST capture a `__weak` reference and, inside the block, take a `__strong` local before use.
- Wrap long-running loops that create many temporary objects in `@autoreleasepool { }` so memory does not grow until the loop ends.

