
- Declare only required capabilities in `Package.appxmanifest` — avoid `broadFileSystemAccess` unless essential
- Use DPAPI for local secret storage (see secure-storage.md)
- No PII in logs, even at debug level
- Respect user consent: app must remain functional if optional data collection is denied

