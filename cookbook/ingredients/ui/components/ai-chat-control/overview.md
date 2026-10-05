
A compact, inline chat control for conversing with a configured AI provider. Supports multi-turn conversation with scrollable message history, text input, and asynchronous response handling. Designed for embedding in settings panels, sidebars, or inspector views. A full-size variant for standalone windows can compose this control with additional chrome (toolbar, model picker, conversation management).

This spec covers the chat control only — provider configuration (API key, model, endpoint) is managed externally via the AI settings panel (see `ingredient.ui.panel.ai-settings-panel`).

### Terminology

| Term | Definition |
|------|-----------|
| Message | A single unit of conversation: user input, assistant response, or error |
| Conversation | An ordered sequence of messages in a single chat session |
| Provider | The AI backend that generates responses (Anthropic, OpenAI, Google, Custom) |
| Typing indicator | Animated placeholder shown while waiting for an AI response |
| Mini variant | Fixed-height version for embedding in panels (~200pt) |
| Full variant | Flexible-height version for standalone windows (future) |

