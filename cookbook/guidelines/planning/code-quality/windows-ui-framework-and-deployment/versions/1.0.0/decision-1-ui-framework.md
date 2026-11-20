
Pick the framework from target devices and existing investment, not from hype. There is no single mandate.

- **New, Windows-only desktop app**: agents **SHOULD** default to **WinUI 3** on the **Windows App SDK** (Microsoft's current recommendation for new native apps, runs down to Windows 10 1809). Build with **Visual Studio + MSBuild** — the only officially supported toolchain.
- **Existing WPF app**: **MUST NOT** be told it is dead. WPF is fully supported and still receives feature updates; .NET 9+ ships a **Fluent theme** giving a Windows 11 look with light/dark and accent-color support. Keep WPF and modernize in place unless there is a concrete reason to move.
- **Existing WinForms app**: also fully supported and actively invested in (async controls, dark mode). Stay unless a concrete need forces a change.
- **Existing UWP app**: agents **MUST NOT** claim "UWP is deprecated, port to WinUI now." Per Microsoft's developer FAQ (revised 2026-05-28), UWP and WinUI for UWP are **NOT deprecated** — they receive bug, reliability, and security fixes — but most **new** features go to WinUI. Treat UWP as feature-frozen, not abandoned.
- **Cross-platform native**: consider **.NET MAUI** (produces a WinUI app on Windows) or **React Native for Desktop**. You **MUST** start with these if multi-platform is a real near-term goal — you cannot start in WinUI and add MAUI later.

### UWP is still the recommended choice for some targets

- Agents **MUST** recommend **UWP** when the target is **Xbox, Surface Hub, HoloLens, or IoT** — the Windows App SDK does **not** support these platforms.
- For **game development**, agents **SHOULD** recommend the **Microsoft Game Development Kit (GDK)**, not UWP or WinUI.
- WinUI/Windows App SDK content **MUST NOT** be mixed into a UWP app, and WinUI for UWP (formerly WinUI 2) **MUST NOT** be mixed with WinUI 3 — they are incompatible.

