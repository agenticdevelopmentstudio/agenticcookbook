
- Chunk documents before embedding; chunk size and overlap directly determine retrieval quality. There is no universal best size — start with a moderate window with small overlap and tune against a retrieval eval set.
- **MUST** store, with each chunk, a stable reference back to its source document and position so retrieved context is attributable and citable.
- Prefer chunking on semantic/structural boundaries (headings, paragraphs, code blocks) over fixed character counts where the source structure allows it.

