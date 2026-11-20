
Last-write-wins, across two peers:

```python
def test_last_write_wins(peer_a, peer_b):
    # Both peers start from the same record
    peer_a.execute("UPDATE tasks SET title = 'A title', updated_at = '2026-04-06T10:00:00Z' WHERE id = 't1'")
    peer_b.execute("UPDATE tasks SET title = 'B title', updated_at = '2026-04-06T11:00:00Z' WHERE id = 't1'")

    # Apply peer_a's changes to peer_b (B's timestamp is later)
    changes_a = export_changes(peer_a)
    apply_changes(peer_b, changes_a)

    result = peer_b.execute("SELECT title FROM tasks WHERE id = 't1'").fetchone()
    assert result[0] == 'B title'  # last-write-wins: B's later timestamp survives
```

