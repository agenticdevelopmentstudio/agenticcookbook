
The deployment model determines whether the app has **package identity**, which gates a large set of Windows APIs.

| Model | Package identity | Use when |
|-------|------------------|----------|
| Packaged (MSIX) | Yes | New apps; want Store/AppInstaller auto-update, clean Intune/ConfigMgr deployment |
| Packaged with external location (sparse) | Yes | Existing Win32/WPF/WinForms app keeping its own installer/binaries (Windows 10 2004+) |
| Unpackaged | No | Simple xcopy/legacy installer flows that need no identity-gated features |
| Self-contained | Independent of the above | Ship all Windows App SDK binaries inline; no separate runtime install, larger footprint |
