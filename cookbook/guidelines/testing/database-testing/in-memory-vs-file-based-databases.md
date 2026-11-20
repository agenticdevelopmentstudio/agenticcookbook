
```python
import sqlite3

conn = sqlite3.connect(':memory:')
conn.executescript(open('schema.sql').read())
# ... run tests ...
conn.close()  # database destroyed automatically
```

