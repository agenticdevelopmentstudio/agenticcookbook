
- When retrieval returns no supporting evidence, the system **SHOULD** abstain ("I don't have enough information") rather than answer from parametric memory.
- You **MUST** include "unanswerable from context" cases in the eval set and score abstention explicitly — otherwise a model that always answers looks perfect on answerable queries while hallucinating on the rest.
- An abstention is a **correct** outcome when context is insufficient; do not penalize it as a miss in aggregate scoring.

