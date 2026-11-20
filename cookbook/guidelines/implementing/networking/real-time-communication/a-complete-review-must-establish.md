
- `should-choose-the-simplest-technique`: whether each real-time feature uses the simplest technique from the table that meets its needs
- `should-start-with-sse`: whether server-push uses SSE
- `should-use-websocket-only-for-bidirectional-streaming`: whether every WebSocket carries bidirectional streaming
- `may-poll-for-very-low-frequency`: whether polling is limited to a fallback for very low frequency updates
- `must-reconnect-with-backoff`: reconnection logic present for SSE/WebSocket connections;
- `must-reconnect-with-backoff`: reconnection uses backoff (not immediate retry loop)
