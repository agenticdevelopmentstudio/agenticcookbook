
- Every public header MUST wrap its declarations in `NS_ASSUME_NONNULL_BEGIN` and `NS_ASSUME_NONNULL_END`, and mark only the exceptions `nullable`. Unannotated declarations inside the region are treated as non-null.
- Use `nullable`, `nonnull` and `null_resettable` on properties, parameters and return types; use `_Nullable` and `_Nonnull` where the simple forms do not fit, such as `_Nullable id * _Nonnull`.
- Without any annotation Swift imports a type as an implicitly unwrapped optional, which hides crashes. `typedef` types are not assumed non-null even inside an audited region, so annotate each use.
- A method documented to return `nil` on failure MUST be declared `nullable`, and a method that must never receive `nil` MUST say so in its signature, not only in a comment.

