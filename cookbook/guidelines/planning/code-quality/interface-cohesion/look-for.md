
- `should-group-protocol-with-primary-implementation`: a protocol or interface and its primary concrete implementation placed in different groups, when the implementation is under 50 files
- `should-treat-barrel-reexports-as-one-candidate`: a barrel (`index.ts`, `__init__.py`, `Public.swift`) re-exporting from several subdirectories, and whether those subdirectories were considered as one candidate
- `should-place-shared-types-with-primary-consumer`: shared types grouped by where they are defined rather than with the module that mainly uses them
- `should-note-fragmented-interfaces`: one logical interface declared across three or more files with no barrel, and whether it is listed as a cohesion anomaly
- `should-not-count-internal-helpers-as-interface`: private, internal or file-private symbols counted as part of an interface surface
- `should-attend-to-protocol-extension-pairs`: Swift protocol + extension pairs split across files, and whether they are kept with the protocol
- `should-treat-java-interface-triads-as-one-unit`: Java interface + abstract class + primary implementation triads split across groups
- `should-place-shared-types-with-primary-consumer`: Trace shared types to their consumers.
