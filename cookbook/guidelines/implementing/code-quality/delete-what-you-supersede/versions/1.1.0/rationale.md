
- `should-delete-as-you-go`: A planned cleanup that never happens is the usual way dead paths survive.
- `should-search-whole-identifier`: A search for `foo` also matches `foobar`, and a search that skips strings, config and docs misses the references that break at runtime.
- `must-delete-not-comment-out`: Version control keeps the history.
- `should-rename-when-meaning-changes`: A field called `isDisplayed` that now holds an optional `Bool?`, or a `userList` that is now a dictionary, misleads every later reader.
