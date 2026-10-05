
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pr-fix-001 | fix-preference-default | PR body with no preference metadata | The agent treats the preference as "auto" |
| pr-fix-002 | fix-preference-storage | Contributor chooses "review each change" | PR body contains `<!-- fix-preference: review -->` |
| pr-fix-003 | fix-or-suggest, fix-preference-honored | Preference "auto" and a fixable Phase 1 issue | The Fix Bot pushes a corrected commit |
| pr-fix-004 | fix-or-suggest, fix-preference-honored | Preference "review" and a fixable Phase 1 issue | The Fix Bot posts a suggested change and pushes no commit |
| pr-fix-005 | dedicated-persona | Any automated fix | The author is `@cookbook-fix-bot[bot]`, never a phase bot |
| pr-fix-006 | scope-of-fixes | A Phase 2 refactoring proposal approved by the human reviewer | The Fix Bot applies it |

