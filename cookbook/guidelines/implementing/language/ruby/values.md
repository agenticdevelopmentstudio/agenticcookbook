
- Model records as `Data.define(:name, :path)`. A `Data` instance is immutable, requires every member, and is copied with changes through `with`. Use `Struct` only when you need mutation.
- Return `to_h` when you need to serialize.

