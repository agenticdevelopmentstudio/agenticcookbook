
# Foreign keys and referential integrity

SQLite supports foreign key constraints but disables them by default. This is the most common SQLite pitfall: developers declare FK relationships, ship code, and discover constraints were silently never enforced.

