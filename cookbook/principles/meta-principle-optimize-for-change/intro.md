
# Meta-Principle: Optimize for Change

Every principle above is a strategy for making future change cheaper and safer. When evaluating any technical decision, the primary question is: "Does this make future change easier or harder?"

- Before committing to an architecture, ask: "What would it cost to reverse this in six months?"
- Prefer decisions that keep options open over decisions that lock in a technology or pattern
- When two approaches are otherwise equal, choose the one that is easier to change later
- Treat **cognitive load** as the metric the structural principles serve: simplicity, locality of behavior, and boundaries all exist to reduce the cognitive load of understanding and changing the system, so a design — or an agent workflow — **SHOULD** be tested by whether it lowers that load. Caveat: AI and multi-agent tooling can *shift* load onto the human orchestrator rather than remove it, so use cognitive load as a lens (proxies: fan-out, file count, time-to-onboard), not a thresholded metric.

