<!-- leaf: principles/yagni · source: principles/yagni.md -->

# YAGNI

Build for today's known requirements. Speculative generality adds code that must be maintained but delivers no current value. If a future need materializes, the cost of adding it then is almost always lower than maintaining premature abstractions now.

- Before adding a parameter, config option, or extension point, confirm a current requirement demands it
- Delete dead code and unused abstractions — they are not "free" to keep around
- When someone says "we might need this later," treat that as a reason to wait, not a reason to build
