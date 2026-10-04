
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

