
Review changed Ruby against the rules above.

- `must-begin-with-frozen-string-literal`, `must-put-magic-comment-in-first-section`: Each file begins with `# frozen_string_literal: true` in the first comment section.
- `must-copy-before-mutating-strings`: No code mutates a literal without making a copy.
- `should-use-open3-with-separate-arguments`, `must-not-build-command-strings-from-input`, `must-pass-argument-lists-to-spawn`: `Open3` and `Process` calls pass separate arguments. No interpolated command string.
- `must-check-process-status`, `should-rescue-enoent-when-absence-expected`: The `Process::Status` is checked. `Errno::ENOENT` is rescued where a missing tool is expected.
- `should-model-records-with-data-define`, `should-use-struct-only-for-mutation`: Records are `Data.define` unless mutation is required.
- `must-not-rescue-exception`, `must-not-use-rescue-modifier`, `must-not-return-from-ensure`, `should-raise-with-raise`, `should-rescue-by-class-name`: No `rescue Exception`, no `rescue` modifier, no `return` inside `ensure`. Errors are raised with `raise` and rescued by name.
- `must-pass-hashes-as-explicit-keywords`, `must-forward-all-argument-kinds`: Hash-to-keyword conversions use explicit `**`. Delegating methods use `*args, **kwargs, &block` or `...`.
- `should-limit-ruby2-keywords-to-old-rubies`: A `ruby2_keywords` call has a stated compatibility reason.
- `must-use-snake-case`, `must-end-predicates-in-question-mark`, `must-pair-bang-methods`: Names follow snake_case, predicate and bang conventions.
- `should-configure-style-in-rubocop-yml`, `should-set-rubocop-target-version`: `.rubocop.yml` sets the target Ruby version, and the new code passes it.
- `must-have-one-global-gem-source`, `must-commit-gemfile-lock`: Gemfile changes keep one source and update the committed `Gemfile.lock`.
- `should-treat-ruby-as-code`: a Ruby file written as a shell script with syntax (string-built commands, unchecked results) instead of as code.
- `should-feed-stdin-through-stdin-data`: standard input fed to a child some way other than `stdin_data:`.
- `should-serialize-with-to-h`: serialization that builds its own hash instead of returning `to_h`.
- `should-subclass-standard-error`: a domain error that does not subclass `StandardError`.
- `must-use-rubocop-version-env-only-in-ci`: `RUBOCOP_TARGET_RUBY_VERSION` set anywhere but CI.
- `should-group-dev-and-test-gems`, `should-omit-unneeded-gem-groups`: development and test gems outside a group, or installs that pull them in where they are not needed.
