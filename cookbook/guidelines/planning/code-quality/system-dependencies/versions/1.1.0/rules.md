
- **should-place-heavy-os-framework-users-in-platform-group**: Files that import three or more OS-specific frameworks **SHOULD** typically be placed in a platform-specific scope group — heavy OS framework usage marks a boundary.
- **should-group-hardware-api-code**: Camera, GPS, Bluetooth, and biometric code files **SHOULD** be grouped together — hardware APIs are natural boundaries.
- **should-mark-hardware-dependent-groups**: The analysis **SHOULD** mark a scope group of hardware API code as hardware-dependent.
- **should-separate-network-and-persistence**: Files that talk to the network and files that write to local storage **SHOULD** be separated unless they are part of a unified data synchronization layer — network and persistence are separate concerns.
- **should-identify-sdk-wrapper-groups**: If a third-party SDK is touched by more than 2–3 files, those files likely form a wrapper/adapter scope group that isolates the SDK from the rest of the codebase, and the analysis **SHOULD** identify this group explicitly — third-party SDK boundaries.
- **should-not-treat-widespread-dependencies-as-boundaries**: Logging frameworks and analytics SDKs that appear across all candidate groups **SHOULD NOT** be treated as boundaries — they are cross-cutting concerns (see `cross-cutting-detection`); system dependencies that appear in many groups are cross-cutting.
