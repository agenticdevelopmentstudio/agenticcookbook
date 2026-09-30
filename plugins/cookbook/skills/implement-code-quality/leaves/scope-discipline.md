<!-- leaf: implement-code-quality/scope-discipline · source: guidelines/implementing/code-quality/scope-discipline.md -->

**Rules** (cite as `implement-code-quality/scope-discipline#<slug>`):

- `goal-stated-one-sentence-request` MUST — The goal MUST be stated in one sentence. If the request is ambiguous or could be interpreted broadly, ask before …
- `only-what-requested-modified-asked-fix-bug` MUST — Only what was requested MUST be modified. If asked to fix a bug, fix that bug — do not refactor surrounding code, add …
- `them-user-but-not-fix-them-note-like` MUST — If you discover issues outside the stated scope — broken imports, outdated comments, missing error handling — note them …

# Scope discipline

Every task has a boundary. Stay inside it.

## Before starting

The goal MUST be stated in one sentence. If the request is ambiguous or could be interpreted broadly, ask before assuming broad scope. For multi-repo work, confirm which repository before making changes.

## During work

Only what was requested MUST be modified. If asked to fix a bug, fix that bug — do not refactor surrounding code, add missing tests for unrelated functions, update documentation for other features, or "improve" adjacent components.

If you discover issues outside the stated scope — broken imports, outdated comments, missing error handling — **note them** for the user but MUST NOT fix them. A note like "I noticed X is also broken, want me to fix that separately?" preserves the user's ability to prioritize.

## Recognizing scope creep

Watch for these signals that scope is expanding:
- Modifying files not directly related to the stated goal
- Adding functionality the user didn't ask for
- Refactoring code that works correctly but "could be better"
- Redesigning a component when asked to fix one behavior
- Touching more than the minimum files needed for the change

## Why this matters

Unbounded scope leads to:
- Changes the user didn't expect or want, requiring reverts
- Compound bugs from modifying working code alongside new work
- Longer review cycles because the diff includes unrelated changes
- Loss of trust — the user can't predict what will change

Small, focused changes are easier to review, easier to revert, and easier to understand.
