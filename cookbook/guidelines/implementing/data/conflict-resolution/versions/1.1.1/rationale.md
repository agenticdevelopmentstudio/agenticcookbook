
- `must-have-explicit-conflict-strategy`: "No strategy" means silent data loss.
- `should-use-hlc-for-lww`: Physical clocks on different devices can diverge by seconds or more, causing the wrong write to win.

