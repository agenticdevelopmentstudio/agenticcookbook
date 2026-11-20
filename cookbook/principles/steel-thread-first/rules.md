
- **should-build-the-steel-thread-first**: Before building breadth, SHOULD build the thinnest end-to-end slice that exercises every integration boundary and the deployment path — a "steel thread" or walking skeleton — and prove the whole shape connects once, end to end, then fill it in.
- **should-keep-the-thread-thin-but-complete**: Thin but complete: the thread SHOULD be one real path through every layer and boundary (UI → API → store → deploy), not a finished feature — connect the architecture before investing in any single part.
- **should-build-the-shell-only-for-the-committed-path**: This is the balance with YAGNI: SHOULD build the shell only for the path you are committed to and that is expensive to wire up later.
- **should-not-pre-build-unneeded-features**: SHOULD NOT pre-build features, options, or abstractions you don't yet need — that remains YAGNI.
- **should-front-load-risky-integrations**: Front-load the risky integrations: the thread SHOULD pierce the boundaries most likely to surprise you (auth, third-party APIs, the deploy pipeline), so failures surface while they are cheap.
- **should-validate-shape-before-breadth**: For agents: SHOULD validate the end-to-end shape before spending effort on breadth, so a wrong architecture is caught early instead of after generating volume against it.
