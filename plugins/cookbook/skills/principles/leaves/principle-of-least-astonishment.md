<!-- leaf: principles/principle-of-least-astonishment · source: principles/principle-of-least-astonishment.md -->

# Principle of least astonishment

APIs, UI, and system behavior should match what users and callers expect. If a name suggests one behavior, it must deliver that behavior. Side effects should be obvious from the API signature.

- Name functions and types so a reader can predict what they do without reading the implementation
- If a method mutates state, make that visible in the name or signature — never hide side effects
- Follow platform naming conventions even when you prefer a different style
- When reviewing code, ask: "Would a new team member be surprised by this behavior?"
