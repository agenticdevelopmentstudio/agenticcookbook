<!-- leaf: implement-platform-integration/search-integration · source: guidelines/implementing/platform-integration/search-integration.md -->

**Rules** (cite as `implement-platform-integration/search-integration#<slug>`):

- `app-content-discoverable-through-platform-system` SHOULD — App content SHOULD be discoverable through the platform's system search, enabling users to find content without opening …
- `indexed-item-deep-link-back-relevant` MUST — Each indexed item MUST deep link back to the relevant content

# Search integration

App content SHOULD be discoverable through the platform's system search, enabling users to find content without opening the app. Search integration turns the app from an island into a participant in the user's information flow.

- Index content that users would reasonably search for — documents, contacts, messages, settings
- Keep the search index current — add items when created, remove when deleted
- Each indexed item MUST deep link back to the relevant content
- Include rich metadata (thumbnails, descriptions, categories) for meaningful search results

## Apple (iOS / macOS)

Use Core Spotlight (`CSSearchableItem`, `CSSearchableItemAttributeSet`) to index content. On iOS 17+, conform entities to `IndexedEntity` for semantic indexing with natural language support. Support `NSUserActivity` donation for Handoff-eligible items to appear in Spotlight suggestions.

## Android

Use Firebase App Indexing or `AppIndexingApi` for on-device search integration. Declare searchable content in `searchable.xml` and implement `SearchableInfo`. Support Google Assistant via structured content markup.

## Windows

Use the Windows Search indexer with `ISearchManager` and property handlers. Register file type associations and protocol handlers so content appears in Start menu search. For UWP/WinUI, use `SearchPane` or in-app search with system integration.

## Web

Use structured data (JSON-LD, Schema.org) for search engine discoverability. Implement OpenGraph and Twitter Card meta tags. Support the Web App Manifest for PWA search integration. Ensure server-side rendering or pre-rendering for crawlability.
