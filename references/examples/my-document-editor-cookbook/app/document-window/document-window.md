---
id: 8dcd503b-269e-4c94-886b-1ca32dcf46bd
title: Document Window
domain: agenticdevelopercookbook://reference/examples/my-document-editor-cookbook/app/document-window/document-window
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Document Window
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Document Window

## Overview

The main document editing window containing a toolbar and a rich text editor surface. One window per open document.

## Requirements

**window-title**: The window title MUST display the document name, or "Untitled" for unsaved documents.

**window-close-prompt**: The window MUST prompt to save unsaved changes before closing.

**window-resize**: The editor surface MUST fill available space when the window is resized.
