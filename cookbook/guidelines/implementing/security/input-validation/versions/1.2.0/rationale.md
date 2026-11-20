
- `must-not-trust-client-input`, `must-duplicate-validation-server-side`: Client-side validation is UX, not security. Client-side validation is a UX feature, not a security control.
- `should-prefer-allowlists-over-denylists`: Denylists have gaps.
- `must-validate-at-deserialization-boundary`, `must-not-embed-secrets-in-server-rendered-output`, `should-rate-limit-server-render-endpoints`, `must-pin-patched-framework-version`: Server-side rendering and server-invoked functions create a deserialization boundary where
client-controlled input is reconstructed and executed in a trusted context. The framework's
serialization layer is not a validation layer.
