
# Zero-downtime migrations: expand and contract

When the database is serving live traffic, a migration cannot pause the app or rewrite a whole table in place. This is the opposite of an offline table-recreate (e.g. SQLite's 12-step rebuild), which assumes nobody is reading the table.
