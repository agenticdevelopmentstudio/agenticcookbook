
- `should-place-heavy-os-framework-users-in-platform-group`: Files that import three or more OS-specific frameworks are tightly coupled to the platform runtime.
- `should-group-hardware-api-code`, `should-mark-hardware-dependent-groups`: Camera, GPS, Bluetooth, and biometric code has distinct permission requirements and testing needs.
- `should-separate-network-and-persistence`: Files that talk to the network and files that write to local storage are often conflated.
