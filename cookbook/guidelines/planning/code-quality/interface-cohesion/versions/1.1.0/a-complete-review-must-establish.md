
- `should-group-protocol-with-primary-implementation`: whether each protocol sits in the same group as its primary implementation, unless that implementation is 50+ files
- `should-treat-barrel-reexports-as-one-candidate`: whether the subdirectories a barrel re-exports from were treated as one candidate, unless large enough for separate groups sharing an API layer
- `should-place-shared-types-with-primary-consumer`: whether shared types are placed with their primary consumer
- `should-note-fragmented-interfaces`: whether every fragmented interface is noted as a cohesion anomaly
- `should-not-count-internal-helpers-as-interface`: whether internal helpers were kept out of the interface analysis
- `should-attend-to-protocol-extension-pairs`: whether Swift protocol + extension pairs were examined
- `should-treat-java-interface-triads-as-one-unit`: whether Java interface triads were treated as one unit
