
1. **Heavy OS framework usage marks a boundary.** Files that import three or more OS-specific frameworks are tightly coupled to the platform runtime and likely belong in a platform-specific scope group.
2. **Hardware APIs are natural boundaries.** Camera, GPS, Bluetooth, and biometric code has distinct permission requirements and testing needs — group these files together and mark the scope group as hardware-dependent.
3. **Network and persistence are separate concerns.** Files that talk to the network and files that write to local storage are often conflated — separate them unless they are part of a unified data synchronization layer.
4. **Third-party SDK boundaries.** If a third-party SDK is touched by more than 2–3 files, those files likely form a wrapper/adapter scope group that isolates the SDK from the rest of the codebase. Identify this group explicitly.
5. **System dependencies that appear in many groups are cross-cutting.** Logging frameworks and analytics SDKs that appear across all candidate groups are not boundaries — they are cross-cutting concerns (see `cross-cutting-detection`).

