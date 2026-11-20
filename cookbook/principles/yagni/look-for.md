
- `should-confirm-requirement-before-adding-extension-points`: a new parameter, config option, or extension point that no current requirement demands
- `should-delete-dead-code-and-unused-abstractions`: dead code or an unused abstraction left in place
- `should-treat-might-need-later-as-reason-to-wait`: code built because "we might need this later," with no current need behind it
- `should-build-for-todays-known-requirements`: Build skills and agents for today's known requirements;
- `should-confirm-requirement-before-adding-extension-points`: speculative generality in prompts (adding "in case we need it" context, future-proofing flags, unused parameters) adds maintenance cost with no current value;
- `must-not-build-speculative-generality`: no speculative abstractions, hooks for future features, or generalization beyond current need;
- `should-treat-might-need-later-as-reason-to-wait`: cost of premature abstraction (ongoing maintenance) exceeds cost of adding it later when needed
