<!-- leaf: principles/design-for-deletion · source: principles/design-for-deletion.md -->

# Design for deletion

Every line of code is a maintenance liability. Build disposable software, not reusable software:

- Write code that is easy to throw away without affecting the rest of the system
- Treat lines of code as lines spent — deleting code reduces maintenance cost
- Do not abstract prematurely in pursuit of reuse
- When in doubt, duplicate rather than couple
