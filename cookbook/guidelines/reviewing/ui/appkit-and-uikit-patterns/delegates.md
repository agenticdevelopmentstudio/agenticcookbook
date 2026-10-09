
- Every delegate and data-source property is `weak`. Flag a strong one unless a comment explains the ownership.
- Delegate protocols are narrow. No callback carries mutable shared state.

