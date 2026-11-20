
- **should-confirm-requirement-before-adding-extension-points**: Before adding a parameter, config option, or extension point, SHOULD confirm a current requirement demands it.
- **should-delete-dead-code-and-unused-abstractions**: SHOULD delete dead code and unused abstractions — they are not "free" to keep around.
- **should-treat-might-need-later-as-reason-to-wait**: When someone says "we might need this later," SHOULD treat that as a reason to wait, not a reason to build.
- **should-build-for-todays-known-requirements**: Code SHOULD be built for today's known requirements, addressing actual current workflows and not hypothetical future ones.
- **must-not-build-speculative-generality**: Code MUST NOT contain speculative abstractions, hooks for future features, unused abstraction layers, extension points or generalization beyond what current requirements demand.
