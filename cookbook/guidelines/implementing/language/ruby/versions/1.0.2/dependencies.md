
- A `Gemfile` MUST have one global `source`, and its `Gemfile.lock` MUST be committed.
- Development and test gems SHOULD be kept in groups, and installs SHOULD omit them where they are not needed with `bundle config set --local without <group>`.

