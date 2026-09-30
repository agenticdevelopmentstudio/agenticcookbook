<!-- leaf: implement-networking/pagination · source: guidelines/implementing/networking/pagination.md -->

**Rules** (cite as `implement-networking/pagination#<slug>`):

- `cursor-pagination` SHOULD — SHOULD be preferred for most APIs — stable under concurrent mutations, consistent performance at any depth. Use offset …

# Pagination

**Cursor pagination** SHOULD be preferred for most APIs — stable under concurrent mutations, consistent
performance at any depth. Use offset pagination only when users need page numbers or data
is relatively static.

**Cursor response:**
```json
{
  "data": [ ... ],
  "pagination": {
    "next_cursor": "eyJpZCI6MTAwfQ==",
    "has_more": true
  }
}
```

**Offset response:**
```json
{
  "data": [ ... ],
  "pagination": {
    "offset": 20,
    "limit": 10,
    "total": 142
  }
}
```

References:
- [Google AIP-158: Pagination](https://google.aip.dev/158)
- [Zalando: Pagination](https://opensource.zalando.com/restful-api-guidelines/#pagination)
