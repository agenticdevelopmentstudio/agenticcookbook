---
id: CA56F1AA-7089-498F-8BCC-C11A0D81BE3D
title: "Package Document Type"
domain: agenticdevelopercookbook://ingredients/infrastructure/package-document-type
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Registers a directory-bundle document type with a custom UTType and wires it into DocumentGroup scenes with auto-save and session restoration"
platforms:
  - ios
  - macos
  - swift
tags:
  - infrastructure
  - package-document
  - uttype
  - documentgroup
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/package-document
  - agenticdevelopercookbook://ingredients/infrastructure/package-document-storage
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Package Document Type

## Overview

A package document type declares a directory bundle — shown by Finder as a single file — as a first-class document: a custom UTType conforming to `com.apple.package`, a unique file extension (e.g., `.catnip-proj`, `.catnip-workspace`), a `ReferenceFileDocument` class that reads and writes a `FileWrapper`, and a `DocumentGroup` scene that gives the type open, save, and close behavior. Auto-save follows automatically from the document's `@Published` model, and the app restores the set of open documents across launches. Use it for each document kind (project, workspace) an app persists as a package.

### Terminology

| Term | Definition |
|------|-----------|
| Package document | A directory bundle that macOS presents as a single file in Finder, identified by a custom UTType conforming to `com.apple.package` |
| UTType | A Uniform Type Identifier declared in Info.plist that maps a file extension to a content type and conformance hierarchy |
| ReferenceFileDocument | A SwiftUI protocol for reference-type documents that triggers auto-save when the document's `objectWillChange` publisher fires |
| FileWrapper | An Apple framework class representing a file, directory, or symbolic link in memory; used to read from and write to package directories |
| Document scene | A SwiftUI `DocumentGroup` scene that manages the open/save/close lifecycle for a document type |

### UTType Registration

Each document type requires an exported UTType entry in Info.plist:

```
UTExportedTypeDeclarations:
  - UTTypeIdentifier: com.example.catnip-project
    UTTypeDescription: Catnip Project
    UTTypeConformsTo: [com.apple.package]
    UTTypeTagSpecification:
      public.filename-extension: [catnip-proj]
```

And a matching Swift `UTType` extension:

```swift
extension UTType {
    static let catnipProject = UTType(exportedAs: "com.example.catnip-project")
    static let catnipWorkspace = UTType(exportedAs: "com.example.catnip-workspace")
}
```

## Behavioral Requirements

### UTType registration

- **package-uttype-declaration**: Each document type MUST declare a custom UTType conforming to `com.apple.package` in the app's Info.plist as an exported type.
- **unique-file-extension**: Each UTType MUST specify a unique file extension in `UTTypeTagSpecification` under `public.filename-extension`.
- **swift-uttype-property**: The UTType MUST be declared as a Swift `UTType` static property via `UTType(exportedAs:)` for use in document and file panel APIs.

### Document protocol conformance

- **reference-file-document**: Each document class MUST conform to `ReferenceFileDocument` (SwiftUI) and declare its `readableContentTypes` and `writableContentTypes` as the corresponding custom UTType.
- **published-model-property**: The document MUST expose a `@Published var model` property whose changes trigger `objectWillChange`, enabling SwiftUI auto-save.
- **filewrapper-read-write**: The document MUST implement `init(configuration:)` to read from a `FileWrapper` and `fileWrapper(snapshot:configuration:)` to write to a `FileWrapper`.

### Document scenes

- **document-group-scene**: The app MUST declare a `DocumentGroup(newDocument:)` scene for each document type, associating it with the correct `ReferenceFileDocument` subclass.
- **non-document-window-group**: Non-document windows (e.g., settings, welcome screen) MUST use `WindowGroup` scenes, not `DocumentGroup`.
- **custom-menu-save-panel**: Custom menu commands for creating new documents MUST use `NSSavePanel` to select the save location and then programmatically create the document.

### Lifecycle

- **autosave-via-published**: Auto-save MUST be triggered automatically by the `@Published` model property's `objectWillChange` publisher. No manual save action is required from the user.
- **save-open-urls-on-quit**: On application quit, the document system MUST save the URLs of all currently open documents for session restoration.
- **restore-urls-on-launch**: On application launch, the document system MUST attempt to reopen previously saved document URLs, logging any that fail to open.

## Appearance

Not applicable — this ingredient defines document registration and lifecycle, not a visual component. Finder renders the package as a single file icon for the registered extension.

## States

| State | Behavior |
|-------|----------|
| New document | Empty model with default values; the first save creates the package directory |
| Open document | Model loaded; changes to `model` trigger auto-save |
| Auto-save in progress | Model property changed; the system snapshots the model and writes the package |
| Session restoration | App launches; previously open document URLs are reopened; any that fail are logged and skipped |

## Accessibility

Not applicable — this ingredient has no direct user interface. Document open/save/error dialogs inherit platform-standard accessibility from `NSSavePanel`, `NSOpenPanel`, and SwiftUI alert presentations.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pd-type-001 | package-uttype-declaration, unique-file-extension, swift-uttype-property | Register UTType for `.catnip-proj` conforming to `com.apple.package` | Finder displays the package directory as a single file icon with the correct extension |
| pd-type-002 | reference-file-document, published-model-property | Create a new `ProjectDocument` and modify the `model` property | `objectWillChange` fires; auto-save triggers |
| pd-type-003 | filewrapper-read-write | Call `fileWrapper(snapshot:configuration:)` on a document | Returns a `FileWrapper` of kind directory containing the document's database file |
| pd-type-004 | document-group-scene | Launch the app | `DocumentGroup` scenes are registered for each document type; File > Open shows the correct file type filters |
| pd-type-005 | autosave-via-published | Modify the model's `@Published` property | Auto-save fires without any user action |
| pd-type-006 | save-open-urls-on-quit | Open two documents, quit the app | Both document URLs are saved for session restoration |
| pd-type-007 | restore-urls-on-launch | Launch the app after quitting with two documents open | Both documents reopen; if one URL is invalid, the valid one still opens and the failure is logged |
| pd-type-008 | non-document-window-group | Inspect the scenes for the settings and welcome windows | They are `WindowGroup` scenes, not `DocumentGroup` |

## Edge Cases

- **Concurrent access**: If two processes or two app instances attempt to open the same package document simultaneously, behavior is undefined. The pattern relies on macOS file coordination (`NSFileCoordinator`) when available, but does not implement custom locking. Documents opened via `DocumentGroup` benefit from the system's built-in file coordination.
- **Package opened by external tool**: If a user right-clicks "Show Package Contents" and modifies the package externally, the app has no mechanism to detect this. The next open will read whatever state the package is in.
- **Invalid URL at restoration**: A saved URL that no longer exists is logged and skipped; it MUST NOT prevent other documents from reopening.
- **Duplicate extension**: Two document types registering the same extension is a misconfiguration; each type MUST keep a unique extension.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `UTTypeIdentifier` | string | (required) | Reverse-DNS identifier of the exported type |
| `public.filename-extension` | string[] | (required) | Unique file extension(s) for the package |
| `readableContentTypes` / `writableContentTypes` | UTType[] | the custom UTType | Content types the document class opens and saves |

## Logging

Subsystem: `{{bundle_id}}` | Category: `PackageDocument`

| Event | Level | Message |
|-------|-------|---------|
| Document created | info | `PackageDocument: created new document "{{filename}}"` |
| Session URLs saved | debug | `PackageDocument: saved {{count}} open document URLs for session restoration` |
| Session restoration started | info | `PackageDocument: restoring {{count}} documents from previous session` |
| Session restoration failed for URL | warning | `PackageDocument: failed to restore document at "{{url}}": {{error}}` |

## Platform Notes

- **macOS (SwiftUI)**: Use `ReferenceFileDocument` with `DocumentGroup(newDocument:)` for each document type. The `@Published var model` pattern drives auto-save through `objectWillChange`. For file creation outside the standard `DocumentGroup` flow (e.g., "New Project" menu items), use `NSSavePanel` to choose a location and then programmatically create the package directory and initial database. `NSWorkspace` file coordination applies automatically to `DocumentGroup`-managed documents. UTType declarations go in the target's Info.plist under `UTExportedTypeDeclarations`.
- **macOS (AppKit)**: Use an `NSDocument` subclass with `override class var readableTypes` and `override class var writableTypes`. `NSDocument` provides auto-save for free when `autosavesInPlace` returns `true`. Package document support is enabled by returning `true` from `class var isNativeType(_:)` for the custom UTType.
- **iOS**: `ReferenceFileDocument` works on iOS with `DocumentGroup`. The package is stored in the app's container or iCloud Drive. `NSSavePanel` and `NSOpenPanel` are not available — use `.fileImporter()` and `.fileExporter()` modifiers instead. iOS sandboxing requires security-scoped URL access for user-selected documents.
- **visionOS**: Same as iOS. `DocumentGroup` renders document management UI in the visionOS window style.
- **Compose / React/Web**: Not applicable — UTType, `DocumentGroup`, and `FileWrapper` are Apple frameworks.

## Design Decisions

**Decision**: Document creation flows live in the menu-commands recipe, not here.
**Rationale**: This ingredient covers registration and lifecycle. The "New Project" and "New Workspace" creation flows (NSOpenPanel, git validation, NSSavePanel) involve menu command structure and file picker UX, so they are documented in the menu-commands recipe.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [state-recovery](agenticdevelopercookbook://compliance/reliability#state-recovery) | partial | Reliability |
| [error-recovery](agenticdevelopercookbook://compliance/reliability#error-recovery) | partial | Reliability |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Package Document recipe |
