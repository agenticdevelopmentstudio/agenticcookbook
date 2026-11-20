
Limit blast radius by limiting capability, permissions, and autonomy.

- You **MUST** grant each agent/tool the least privilege needed — scoped credentials, narrow API surface, no ambient admin access.
- You **MUST** maintain an explicit allow-list of callable tools; **MUST NOT** expose open-ended capabilities (arbitrary shell, unrestricted HTTP, broad filesystem) without a specific justification and additional controls.
- You **SHOULD** require human-in-the-loop confirmation for high-impact or irreversible actions: sending money, deleting data, sending external communications, deploying, or modifying access. Make the confirmation describe the concrete effect, not just "approve?".
- You **SHOULD** rate-limit and budget tool calls to bound runaway loops (relates to LLM10: Unbounded Consumption).

