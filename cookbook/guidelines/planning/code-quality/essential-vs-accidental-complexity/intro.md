
# Essential vs accidental complexity

Fred Brooks's *No Silver Bullet* (1986; reprinted in *The Mythical Man-Month*, 1995) splits software difficulty into **essential** complexity — the irreducible interlocking of the problem domain itself — and **accidental** (incidental) complexity — everything else: boilerplate, scaffolding, syntax, glue code, build tooling, and ceremony. You **SHOULD** use this split as a thinking tool when scoping a new module: it tells you where an agent can help and where human design judgment must stay in the loop.

