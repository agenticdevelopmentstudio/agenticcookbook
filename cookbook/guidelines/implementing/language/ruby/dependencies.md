
- A `Gemfile` has one global `source`, and its `Gemfile.lock` is committed.
- Keep development and test gems in groups, and install without them where they are not needed with `bundle config set --local without <group>`.

