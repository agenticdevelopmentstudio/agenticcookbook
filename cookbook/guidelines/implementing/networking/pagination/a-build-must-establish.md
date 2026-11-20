
- `should-prefer-cursor-pagination`: list endpoints return a `next_cursor` and `has_more`, or the code says why offset is used
- `should-use-offset-only-for-page-numbers-or-static-data`: every offset-paginated endpoint is one whose users need page numbers or whose data is relatively static
- `should-handle-cursor-and-offset-pagination`: the client handles both cursor-based and offset-based pagination
- `should-use-infinite-scroll-or-load-more-for-cursor`: a cursor-paged list uses infinite scroll or a "Load more" control
- `must-not-refetch-all-on-page-change`: a page change does not re-fetch the full result
- `should-send-stored-cursor-on-next-page`: the client stores the cursor and sends it on the next page request, or the build says why not
- `must-paginate-collection-endpoints`: every collection endpoint returns a paginated response, not an unbounded list
- `should-include-pagination-envelope`: every paginated response carries an envelope with `has_more` or `total`, or the build says why not
