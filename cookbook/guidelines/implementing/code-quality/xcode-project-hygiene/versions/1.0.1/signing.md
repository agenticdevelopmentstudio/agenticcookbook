
- Put the team ID and signing style in the xcconfig. Use automatic signing for local development and an explicit, documented identity for release builds.
- Never check in a certificate, a private key or a provisioning profile. CI supplies them from its secret store.

