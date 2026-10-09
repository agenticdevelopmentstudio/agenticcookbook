---
id: f29e82ca-611e-409a-9121-8abe1719b434
title: "Ruby"
domain: agenticdevelopercookbook://guidelines/implementing/language/ruby
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Write Ruby with frozen string literals, shell-free process calls, immutable Data values, narrow rescue clauses, explicit keyword arguments and a pinned RuboCop and Bundler setup."
platforms:
  - macos
  - linux
languages:
  - ruby
tags:
  - language
  - ruby
  - open3
  - keyword-arguments
  - rubocop
  - bundler
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/language/python
  - agenticdevelopercookbook://guidelines/implementing/code-quality/shell-scripts
  - agenticdevelopercookbook://guidelines/implementing/code-quality/linting
  - agenticdevelopercookbook://guidelines/reviewing/language/ruby
  - agenticdevelopercookbook://principles/immutability-by-default
  - agenticdevelopercookbook://principles/explicit-over-implicit
references:
  - https://docs.ruby-lang.org/en/master/Open3.html
  - https://docs.ruby-lang.org/en/master/Process.html
  - https://docs.ruby-lang.org/en/master/Data.html
  - https://rubystyle.guide/
  - https://www.ruby-lang.org/en/news/2019/12/12/separation-of-positional-and-keyword-arguments-in-ruby-3-0/
  - https://docs.rubocop.org/rubocop/configuration.html
  - https://guides.rubygems.org/gemfile/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - new-module
  - refactor
  - error-handling
---

# Ruby

Ruby is used here for build tooling and Apple-ecosystem scripts (Fastlane, CocoaPods, Bundler). Treat a Ruby file as code, not as a shell script with syntax.

## File header

- Begin every file with `# frozen_string_literal: true`. The comment applies to that file only and must be in the first comment section.
- Mutate a string only after `+""` or `String.new`, or `dup` a frozen one.

## Running other programs

- Use `Open3.capture2`, `capture2e` or `capture3` with separate arguments: `Open3.capture2e("git", "status")`. With an executable path plus arguments no shell is involved. A single command string is handed to the shell, so never build one from outside input.
- These calls return the output and a `Process::Status`; check `status.success?` rather than ignoring it. A missing executable raises `Errno::ENOENT`, so rescue that when absence is expected.
- Feed standard input through the `stdin_data:` option.
- `Process.spawn` and similar calls also route a single string that contains shell metacharacters through `/bin/sh`. Pass an argument list instead.

## Values

- Model records as `Data.define(:name, :path)`. A `Data` instance is immutable, requires every member, and is copied with changes through `with`. Use `Struct` only when you need mutation.
- Return `to_h` when you need to serialize.

## Errors

- Never `rescue Exception`; a bare `rescue` catches `StandardError`, which is the right default. Name the class you handle.
- Do not use the `rescue` modifier (`foo rescue nil`); it hides which error occurred.
- Do not `return` from an `ensure` block; it discards the in-flight exception.
- Raise with `raise`, not `fail`. Define domain errors as subclasses of `StandardError`.

## Keyword arguments

- Since Ruby 3.0 positional hashes and keyword arguments are separate. Pass a hash as keywords with `**opts` explicitly, and accept it with `**opts`.
- A method that forwards its arguments declares `*args, **kwargs, &block` or uses `...`. Use `ruby2_keywords` only in code that must also run on Ruby 2.6 to 3.0.

## Style

- Methods and variables are `snake_case`. A predicate ends in `?`. A bang method (`!`) exists only when a non-bang counterpart exists too.
- Configure style in `.rubocop.yml`, and set `AllCops: TargetRubyVersion` or let it come from the gemspec, `.ruby-version` or `.tool-versions`. The `RUBOCOP_TARGET_RUBY_VERSION` environment variable overrides all of them, so use it only in CI.

## Dependencies

- A `Gemfile` has one global `source`, and its `Gemfile.lock` is committed.
- Keep development and test gems in groups, and install without them where they are not needed with `bundle config set --local without <group>`.

## Why this matters

Ruby's defaults are permissive: strings are mutable, a command string goes to the shell, `rescue` swallows broadly. Opting into the strict form in each file keeps scripts predictable and keeps untrusted input away from a shell.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
