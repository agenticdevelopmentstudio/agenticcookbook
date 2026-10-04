
- **Platform authenticators** (Face ID, Windows Hello) vs **roaming authenticators** (FIDO2 security keys via USB/NFC/BLE).
- **Synced passkeys** replicate via a provider (iCloud Keychain, Google Password Manager); convenient, recover across devices. **Device-bound passkeys** never leave one device; highest assurance.
- For most users, synced passkeys **SHOULD** be the default. For admin/high-privilege accounts, a **device-bound** authenticator (security key) **SHOULD** be required.
- Users **SHOULD** be encouraged to register **at least two** authenticators so loss of one does not lock them out.

