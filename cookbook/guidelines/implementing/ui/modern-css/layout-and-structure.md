
- Author component responsiveness with **container queries** keyed to the component's own size: wrap the component in a query container (`container-type: inline-size`) and use `@container`, so the component adapts wherever it is placed.
- Use **viewport media queries** only for genuinely page-level concerns (overall page shell, print, `prefers-*` user preferences).
- Use **subgrid** to align nested items to an ancestor grid's tracks. Provide a non-subgrid fallback (explicit tracks) only if you target pre-cutoff versions.
- Prefer **logical properties** (`margin-inline`, `inset-block`) over physical ones for internationalization-ready layout.

