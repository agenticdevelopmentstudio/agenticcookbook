
| Metric | Question it answers | Target |
|--------|--------------------|--------|
| Groundedness / faithfulness | Is every claim entailed by retrieved context? | Maximize |
| Hallucination rate | Fraction of answers with ≥1 unsupported claim | Minimize |
| Citation accuracy | Do cited spans actually support the claim? | Maximize |
| Retrieval recall@k | Did retrieval surface the needed evidence? | Maximize |
| Abstention correctness | Does it decline when context is insufficient? | Maximize |
