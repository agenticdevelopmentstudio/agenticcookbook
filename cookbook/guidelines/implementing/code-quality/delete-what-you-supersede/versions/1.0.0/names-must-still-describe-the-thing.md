
- When a change alters what a value, function or field holds, rename it to match. A field called `isDisplayed` that now holds an optional `Bool?`, or a `userList` that is now a dictionary, misleads every later reader.
- After you change a type or a behavior, reread the names that touch it, including parameter names, variable names, file names and test names.
- A rename is a change to every caller, so apply the rename rule above in the same change.

