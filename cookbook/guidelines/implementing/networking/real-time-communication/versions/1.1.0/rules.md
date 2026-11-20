
- **should-choose-the-simplest-technique**: Real-time features SHOULD use the simplest technique that meets their needs.
- **should-start-with-sse**: Server-push SHOULD **start with SSE**.
  - It has built-in reconnection, works over standard HTTP, and is sufficient for 80%+ of "real-time" needs.
- **should-use-websocket-only-for-bidirectional-streaming**: WebSocket SHOULD only be used when bidirectional streaming is required.
- **may-poll-for-very-low-frequency**: Polling MAY be used as a fallback for very low frequency updates.
