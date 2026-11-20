
- `should-build-the-steel-thread-first`: breadth built before any end-to-end slice through every integration boundary and the deployment path
- `should-keep-the-thread-thin-but-complete`: a thread that skips a layer or boundary, or a finished feature built before the architecture is connected
- `should-build-the-shell-only-for-the-committed-path`: shell built for a path no one is committed to, or one cheap to wire up later
- `should-not-pre-build-unneeded-features`: features, options, or abstractions built into the thread ahead of need
- `should-front-load-risky-integrations`: a thread that avoids the riskiest boundaries (auth, third-party APIs, the deploy pipeline)
- `should-validate-shape-before-breadth`: an agent generating volume before the end-to-end shape was validated
