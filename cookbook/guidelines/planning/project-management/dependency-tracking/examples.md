
This section is informative; the entries below are illustrations, not a format the guideline requires.

A dependency statement:

> We are dependent on the identity team to deliver the token-refresh endpoint on 2026-12-15 in order for us to deliver offline sign-in.

The same dependency as a RAID-log entry:

| Category | Description | Internal or external | Owner | Confirmed by | Need-by | Status |
|---|---|---|---|---|---|---|
| Dependency | Identity team delivers the token-refresh endpoint | External | Priya (mobile) | Sam (identity), in the identity team's log | 2026-12-15 | Blocked: waiting on security review, 4 days |

The blocked item it holds up, in a tracker: the offline sign-in issue is "blocked by" the token-refresh issue, carries the board's Blocked icon, and is linked to the release milestone it affects.

