
# Connascence

Coupling is not binary — it has a *strength* you can rank, and a good refactor moves it to a weaker form. Connascence names the ways two pieces of code must change together. Two rules govern it: **minimize** overall connascence by keeping coupled things close, and **weaken** strong forms into weaker ones as the distance between them grows. This turns "this feels too coupled" into an objective call.

- Rank, don't just detect: judge each coupling on three axes — strength (how hard it is to change in concert), degree (how many elements share it), and locality (how far apart they live). A positional dependency is stronger than a name dependency; a shared magic value (connascence of meaning) is stronger still.
- Weaken with distance: the same coupling is cheap inside one function and expensive across two services. The farther apart two coupled elements live, the weaker the form between them must be — e.g. positional args → named parameters → a typed message across a boundary.
- Prefer the weakest form that does the job: replace positional arguments with named ones, magic numbers with named constants, duck-typed shapes with explicit types.
- Use it as the vocabulary for coupling reviews: "connascence of position across a module boundary — convert to connascence of name" is a decision, not a matter of taste.
- Reference lattice (weak → strong): static — name < type < meaning < position < algorithm; dynamic — execution < timing < value < identity. Reach for the full lattice only when the three axes above don't settle the call.

