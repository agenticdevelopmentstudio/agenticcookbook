
- Each public header has `NS_ASSUME_NONNULL_BEGIN` and `NS_ASSUME_NONNULL_END`.
- Anything that can be `nil` is marked `nullable`, and the implementation actually returns `nil` there.
- Typedef'd pointers inside the audited region carry their own annotation.
- No new unannotated public declaration, which Swift would import as an implicitly unwrapped optional.

