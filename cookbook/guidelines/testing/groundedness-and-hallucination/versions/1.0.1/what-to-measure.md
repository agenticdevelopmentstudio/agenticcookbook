
| Metric | Question it answers | Target |
|--------|--------------------|--------|
| Groundedness / faithfulness | Is every claim entailed by retrieved context? | Maximize |
| Hallucination rate | Fraction of answers with ≥1 unsupported claim | Minimize |
| Citation accuracy | Do cited spans actually support the claim? | Maximize |
| Retrieval recall@k | Did retrieval surface the needed evidence? | Maximize |
| Abstention correctness | Does it decline when context is insufficient? | Maximize |

- Score groundedness at **claim granularity**, not whole-answer granularity: decompose the answer into atomic claims and label each `supported` / `partial` / `unsupported` (the FActScore decomposition approach, [arxiv.org/abs/2305.14251](https://arxiv.org/abs/2305.14251)).
- You **MUST** measure retrieval quality (recall@k, context precision) independently — most ungrounded answers trace to missing evidence, not generation, and fixing the generator cannot recover evidence that was never retrieved.

