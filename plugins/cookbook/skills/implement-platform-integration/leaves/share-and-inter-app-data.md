<!-- leaf: implement-platform-integration/share-and-inter-app-data · source: guidelines/implementing/platform-integration/share-and-inter-app-data.md -->

**Rules** (cite as `implement-platform-integration/share-and-inter-app-data#<slug>`):

- `apps-participate-platform-share-inter` SHOULD — Apps SHOULD participate in the platform's share and inter-app data exchange mechanisms to integrate with other apps and …

# Share and inter-app data flow

Apps SHOULD participate in the platform's share and inter-app data exchange mechanisms to integrate with other apps and workflows. Users expect to move data between apps without friction.

- Support both sending and receiving data through the platform share sheet
- Register as a handler for relevant file types and UTIs/MIME types
- Support drag and drop for content that makes sense in multi-window contexts
- Validate all received data — inter-app data is an untrusted input boundary

## Apple (iOS / macOS)

Implement `UIActivityViewController` (iOS) or `NSSharingServicePicker` (macOS) to share content. Create Share Extensions to receive content from other apps. Register UTI declarations in `Info.plist` for file type associations. Support drag and drop via `NSItemProvider` on iPadOS and macOS. On macOS, support the Services menu via `NSServices` for system-wide text operations.

## Android

Declare `<intent-filter>` with `ACTION_SEND` and appropriate MIME types to receive shared content. Use `Intent.createChooser()` to send. Implement Direct Share targets with `ChooserTargetService` for frequently shared-to contacts. Support `ContentProvider` for structured data sharing between apps. Register as a document provider via `DocumentsProvider` for the system file picker.

## Windows

Implement the Share Contract (`DataTransferManager`) to send and receive content. Register as a share target in the app manifest. Support drag and drop via `DragDrop` APIs. Register file type associations in `Package.appxmanifest` for Open With integration. Support clipboard with rich content formats.

## Web

Use the Web Share API (`navigator.share()`) to invoke the native share sheet. Register as a share target in the Web App Manifest (`share_target`). Support drag and drop via the HTML Drag and Drop API. Use the File Handling API to register as a handler for specific file types in PWAs.
