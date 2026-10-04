
Per `yagni` and `make-it-work-make-it-right-make-it-fast`, fuzzing is **adopted where a concrete attack surface justifies it**, not mandated repository-wide.

- You **SHOULD** fuzz any code that parses, decodes, or deserializes data crossing a trust boundary: file/media parsers, network protocol decoders, serialization formats, regex/template/expression evaluators, decompressors.
- You **SHOULD** prioritize fuzzing in memory-unsafe languages (C, C++, and `unsafe` Rust/Go FFI) where defects become memory-corruption vulnerabilities.
- You **SHOULD NOT** treat broad business/UI logic with no untrusted-input boundary as a default fuzzing target; prefer property-based testing (see `agenticdevelopercookbook://guidelines/testing/property-based-testing`) there.
- Targets **MUST** be deterministic for a given input (no clock/network/global-state dependence) so crashes reproduce.

