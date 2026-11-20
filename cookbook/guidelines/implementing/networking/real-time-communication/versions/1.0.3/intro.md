
# Real-Time Communication

Choose the simplest technique that meets your needs.

| Technique | Direction | Use When |
|-----------|-----------|----------|
| Polling | Client-pull | Low frequency (<1/min), simplicity paramount |
| SSE | Server-push | Notifications, live feeds, dashboards, progress |
| WebSocket | Bidirectional | Chat, multiplayer, collaborative editing |

**Start with SSE** for server-push — it has built-in reconnection, works over standard HTTP,
and is sufficient for 80%+ of "real-time" needs. WebSocket SHOULD only be used when
bidirectional streaming is required. Polling MAY be used as a fallback for very low frequency updates.

References:
- [MDN: Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
- [MDN: WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [RFC 6455: WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455)

