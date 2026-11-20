
- The suite **MUST** include cases where a tool returns an error, an empty result, or a timeout, and assert the agent recovers (retries sensibly, picks a fallback, or reports failure) rather than hallucinating success.
- Include cases where the correct action is to call **no** tool, to confirm the agent does not invoke tools spuriously.

