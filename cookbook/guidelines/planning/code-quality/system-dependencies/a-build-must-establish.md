
- `should-place-heavy-os-framework-users-in-platform-group`: every file importing three or more OS-specific frameworks sits in a platform-specific candidate, or the findings say why not
- `should-group-hardware-api-code`: every hardware API in the findings has its files in one candidate, or the findings say why not
- `should-mark-hardware-dependent-groups`: every hardware API candidate is marked hardware-dependent
- `should-separate-network-and-persistence`: no candidate mixes network and local-storage files unless it is a unified data synchronization layer
- `should-identify-sdk-wrapper-groups`: every third-party SDK used in more than 2–3 files has its wrapper/adapter group named in the candidates
- `should-not-treat-widespread-dependencies-as-boundaries`: every dependency appearing across the candidate groups is listed under cross-cutting system dependencies and drives no boundary
