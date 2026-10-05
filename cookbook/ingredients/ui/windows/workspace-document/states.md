
| State | Behavior |
|-------|----------|
| Entry removed | Entry disappears from sidebar, coordinator stopped (if directory), document updated |
| Entry added | Entry appears in sidebar, coordinator started (if directory), document updated |
| Self-referential add rejected | Add operation silently rejected, warning logged (prevent-self-referential) |
| Entry type migrated | Entry with incorrect type auto-corrected on load (auto-correct-entry-type) |

