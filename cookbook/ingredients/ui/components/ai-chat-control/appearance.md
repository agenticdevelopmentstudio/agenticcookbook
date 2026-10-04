
### Mini variant layout

```
┌──────────────────────────────────────┐
│  User message              ▐ accent  │  ← right-aligned
│  ▌ secondary  Assistant message      │  ← left-aligned
│  ▌ red        Error message          │  ← left-aligned
│  ▌ ...                               │  ← typing indicator
├──────────────────────────────────────┤
│  [Message...                   ] [➤] │  ← input row
└──────────────────────────────────────┘
```

### Container
- **Corner radius**: 8pt
- **Border**: 1pt, system quaternary color
- **Background**: system background at 0.5 opacity
- **Mini variant height**: 200pt (fixed, not resizable)

### Message bubbles
- **Font**: System font, 12pt
- **Horizontal padding**: 8pt
- **Vertical padding**: 5pt
- **Corner radius**: 6pt
- **Text selection**: Enabled
- **Minimum spacer**: 40pt on the opposite side (prevents full-width bubbles)

| Role | Background | Foreground | Alignment |
|------|-----------|-----------|-----------|
| User | Accent color, 15% opacity | Primary | Right-aligned |
| Assistant | Secondary color, 10% opacity | Primary | Left-aligned |
| Error | Red, 10% opacity | Red | Left-aligned |

### Message area
- **Vertical spacing** between messages: 8pt
- **Padding**: 8pt all sides

### Input row
- **Font**: System font, 12pt, plain style (no border)
- **Placeholder**: "Message..."
- **HStack spacing**: 6pt
- **Horizontal padding**: 8pt
- **Vertical padding**: 6pt

### Send button
- **Icon**: arrow.up.circle.fill (SF Symbols) / equivalent per platform
- **Size**: 16pt
- **Color**: System tint/accent
- **Style**: Plain (no button chrome)

### Typing indicator
- **Animation**: Cycling dots (1→2→3→1), 0.4 second interval
- **Font**: System monospaced, 12pt
- **Color**: Secondary
- **Background**: Secondary color, 10% opacity
- **Corner radius**: 6pt
- **Alignment**: Left-aligned (same as assistant messages)

