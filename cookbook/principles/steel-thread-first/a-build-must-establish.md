
- `should-build-the-steel-thread-first`: a thinnest end-to-end slice through every integration boundary and the deployment path was proven before breadth was built, or the work says why not
- `should-keep-the-thread-thin-but-complete`: the thread is one real path through every layer and boundary (UI → API → store → deploy), not a finished feature, or the work says why not
- `should-build-the-shell-only-for-the-committed-path`: the shell covers only the path committed to that is expensive to wire up later, or the work says why not
- `should-not-pre-build-unneeded-features`: no feature, option, or abstraction was pre-built before it was needed, or the work says why
- `should-front-load-risky-integrations`: the thread pierces the boundaries most likely to surprise (auth, third-party APIs, the deploy pipeline), or the work says why not
- `should-validate-shape-before-breadth`: the agent validated the end-to-end shape before spending effort on breadth, or the work says why not
