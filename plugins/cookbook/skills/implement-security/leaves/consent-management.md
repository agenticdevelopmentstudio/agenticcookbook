<!-- leaf: implement-security/consent-management · source: guidelines/implementing/security/consent-management.md -->

**Rules** (cite as `implement-security/consent-management#<slug>`):

- `similar-regimes-consent` MUST — Per GDPR Art. 7 (and similar regimes), consent MUST be:
- `freely-given` MUST — not bundled with service access; refusal MUST NOT degrade core functionality that does not depend on the processing.
- `specific-and-granular` MUST — each distinct purpose (analytics, marketing, personalization, third-party sharing) MUST have its own toggle. A single …
- `unambiguous` MUST — require an affirmative action (an explicit opt-in). Pre-ticked boxes, implied consent, or "continue = consent" MUST NOT …
- `only-immutable-record-not-overwrite-delete-prior-entries` MUST — Persist each decision as an append-only, immutable record. MUST NOT overwrite or delete prior entries — withdrawal is a …
- `record-capture-subject-id-purpose` MUST — Each record MUST capture: subject id, purpose(s), grant/withdraw action, timestamp (UTC), the policy/notice version …
- `log-queryable-answer-does-subject` SHOULD — The log SHOULD be queryable to answer "does subject X currently consent to purpose Y?" without replaying history at …
- `withdrawal-easy-granting-same-number` MUST — Withdrawal MUST be as easy as granting — same number of clicks, same surface, no dark patterns or friction.
- `withdrawal-you-propagate-change-so-processing` MUST — On withdrawal you MUST propagate the change so processing actually stops: stop new collection, halt downstream jobs, …
- `before-withdrawal-but-prevent-further-processing-purpose` MUST — Withdrawal is prospective: it does not invalidate processing already performed lawfully before withdrawal, but it MUST …
- `cookies-tracking-analytics-gated-do-load-scripts` MUST — Non-essential cookies, tracking, and analytics MUST be gated: do not load scripts, set tags, or send events until …
- `does-require-consent-not-presented-optional` SHOULD — Strictly necessary processing (security, fraud prevention, delivering the requested service) does not require consent …
- `version-bump-alone-trigger-re-consent-only` SHOULD — Re-request consent when the purpose changes, a new data category is added, or a new processor is introduced. A …
- `must-not` MUST — infer consent from inactivity, scrolling, or continued use.
- `must-not-2` MUST — make "reject all" harder to reach than "accept all".
- `must-not-3` MUST — treat children's data without the heightened, age-appropriate consent and verifiable-parental-consent paths the …

# Consent management

Capture consent that is freely given, specific, informed, granular, and withdrawable; record every grant and withdrawal as an auditable, append-only log; and gate all non-essential processing on it. This is engineering guidance for building consent flows, not legal advice — confirm obligations with counsel for each jurisdiction.

## Conditions for valid consent

Per GDPR Art. 7 (and similar regimes), consent **MUST** be:

- **Freely given**: not bundled with service access; refusal **MUST NOT** degrade core functionality that does not depend on the processing.
- **Specific and granular**: each distinct purpose (analytics, marketing, personalization, third-party sharing) **MUST** have its own toggle. A single blanket "I agree" **MUST NOT** cover unrelated purposes.
- **Informed**: present the purpose, controller identity, data categories, and the right to withdraw before capture.
- **Unambiguous**: require an affirmative action (an explicit opt-in). Pre-ticked boxes, implied consent, or "continue = consent" **MUST NOT** be used.

## Recording consent

- Persist each decision as an **append-only, immutable** record. **MUST NOT** overwrite or delete prior entries — withdrawal is a new event, not a mutation.
- Each record **MUST** capture: subject id, purpose(s), grant/withdraw action, timestamp (UTC), the **policy/notice version** shown, and the capture mechanism (e.g., banner, settings page).
- Store the exact consent-notice text or a content hash so you can prove what the user saw. Pin the policy to a dated, versioned revision.
- The log **SHOULD** be queryable to answer "does subject X currently consent to purpose Y?" without replaying history at read time (maintain a derived current-state view alongside the event log).

## Withdrawal

- Withdrawal **MUST** be as easy as granting — same number of clicks, same surface, no dark patterns or friction.
- On withdrawal you **MUST** propagate the change so processing actually stops: stop new collection, halt downstream jobs, and notify processors/third parties that received the data.
- Withdrawal is **prospective**: it does not invalidate processing already performed lawfully before withdrawal, but it **MUST** prevent further processing for that purpose.

## Gating and lifecycle

- Non-essential cookies, tracking, and analytics **MUST** be gated: do not load scripts, set tags, or send events until consent for that purpose is granted (consent-before-processing, not load-then-suppress).
- Strictly necessary processing (security, fraud prevention, delivering the requested service) does not require consent and **SHOULD NOT** be presented as optional.
- Re-request consent when the purpose changes, a new data category is added, or a new processor is introduced. A policy-version bump alone **SHOULD** trigger re-consent only when the change is material to the user's decision.
- Set a re-confirmation cadence for long-lived consent (commonly revisited at 12–24 months) per applicable guidance and risk.

## Anti-patterns

- **MUST NOT** infer consent from inactivity, scrolling, or continued use.
- **MUST NOT** make "reject all" harder to reach than "accept all".
- **MUST NOT** treat children's data without the heightened, age-appropriate consent and verifiable-parental-consent paths the relevant regime requires.
