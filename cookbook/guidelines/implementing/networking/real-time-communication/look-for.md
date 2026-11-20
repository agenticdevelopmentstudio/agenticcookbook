
- `should-choose-the-simplest-technique`: a more complex technique than the feature's direction and frequency need (WebSocket for one-way push, push for a once-a-minute value).
- `should-start-with-sse`: server-push built on WebSocket or polling where SSE would serve.
- `should-use-websocket-only-for-bidirectional-streaming`: a WebSocket that carries traffic in one direction only.
- `may-poll-for-very-low-frequency`: polling used for updates more frequent than very low frequency.
- `must-reconnect-with-backoff`: reconnection with backoff required for persistent connections
