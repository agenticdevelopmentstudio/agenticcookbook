---
name: verify-skills-and-agents
description: "Verify a review's findings on skills and agents: check each finding against the rules in review-skills-and-agents."
---

# verify-skills-and-agents

Verify a worker's review against the same rules it used.

1. The rules are the leaves of `review-skills-and-agents`: read `../review-skills-and-agents/index.md` and the
   leaves the worker cited or should have.
2. For each `violated` finding: is the violation real in the code, and does it
   cite the rule that it breaks? Reject what fails either test.
3. For each `clean` claim on a MUST rule: is it plausible from the code? Flag
   the ones that are not.
4. A rule the worker gave no status is a coverage gap; report it.

Leaves: [../review-skills-and-agents/index.md](../review-skills-and-agents/index.md) — one line per leaf. Leaves are plain files, not skills; read them with the Read tool.
