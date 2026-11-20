# Devteam text batch 5 (R7)

All 18 topics placed: `roles gaps` reports 0 lacking for every speciality, `roles check` exits 0, `roles lossless` exits 0, each bumped and approved. Nothing was left unplaced.

Base note: `data/conflict-resolution`, `data/offline-first-architecture` and `data/sync-tooling` fail `roles lossless --base 0005775` with "planning/data/<topic> is not in 0005775" (each absorbed a folded copy). They pass with `--base 1a179b2`, the base recorded in their own `lossless.json`, so that base was used for those three.

No contradictions (R4) found in any topic. No sentence was left unplaced.

## cookbook-compliance
- new rules: none
- reader-specific: none

## source-fidelity
- new rules: none
- reader-specific: none

## delete-what-you-supersede
- new rules: none. All ten sentences are process wording about the evidence unit and what a finding contains, placed under `must-update-every-caller`.
- reader-specific: "Work through the leads in the `__evidence__/hygiene-scan` unit and confirm each one against the code."; "The scan is a list of leads, not findings: a lead is a text match, so open the file and decide whether the reference really points at the removed or renamed thing, or at something unrelated that shares the name."; "File one finding per surviving reference (or one per file when a file has several), and say which of the removed or renamed symbols it still names."; "If the unit is absent, the change removed and renamed nothing the scan could see; do not go hunting for leads of your own."; "Each finding names the surviving reference (file and line) and the removed or renamed symbol or path it still points at;"; "every lead you dismiss was opened and judged, not skipped;"; "matches that only share a substring or an unrelated name are not reported;"; "the symbol's own new definition is not reported."

## xcode-project-hygiene
- new rules: none (cited `should-leave-target-level-settings-empty`, `should-add-entitlements-only-for-used-capabilities`)
- reader-specific: none

## conflict-resolution, offline-first-architecture, sync-tooling
- new rules: none
- reader-specific: "A review passes when it establishes every item above." (placed under the first rule of each topic: `must-have-explicit-conflict-strategy`, `must-enable-wal-for-synced-databases`, `should-choose-tool-by-requirements`; it concerns the whole bar, not one rule)

## rtl-support
- new rules: none
- reader-specific: "and confirm the layout has been tested with an RTL locale enabled."

## pagination
- new rules (all from api/pagination-client and api/pagination text; each also has a build-bar line and a line in the other review part):
  - `should-handle-cursor-and-offset-pagination`: "A client SHOULD handle both cursor-based pagination (`next_cursor`, `has_more`) and offset-based pagination." from "Client handles cursor-based pagination (`next_cursor`, `has_more`) and offset-based;" (SHOULD, plain check)
  - `should-use-infinite-scroll-or-load-more-for-cursor`: "A client paging by cursor SHOULD use infinite scroll or a \"Load more\" control." from "infinite scroll or \"Load more\" for cursor;" (SHOULD)
  - `must-not-refetch-all-on-page-change`: "A client MUST NOT re-fetch everything on a page change." from "no full re-fetch on page change" (MUST NOT, "no" wording)
  - `should-send-stored-cursor-on-next-page`: "A client SHOULD store the cursor and send it on the next page request." from "cursor stored and sent on next page request;" (SHOULD)
  - `must-paginate-collection-endpoints`: "Every collection endpoint MUST return a paginated response, not an unbounded list." from "All collection endpoints return paginated responses (not unbounded lists);" (MUST, "all" wording)
  - `should-include-pagination-envelope`: "A paginated response SHOULD carry a pagination envelope with `has_more` or `total`." from "pagination envelope present with `has_more` or `total`" (SHOULD)
- "cursor-based pagination used unless offset explicitly justified;" cited existing `should-prefer-cursor-pagination`.
- reader-specific: none

## notifications
- new rules: `android-do-not-send-without-runtime-permission`: "MUST NOT send notifications without runtime permission on Android 13+." from "no notifications sent without runtime permission on Android 13+" (MUST NOT)
- reader-specific: none

## widgets-and-glanceable-surfaces
- new rules: none
- reader-specific: none

## security-headers-checklist
- new rules: none
- reader-specific: none

## test-doubles
- new rules: `should-use-platform-appropriate-mock-library`: "SHOULD use the platform-appropriate mock library (NSubstitute/.NET, MockK/Kotlin, pytest-mock/Python, vitest/TS)." from "platform-appropriate mock library used (NSubstitute/.NET, MockK/Kotlin, pytest-mock/Python, vitest/TS)" (SHOULD)
- reader-specific: none

## feedback-patterns
- new rules: `should-implement-toasts-banners-and-dialogs`: "SHOULD implement toast/snackbar (auto-dismiss 3-5s), inline alerts/banners, and modal dialogs." from "Implement toast/snackbar (auto-dismiss 3-5s), inline alerts/banners, and modal dialogs;" (SHOULD)
- reader-specific: none

## high-dpi-display-scaling
- new rules: none
- reader-specific: none

## algorithmic-complexity
- new rules:
  - `should-classify-complexity-of-changed-algorithms`: "SHOULD identify every algorithm or data-structure choice the change introduces or changes, with a complexity classification, and flag the performance-critical paths it touches. A change that introduces none SHOULD be explicitly cleared." from "Any algorithm or data-structure choice the diff introduces or changes is identified with a complexity classification, and performance-critical paths it touches are flagged;" and "a diff that introduces none is explicitly cleared." (SHOULD, plain check)
  - `must-limit-scope-to-the-change`: "Scope MUST be the change under review, NOT a whole-codebase inventory." from "Scope is the change under review — NOT a whole-codebase inventory." (MUST, the NOT is emphatic)
- reader-specific: "In the code **this diff adds or changes**, locate sorting, searching, graph traversal, caching strategies, data structure choices, recursion patterns, and nested loop depth."; "Any algorithm or data-structure choice the diff introduces or changes is identified ..."; "a diff that introduces none is explicitly cleared." (all name "the diff")

## native-controls
- new rules:
  - `should-prefer-winui3-controls-over-custom-drawn`: "On Windows, SHOULD use WinUI 3 controls over custom-drawn equivalents." from "WinUI 3 controls over custom-drawn equivalents;" and "No custom reimplementations of standard WinUI 3 controls;" (SHOULD; the bar's "No" is stricter, a possible R4 tension left as one rule)
  - `should-use-windows-app-sdk-for-system-integration`: "On Windows, SHOULD use Windows App SDK APIs for system integration (file access, notifications, and background tasks)." from "Windows App SDK APIs for system integration;" and "system APIs used for file access, notifications, and background tasks;" (SHOULD)
  - `should-document-native-control-deviations`: "SHOULD document deviations from native controls with their rationale." from "deviations from native controls documented with rationale" (SHOULD)
- reader-specific: none

## principle-of-least-astonishment
- new rules:
  - `must-not-give-get-endpoints-side-effects`: "GET endpoints MUST NOT have side effects." from "No GET endpoints with side effects;" (MUST NOT)
  - `must-make-idempotent-methods-idempotent`: "Idempotent methods (GET/PUT/DELETE) MUST actually be idempotent." from "idempotent methods (GET/PUT/DELETE) are actually idempotent;" (MUST)
  - `must-not-hide-side-effects-of-primary-actions`: "Primary actions MUST NOT have hidden side effects." from "no hidden side effects from primary actions;" (MUST NOT)
- reader-specific: none
