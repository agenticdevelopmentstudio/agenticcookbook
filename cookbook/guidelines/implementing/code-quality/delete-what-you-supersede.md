---
id: 2575d546-fbd4-46a6-a143-b886c7d04f01
title: "Delete what you supersede"
domain: agenticdevelopercookbook://guidelines/implementing/code-quality/delete-what-you-supersede
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "While writing a change, remove the old path, rename every caller, delete what the change orphans, and leave no commented-out code; names must still describe the thing."
platforms: []
tags:
  - code-quality
  - refactoring
  - hygiene
depends-on: []
related:
  - agenticdevelopercookbook://principles/design-for-deletion
  - agenticdevelopercookbook://guidelines/reviewing/code-quality/code-hygiene
  - agenticdevelopercookbook://guidelines/implementing/code-quality/scope-discipline
  - agenticdevelopercookbook://guidelines/implementing/code-quality/naming
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - new-module
  - refactor
---

# Delete what you supersede

A change that adds the new way and leaves the old way in place is half done. This is the writing-side counterpart of the `code-hygiene` review guideline: do the deleting while you build, so the reviewer has nothing left to find. Each rule below is cheap at the moment you make the change and expensive afterwards, when nobody remembers what the old path was for.

## Remove the old path in the same change

- When you replace an implementation, you MUST delete the one it replaces in the same change. Do not leave old and new side by side, and do not park the old one behind a flag that is permanently off.
- Do the deletion as you go, not as a cleanup pass you plan to do later. A planned cleanup that never happens is the usual way dead paths survive.
- Delete the old tests with the old code, and move any behavior they pinned that still matters onto the new path.

## Rename every caller

- When you rename or move a function, type, file or route, you MUST update every caller, import, export, doc reference and string that names it. Search for the old name across the whole repo, not only the files you opened.
- Search for the whole identifier, not a fragment. A search for `foo` also matches `foobar`, and a search that skips strings, config and docs misses the references that break at runtime.
- Finish with a final search for the old name. Any remaining hit is either a missed caller or a deliberate compatibility shim, and a shim MUST say so in a comment that names when it goes away.

## Delete orphaned files, assets, flags and config keys

- After the change, anything that nothing references MUST go: files, functions, exports, types, images and other assets, feature flags, config keys, environment variables, migrations of paths that no longer exist.
- A flag whose rollout is finished, or whose old branch you just removed, is an orphan. Remove the flag and the branch it guarded.
- Dependencies your change made unused SHOULD come out of the manifest in the same change.
- Confirm with a reference search before deleting. You MUST NOT delete what you cannot show is unused, and you MUST NOT widen the cleanup to unrelated dead code; note that for the user instead.

## No commented-out code

- Code you no longer need MUST be deleted, not commented out. Version control keeps the history.
- Do not leave a block of old code with a note such as "kept for reference" or "old approach". If the reasoning behind the old approach matters, write it as a sentence in a comment and delete the code.
- A temporary disable while debugging is fine on your machine and MUST NOT reach a commit.

## Names must still describe the thing

- When a change alters what a value, function or field holds, rename it to match. A field called `isDisplayed` that now holds an optional `Bool?`, or a `userList` that is now a dictionary, misleads every later reader.
- After you change a type or a behavior, reread the names that touch it, including parameter names, variable names, file names and test names.
- A rename is a change to every caller, so apply the rename rule above in the same change.

## Why this matters

Leftovers mislead the next reader, human or agent, about which path is live, and they inflate context and review cost. Deleting at the moment of change is the cheapest time to do it, because you still know exactly what the change superseded.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
