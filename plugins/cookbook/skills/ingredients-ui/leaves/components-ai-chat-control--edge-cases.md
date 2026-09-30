<!-- leaf: ingredients-ui/components-ai-chat-control--edge-cases · source: ingredients/ui/components/ai-chat-control.md -->

# AI Chat Control

## Edge Cases

- **Extremely long response**: Message bubble wraps text; does not truncate. Scroll area accommodates.
- **Extremely long input**: Text field accepts input without truncation. Long messages display correctly in bubble.
- **Rapid send attempts**: Only the first send is accepted while loading; subsequent attempts are ignored (block-send-while-loading).
- **Network timeout**: After 30 seconds, display timeout error message. User can retry.
- **Provider returns empty response**: Display "(Empty response)" as assistant message.
- **Provider returns malformed JSON**: Display "(Unable to parse response)" as assistant message.
- **Concurrent provider change**: If the user changes provider while a request is in flight, the in-flight response is still displayed. The next request uses the new provider.
- **Keychain unavailable**: Display error "No API key configured" (same as missing key).
