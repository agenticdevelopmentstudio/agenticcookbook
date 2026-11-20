
- Records SHOULD be modeled as `Data.define(:name, :path)`. A `Data` instance is immutable, requires every member, and is copied with changes through `with`. Code SHOULD use `Struct` only when it needs mutation.
- Code SHOULD return `to_h` when it needs to serialize.

