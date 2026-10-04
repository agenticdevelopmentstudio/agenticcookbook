
### Editor pane layout

```
┌────────────────────────────────────────────────────────┐
│  ▼  📄 ContentView.swift  ●                           │  ← pane header (collapsible)
├──────────────────────────────────────────────────┬─────┤
│ 1  import SwiftUI                                │▓▓▓▓▓│
│ 2                                                │▓░░▓▓│
│ 3  struct ContentView: View {                    │▓░░▓▓│
│ 4      var body: some View {                     │▓░░▓▓│
│ 5          VStack {                              │▓░░▓▓│
│ 6              Image(systemName: "globe")        │▓░░▓▓│
│ 7                  .imageScale(.large)           │▓▓▓▓▓│
│ 8                  .foregroundStyle(.tint)       │▓▓▓▓▓│
│ 9              Text("Hello, world!")             │▓▓▓▓▓│
│10          }                                     │▓▓▓▓▓│
│11          .padding()                            │▓▓▓▓▓│
│12      }                                         │     │
│13  }                                             │     │
│14                                                │     │
│                                                  │     │
└──────────────────────────────────────────────────┴─────┘
 ↑ gutter (line numbers)   ↑ editor area            ↑ minimap
```

### No file selected (empty state)

```
┌────────────────────────────────────────────────────────┐
│  ▼  Editor                                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│                                                        │
│                      📄                                │
│           Select a file to view its contents           │
│                                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Binary file placeholder

```
┌────────────────────────────────────────────────────────┐
│  ▼  📄 image.png                                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│                                                        │
│                      ⚠️                                │
│           Cannot display this file type                │
│                                                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

- **Gutter**: Monospaced, right-aligned line numbers, secondary text color, subtle separator from editor area
- **Editor area**: Monospaced font (Menlo 13pt default), themed background per color-profile
- **Minimap**: ~60pt wide trailing column, scaled-down representation of the file
- **Dirty indicator**: Small filled circle (●) adjacent to the filename in the pane header, or platform-standard edited-document indicator

