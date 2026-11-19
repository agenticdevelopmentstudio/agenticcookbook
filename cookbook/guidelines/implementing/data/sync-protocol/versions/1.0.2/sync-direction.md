
**Pull-only:** Client polls the server for new data. The server is the source of truth. Use for read-heavy apps (catalogs, news feeds, configuration).

**Push-only:** Client sends local changes when connectivity returns. Use for write-heavy offline scenarios (field data collection, surveys).

**Bidirectional (standard pattern):** Push local changes and pull server changes in a single round trip:

```
1. Push  — send dirty local records to server
2. Server validates, resolves conflicts, returns results
3. Pull  — receive server changes (including other devices)
4. Apply — upsert server records locally, clear dirty flags
5. Checkpoint — store the server's current sync version
```

SHOULD combine push and pull into a single HTTP request. Separate push and pull calls double the round trips, which is costly on high-latency mobile networks.

**Shoulder-tap optimization:** Rather than polling, have the server send a lightweight notification (push notification, WebSocket message, or SSE event) that new data is available. The client then pulls the actual data. This achieves low latency without a persistent connection for data transfer.

