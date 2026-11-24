# Integrate: risk-tracking

## For the owner

No `cookr validate` owner-decides rows for this topic.

Open questions from the owner list:

- Which review cadence the rule names: PRINCE2 ties formal review to stage ends and progress reviews, the NAO example is monthly, and the Kanban Guide allows continuous or fixed-interval review; the owner decides whether the rule names one interval or requires the team to set one.
- Which response vocabulary the cookbook adopts: ISO 31000's treatment options, PRINCE2's avoid, reduce, transfer, share, accept and prepare contingent plans, PMBOK 8's mitigate, avoid, transfer, accept and escalate, or the ROAM categories (resolved, owned, accepted, mitigated).
- Whether opportunities (positive risks) are in this topic's scope: ISO 31000, PRINCE2 and PMBOK 8 all treat them alongside threats, while the listed rules speak only of concerns.
- Whether the rule requires a separate actionee beside the owner, as PRINCE2 does, or lets one person hold both, which PRINCE2 says is common.
- Which tracker mapping the cookbook recommends for a small team: a custom 'Risk' issue type with fields in GitHub or Jira, a RAID log document, or a project health flag such as Linear's 'At risk', which marks a project but is not a per-risk record.

- from the phase 3 code review (claude-code-review/f8): the name `concern-has-status-and-raiser` promises a status, but the rule requires only the raiser. It is a prior rule, whose name stays fixed, so the rename is the owner's; the review suggests renaming it to match its text.

## Lossless

New topic, no base text (`cookr roles lossless`: not in the base commit).

## Validate

`cookr validate` passed. Bumped 1.0.0 → 1.0.1; /add-artifact approved it (no lint failures; two warnings: the build bar holds 30 lines, one per rule, and the names `concern-has-status-and-raiser` and `risk-identification-and-attention-flagging` say more than their rules, left as named because rule names stay stable).

integrated: 2026-11-24
