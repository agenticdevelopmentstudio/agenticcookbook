
- Every Objective-C and Core Foundation cast says who owns the result: `__bridge`, `__bridge_retained` or `__bridge_transfer`. Check that every `__bridge_retained` has a matching `CFRelease`, and that no object is released twice.

