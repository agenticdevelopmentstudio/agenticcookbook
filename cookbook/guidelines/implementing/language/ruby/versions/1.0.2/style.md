
- Methods and variables MUST be `snake_case`. A predicate MUST end in `?`. A bang method (`!`) MUST exist only when a non-bang counterpart exists too.
- Style SHOULD be configured in `.rubocop.yml`, and the project SHOULD set `AllCops: TargetRubyVersion` or let it come from the gemspec, `.ruby-version` or `.tool-versions`. The `RUBOCOP_TARGET_RUBY_VERSION` environment variable overrides all of them, so it MUST be used only in CI.

