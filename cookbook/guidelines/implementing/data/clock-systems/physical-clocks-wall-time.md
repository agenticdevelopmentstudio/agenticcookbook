
Wall-clock timestamps (`datetime('now')`, `Date.now()`, `System.currentTimeMillis()`) are simple but unreliable for ordering across devices.

**The problem:** Different devices have different clocks. NTP corrections, manual time changes, and clock drift can result in two devices disagreeing about which event came first — sometimes by seconds or more. A client with a fast clock will always "win" LWW conflicts regardless of actual operation order.

**When acceptable:**
- Single-user-per-record apps (no concurrent editing)
- The server assigns all timestamps (client clocks are never trusted for ordering)
- Ordering accuracy within a few seconds is sufficient

**MUST NOT use raw wall-clock time** as the sole ordering mechanism in multi-device collaborative apps.

