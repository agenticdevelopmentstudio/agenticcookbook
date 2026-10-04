
- **no-fouc**: The page MUST NOT flash the wrong appearance on load. An inline `<script>` in `<head>` (before any stylesheet or framework code) MUST read the stored forced mode from site settings and apply the appropriate CSS class to `<html>` synchronously. If no forced mode is stored, it MUST check `prefers-color-scheme` and apply the matching class. This script MUST be wrapped in try/catch so a settings read failure defaults to no class (light mode).

