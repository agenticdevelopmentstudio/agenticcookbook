
- `should-pick-framework-from-targets-and-investment`: There is no single mandate.
- `must-not-call-wpf-dead`, `should-keep-wpf-and-modernize`: WPF is fully supported and still receives feature updates; .NET 9+ ships a **Fluent theme** giving a Windows 11 look with light/dark and accent-color support.
- `should-keep-winforms`: WinForms is also fully supported and actively invested in (async controls, dark mode).
- `must-not-claim-uwp-deprecated`, `should-treat-uwp-as-feature-frozen`: Per Microsoft's developer FAQ (revised 2026-05-28), UWP and WinUI for UWP are **NOT deprecated** — they receive bug, reliability, and security fixes — but most **new** features go to WinUI.
- `must-recommend-uwp-for-unsupported-targets`: The Windows App SDK does **not** support Xbox, Surface Hub, HoloLens, or IoT.
- `must-not-mix-winui-into-uwp`, `must-not-mix-winui2-with-winui3`: They are incompatible.
- `should-settle-framework-by-first-ui-module`, `should-settle-deployment-by-first-identity-feature`: Both are costly to change once code depends on them ([adc.principle.small-reversible-decisions](cookbook:4554e680-aca3-4bb2-bc99-1ac381c428b2)).
- `should-prefer-msix-when-uncertain`: Adding identity-gated features later is free, removing the identity assumption is not.
