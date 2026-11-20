
```python
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA journal_mode=WAL")
```
