
Instead of replacing the whole row, merge at the column level. If Device A changes `title` and Device B changes `status`, both edits survive.

Requires storing the **base version** — the last-synced state — for three-way comparison:

```python
def field_level_merge(client, server, base):
    merged = {}
    for field in all_fields:
        client_changed = client[field] != base[field]
        server_changed = server[field] != base[field]
        if client_changed and not server_changed:
            merged[field] = client[field]
        elif server_changed and not client_changed:
            merged[field] = server[field]
        elif client_changed and server_changed:
            if client[field] == server[field]:
                merged[field] = client[field]   # both agree
            else:
                merged[field] = resolve_field_conflict(field, client, server)
        else:
            merged[field] = base[field]
    return merged
```

MUST identify fields that form semantic groups and resolve them atomically — for example, `quantity` and `unit_price` should not be independently merged if `total` depends on both.

cr-sqlite implements per-column CRDTs that achieve field-level merge automatically, falling back to LWW only when the same field is concurrently modified.

