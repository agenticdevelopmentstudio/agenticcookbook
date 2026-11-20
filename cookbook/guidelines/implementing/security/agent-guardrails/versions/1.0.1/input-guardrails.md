
Validate and moderate everything reaching the model.

- **off-band-input**: The system **MUST** screen input for prompt injection, jailbreaks, off-topic requests, and unsafe content before it reaches the model.
- **untrusted-context**: Content from tools, retrieval, files, or other users **MUST** be treated as untrusted and labeled as data, never merged into the instruction channel.
- **layered-defense**: Input checks **SHOULD** combine cheap deterministic rules (length, encoding, allow-listed topics) with a moderation/classifier pass; prompt-level instructions **MAY** supplement but **MUST NOT** be the only defense.

