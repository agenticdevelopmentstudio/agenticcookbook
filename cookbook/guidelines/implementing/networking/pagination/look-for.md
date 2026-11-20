
- `should-prefer-cursor-pagination`: a list endpoint paginated by offset where neither page numbers nor relatively static data call for it.
- `should-use-offset-only-for-page-numbers-or-static-data`: offset pagination over data that changes under concurrent mutations, with no need for page numbers.
- `should-handle-cursor-and-offset-pagination`: Client handles cursor-based pagination (`next_cursor`, `has_more`) and offset-based;
- `should-use-infinite-scroll-or-load-more-for-cursor`: infinite scroll or "Load more" for cursor;
- `must-not-refetch-all-on-page-change`: no full re-fetch on page change
- `should-send-stored-cursor-on-next-page`: a client that does not store the cursor and send it on the next page request
- `must-paginate-collection-endpoints`: a collection endpoint that returns an unbounded list
- `should-include-pagination-envelope`: a paginated response with no envelope carrying `has_more` or `total`
