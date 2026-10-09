---
id: f6836f90-5090-4857-bab9-74feb7c68223
title: "Ruby"
domain: agenticdevelopercookbook://guidelines/reviewing/language/ruby
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review Ruby for the frozen-string header, shell-free process calls, Data values, narrow rescues, explicit keyword arguments and style configuration."
platforms:
  - macos
  - linux
languages:
  - ruby
tags:
  - language
  - ruby
  - review
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/language/ruby
  - agenticdevelopercookbook://guidelines/reviewing/language/python
references:
  - https://docs.ruby-lang.org/en/master/Open3.html
  - https://rubystyle.guide/
  - https://docs.rubocop.org/rubocop/configuration.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
  - security-review
---

# Ruby

Review changed Ruby against [Ruby](agenticdevelopercookbook://guidelines/implementing/language/ruby).

## Header and strings

- Each file begins with `# frozen_string_literal: true` in the first comment section.
- No code mutates a literal without making a copy.

## Processes

- `Open3` and `Process` calls pass separate arguments. No interpolated command string.
- The `Process::Status` is checked. `Errno::ENOENT` is rescued where a missing tool is expected.

## Values and errors

- Records are `Data.define` unless mutation is required.
- No `rescue Exception`, no `rescue` modifier, no `return` inside `ensure`. Errors are raised with `raise` and rescued by name.

## Keyword arguments

- Hash-to-keyword conversions use explicit `**`. Delegating methods use `*args, **kwargs, &block` or `...`.
- A `ruby2_keywords` call has a stated compatibility reason.

## Style and dependencies

- Names follow snake_case, predicate and bang conventions.
- `.rubocop.yml` sets the target Ruby version, and the new code passes it.
- Gemfile changes keep one source and update the committed `Gemfile.lock`.

## Why this matters

A Ruby shell-injection or swallowed error looks fine in a diff. A checklist makes the reviewer look at exactly those lines.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
