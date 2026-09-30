<!-- leaf: ingredients-ui/components-ai-chat-control--states · source: ingredients/ui/components/ai-chat-control.md -->

# AI Chat Control

## States

| State | Behavior |
|-------|----------|
| Empty | No messages; message area is blank; input field active |
| Conversing | Messages visible; input field active; send button enabled when text present |
| Loading | Typing indicator visible; send button replaced with spinner; input field active but send disabled |
| Error displayed | Error message visible in red; input field active; user can continue chatting |
| AI disabled | Sending blocked; error message shown if attempted |
| No API key | Sending blocked; error message shown if attempted |
