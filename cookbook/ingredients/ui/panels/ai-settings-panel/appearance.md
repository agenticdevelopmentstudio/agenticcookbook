
```
┌──────────────────────────────────────────────────┐
│ AI                                               │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌─ General ──────────────────────────────────┐  │
│  │ Enable AI Features           [  toggle  ]  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Provider ─────────────────────────────────┐  │
│  │ Provider          [Claude (Anthropic)  ▾]  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Model ────────────────────────────────────┐  │
│  │ Model             [claude-haiku-4-5... ▾]  │  │
│  │ Custom Model      [                     ]  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Authentication ───────────────────────────┐  │
│  │ ••••••••••••                      [Clear]  │  │
│  │ API Key           [Enter new key...     ]  │  │
│  │ [Test API Key]  ✅ API key is valid        │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Quick Chat ───────────────────────────────┐  │
│  │ (see ingredient.ui.component.ai-chat-control)            │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

With Custom provider selected, the Endpoint section appears above Quick Chat:

```
│  ┌─ Endpoint ─────────────────────────────────┐  │
│  │ Base URL          [https://api.example.com] │  │
│  └────────────────────────────────────────────┘  │
```

- **Layout**: Vertical form with grouped sections, consistent with settings window content panel style
- **Controls**: Native controls only — toggle, picker, secure text field, text field, stepper, button
- **Status dot**: 8pt circle, filled — green (`#34C759` / systemGreen), red (`#FF3B30` / systemRed), gray (`#8E8E93` / systemGray)
- **Section headers**: Platform-native grouped form section headers
- **Disabled state**: All controls below the enable toggle use reduced opacity (0.4) when AI features are disabled

