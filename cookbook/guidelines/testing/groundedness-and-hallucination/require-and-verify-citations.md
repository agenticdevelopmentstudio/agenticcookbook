
- The system **SHOULD** emit citations to specific source spans (doc id + offset/quote), not just document-level pointers.
- You **MUST** verify cited spans rather than trust them: re-check that each quoted span exists in the source and entails the claim. Models cite plausibly but incorrectly, so an unverified citation is not evidence of groundedness.

