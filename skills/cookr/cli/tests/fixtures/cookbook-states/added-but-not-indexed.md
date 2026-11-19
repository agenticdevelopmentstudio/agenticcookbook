---
id: 11111111-2222-3333-4444-555555555555
title: Added But Not Indexed
type: recipe
version: 1.0.0
status: draft
language: en
created: 2026-05-15
modified: 2026-05-15
author: cookbook-tests
copyright: 2026 cookbook-tests
license: MIT
summary: A recipe with frontmatter but no INDEX entry.
---
# Added But Not Indexed

This recipe has full frontmatter so Phase A passes, but it isn't listed in
recipes/INDEX.md — `validate` should report drift, `lint --no-llm` should not.
