
You MUST check these before writing a custom implementation, nearest first:

1. **The platform / standard library** — the language or OS may already provide it (see native-controls).
2. **Dependencies you already have** — the capability may already live in a library the project uses. Check before adding anything.
3. **Your own and shared codebases** — a sibling project or shared module may already implement it; reuse beats a parallel copy (see dry).
4. **Proven open source** — battle-tested libraries, evaluated per open-source-preference.

