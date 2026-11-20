
The DORA research program (Accelerate / State of DevOps) identifies trunk-based development as a capability that predicts higher software delivery performance — fewer active branches, branches that live less than a day, and no code-freeze/integration phases. Treat this as a validated *correlation with* delivery performance, not a guarantee; the mechanism is that small, frequent integrations shrink merge conflicts and keep feedback fast.

- Long-lived feature branches accumulate divergence; the eventual merge is large, risky, and hard to review — the opposite of small-reversible-decisions.
- Daily integration surfaces conflicts while they are small and the context is fresh.
- A continuously releasable trunk decouples *merging* from *releasing*: code ships dark, then is enabled via a flag.

