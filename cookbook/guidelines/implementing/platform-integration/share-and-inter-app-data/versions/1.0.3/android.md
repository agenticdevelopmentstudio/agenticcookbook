
Declare `<intent-filter>` with `ACTION_SEND` and appropriate MIME types to receive shared content. Use `Intent.createChooser()` to send. Implement Direct Share targets with `ChooserTargetService` for frequently shared-to contacts. Support `ContentProvider` for structured data sharing between apps. Register as a document provider via `DocumentsProvider` for the system file picker.

