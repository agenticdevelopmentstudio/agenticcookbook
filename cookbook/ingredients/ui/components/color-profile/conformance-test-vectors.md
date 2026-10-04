
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| profile-001 | built-in-profiles | Launch fresh app | 8 built-in profiles available |
| profile-002 | stable-builtin-uuids | Reference Solarized Dark by UUID across updates | UUID is stable |
| profile-003 | duplicate-profile | Duplicate Dracula | New "Dracula Copy" profile created, editable, deletable |
| profile-004 | deletable-custom-only | Attempt to delete Solarized Dark | Delete action disabled/hidden |
| profile-005 | fallback-to-default | Set active profile to invalid UUID | Falls back to Solarized Dark |
| profile-006 | auto-appearance-mode | Set profile to auto, switch system to dark mode | Dark-appropriate colors applied |

