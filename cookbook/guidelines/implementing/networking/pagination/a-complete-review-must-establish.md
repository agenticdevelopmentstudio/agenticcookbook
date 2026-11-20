
- `should-prefer-cursor-pagination`: whether list endpoints use cursor pagination
- `should-use-offset-only-for-page-numbers-or-static-data`: whether each offset-paginated endpoint serves page numbers or relatively static data
- `should-handle-cursor-and-offset-pagination`: whether the client handles both cursor-based and offset-based pagination
- `should-use-infinite-scroll-or-load-more-for-cursor`: whether a cursor-paged list uses infinite scroll or a "Load more" control
- `must-not-refetch-all-on-page-change`: whether a page change re-fetches the full result
- `should-send-stored-cursor-on-next-page`: cursor stored and sent on next page request;
- `must-paginate-collection-endpoints`: All collection endpoints return paginated responses (not unbounded lists);
- `should-prefer-cursor-pagination`: cursor-based pagination used unless offset explicitly justified;
- `should-include-pagination-envelope`: pagination envelope present with `has_more` or `total`
