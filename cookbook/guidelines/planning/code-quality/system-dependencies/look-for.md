
- `should-place-heavy-os-framework-users-in-platform-group`: files importing three or more OS-specific frameworks placed outside a platform-specific group
- `should-group-hardware-api-code`: camera, GPS, Bluetooth or biometric code spread across groups
- `should-mark-hardware-dependent-groups`: groups of hardware API code not marked hardware-dependent
- `should-separate-network-and-persistence`: network and local-storage files sharing a group that is not a unified data synchronization layer
- `should-identify-sdk-wrapper-groups`: third-party SDKs touched by more than 2–3 files with no wrapper/adapter group named
- `should-not-treat-widespread-dependencies-as-boundaries`: logging frameworks or analytics SDKs present in every group used as a boundary
- `should-identify-introduced-system-dependencies`: Identify OS framework imports, SDK usage, system service calls (keychain, filesystem, network), hardware APIs (camera, GPS, bluetooth), and third-party library dependencies **introduced or changed by this diff**, mapping each to the code unit that uses it.
- `must-scope-system-dependencies-to-the-change`: a dependency inventory that covers the whole codebase rather than the change under review
