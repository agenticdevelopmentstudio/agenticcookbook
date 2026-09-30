<!-- leaf: principles/steel-thread-first · source: principles/steel-thread-first.md -->

# Steel thread first

Before building breadth, build the thinnest end-to-end slice that exercises every integration boundary and the deployment path — a "steel thread" or walking skeleton. This is the disciplined answer to "when is scaffolding for a larger design justified?": prove the whole shape connects once, end to end, then fill it in. It bounds the cost of a wrong architecture without inviting speculative generality.

- Thin but complete: one real path through every layer and boundary (UI → API → store → deploy), not a finished feature — connect the architecture before investing in any single part.
- This is the balance with YAGNI: build the shell only for the path you are committed to and that is expensive to wire up later. Do not pre-build features, options, or abstractions you don't yet need — that remains YAGNI.
- Front-load the risky integrations: the thread should pierce the boundaries most likely to surprise you (auth, third-party APIs, the deploy pipeline), so failures surface while they are cheap.
- For agents: validate the end-to-end shape before spending effort on breadth, so a wrong architecture is caught early instead of after generating volume against it.
