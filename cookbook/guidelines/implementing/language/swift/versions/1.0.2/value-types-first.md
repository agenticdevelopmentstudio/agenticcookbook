
- Code SHOULD start with a `struct` (or `enum`) and move to a `class` only when it needs a class feature. Apple's guidance is to choose structures by default.
- Code SHOULD use a class for identity (compare with `===`, one shared mutable instance such as a file handle, a connection or a hardware intermediary), for Objective-C interoperability, or for inheritance from a framework class you are expected to subclass.
- Value semantics keep a change local: a copy changed in one place is not visible elsewhere unless the code passes it back. Code SHOULD prefer `let` and immutable properties, and add `var` where mutation is the point.
- Code SHOULD share behavior across structures with protocols and protocol extensions, not with class inheritance.
- Classes SHOULD be marked `final` unless a subclass is part of the design.

