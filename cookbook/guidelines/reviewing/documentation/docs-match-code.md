---
id: 744c30a2-5dfa-41c6-8746-37372ba6465c
title: "Docs match the code"
domain: agenticdevelopercookbook://guidelines/reviewing/documentation/docs-match-code
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review that comments, docstrings, READMEs and instruction files describe what the code does now, that examples run, and that nothing documents behavior that was removed."
platforms: []
tags:
  - documentation
  - review
  - accuracy
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/documentation/writing-comments-and-docs
  - agenticdevelopercookbook://guidelines/reviewing/code-quality/code-hygiene
  - agenticdevelopercookbook://guidelines/implementing/code-quality/code-for-the-ai-reader
  - agenticdevelopercookbook://principles/dry
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
  - pre-commit
---

# Docs match the code

Documentation that disagrees with the code is worse than none, because readers trust it. When a change touches behavior, review every place that describes that behavior, not only the files in the diff. Agents are especially exposed: an instruction file that names a command that no longer exists sends the next session down a dead end with full confidence.

## Comments and docstrings describe current behavior

- For every changed function, read its comment and docstring against the new body. Check parameters, return values, errors raised, side effects and units.
- Flag a comment that explains a branch, a workaround or a constant the change removed or altered.
- Flag comments that narrate history ("now we", "previously", "changed to") instead of stating what is true now. History belongs in version control.
- Check the neighbors too. A docstring above an untouched function can be made false by a change in what it calls.

## READMEs and instruction files match what exists

- Every command, flag, path, file name, environment variable and config key mentioned in a README, an AGENTS.md or a similar agent instruction file MUST exist and behave as described. Verify by looking, not by assuming.
- Check install and setup steps against the scripts that do them, and check directory trees and lists of components against the actual directory.
- Instruction files steer agents, so a wrong claim there is a defect of the same weight as a wrong line of code.

## Examples run

- Code samples, command lines and sample output SHOULD be run, or at least read against the current signatures and output format.
- Flag examples that call renamed functions, pass removed arguments, import moved modules, or show output the code no longer produces.
- Where an example can be a test or a doctest, prefer that, so it fails when it goes stale.

## No docs remain for removed behavior

- When a feature, option, endpoint or command is removed, every page, section, table row, changelog promise and help string that describes it MUST go too.
- Search the docs for the removed names. A hit is a finding.
- Also look for the reverse: new behavior with no description anywhere a user would look.

## Stale-claim smells

Raise a finding when you see any of these:

- a count or list that no longer matches ("the three modes", "all five commands");
- "currently", "for now", "temporary", or a version or date that has passed;
- a path, URL or anchor that does not resolve;
- a doc that names a class, function or flag that a search of the repo does not find;
- two docs that give different answers to the same question;
- a TODO or "not yet supported" note for something that now exists.

Quote the stale text and the line of code that contradicts it, so the fix is unambiguous.

## Why this matters

Readers act on what the docs say. A stale claim costs a person an hour and costs an agent a wrong turn it will not question, so a wrong doc is a defect of the same weight as wrong code.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
