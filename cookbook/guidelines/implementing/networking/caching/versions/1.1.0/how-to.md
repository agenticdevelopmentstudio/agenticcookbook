
The headers, by kind of response:

```
Cache-Control: public, max-age=31536000, immutable
```

```
Cache-Control: private, max-age=60
```

```
Cache-Control: no-store
```

**Conditional requests**, step by step:
1. Server sends `ETag: "abc123"`
2. Client revalidates with `If-None-Match: "abc123"`
3. Server responds 304 Not Modified (no body) or 200 with new data

- Framework support: React Query, SWR, Apollo Client all handle this natively
