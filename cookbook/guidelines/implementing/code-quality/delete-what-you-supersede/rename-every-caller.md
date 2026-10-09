
- When you rename or move a function, type, file or route, you MUST update every caller, import, export, doc reference and string that names it. Search for the old name across the whole repo, not only the files you opened.
- Search for the whole identifier, not a fragment. A search for `foo` also matches `foobar`, and a search that skips strings, config and docs misses the references that break at runtime.
- Finish with a final search for the old name. Any remaining hit is either a missed caller or a deliberate compatibility shim, and a shim MUST say so in a comment that names when it goes away.

