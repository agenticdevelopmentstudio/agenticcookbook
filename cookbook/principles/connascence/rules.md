
- **should-minimize-overall-connascence**: SHOULD **minimize** overall connascence by keeping coupled things close.
- **should-rank-coupling-on-three-axes**: SHOULD rank, not just detect: judge each coupling on three axes — strength (how hard it is to change in concert), degree (how many elements share it), and locality (how far apart they live).
- **must-weaken-coupling-with-distance**: MUST **weaken** strong forms into weaker ones as the distance between them grows: the farther apart two coupled elements live, the weaker the form between them must be — e.g. positional args → named parameters → a typed message across a boundary.
- **should-prefer-weakest-form**: SHOULD prefer the weakest form that does the job: replace positional arguments with named ones, magic numbers with named constants, duck-typed shapes with explicit types.
- **should-use-connascence-as-review-vocabulary**: SHOULD use connascence as the vocabulary for coupling reviews: "connascence of position across a module boundary — convert to connascence of name" is a decision, not a matter of taste.
- **should-use-full-lattice-only-when-axes-do-not-settle**: SHOULD reach for the full lattice only when the three axes above don't settle the call.
