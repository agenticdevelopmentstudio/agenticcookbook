<!-- leaf: principles/open-source-preference · source: principles/open-source-preference.md -->

# For novel components, prefer proven open-source solutions

When no native solution exists, research battle-tested open-source libraries and present options to the user before building a custom solution. A custom implementation can always be chosen instead, but it should be a deliberate decision, not a default.

- Before reaching outward, check what you already have: the platform's standard library and the dependencies already in the project often solve the problem — prefer those before adding anything new
- Evaluate candidates by maintenance activity, license compatibility, and community adoption before recommending
- Verify a candidate is real before adopting it: confirm the package actually exists, is actively maintained, and is widely used. Never install a package name an AI suggested without verifying it — hallucinated and typosquatted names are a live supply-chain risk
- Present at least two options with trade-offs rather than silently picking one
- If building custom, document why the available open-source options were rejected
