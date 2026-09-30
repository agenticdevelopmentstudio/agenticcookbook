<!-- leaf: ingredients-ui/components-ai-chat-control--part-2 · source: ingredients/ui/components/ai-chat-control.md -->

# AI Chat Control — continued (part 2)

**Rules** (cite as `ingredients-ui/components-ai-chat-control--part-2#<slug>`):

- `decision` SHOULD — No streaming support in v1.0.0. Rationale: Streaming adds complexity (SSE parsing, incremental rendering) without …

## Platform Notes

- **SwiftUI (macOS / iOS / visionOS)**: Use `ScrollViewReader` with `ScrollView` containing `LazyVStack` for the message area. Use `.id()` on each message for scroll targeting. Input field: `TextField` with `.plain` style and `.onSubmit` for Enter key handling. Send button: `Button` with `.plain` style and SF Symbol icon. Typing indicator: `Timer.publish` driving dot count with modulo arithmetic. API calls: `Task.detached(priority: .userInitiated)` with `URLSession.shared.data(for:)`. Update UI via `await MainActor.run {}`. Read API key with `SecItemCopyMatching` at request time.
- **Compose (Android)**: Use `LazyColumn` with `rememberLazyListState()` for auto-scroll. Input: `OutlinedTextField` with `keyboardActions` for Enter. Send button: `IconButton` with Material icon. Typing indicator: `LaunchedEffect` with `delay`. API calls: `viewModelScope.launch(Dispatchers.IO)` with `HttpURLConnection` or OkHttp. Read API key from `EncryptedSharedPreferences` at request time.
- **React / Web**: Use a `div` with `overflow-y: auto` and `scrollIntoView()` for auto-scroll. Input: `<input>` with `onKeyDown` for Enter. Send button: `<button>` with icon. Typing indicator: `setInterval` cycling dot count. API calls: `fetch` with `AbortController` for timeout. API key: retrieve from server-side secure storage via authenticated endpoint.

## Design Decisions

**Mini variant only (v1.0.0)**: The initial spec covers only the mini variant (fixed 200pt height, embedded in settings). The full variant (flexible height, standalone window, conversation management) is deferred to a future version.

**Decision**: No streaming support in v1.0.0.
**Rationale**: Streaming adds complexity (SSE parsing, incremental rendering) without significant benefit at 256 max tokens. The full variant SHOULD add streaming.
**Approved**: pending

**Decision**: Conversation history is ephemeral (not persisted).
**Rationale**: The primary use case is quick verification of AI configuration. Persistent history adds storage and privacy concerns without matching the use case.
**Approved**: pending
