
# JSON columns and generated columns

SQLite stores JSON as `TEXT`. The built-in `json1` functions let you query into JSON values without fully deserializing them. When combined with generated columns and indexes, JSON fields can be queried with B-tree speed.

