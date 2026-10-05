
- **Concurrent access**: If two processes or two app instances attempt to open the same package document simultaneously, behavior is undefined. The pattern relies on macOS file coordination (`NSFileCoordinator`) when available, but does not implement custom locking. Documents opened via `DocumentGroup` benefit from the system's built-in file coordination.
- **Package opened by external tool**: If a user right-clicks "Show Package Contents" and modifies the package externally, the app has no mechanism to detect this. The next open will read whatever state the package is in.
- **Invalid URL at restoration**: A saved URL that no longer exists is logged and skipped; it MUST NOT prevent other documents from reopening.
- **Duplicate extension**: Two document types registering the same extension is a misconfiguration; each type MUST keep a unique extension.

