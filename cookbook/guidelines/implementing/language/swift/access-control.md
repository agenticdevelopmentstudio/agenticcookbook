
- The default is `internal`. State the narrowest level that works: `private` for the enclosing declaration and its same-file extensions, `fileprivate` for the file, `internal` for the module, `package` for the Swift package, `public` for use outside the module, and `open` only for classes designed for outside subclassing and overriding.
- No declaration may expose a type with a more restrictive level than its own.
- The members of a `public` type are `internal` unless marked. Mark each member that belongs to the interface and nothing else, because the public surface of a framework is an API you must keep.

