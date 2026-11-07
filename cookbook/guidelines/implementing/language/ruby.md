---
id: f29e82ca-611e-409a-9121-8abe1719b434
title: "Ruby"
domain: agenticdevelopercookbook://guidelines/implementing/language/ruby
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-10-09
modified: 2026-11-07
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

- Every file MUST begin with `# frozen_string_literal: true`. The comment applies to that file only and MUST be in the first comment section.
- Code MUST mutate a string only after `+""` or `String.new`, or `dup` a frozen one.

## Running other programs

- Code SHOULD use `Open3.capture2`, `capture2e` or `capture3` with separate arguments: `Open3.capture2e("git", "status")`. With an executable path plus arguments no shell is involved. A single command string is handed to the shell, so code MUST NOT build one from outside input.
- These calls return the output and a `Process::Status`; code MUST check `status.success?` rather than ignoring it. A missing executable raises `Errno::ENOENT`, so code SHOULD rescue that when absence is expected.
- Standard input SHOULD be fed through the `stdin_data:` option.
- `Process.spawn` and similar calls also route a single string that contains shell metacharacters through `/bin/sh`. Code MUST pass an argument list instead.

## Values

- Records SHOULD be modeled as `Data.define(:name, :path)`. A `Data` instance is immutable, requires every member, and is copied with changes through `with`. Code SHOULD use `Struct` only when it needs mutation.
- Code SHOULD return `to_h` when it needs to serialize.

## Errors

- Code MUST NOT `rescue Exception`; a bare `rescue` catches `StandardError`, which is the right default. Code SHOULD name the class it handles.
- Code MUST NOT use the `rescue` modifier (`foo rescue nil`); it hides which error occurred.
- Code MUST NOT `return` from an `ensure` block; it discards the in-flight exception.
- Code SHOULD raise with `raise`, not `fail`, and SHOULD define domain errors as subclasses of `StandardError`.

## Keyword arguments

- Since Ruby 3.0 positional hashes and keyword arguments are separate. Code MUST pass a hash as keywords with `**opts` explicitly, and accept it with `**opts`.
- A method that forwards its arguments MUST declare `*args, **kwargs, &block` or use `...`. `ruby2_keywords` SHOULD be used only in code that must also run on Ruby 2.6 to 3.0.

## Style

- Methods and variables MUST be `snake_case`. A predicate MUST end in `?`. A bang method (`!`) MUST exist only when a non-bang counterpart exists too.
- Style SHOULD be configured in `.rubocop.yml`, and the project SHOULD set `AllCops: TargetRubyVersion` or let it come from the gemspec, `.ruby-version` or `.tool-versions`. The `RUBOCOP_TARGET_RUBY_VERSION` environment variable overrides all of them, so it MUST be used only in CI.

## Dependencies

- A `Gemfile` MUST have one global `source`, and its `Gemfile.lock` MUST be committed.
- Development and test gems SHOULD be kept in groups, and installs SHOULD omit them where they are not needed with `bundle config set --local without <group>`.

## Why this matters

Ruby's defaults are permissive: strings are mutable, a command string goes to the shell, `rescue` swallows broadly. Opting into the strict form in each file keeps scripts predictable and keeps untrusted input away from a shell.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-11-07 | Mike Fullerton | State the rules with RFC 2119 keywords |
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
