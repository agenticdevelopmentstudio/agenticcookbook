---
id: c58dff06-310e-4cb0-886d-ec0929f5b1eb
title: Editor
domain: agenticdevelopercookbook://reference/examples/my-document-editor-cookbook/app/document-window/editor/editor
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Editor
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Editor

## Overview

Rich text editing surface using the platform's native text engine (TextKit 2 on Apple).

## Requirements

**editor-rich-text**: The editor MUST support bold, italic, underline, headings (H1-H3), and bulleted/numbered lists.

**editor-undo**: The editor MUST support undo/redo with platform-standard keyboard shortcuts.

**editor-selection**: The editor MUST sync the current selection state with the toolbar.
