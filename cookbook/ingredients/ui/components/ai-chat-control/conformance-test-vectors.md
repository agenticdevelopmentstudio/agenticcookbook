
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| chat-001 | ordered-message-history | Send "Hello", receive response, send "How are you?" | Three messages in order: user, assistant, user |
| chat-002 | vertical-scroll | Send enough messages to overflow visible area | Message area scrolls; earlier messages accessible by scrolling up |
| chat-003 | auto-scroll-new-message, auto-scroll-typing-indicator, scroll-animation-timing | Send a message | View auto-scrolls to new message with 0.2s ease-out animation |
| chat-004 | enter-key-submit | Type "Hello" and press Enter | Message sent; input cleared |
| chat-005 | send-button-disabled-empty | Input field is empty, observe send button | Send button is disabled |
| chat-006 | send-button-disabled-empty | Input field contains only whitespace | Send button is disabled |
| chat-007 | block-send-while-loading | Send message while response is in progress | Second send is blocked |
| chat-008 | send-full-history | Send "Hello", receive response, send "What did I just say?" | Second request includes both previous messages in history |
| chat-009 | secure-key-retrieval | Send message, inspect memory after response | API key is not retained in view model properties |
| chat-010 | check-ai-enabled | Disable AI features, send message | Error: "AI features are disabled — enable them above" |
| chat-011 | no-api-key-error | No API key configured, send message | Error: "No API key configured" |
| chat-012 | inline-error-display | Send message with invalid API key | Error message displayed inline, not as alert |
| chat-013 | recoverable-after-error | Receive an error, then send another message | Second message sends successfully (not stuck) |
| chat-014 | extract-provider-error | Send message, server returns 401 with `{"error":{"message":"invalid key"}}` | Error shows "invalid key", not "HTTP 401" |
| chat-015 | clear-history-action, clear-removes-all | Send messages, then clear history | All messages removed; message area is empty |
| chat-016 | ephemeral-history | Send messages, quit app, relaunch | Chat history is empty after relaunch |

