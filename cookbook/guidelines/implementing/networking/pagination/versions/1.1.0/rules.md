
- **should-prefer-cursor-pagination**: **Cursor pagination** SHOULD be preferred for most APIs.
  - It is stable under concurrent mutations, with consistent performance at any depth.
- **should-use-offset-only-for-page-numbers-or-static-data**: APIs SHOULD use offset pagination only when users need page numbers or data is relatively static.
