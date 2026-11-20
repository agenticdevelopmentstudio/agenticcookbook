
- Authenticator protocol is **FIDO CTAP 2.x**; security keys speak CTAP, platform authenticators are reached via the OS (Android Credential Manager, iOS/macOS AutoFill, Windows Hello).
- **Platform authenticators** (Face ID, Windows Hello) vs **roaming authenticators** (FIDO2 security keys via USB/NFC/BLE).
- **Synced passkeys** replicate via a provider (iCloud Keychain, Google Password Manager); convenient, recover across devices. **Device-bound passkeys** never leave one device; highest assurance.
