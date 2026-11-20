# Phase 2 batch 4 report

Twenty topics: five language guidelines and fifteen networking guidelines, each converted to roled parts with
named rules and the three bar parts. The change is to format only. No research was added, and no rule's substance
changed. Each topic has one commit, made with `commit_topic.py`.

## Across the batch

- **Language topics held folded reviewer checklists.** objective-c, powershell, python, ruby and swift each
  carried a reviewer copy as extra parts (`introduction` plus checklist parts with `-2` suffixes). That text
  became the `look-for` part (**moved**). Each line is prefixed with the names of the rules it covers, and lines
  were **authored** only for rules it did not cover. Their second "Why this matters" part was renamed "Why a
  review checklist" so that the two rationale headings differ.
- **Networking topics were mostly a single intro.** The statement paragraph stays in `intro` (GF-01). Tables,
  code blocks and samples become `how-to` or `examples` parts, and source lists become `references`. All three
  bar parts are **authored** unless a topic's notes say otherwise.
- **Own-base sentences can never be obsolete.** `cookr roles lossless` refuses `obsolete` for any sentence of a
  topic's own base text ("only a folded copy's may be"). Old labels such as "References:" and
  "**Client-side invalidation:**" were therefore kept verbatim, as group labels or part lead-ins, rather than
  recorded as obsolete. That is why every obsolete count is 0.
- **Wrapped lines count as separate sentences.** Where a source wrapped one sentence across lines
  (real-time-communication, timeouts, api-design), lossless lists each fragment, and each fragment has its own
  moved entry pointing at the same rule.
- **Tripwires.** A split that drops a keyword from either half is refused (http-conditional-requests' "SHOULD
  support ... and MAY require", now one rule). "one" counts as the number 1 (idempotency-keys), so the rule keeps
  the word.
- **FM-13.** None of this batch's source text contains "TODO", "FIXME", "TBD", "placeholder" or "fill in",
  so no word was respelled and nothing needed restoring.

## cookbook/guidelines/implementing/language/objective-c

Commit `10fec523`; 29 rules; lossless.json: 20 moved (reworded), 0 obsolete.

**promoted** (reworded from keyword-less source, 19):
- "Name methods so a call site reads as a phrase, with a label for every argument after the first." → `should-name-call-sites-as-phrases`: "Methods SHOULD be named so a call site reads as a phrase, with a label for every argument after the first."
- "Follow the conventions of the framework you extend rather than inventing new vocabulary." → `should-follow-framework-conventions`: "Code SHOULD follow the conventions of the framework it extends rather than inventing new vocabulary."
- "Prefix every public class, protocol, enum and constant with a project prefix, because Objective-C has no namespaces." → `should-prefix-public-symbols`: "Every public class, protocol, enum and constant SHOULD carry a project prefix, because Objective-C has no namespaces."
- "Mark designated initializers (`NS_DESIGNATED_INITIALIZER`) and forbid inherited ones that cannot work (`NS_UNAVAILABLE`), so a half-initialized object cannot be built." → `should-mark-designated-initializers`: "Designated initializers SHOULD be marked (`NS_DESIGNATED_INITIALIZER`) and inherited ones that cannot work forbidden (`NS_UNAVAILABLE`), so a half-initialized object cannot be built."
- "Report recoverable failure with a `BOOL` or object return plus an `NSError **` out-parameter, not with exceptions." → `should-report-recoverable-failure-with-nserror`: "Recoverable failure SHOULD be reported with a `BOOL` or object return plus an `NSError **` out-parameter, not with exceptions."
- "Build with ARC (`-fobjc-arc`)." → `must-compile-with-arc`: "Objective-C code in a mixed or legacy Apple codebase MUST compile with ARC: build with ARC (`-fobjc-arc`)."
- "Do not call `retain`, `release` or `autorelease` by hand in an ARC file, and do not mix manual reference counting into a target by file-level flags without a written reason." → `should-not-call-retain-release-by-hand`: "Code SHOULD NOT call `retain`, `release` or `autorelease` by hand in an ARC file."; `should-not-mix-manual-reference-counting`: "Code SHOULD NOT mix manual reference counting into a target by file-level flags without a written reason."
- "Declare object properties with an explicit ownership attribute: `strong` for owned objects, `weak` for back-references and delegates, `copy` for `NSString`, `NSArray`, `NSDictionary` and block properties whose mutable subclasses a caller could pass in." → `should-declare-explicit-property-ownership`: "Object properties SHOULD be declared with an explicit ownership attribute: `strong` for owned objects, `weak` for back-references and delegates, `copy` for `NSString`, `NSArray`, `NSDictionary` and block properties whose mutable subclasses a caller could pass in."
- "Reach for `__unsafe_unretained` only where the compiler cannot express the lifetime, and say why in a comment." → `should-limit-unsafe-unretained`: "Code SHOULD reach for `__unsafe_unretained` only where the compiler cannot express the lifetime, and say why in a comment."
- "Name your own methods with that rule in mind, because ARC applies it to them too." → `should-name-methods-by-method-family`: "Your own methods SHOULD be named with the method-family rule in mind, because ARC applies it to them too."
- "Break retain cycles in blocks." → `should-break-retain-cycles-in-blocks`: "Code SHOULD break retain cycles in blocks."
- "Wrap long-running loops that create many temporary objects in `@autoreleasepool { }` so memory does not grow until the loop ends." → `should-wrap-temporary-heavy-loops-in-autoreleasepool`: "Long-running loops that create many temporary objects SHOULD be wrapped in `@autoreleasepool { }` so memory does not grow until the loop ends."
- "Use `__bridge` when ownership does not change, `__bridge_retained` to hand an object to Core Foundation (you now `CFRelease` it), and `__bridge_transfer` to take a Core Foundation object into ARC (ARC now releases it)." → `should-pick-bridge-cast-by-ownership`: "Code SHOULD use `__bridge` when ownership does not change, `__bridge_retained` to hand an object to Core Foundation (you now `CFRelease` it), and `__bridge_transfer` to take a Core Foundation object into ARC (ARC now releases it)."
- "Never use a bare C cast between the two worlds in ARC code." → `must-not-use-bare-bridging-casts`: "Code MUST NOT use a bare C cast between the two worlds in ARC code."
- "Design the Objective-C API so it needs no Swift-side fix-ups: declare generics on collections (`NSArray<MyListItem *> *`) so Swift sees `[MyListItem]`, and use designated nullability." → `should-need-no-swift-fix-ups`: "The Objective-C API SHOULD be designed so it needs no Swift-side fix-ups: declare generics on collections (`NSArray<MyListItem *> *`) so Swift sees `[MyListItem]`, and use designated nullability."
- "When the Swift form should differ from the Objective-C form (a tuple instead of out-parameters, reordered or renamed arguments), mark the Objective-C declaration `NS_REFINED_FOR_SWIFT` and write the Swift-facing API in a Swift extension." → `should-refine-for-swift-in-an-extension`: "When the Swift form should differ from the Objective-C form (a tuple instead of out-parameters, reordered or renamed arguments), the Objective-C declaration SHOULD be marked `NS_REFINED_FOR_SWIFT` and the Swift-facing API written in a Swift extension."
- "Keep the Objective-C implementation as the single source of behavior." → `should-keep-objective-c-as-single-source`: "The Objective-C implementation SHOULD stay the single source of behavior."
- "Use `nullable`, `nonnull` and `null_resettable` on properties, parameters and return types; use `_Nullable` and `_Nonnull` where the simple forms do not fit, such as `_Nullable id * _Nonnull`." → `should-use-nullability-qualifiers`: "Code SHOULD use `nullable`, `nonnull` and `null_resettable` on properties, parameters and return types, and `_Nullable` and `_Nonnull` where the simple forms do not fit, such as `_Nullable id * _Nonnull`."
- "`typedef` types are not assumed non-null even inside an audited region, so annotate each use." → `should-annotate-each-typedef-use`: "`typedef` types are not assumed non-null even inside an audited region, so each use SHOULD be annotated."
- extra promoted: should-remove-observers-at-teardown from reviewer checklist line "Timers, notification observers and KVO registrations are removed in `dealloc` or an earlier teardown, and do not keep their target alive." (line stays verbatim in look-for) -> "Timers, notification observers and KVO registrations SHOULD be removed in `dealloc` or an earlier teardown, and SHOULD NOT keep their target alive."
- intro MUSTs (ARC, nullability, Swift import) and "Do not write new Objective-C where Swift will do" restated as rules; intro kept verbatim. should-not-write-new-objective-c is promoted from "Do not write new Objective-C where Swift will do" (intro, kept).
- bars: look-for MOVED (folded reviewer checklist: introduction, ownership, retain-cycles, core-foundation-bridging, nullability-2, swift-import, errors-and-naming), each line labelled with its rules, plus 7 lines authored for rules it did not cover; review-bar authored; build-bar authored.
- why-this-matters-2 heading renamed "Why a review checklist" (was a second "Why this matters").
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/language/powershell

Commit `d5b2522b`; 21 rules; lossless.json: 7 moved (reworded), 0 obsolete.

**promoted** (reworded from keyword-less source, 1):
- "The verbs `ForEach`, `Ping`, `Sort` and `Tee` are reserved for built-in commands." → `should-not-use-reserved-verbs`: "The verbs `ForEach`, `Ping`, `Sort` and `Tee` are reserved for built-in commands, so your own functions SHOULD NOT use them."
- extra promoted: should-follow-shell-script-rules from intro "The general script rules in Shell scripts (...) (small functions, a `main` that only calls) apply here too." (intro kept verbatim) -> "... SHOULD apply to PowerShell scripts and modules too."
- pipeline-output keeps its two explanatory bullets (streams, redirection) as how-to.
- bars: look-for MOVED (folded checklist: introduction, strict-mode-and-errors, output, naming, state-changing-functions), lines labelled, plus 3 authored lines; review-bar authored; build-bar authored. why-this-matters-2 heading renamed "Why a review checklist".
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/language/python

Commit `7d8860fd`; 36 rules; lossless.json: 32 moved (reworded), 0 obsolete.

**promoted** (reworded from keyword-less source, 32):
- "Catch the narrowest exception that you can handle." → `should-catch-narrowest-exception`: "SHOULD catch the narrowest exception that you can handle."
- "Never write a bare `except:`, and do not catch `Exception` except at a process boundary that logs and exits." → `must-not-use-bare-except`: "MUST NOT write a bare `except:`."; `should-not-catch-exception-outside-boundary`: "SHOULD NOT catch `Exception` except at a process boundary that logs and exits."
- "Define your own errors as subclasses of `Exception`, named with the suffix `Error`." → `should-name-errors-with-error-suffix`: "SHOULD define your own errors as subclasses of `Exception`, named with the suffix `Error`."
- "When you translate an exception, chain it: `raise ConfigError("...") from err`." → `should-chain-translated-exceptions`: "When you translate an exception, SHOULD chain it: `raise ConfigError("...") from err`."
- "Use `from None` only to hide an implementation detail on purpose." → `should-use-from-none-only-on-purpose`: "SHOULD use `from None` only to hide an implementation detail on purpose."
- "Keep the `try` body small." → `should-keep-try-bodies-small`: "SHOULD keep the `try` body small."
- "Put code that runs only on success in `else`, and cleanup in `finally`." → `should-use-else-and-finally`: "SHOULD put code that runs only on success in `else`, and cleanup in `finally`."
- "Never `return`, `break` or `continue` out of a `finally` block; the 3.14 interpreter warns about it (PEP 765)." → `must-not-leave-finally-by-jump`: "MUST NOT `return`, `break` or `continue` out of a `finally` block; the 3.14 interpreter warns about it (PEP 765)."
- "Add context to an in-flight exception with `add_note()` instead of wrapping it where you have nothing to add." → `should-add-note-instead-of-wrapping`: "SHOULD add context to an in-flight exception with `add_note()` instead of wrapping it where you have nothing to add."
- "Put optional extras in `[project.optional-dependencies]` and command-line entry points in `[project.scripts]`." → `should-use-project-tables-for-extras-and-scripts`: "SHOULD put optional extras in `[project.optional-dependencies]` and command-line entry points in `[project.scripts]`."
- "Do not write a `setup.py` for a new project." → `should-not-write-setup-py`: "SHOULD NOT write a `setup.py` for a new project."
- "Declare `requires-python` to match the oldest interpreter you test." → `should-match-requires-python-to-oldest-tested`: "SHOULD declare `requires-python` to match the oldest interpreter you test."
- "A typed library ships a `py.typed` marker file in the package (PEP 561) so type checkers use its annotations." → `should-ship-py-typed`: "A typed library SHOULD ship a `py.typed` marker file in the package (PEP 561) so type checkers use its annotations."
- "Use `pathlib.Path`, not string concatenation or `os.path`." → `should-use-pathlib`: "SHOULD use `pathlib.Path`, not string concatenation or `os.path`."
- "Join with `/`, read and write with `read_text` and `write_text`, and always pass `encoding="utf-8"`." → `should-join-read-and-write-with-path-methods`: "SHOULD join with `/`, and read and write with `read_text` and `write_text`."; `must-pass-utf-8-encoding`: "Reading and writing text MUST always pass `encoding="utf-8"`."
- "Create directories with `mkdir(parents=True, exist_ok=True)` and search with `glob` and `rglob`." → `should-make-and-search-directories-with-path`: "SHOULD create directories with `mkdir(parents=True, exist_ok=True)` and search with `glob` and `rglob`."
- "Resolve a path before you test whether it lies under a root." → `should-resolve-before-containment-check`: "SHOULD resolve a path before you test whether it lies under a root."
- "Run external programs with `subprocess.run`, passing the command as a list: `subprocess.run(["git", "status"], check=True)`." → `should-run-commands-as-lists`: "SHOULD run external programs with `subprocess.run`, passing the command as a list: `subprocess.run(["git", "status"], check=True)`."
- "Never use `shell=True` with a string that contains any value you did not write yourself." → `must-not-shell-out-foreign-values`: "MUST NOT use `shell=True` with a string that contains any value you did not write yourself."
- "If a shell is truly required, quote each interpolated value with `shlex.quote`." → `should-shlex-quote-when-a-shell-is-required`: "If a shell is truly required, SHOULD quote each interpolated value with `shlex.quote`."
- "Pass `check=True` so a non-zero exit raises `CalledProcessError`, or inspect `returncode` on purpose." → `should-check-exit-status`: "SHOULD pass `check=True` so a non-zero exit raises `CalledProcessError`, or inspect `returncode` on purpose."
- "Pass `timeout=` for any command that could hang." → `should-pass-timeout-to-hanging-commands`: "SHOULD pass `timeout=` for any command that could hang."
- "Use `capture_output=True` with `text=True` to read output." → `should-capture-output-as-text`: "SHOULD use `capture_output=True` with `text=True` to read output."
- "Do not combine `capture_output` with explicit `stdout` or `stderr` arguments." → `should-not-mix-capture-output-and-streams`: "SHOULD NOT combine `capture_output` with explicit `stdout` or `stderr` arguments."
- "Build it from `os.environ` plus your changes unless you want a clean one." → `should-build-env-from-os-environ`: "SHOULD build `env` from `os.environ` plus your changes unless you want a clean one."
- "Annotate every function signature and every public attribute." → `should-annotate-signatures-and-public-attributes`: "SHOULD annotate every function signature and every public attribute."
- "Run a type checker in strict mode in CI (for mypy, `--strict`, which includes `--disallow-untyped-defs`)." → `should-type-check-strictly-in-ci`: "SHOULD run a type checker in strict mode in CI (for mypy, `--strict`, which includes `--disallow-untyped-defs`)."
- "Do not silence a checker with a blanket `# type: ignore`; ignore one error code and say why." → `should-not-blanket-ignore-types`: "SHOULD NOT silence a checker with a blanket `# type: ignore`; ignore one error code and say why."
- "Start it with `python -I` (isolated mode), which ignores the script directory, the user site-packages directory and every `PYTHON*` environment variable." → `should-start-untrusted-scripts-isolated`: "A script run from a directory you do not control SHOULD be started with `python -I` (isolated mode), which ignores the script directory, the user site-packages directory and every `PYTHON*` environment variable."
- "Be aware that `-m` puts the current directory on `sys.path`, so do not use `-m` from an untrusted working directory." → `should-not-use-m-from-untrusted-directory`: "`-m` puts the current directory on `sys.path`, so SHOULD NOT use `-m` from an untrusted working directory."
- "Never run an interpreter inside a directory of downloaded files." → `must-not-run-interpreter-in-downloads`: "MUST NOT run an interpreter inside a directory of downloaded files."
- "Run it from your own directory and pass the downloaded path as an argument." → `should-pass-downloads-as-arguments`: "SHOULD run the interpreter from your own directory and pass the downloaded path as an argument."
- bars: look-for MOVED (folded checklist: introduction, packaging-2, typing-2, subprocesses-2, paths-2, exceptions-2, untrusted-directories-2), labelled, plus 11 authored lines; review-bar authored; build-bar authored. why-this-matters-2 heading renamed.
- "always pass encoding" -> MUST (must-pass-utf-8-encoding); "Never ..." -> MUST NOT (bare except, shell=True, interpreter in downloads, finally jumps).
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/language/ruby

Commit `ef40a1f5`; 32 rules; lossless.json: 4 moved (reworded), 0 obsolete.

**promoted** (reworded from keyword-less source, 0):
- none from reworded sentences.
- extra promoted: should-treat-ruby-as-code from intro "Treat a Ruby file as code, not as a shell script with syntax." (intro kept verbatim) -> "A Ruby file SHOULD be treated as code, not as a shell script with syntax."
- bars: look-for MOVED (folded checklist: introduction, header-and-strings, processes, values-and-errors, keyword-arguments-2, style-and-dependencies), labelled, plus 6 authored lines; review-bar authored; build-bar authored. why-this-matters-2 heading renamed.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/language/swift

Commit `297e1ba6`; 25 rules; lossless.json: 0 moved (reworded), 0 obsolete.

- every rule keeps its source sentence verbatim (explanations as sub-bullets), so lossless.json has no entries.
- extra promoted from the folded reviewer "linked-reviews" lines (kept verbatim in look-for): "Concurrency: isolation and `Sendable` follow the strict-concurrency guideline." -> should-follow-strict-concurrency-guideline "Isolation and `Sendable` SHOULD follow the strict-concurrency guideline (link)."; "UI framework: Use AppKit and UIKit, not SwiftUI (link)." -> should-use-appkit-and-uikit "The UI framework SHOULD be AppKit and UIKit, not SwiftUI (link)."; "Lint and tests pass under the repository's own configuration." -> should-pass-repository-lint-and-tests "Lint and tests SHOULD pass under the repository's own configuration."
- related-swift-guidelines (the link list) -> references.
- bars: look-for MOVED (folded checklist: introduction, types, optionals-2, errors, access-control-2, linked-reviews), labelled, plus 3 authored lines; review-bar authored; build-bar authored. why-this-matters-2 heading renamed.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/ai-cost-management

Commit `7ea72649`; 12 rules; lossless.json: 8 moved (reworded), 0 obsolete.

**promoted** (reworded from keyword-less source, 2):
- "Cache key includes: model, prompt template ID, template variables, temperature (if 0)." → `should-key-cache-on-model-template-and-variables`: "The cache key SHOULD include: model, prompt template ID, template variables, temperature (if 0)."
- "**prompt-optimization**: Prompt length directly affects cost." → `should-review-prompts-for-token-efficiency`: "Prompts SHOULD be reviewed for token efficiency."
- the Requirements part's bold-labelled paragraphs became rules under descriptive names; the old labels (response-caching, cost-budgets, tiered-model-selection, batch-over-realtime, cost-per-request-tracking, provider-fallback, prompt-optimization) are why those sentences are reworded entries.
- intro MUST ("Systems MUST treat AI calls as a managed resource...") restated as must-manage-ai-calls-as-a-resource; intro kept.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/api-design

Commit `25eeeb9a`; 12 rules; lossless.json: 4 moved (reworded), 0 obsolete.

- promoted: "Use REST with consistent conventions." -> should-use-consistent-rest "APIs SHOULD use REST with consistent conventions."; "Follow the platform API guidelines (Microsoft, Google, Zalando) for details" -> should-follow-platform-api-guidelines "APIs SHOULD follow the platform API guidelines (Microsoft, Google, Zalando) for details."; "Query params for filtering/sorting: ..." -> should-filter-and-sort-with-query-params "Filtering and sorting SHOULD use query params: ..."; the HTTP methods table -> should-follow-http-method-semantics "Each HTTP method SHOULD carry the semantics, idempotency and success code the HTTP methods table gives it."; "Status codes — use the right one:" -> should-use-the-right-status-code "Responses SHOULD use the right status code, from the status codes listed."; "**Versioning:** URL path versioning (`/v1/users`)." -> should-version-in-the-url-path "APIs SHOULD use URL path versioning (`/v1/users`)."; "Bump major version only for breaking changes." -> should-bump-major-only-for-breaking-changes "APIs SHOULD bump the major version only for breaking changes."
- intro keeps its statement paragraph (GF-01); the methods table -> how-to part http-methods; the status-code list -> how-to part status-codes; "Simple, explicit, industry consensus." -> rationale.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/caching

Commit `1d348366`; 8 rules; lossless.json: 5 moved (reworded), 0 obsolete.

- promoted: "Use HTTP caching headers." -> should-use-http-caching-headers "Caching SHOULD use HTTP caching headers."; "The server controls cache policy; the client honors it." -> should-let-the-server-set-cache-policy "The server SHOULD control cache policy, and the client SHOULD honor it."; "**Immutable assets** (versioned JS/CSS/images): `Cache-Control: public, max-age=31536000, immutable`" -> should-cache-immutable-assets-for-a-year "**Immutable assets** (versioned JS/CSS/images) SHOULD be sent with `Cache-Control: public, max-age=31536000, immutable`."; "**Dynamic but cacheable** (API responses): `Cache-Control: private, max-age=60`" -> should-cache-dynamic-responses-privately "... SHOULD be sent with `Cache-Control: private, max-age=60`."; "**Conditional requests** — use ETags to avoid re-downloading unchanged data:" -> should-revalidate-with-etags "**Conditional requests** SHOULD use ETags to avoid re-downloading unchanged data."; "Stale-while-revalidate: serve cached data immediately, refresh in background" -> should-stale-while-revalidate "Clients SHOULD stale-while-revalidate: serve cached data immediately, refresh in background."
- the header code blocks, the ETag steps and the framework-support line -> how-to part; the source list (with its "References:" label) -> references part.
- note: cookr refuses `obsolete` for any sentence of the topic's own base (only a folded copy's may be), so old labels such as "References:" and "**Client-side invalidation:**" are kept verbatim instead.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/error-responses

Commit `3d1d8753`; 5 rules; lossless.json: 1 moved (reworded), 0 obsolete.

- promoted: "Add extension fields (`errors`, `trace_id`) as needed" -> may-add-extension-fields "Error responses MAY add extension fields (`errors`, `trace_id`) as needed." (MAY, because "as needed" makes it optional; the plain-imperative default would be SHOULD).
- the intro's lead-in "...with `Content-Type: application/problem+json`:" now ends with a period (GF-01 statement); the field list (kept verbatim) -> how-to part "The fields"; the JSON sample -> examples. The "detail" and "instance" field descriptions carry no requirement and stay in the field list.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/http-conditional-requests

Commit `35911c17`; 13 rules; lossless.json: 3 moved (reworded), 0 obsolete.

- promoted: "Use both: `If-Match` for correctness under concurrent edits, idempotency keys for retry safety." -> should-use-if-match-and-idempotency-keys-together "Writes SHOULD use both: ..."; "Surface `412` distinctly from `409 Conflict`: ..." -> should-surface-412-apart-from-409 "Clients and servers SHOULD surface `412` distinctly from `409 Conflict`: ..."; "Behind proxies/CDNs, ensure ETags are passed through unmodified; some intermediaries rewrite or drop them." -> should-pass-etags-through-intermediaries "Behind proxies/CDNs, deployments SHOULD ensure ETags are passed through unmodified; some intermediaries rewrite or drop them."
- the four section parts (etags-as-validators, efficient-reads, optimistic-concurrency, boundaries-and-pitfalls) became the rules part with their headings as bold group labels; the `If-Match: *` / `If-None-Match: *` semantics line -> how-to; the lost-update guard and "Distinct from idempotency keys" explanations -> rationale. The SHOULD-support/MAY-require sentence stays one rule (should-support-and-may-require-if-match) because cookr's tripwire refuses a split that drops the MAY from either half.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/idempotency-keys

Commit `b055c6e9`; 21 rules; lossless.json: 13 moved (reworded), 0 obsolete.

- promoted (keyword-less source -> rule): "Do not add one out of habit (yagni)." -> should-not-add-keys-out-of-habit "On `GET`, `HEAD`, `PUT` or `DELETE`, endpoints SHOULD NOT add one (an idempotency key) out of habit (yagni)."; "The client sends `Idempotency-Key: <opaque-value>`." -> should-send-the-key-in-the-header "The client SHOULD send `Idempotency-Key: <opaque-value>`."; "Store the tuple `(principal, endpoint, key)`." -> should-store-the-principal-endpoint-key-tuple "The server SHOULD store the tuple `(principal, endpoint, key)`."; "**Fingerprint the request.** Compute a hash of the request payload (and any semantically significant headers). Store it alongside the key." -> should-fingerprint-the-request "The server SHOULD fingerprint the request: compute a hash ... and store it alongside the key."; "**New key:** acquire a lock on the key, then execute the operation. On completion, persist the key → {...} and release the lock." -> should-lock-new-keys-before-executing "For a **new key**, the server SHOULD acquire a lock on the key, then execute the operation; on completion, persist ... and release the lock."; "Use a row lock, advisory lock, or atomic conditional insert — not a read-then-write race." -> should-lock-atomically "The server SHOULD use a row lock, ..."; "Persist key records durably (...)" -> should-persist-key-records-durably "The server SHOULD persist key records durably (...)"; "Keep the TTL longer than the client's maximum retry window." -> should-outlast-the-retry-window "The server SHOULD keep the TTL longer ..."; "Only finalize (persist as replayable) once the side effect has committed." -> should-finalize-after-commit "The server SHOULD only finalize ..."; "Generate the key **once per logical operation**, ..." -> should-generate-one-key-per-operation "The client SHOULD generate the key **once per logical operation**, ..."; "A fresh user-initiated action gets a fresh key." -> should-use-a-fresh-key-per-user-action "A fresh user-initiated action SHOULD get a fresh key."; anti-patterns (kept verbatim in look-for) -> "Deriving the key from a timestamp or auto-increment — low entropy invites collisions." -> should-not-derive-keys-from-timestamps "Keys SHOULD NOT be derived from a timestamp or auto-increment — low entropy invites collisions."; "Treating a `409`/`422` from key handling as a transient error and retrying blindly (see ...)." -> should-not-retry-key-rejections-blindly "Clients SHOULD NOT treat a `409`/`422` from key handling as a transient error and retry blindly (see ...)."; "Caching only the status code and not the body, so a replay returns an incomplete response." -> should-not-cache-status-without-body "The server SHOULD NOT cache only the status code and not the body, so a replay returns an incomplete response."
- "Failing fast here surfaces a client bug instead of double-charging." and "Recording the key before the operation succeeds risks replaying ..." -> rationale. Section headings kept as bold group labels in rules (including the step label "**Look up the key.**", which cookr does not allow as obsolete).
- intro's "treat the spec as in-progress/forecast, not a finalized RFC" stays in the intro as reader guidance about the spec; it is not made a rule.
- bars: look-for MOVED in part (the three Anti-patterns lines, verbatim) + 18 authored lines; review-bar authored; build-bar authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/mcp-server-design

Commit `1a16a02a`; 30 rules; lossless.json: 19 moved (reworded), 0 obsolete.

**promoted** (reworded from keyword-less source, 19):
- "Set `annotations` to describe tool behavior so hosts can apply policy." → `should-set-annotations`: "A server SHOULD set `annotations` to describe tool behavior so hosts can apply policy."
- "Pick by purpose, not convenience." → `should-pick-primitives-by-purpose`: "A server SHOULD pick each primitive by purpose, not convenience."
- "Do not expose read-only context as a tool merely because tools are easier to wire up; that puts routing load on the model and invites accidental invocation." → `should-not-expose-read-only-context-as-tools`: "A server SHOULD NOT expose read-only context as a tool merely because tools are easier to wire up; that puts routing load on the model and invites accidental invocation."
- "The spec distinguishes two error channels — use both correctly (fail-fast at the right layer)." → `should-use-both-error-channels`: "The spec distinguishes two error channels, and a server SHOULD use both correctly (fail-fast at the right layer)."
- "**Tool execution errors** (API failure, validation, business-logic): return them **in the result** with `isError: true` and an actionable message." → `should-return-tool-errors-in-the-result`: "**Tool execution errors** (API failure, validation, business-logic) SHOULD be returned **in the result** with `isError: true` and an actionable message."
- "**Protocol errors** (unknown tool, malformed request): return a JSON-RPC `error`." → `should-return-protocol-errors-as-json-rpc`: "**Protocol errors** (unknown tool, malformed request) SHOULD be returned as a JSON-RPC `error`."
- "Do not throw a protocol error for a recoverable tool failure — the model loses the signal it needs to retry." → `should-not-throw-protocol-errors-for-tool-failures`: "A server SHOULD NOT throw a protocol error for a recoverable tool failure — the model loses the signal it needs to retry."
- "**Pin to a dated spec revision.** Default to the stable **2025-11-25** revision unless the host requires an older one." → `should-pin-a-dated-spec-revision`: "A server SHOULD pin to a dated spec revision."; `should-default-to-the-stable-revision`: "A server SHOULD default to the stable **2025-11-25** revision unless the host requires an older one."
- "Negotiate the revision during initialization rather than hard-coding it." → `should-negotiate-the-revision`: "A server SHOULD negotiate the revision during initialization rather than hard-coding it."
- "Treat any release-candidate or draft revision as a forecast and gate it behind explicit opt-in." → `should-gate-draft-revisions`: "A server SHOULD treat any release-candidate or draft revision as a forecast and gate it behind explicit opt-in."
- "Assume a human-in-the-loop may gate invocations; write descriptions and errors that make consent decisions clear." → `should-write-for-consent`: "A server SHOULD assume a human-in-the-loop may gate invocations, and write descriptions and errors that make consent decisions clear."
- "For backward compatibility, also serialize the structured result as JSON in a `text` content block." → `should-also-return-text-json`: "For backward compatibility, a tool SHOULD also serialize the structured result as JSON in a `text` content block."
- "Sanitize outputs and never leak secrets or internal identifiers the host should not see." → `must-not-leak-secrets-in-outputs`: "A server SHOULD sanitize outputs and MUST NOT leak secrets or internal identifiers the host should not see."
- "Keep them unique within the server." → `should-keep-tool-names-unique`: "A server SHOULD keep tool names unique within the server."
- "Use the optional `title` for a human-readable display label; keep `name` stable as the machine identifier." → `should-use-title-for-display`: "A tool SHOULD use the optional `title` for a human-readable display label and keep `name` stable as the machine identifier."
- "Define a strict `inputSchema` (JSON Schema, defaults to 2020-12)." → `should-define-a-strict-input-schema`: "A tool SHOULD define a strict `inputSchema` (JSON Schema, defaults to 2020-12)."
- "For zero-parameter tools, use `{ "type": "object", "additionalProperties": false }`." → `should-close-zero-parameter-schemas`: "For zero-parameter tools, the `inputSchema` SHOULD be `{ "type": "object", "additionalProperties": false }`."
- "Keep the tool surface small." → `should-keep-the-tool-surface-small`: "A server SHOULD keep the tool surface small: many overlapping tools degrade routing accuracy, so consolidate or parameterize instead."
- "Many overlapping tools degrade routing accuracy; consolidate or parameterize instead." → `should-keep-the-tool-surface-small`: "A server SHOULD keep the tool surface small: many overlapping tools degrade routing accuracy, so consolidate or parameterize instead."
- promoted: the lossless.json moved entries listed above — the intro's spec-revision paragraph and the keyword-less imperatives of the six sections. "Sanitize outputs and never leak secrets ..." -> must-not-leak-secrets-in-outputs "A server SHOULD sanitize outputs and MUST NOT leak secrets or internal identifiers the host should not see." ("never" -> MUST NOT, plain "Sanitize" -> SHOULD).
- the intro keeps its statement paragraph, including "so treat them as the public contract" (framing for the tool-design rules, not made a separate rule). "Validate inputs, enforce access control, and rate-limit on the server." stays verbatim as a sub-bullet of must-not-rely-on-annotations-alone. The primitive table (with "A server offers three primitives.") and the annotation-defaults table -> how-to parts; two explanatory sentences -> rationale.
- contradiction (unfixed): Structured output says "Sanitize outputs and never leak secrets or internal identifiers the host should not see." (no keyword, so SHOULD for sanitizing) while Security baseline says "Servers **MUST** validate all tool inputs, enforce access controls, rate-limit invocations, and sanitize outputs." — output sanitizing is SHOULD in one place and MUST in the other. Both rules keep their own level.
- bars: all three authored.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/offline-and-connectivity

Commit `7e55cb57`; 10 rules; lossless.json: 2 moved (reworded), 0 obsolete.

- the pattern list (kept verbatim as the how-to part "Patterns") is a menu ordered by complexity, so the rules drawn from it are conditioned on the pattern in use. Promoted: "For apps that must work offline, design for local-first with background sync." -> should-design-local-first "For apps that must work offline, the app SHOULD be designed for local-first with background sync." (intro sentence kept for GF-01); "**Optimistic updates** — apply changes to local UI immediately, sync in background. Roll back on server failure." -> should-roll-back-failed-optimistic-updates "An app using **optimistic updates** SHOULD apply changes to local UI immediately, sync in background, and roll back on server failure."; "Failed items stay in queue for retry." -> should-keep-failed-items-queued "In **queue-based sync**, failed items SHOULD stay in queue for retry."; "**Conflict resolution** — use ETags or version numbers to detect conflicts." -> should-detect-conflicts-with-versions "For **conflict resolution**, an app SHOULD use ETags or version numbers to detect conflicts."; "Return 409 with both versions." -> should-return-409-with-both-versions "On a detected conflict, the server SHOULD return 409 with both versions."; "Simple apps use server-wins; collaborative apps need merge UI or CRDTs." -> should-fit-resolution-to-collaboration "Simple apps SHOULD use server-wins; collaborative apps SHOULD use merge UI or CRDTs." ("need" read as a plain imperative, SHOULD); "Track `last_synced_at` per entity for delta sync" -> should-track-last-synced-at "The app SHOULD track `last_synced_at` per entity for delta sync."; "Show clear connectivity status to the user" -> should-show-connectivity-status "The app SHOULD show clear connectivity status to the user."
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/pagination

Commit `4d265949`; 2 rules; lossless.json: 0 moved (reworded), 0 obsolete.

- the intro keeps its paragraph verbatim (GF-01); the rules restate it, so lossless.json has no entries. Promoted: "Use offset pagination only when users need page numbers or data is relatively static." -> should-use-offset-only-for-page-numbers-or-static-data "APIs SHOULD use offset pagination only when users need page numbers or data is relatively static."
- the two response samples -> examples (they show shapes and add no rule); the source list -> references.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/rate-limiting

Commit `32bab150`; 6 rules; lossless.json: 2 moved (reworded), 0 obsolete.

- intro statement kept (GF-01) and restated. Promoted: "Respect server rate limits." -> should-respect-server-rate-limits "Clients SHOULD respect server rate limits."; "Handle 429 responses gracefully." -> should-handle-429-gracefully "Clients SHOULD handle 429 responses gracefully."; "If no `Retry-After`, use exponential backoff (see Retry section)" -> should-back-off-without-retry-after "If no `Retry-After`, clients SHOULD use exponential backoff (see Retry section)"; "Queue and batch requests at the allowed rate rather than fire-and-retry" -> should-queue-and-batch-at-the-allowed-rate "Clients SHOULD queue and batch requests at the allowed rate rather than fire-and-retry".
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/real-time-communication

Commit `5382547c`; 4 rules; lossless.json: 4 moved (reworded), 0 obsolete.

- intro statement kept (GF-01). Promoted: "Choose the simplest technique that meets your needs." -> should-choose-the-simplest-technique "Real-time features SHOULD use the simplest technique that meets their needs."; "**Start with SSE** for server-push — it has built-in reconnection, works over standard HTTP, and is sufficient for 80%+ of "real-time" needs." -> should-start-with-sse "Server-push SHOULD **start with SSE**." (reasons kept verbatim-close as its sub-bullet).
- the technique table -> how-to part "Choosing a technique"; the source list -> references. Two lossless entries per rule because the source wrapped its sentences across lines.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/retry-and-resilience

Commit `db3222d3`; 7 rules; lossless.json: 2 moved (reworded), 0 obsolete.

- intro statement kept (GF-01). Promoted: "Retry transient failures with exponential backoff and jitter." -> should-retry-transient-failures "Clients SHOULD retry transient failures with exponential backoff and jitter."; "**Exponential backoff with full jitter:** `delay = random(0, min(max_delay, base * 2^attempt))`" -> should-back-off-with-full-jitter "Retry delays SHOULD use **exponential backoff with full jitter**: `delay = ...`."; the parameter table -> should-use-the-default-retry-parameters "Retries SHOULD use the defaults in the parameter table: base delay 1 second, max delay cap 30 seconds, max retries 3-5 (idempotent), 0 (non-idempotent unless safe)."; "**Retryable status codes:** 408, 429, 500 (idempotent only), 502, 503, 504." -> should-treat-listed-codes-as-retryable "Clients SHOULD treat these as the **retryable status codes**: 408, 429, 500 (idempotent only), 502, 503, 504."; "**Circuit breaker** for cascading failure prevention:" (with its four steps, kept verbatim as sub-bullets) -> should-use-a-circuit-breaker "Clients SHOULD use a **circuit breaker** for cascading failure prevention."
- the formula block and defaults table (with their label) -> how-to "Backoff and its defaults"; sources -> references.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/robust-protocol-maintenance

Commit `3ff024de`; 7 rules; lossless.json: 0 moved (reworded), 0 obsolete.

- the existing rules part's six bullets kept verbatim and named. Promoted: the boundary table (Machine-to-machine: "**Strict** parse, reject + report"; External/3rd-party input you don't control: "**Strict** parse, but graceful degradation"; Human/UX edge: "**Forgiving** — normalize then validate") -> should-match-posture-to-boundary "Each boundary SHOULD take the posture the boundary table gives it: **strict** parse, reject + report on machine-to-machine paths (wire, internal API); **strict** parse, but graceful degradation for external/3rd-party input you don't control; **forgiving** — normalize then validate — at the human/UX edge (forms, CLI args, NL)." The table stays verbatim as the how-to part.
- the "Do **NOT** read this guideline as ..." paragraph split off into rationale part do-not-over-rotate; why-naive-tolerance-fails -> rationale. No sentence reworded, so lossless.json has no entries.
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/timeouts

Commit `34ffebd6`; 4 rules; lossless.json: 2 moved (reworded), 0 obsolete.

- intro statement (two MUST sentences) kept (GF-01) and restated as two rules. Promoted: the timeout table -> should-use-the-default-timeouts "Timeouts SHOULD use the defaults in the timeout table: connection (TCP + TLS handshake) 10 seconds, read / response (time to first byte) 30 seconds, total / request (entire lifecycle including retries) 60-120 seconds."; "For long-running operations, use **202 Accepted** + polling pattern instead of extending timeouts." -> should-use-202-for-long-running-operations "For long-running operations, services SHOULD use **202 Accepted** + polling pattern instead of extending timeouts." (two lossless entries because the source wrapped the sentence).
- table -> how-to "Timeout defaults".
- bars: all three authored.
- **contradictions**: none.
- **unfinished**: none.

## cookbook/guidelines/implementing/networking/web-services

Commit `0decce67`; 1 rules; lossless.json: 0 moved (reworded), 0 obsolete.

- no promoted rules: the one rule (must-use-flask) keeps its MUST. The intro keeps both sentences; "The dashboard service runs on Flask with a REST API and SSE/polling for live updates." describes one service and is not made a rule.
- bars: all three authored.
- the conversion commit had no lossless.json (the topic has no missing sentences); a follow-up commit `fda90eb9` adds the empty record the other topics carry, after roles check and approve.py passed again.
- **contradictions**: none.
- **unfinished**: none.
