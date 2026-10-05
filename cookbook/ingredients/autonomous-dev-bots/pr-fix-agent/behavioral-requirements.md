
### Contributor preferences

- **fix-preference-prompt**: The `/contribute-to-cookbook` skill MUST ask the contributor before PR submission: "If the review pipeline finds fixable issues, would you like us to fix them automatically, or review each change?"
- **fix-preference-default**: The default preference MUST be "fix automatically".
- **fix-preference-storage**: The preference MUST be stored in the PR body as metadata (e.g., `<!-- fix-preference: auto -->` or `<!-- fix-preference: review -->`).
- **fix-preference-honored**: The refactoring agent MUST honor the stored preference — committing directly for "auto", posting suggested changes for "review".

### Refactoring agent

- **dedicated-persona**: All automated fixes and refactoring MUST be applied by a single dedicated refactoring agent with its own GitHub App identity, distinct from the three phase bots.
- **fix-or-suggest**: The refactoring agent MUST commit directly if the contributor chose "fix automatically", or post GitHub suggested changes if the contributor chose "review each change".
- **scope-of-fixes**: The refactoring agent handles fixes from all phases: structural fixes from Phase 1, refactoring proposals approved by the human reviewer from Phase 2.

