
```
┌──────────────────────────────────────────────────────┐
│  App (SwiftUI)                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Commands {                                       │ │
│  │    CommandGroup(replacing: .newItem) {             │ │
│  │      ┌─────────────────────────────────────────┐  │ │
│  │      │  "New Project"    Cmd-N                  │  │ │
│  │      │  "New Session"    Cmd-Shift-N            │  │ │
│  │      │  "New Workspace"  Cmd-Option-N           │  │ │
│  │      └─────────────────────────────────────────┘  │ │
│  │    }                                              │ │
│  │  }                                                │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌────────────────────────┐  ┌───────────────────────┐ │
│  │  Window A               │  │  Window B              │ │
│  │  .focusedObject(stateA) │  │  .focusedObject(stateB)│ │
│  └────────────────────────┘  └───────────────────────┘ │
│               ▲                                        │
│               │ @FocusedObject                         │
│  ┌────────────┴─────────────────────────────────────┐ │
│  │  "New Session" reads focused window's state       │ │
│  │  to create session within that window's project   │ │
│  └──────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘

New Project flow:
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌──────────────┐
│ Menu item │───▶│ NSOpenPanel│───▶│ Validate  │───▶│ Create & Open│
│ Cmd-N     │    │ (dir pick) │    │ directory  │    │ document     │
└──────────┘    └───────────┘    └───────────┘    └──────────────┘
                                       │
                                  ┌────▼─────┐
                                  │ .git?    │
                                  │ existing │
                                  │ package? │
                                  └──────────┘

New Workspace flow:
┌──────────┐    ┌───────────┐    ┌──────────────┐
│ Menu item │───▶│ NSSavePanel│───▶│ Create & Open│
│ Cmd-Opt-N │    │ (file save)│    │ document     │
└──────────┘    └───────────┘    └──────────────┘
```

