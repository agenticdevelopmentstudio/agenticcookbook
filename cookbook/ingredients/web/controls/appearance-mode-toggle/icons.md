
- **dark-mode-icon**: The forced dark mode MUST display a moon icon.
- **light-mode-icon**: The forced light mode MUST display a sun icon.
- **auto-mode-icon-base**: In `auto` mode, the icon MUST be the same sun or moon icon that matches the current system appearance (moon if system is dark, sun if system is light).
- **auto-mode-indicator**: In `auto` mode, a small sync/refresh badge (circular arrows) MUST appear in the bottom-right corner of the button, overlapping the base icon slightly. The badge MUST be roughly half the size of the base icon (e.g., if the icon is 20px, the badge is ~10px). It MUST be tinted in the site's highlight/accent color. The base icon underneath MUST remain fully visible and unchanged — the badge is a corner annotation, not a full overlay.
- **auto-indicator-no-full-overlay**: The auto indicator MUST NOT be rendered at the same size as the base icon or centered over it. A full-size overlay obscures the sun/moon and makes the mode unreadable. The indicator is a small corner badge only.
- **icon-size-consistent**: All three modes MUST render their base icons at the same size. The auto indicator badge MUST NOT cause the button to grow or shift layout.

