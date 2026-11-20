
- **should-prefer-cursor-pagination**: **Cursor pagination** SHOULD be preferred for most APIs.
  - It is stable under concurrent mutations, with consistent performance at any depth.
- **should-use-offset-only-for-page-numbers-or-static-data**: APIs SHOULD use offset pagination only when users need page numbers or data is relatively static.
- **should-handle-cursor-and-offset-pagination**: A client SHOULD handle both cursor-based pagination (`next_cursor`, `has_more`) and offset-based pagination.
- **should-use-infinite-scroll-or-load-more-for-cursor**: A client paging by cursor SHOULD use infinite scroll or a "Load more" control.
- **must-not-refetch-all-on-page-change**: A client MUST NOT re-fetch everything on a page change.
- **should-send-stored-cursor-on-next-page**: A client SHOULD store the cursor and send it on the next page request.
- **must-paginate-collection-endpoints**: Every collection endpoint MUST return a paginated response, not an unbounded list.
- **should-include-pagination-envelope**: A paginated response SHOULD carry a pagination envelope with `has_more` or `total`.
