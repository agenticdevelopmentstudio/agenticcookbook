
Test databases SHOULD use relaxed durability settings. Test data is disposable — crash safety is irrelevant.

```python
conn = sqlite3.connect(':memory:')
conn.execute("PRAGMA journal_mode = OFF")
conn.execute("PRAGMA synchronous = OFF")
```

These settings are UNSAFE for production but maximize test throughput. Apply them only in test fixtures.

