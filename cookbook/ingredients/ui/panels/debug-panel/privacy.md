
- **Data collected**: Feature flag overrides, experiment variant selections, analytics event log (in-memory only)
- **Storage**: Overrides in platform local storage (UserDefaults / SharedPreferences / localStorage). Event log is in-memory only.
- **Transmission**: None — debug panel data never leaves the device
- **Retention**: Overrides persist until cleared. Event log cleared on app restart.

