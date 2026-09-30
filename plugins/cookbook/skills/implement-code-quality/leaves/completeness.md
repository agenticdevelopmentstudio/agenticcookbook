<!-- leaf: implement-code-quality/completeness · source: guidelines/implementing/code-quality/completeness.md -->

**Rules** (cite as `implement-code-quality/completeness#<slug>`):

- `parts-request-implemented-work-presented-complete` MUST — All parts of the request MUST be implemented. Work presented as complete that is not is worse than work that is …
- `unhappy-paths-handled-just-happy-path` MUST — The unhappy paths MUST be handled, not just the happy path — empty, null, error, timeout, and conflict cases are part …
- `you-not-silently-drop-part-request` MUST — You MUST NOT silently drop a part of the request. If something genuinely should be deferred, say so explicitly and get …
- `requested-requirements-you-distinguish-we-might-need` MUST — YAGNI defers *speculative* generality, not *known, requested* requirements. You MUST distinguish "we might need this …
- `you-not-block-ask-input-has` MUST — You MUST NOT block to ask for input that has already been provided or pre-specified. Re-reading the request before …
- `you-confirm-work-actually-runs` MUST — You MUST confirm the work actually runs and meets the request (see post-generation-verification) before reporting it …

# Completeness: finish the work, don't defer by default

Deliver the full scope that was agreed. This is the complement to scope-discipline: scope-discipline says don't do *more* than asked; completeness says don't quietly do *less*. Declaring work done when it is partial, or scoping pieces out without saying so, is a recurring AI failure mode.

## Finish the agreed scope

- All parts of the request MUST be implemented. Work presented as complete that is not is worse than work that is honestly reported as partial.
- The unhappy paths MUST be handled, not just the happy path — empty, null, error, timeout, and conflict cases are part of "done," not extras.

## Don't prematurely scope out

- You MUST NOT silently drop a part of the request. If something genuinely should be deferred, say so explicitly and get agreement — surface it as a note (the same way scope-discipline notes adjacent issues), do not bury it.
- "Out of scope" is a decision the user makes with you, not one you make on their behalf.

## YAGNI is not a license to skip required work

- YAGNI defers *speculative* generality, not *known, requested* requirements. You MUST distinguish "we might need this later" (defer) from "this was asked for" (do it).
- When you invoke YAGNI to not build something, name what you are skipping and why, so the choice is visible.

## Don't stall on settled questions

- You MUST NOT block to ask for input that has already been provided or pre-specified. Re-reading the request before pausing avoids stalling work that was meant to proceed.

## Verify before declaring done

- You MUST confirm the work actually runs and meets the request (see post-generation-verification) before reporting it complete. "It should work" is not "it works."
