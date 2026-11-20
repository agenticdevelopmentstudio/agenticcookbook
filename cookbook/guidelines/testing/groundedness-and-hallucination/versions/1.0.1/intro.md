
# Groundedness and hallucination checks

For retrieval-grounded (RAG) systems, an answer is only trustworthy if each claim is supported by the retrieved context. You **MUST** measure groundedness (claim-level support) and a hallucination rate against retrieved sources, and the system **SHOULD** abstain rather than fabricate when support is missing.

