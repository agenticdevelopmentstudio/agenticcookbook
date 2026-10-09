
- Methods and variables are `snake_case`. A predicate ends in `?`. A bang method (`!`) exists only when a non-bang counterpart exists too.
- Configure style in `.rubocop.yml`, and set `AllCops: TargetRubyVersion` or let it come from the gemspec, `.ruby-version` or `.tool-versions`. The `RUBOCOP_TARGET_RUBY_VERSION` environment variable overrides all of them, so use it only in CI.

