
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| status-001 | slide-in-animation | Set isSyncing = true | Bar slides in from bottom |
| status-002 | slide-out-animation | Set isSyncing = false | Bar slides out to bottom |
| status-003 | overlay-not-push | Bar visible over scrollable content | Content beneath is still scrollable |
| status-004 | update-text-while-visible | Change text while visible | Text updates without bar re-animating |
| status-005 | non-blocking-interaction | Tap content behind visible bar | Content responds to tap |

