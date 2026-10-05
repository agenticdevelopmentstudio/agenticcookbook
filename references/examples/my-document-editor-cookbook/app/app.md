---
id: a9b0edec-ac60-4bcf-84d7-428d114a7b30
title: My Document Editor — App
domain: agenticdevelopercookbook://reference/examples/my-document-editor-cookbook/app/app
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: My Document Editor — App
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# My Document Editor — App

## Overview

Application entry point and lifecycle management for a multi-platform document editor.

## Requirements

**app-launch**: The app MUST open a new untitled document window on launch if no documents are restored.

**app-restore**: The app MUST restore previously open documents on relaunch.

**app-lifecycle**: The app MUST save all open documents when entering the background on iOS.
