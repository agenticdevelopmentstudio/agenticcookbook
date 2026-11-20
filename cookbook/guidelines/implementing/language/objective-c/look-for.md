
Review changed Objective-C against the rules above. Read the header and the implementation together.

- `should-declare-explicit-property-ownership`: Every object property has an explicit `strong`, `weak` or `copy` attribute. Flag `assign` on an object property.
- `should-declare-explicit-property-ownership`: `NSString`, collection and block properties that a caller could hand a mutable value to are `copy`.
- `should-declare-explicit-property-ownership`: Delegates and back-references are `weak`.
- `should-not-call-retain-release-by-hand`, `should-not-mix-manual-reference-counting`: No manual `retain`, `release` or `autorelease` in an ARC file, and no per-file `-fno-objc-arc` without a written reason.
- `should-name-methods-by-method-family`: A name starting with `alloc`, `new`, `copy` or `mutableCopy` is only used for methods that return an owned object.
- `must-capture-weak-self-in-stored-blocks`, `should-break-retain-cycles-in-blocks`: A block stored on `self` that mentions `self` (directly, or through an ivar) captures a weak reference, and uses a strong local inside.
- `should-remove-observers-at-teardown`: Timers, notification observers and KVO registrations are removed in `dealloc` or an earlier teardown, and do not keep their target alive.
- `must-state-bridge-cast-ownership`, `should-pick-bridge-cast-by-ownership`, `must-not-use-bare-bridging-casts`: Every Objective-C and Core Foundation cast says who owns the result: `__bridge`, `__bridge_retained` or `__bridge_transfer`. Check that every `__bridge_retained` has a matching `CFRelease`, and that no object is released twice.
- `must-wrap-public-headers-in-assume-nonnull`, `must-declare-nullability-in-public-headers`: Each public header has `NS_ASSUME_NONNULL_BEGIN` and `NS_ASSUME_NONNULL_END`.
- `must-declare-nil-returning-methods-nullable`: Anything that can be `nil` is marked `nullable`, and the implementation actually returns `nil` there.
- `should-annotate-each-typedef-use`: Typedef'd pointers inside the audited region carry their own annotation.
- `should-use-nullability-qualifiers`: No new unannotated public declaration, which Swift would import as an implicitly unwrapped optional.
- `should-need-no-swift-fix-ups`, `should-refine-for-swift-in-an-extension`, `should-keep-objective-c-as-single-source`: Collections carry generics. A refined API uses `NS_REFINED_FOR_SWIFT` and the Swift-side wrapper calls the original instead of copying its logic.
- `should-mark-designated-initializers`: Designated initializers are marked, and unusable inherited ones are `NS_UNAVAILABLE`.
- `should-report-recoverable-failure-with-nserror`, `should-prefix-public-symbols`: Recoverable failure uses `NSError **`, not an exception. Public symbols carry the project prefix.
- `must-compile-with-arc`: the target builds with `-fobjc-arc`; a file compiled without ARC is a finding.
- `must-shape-for-swift-import`: the header, read as Swift would import it, gives idiomatic Swift: no implicitly unwrapped optionals, typed collections, refined signatures where the Objective-C shape is awkward.
- `should-not-write-new-objective-c`: a new Objective-C file where Swift would do, outside an existing module, a C++ interop shim or a framework with an Objective-C public surface.
- `must-declare-non-nil-parameters-in-signature`: a parameter that must never be `nil` is non-null in its signature, not only in a comment.
- `should-limit-unsafe-unretained`: each `__unsafe_unretained` sits where the compiler cannot express the lifetime, with a comment saying why.
- `should-wrap-temporary-heavy-loops-in-autoreleasepool`: a long-running loop that creates many temporary objects runs inside `@autoreleasepool { }`.
- `should-name-call-sites-as-phrases`, `should-follow-framework-conventions`: a call site reads as a phrase, every argument after the first is labelled, and the names follow the framework the code extends.
