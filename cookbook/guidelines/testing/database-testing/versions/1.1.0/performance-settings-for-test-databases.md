
```python
conn = sqlite3.connect(':memory:')
conn.execute("PRAGMA journal_mode = OFF")
conn.execute("PRAGMA synchronous = OFF")
```

