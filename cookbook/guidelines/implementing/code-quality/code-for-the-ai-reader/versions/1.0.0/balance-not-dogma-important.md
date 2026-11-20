
This guidance is in genuine tension with some human-readability norms, and you **MUST NOT** maximize machine-legibility at all costs:

- Very short files and aggressive file-splitting can aid humans but scatter related behavior an agent must assemble from many sources. Favor **locality of related behavior**.
- Heavy DRY and deep indirection trade duplication for hidden coupling. A small, explicit repetition is often easier for both readers than a clever abstraction three layers deep. Apply judgment per case.
- The claim "agents now read code more than humans do" is a **plausible direction of travel, not a measured fact** — do not cite it as an established statistic. Justify each choice by concrete readability for the next reader, human or agent, not by appeal to that trend.
- When a human-readability convention and an AI-readability heuristic conflict and the cost is low, prefer the option that keeps behavior explicit and local. When the human cost is high, weigh both and document the trade-off.

