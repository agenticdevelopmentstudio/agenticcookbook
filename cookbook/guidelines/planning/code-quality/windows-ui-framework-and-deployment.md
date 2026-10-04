---
id: 2fd49a5f-4be1-4b0d-b2e7-41cbcbab66ee
title: "Choosing a Windows UI framework and deployment model"
domain: agenticdevelopercookbook://guidelines/planning/code-quality/windows-ui-framework-and-deployment
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Decide a Windows UI framework and deployment model deliberately and early; package identity is mandatory for notifications and background tasks."
platforms:
  - windows
  - csharp
tags:
  - windows
  - architecture
  - packaging
depends-on: []
related:
  - agenticdevelopercookbook://principles/small-reversible-decisions
  - agenticdevelopercookbook://principles/explicit-over-implicit
references:
  - https://learn.microsoft.com/en-us/windows/apps/get-started/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - new-module
  - configuration
---

# Choosing a Windows UI framework and deployment model

Two high-altitude, hard-to-reverse Windows decisions are often made implicitly: which UI framework to build on, and which deployment model to ship. Make both explicitly and early — they shape API access, distribution, and migration cost for the life of the app.

## Decision 1: UI framework

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

## Decision 2: Deployment model

The deployment model determines whether the app has **package identity**, which gates a large set of Windows APIs.

| Model | Package identity | Use when |
|-------|------------------|----------|
| Packaged (MSIX) | Yes | New apps; want Store/AppInstaller auto-update, clean Intune/ConfigMgr deployment |
| Packaged with external location (sparse) | Yes | Existing Win32/WPF/WinForms app keeping its own installer/binaries (Windows 10 2004+) |
| Unpackaged | No | Simple xcopy/legacy installer flows that need no identity-gated features |
| Self-contained | Independent of the above | Ship all Windows App SDK binaries inline; no separate runtime install, larger footprint |

- An app that needs **toast/push notifications, background tasks, app extensions, share targets, file associations, startup tasks, or Windows AI Foundry APIs** **MUST** have **package identity** — choose packaged MSIX or packaged-with-external-location. Do not pick unpackaged for these apps.
- New apps **SHOULD** default to **packaged MSIX** unless a deployment constraint rules it out.
- Existing apps that must keep their installer **SHOULD** use **packaged with external location** to gain identity without replacing the installer.
- Unpackaged apps **MUST** install the Windows App SDK runtime (or ship self-contained) and call `Bootstrap.Initialize()` at startup; set `<WindowsPackageType>None</WindowsPackageType>` in the project. Packaged apps **MUST NOT** set that property.
- The chosen model **MUST** be recorded in the project's planning notes (per `agenticdevelopercookbook://principles/explicit-over-implicit`) so the identity assumption is visible to every later decision.

## Make it reversible where you can

- Defer the framework choice no later than the first UI module; defer the deployment choice no later than the first identity-gated feature. Both are costly to change once code depends on them (`agenticdevelopercookbook://principles/small-reversible-decisions`).
- When requirements are uncertain, agents **SHOULD** prefer packaged MSIX — adding identity-gated features later is free, removing the identity assumption is not.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
