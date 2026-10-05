---
id: c0c71331-7ea4-4452-b08c-9fa367deb6e5
title: 'Research: Text Engine Evaluation'
domain: agenticdevelopercookbook://reference/examples/my-document-editor-cookbook/context/research/text-engine-evaluation
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: 'Research: Text Engine Evaluation'
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Research: Text Engine Evaluation

## Question

Which text rendering and editing engine should the editor use on Apple platforms?

## Options Evaluated

### TextKit 2
- Native Apple framework, first-class SwiftUI support
- Handles complex text layout (RTL, CJK, emoji)
- Active development by Apple

### Custom Engine
- Full control over rendering pipeline
- Higher maintenance burden
- Risk of platform inconsistencies

## Conclusion

TextKit 2. The native framework covers all requirements, integrates cleanly with the platform, and avoids the maintenance cost of a custom engine.
