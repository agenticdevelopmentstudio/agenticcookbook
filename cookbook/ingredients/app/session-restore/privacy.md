
- **Data collected**: Paths of the documents open at quit time.
- **Storage**: Platform persistence (`UserDefaults`, `SharedPreferences`, `localStorage`), on-device only.
- **Transmission**: None — the URL list never leaves the device.
- **Retention**: Until replaced by the next quit; an empty list is saved when no documents are open.

