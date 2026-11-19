
The UI MUST read exclusively from local SQLite, never from the network. Changes appear instantly after the local write — the user does not wait for the server.

```
User action
  → Write to local SQLite + enqueue to outbox (one transaction)
  → UI reads from SQLite (instant — no network round trip)
  → Background: sync worker sends outbox to server
      → If server confirms: mark outbox entry as done
      → If server rejects: roll back local change, notify user
```

This means every write the user sees is "optimistic" — it is applied locally before the server confirms it. Design the UI to handle the rare case where the server rejects a write.

