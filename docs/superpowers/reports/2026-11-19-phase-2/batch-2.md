# Phase 2 batch 2 report

Twenty-three topics under `cookbook/guidelines/implementing/code-quality/`, each converted to roled parts as a format change only. Every topic has a `rules` part of named requirements, the three bar parts (`look-for`, `a-complete-review-must-establish`, `a-build-must-establish`, one line per rule), intro first and history last in `artifact.json`, and a `lossless.json` that passes `cookr roles lossless --base 0005775 --draft`. `roles check` exits 0 and `approve.py` printed `RESULT: APPROVED` for every topic. No entry anywhere is `obsolete`.

| Topic | Commit | Rules | Moved | Obsolete | Bars |
|---|---|---|---|---|---|
| architecture | a480d8b | 5 | 3 | 0 | authored |
| atomic-commits | f42d65e | 13 | 10 | 0 | authored |
| code-for-the-ai-reader | 58979cf7 | 19 | 15 | 0 | authored |
| completeness | eeafb8c7 | 11 | 5 | 0 | authored |
| delete-what-you-supersede | d766e719, 452c117e, 4aa4dc22 | 21 | 16 | 0 | authored |
| dependency-injection | 1c074190 | 8 | 6 | 0 | authored |
| file-paths | 9027c6f9 | 2 | 0 | 0 | authored |
| hilt-dependency-injection | 323463e5 | 28 | 24 | 0 | authored |
| linting | 8225de4a | 22 | 7 | 0 | authored |
| naming | 514ff058 | 8 | 7 | 0 | authored |
| no-external-dependencies-in-core-librari | 7f396178 | 1 | 0 | 0 | authored |
| nullable-reference-types | 6b7ce8b9 | 5 | 3 | 0 | authored |
| scope-discipline | c0509d01 | 7 | 6 | 0 | authored |
| shared-components-and-tiers | 4f1b4996 | 21 | 23 | 0 | authored |
| shell-scripts | 60003a2a | 13 | 15 | 0 | look-for moved; bars authored |
| type-hints | 2f9baf90 | 2 | 0 | 0 | authored |
| typescript-strictness | 3bc4b8fa | 17 | 23 | 0 | authored |
| use-roadmaplib | 35a88428 | 2 | 0 | 0 | authored |
| value-objects | 41721fda | 4 | 3 | 0 | authored |
| verification-harness | 279fbb78 | 17 | 17 | 0 | authored |
| visual-studio-project-files | 34f05f0d | 18 | 8 | 0 | look-for moved; bars authored |
| xcode-project-hygiene | 2e57c1cc | 25 | 24 | 0 | look-for moved; bars authored |
| yaml-frontmatter | e1677a08 | 2 | 0 | 0 | authored |

## Where this batch differs from the brief

- **Folded review copies became `look-for` (moved).** `shell-scripts`, `visual-studio-project-files` and `xcode-project-hygiene` each still held the text of their old reviewing copy. That checklist text is kept verbatim as the review-focus part, each line keyed to the rule it checks, with a line added for every rule it did not cover. The implementing sections it duplicated became the rules and were removed.
- **Explanation kept verbatim beside its rule.** Where a section mixed a requirement with its reason, the reason stays word for word as a sub-bullet under the rule (or in a `rationale` part keyed to the rule names), so only the requirement sentence needed a `moved` entry.
- **lossless keeps numbers and flip words per clause.** A rule that splits a source sentence at a comma or parenthesis must keep its numbers ("one"), negations and words such as "only" in the same clause, or `lossless` refuses the mapping. Several rules were reworded to keep those words together.
- **Base sentences are never obsolete.** `lossless` refuses `obsolete` for any sentence of the topic's own base, including an H1 and a pointer sentence; in `linting` both were mapped with `moved` instead.
- **FM-13.** In `delete-what-you-supersede` the word "TODO" was first respelled to pass approve.py's FM-13 check. After FM-13 was narrowed to real placeholder markers, the source word was restored (commit `4aa4dc22`). No other topic in this batch respelled one.

## cookbook/guidelines/implementing/code-quality/architecture

Commit `a480d8b`. 5 rules; lossless: 3 moved, 0 obsolete. The intro keeps its statement sentence (GF-01); the C# block moves to an `examples` part.

**promoted** (3 rules):
- "Use MVVM with CommunityToolkit.Mvvm — source-generated `ObservableObject`, `RelayCommand`, and messaging." → `should-use-mvvm-with-community-toolkit`: "SHOULD use MVVM with CommunityToolkit.Mvvm — source-generated `ObservableObject`, `RelayCommand`, and messaging."
- "Navigation service abstraction in the ViewModel layer" → `should-put-navigation-service-in-viewmodel-layer`: "A navigation service abstraction SHOULD live in the ViewModel layer."
- "Use Template Studio for project scaffolding with MVVM, navigation, and theming pre-wired" → `should-scaffold-with-template-studio`: "SHOULD use Template Studio for project scaffolding with MVVM, navigation, and theming pre-wired."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/atomic-commits

Commit `f42d65e`. 13 rules; lossless: 10 moved, 0 obsolete. The intro keeps "One logical change per commit." as its statement. The two near-identical `small-diffs-for-agent-generated-changes` parts (a fold leftover) are merged into four rules and a `rationale` part, and removed. The build-verify-commit loop stays as a `how-to` without its closing paragraph (now rules and rationale); "What counts as one logical change" is `examples`; "Why this matters" is `rationale`.

**promoted** (7 rules):
- "One logical change per commit." → `should-make-one-logical-change-per-commit`: "Each commit SHOULD hold one logical change."
- "A change may touch multiple files if they are part of the same concept" → `may-touch-multiple-files-for-one-concept`: "A change MAY touch multiple files if they are part of the same concept — an interface and its implementation, a component and its test file." (lower-case "may" read as a permission)
- "Commits should happen as work progresses" → `should-commit-as-work-progresses`: "Commits SHOULD happen as work progresses." (lower-case "should")
- "do not batch up unrelated changes" → `should-not-batch-unrelated-changes`: "Unrelated changes SHOULD NOT be batched up."
- "**Build** — run the platform build command (...)" → `should-build-every-logical-change`: "For every logical change, SHOULD run the platform build command (`xcodebuild`, `./gradlew build`, `npm run build`, `dotnet build`, `cargo build`)."
- "**Commit** — commit the passing change with a descriptive message" / "**Repeat** — move to the next logical change" → `should-commit-each-passing-change`: "SHOULD commit each passing change with a descriptive message before moving to the next logical change." (the loop's steps also stay verbatim in the how-to)
- "If a change breaks the build, fix it before moving on — do not add more changes on top of a broken state." → `should-fix-broken-build-before-moving-on`: "If a change breaks the build, SHOULD fix it before moving on — SHOULD NOT add more changes on top of a broken state."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none. (The two small-diff parts said the same thing twice; `should-plan-small-prs-before-coding` joins "planned ... before writing code" and "split ... up front".)

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/code-for-the-ai-reader

Commit `58979cf7`. 19 rules; lossless: 15 moved, 0 obsolete. The intro stays as written (its last sentence is also a rule). The four bulleted sections become the `rules` part and a `rationale` part, and are removed.

**promoted** (14 rules):
- "Treat machine-legibility as one reader audience to serve — not a license to abandon human readability." → `should-treat-machine-legibility-as-one-audience`: "Machine-legibility SHOULD be treated as one reader audience to serve — not a license to abandon human readability."
- "Prefer one canonical spelling of a concept over synonyms scattered across the codebase." → `should-use-one-canonical-spelling`: "SHOULD prefer one canonical spelling of a concept over synonyms scattered across the codebase."
- "Avoid constructing identifiers at runtime (string-concatenated method names, dynamically generated attributes)." → `should-avoid-runtime-constructed-identifiers`: "SHOULD avoid constructing identifiers at runtime (...)."
- "Keep call sites discoverable: a function **SHOULD** be reachable ..." → `should-keep-call-sites-discoverable`: "Call sites SHOULD be kept discoverable: a function **SHOULD** be reachable by searching for its name, not only through a registry, decorator, or dependency-injection wiring that hides the connection." (the lead clause gained the SHOULD the second clause already had)
- "Minimize reflection, dynamic dispatch, and runtime metaprogramming that hides what code actually does." → `should-minimize-hidden-runtime-behavior`: "SHOULD minimize reflection, dynamic dispatch, and runtime metaprogramming that hides what code actually does."
- "Function signatures act as design documents the agent reads first — keep parameter names and return types explicit and accurate." → `should-keep-signatures-explicit`: "... — parameter names and return types SHOULD be kept explicit and accurate. (See the reference.)"
- "Prefer them where a language makes them optional." → `should-prefer-explicit-types-and-names`: "SHOULD prefer explicit types and verbose intention-revealing names where a language makes them optional."
- "Prefer explicit control flow over implicit magic (auto-registration, monkey-patching, import-time side effects)." → `should-prefer-explicit-control-flow`: "SHOULD prefer explicit control flow over implicit magic (...)."
- "A test named for the behavior it verifies doubles as greppable documentation of intent." → `should-name-tests-for-behavior`: "A test SHOULD be named for the behavior it verifies, so it doubles as greppable documentation of intent." (a descriptive sentence read as a recommendation; a judge should confirm)
- "Favor **locality of related behavior**." → `should-favor-locality-of-related-behavior`: "SHOULD favor **locality of related behavior** over very short files and aggressive file-splitting that scatter related behavior an agent must assemble from many sources."
- "Apply judgment per case." → `should-judge-dry-per-case`: "Between heavy DRY with deep indirection and a small, explicit repetition, SHOULD apply judgment per case."
- "do not cite it as an established statistic" → `should-not-cite-agent-readership-as-statistic`: "The claim "agents now read code more than humans do" SHOULD NOT be cited as an established statistic."
- "Justify each choice by concrete readability for the next reader, human or agent, not by appeal to that trend." → `should-justify-by-concrete-readability`: "Each choice SHOULD be justified by concrete readability for the next reader, human or agent, not by appeal to that trend."
- "When ... the cost is low, prefer the option that keeps behavior explicit and local." → `should-prefer-explicit-and-local-when-cost-low`: "When a human-readability convention and an AI-readability heuristic conflict and the cost is low, SHOULD prefer the option that keeps behavior explicit and local."
- "When the human cost is high, weigh both and document the trade-off." → `should-weigh-and-document-when-human-cost-high`: "When the human cost is high, SHOULD weigh both and document the trade-off."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `should-keep-call-sites-discoverable` ("a function **SHOULD** be reachable by searching for its name, not only through a registry, decorator, or dependency-injection wiring that hides the connection") pulls against the dependency-injection topics in this batch, which ask for wiring through a container (`hilt-dependency-injection`: "Use `@Inject constructor(...)` for all classes Hilt can construct"). The two can both hold (a constructor call site still names the type), so this is a tension to note, left unfixed. `should-keep-signatures-explicit` keeps "(See the reference.)", which names no reference; left as written.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/completeness

Commit `eeafb8c7`. 11 rules; lossless: 5 moved, 0 obsolete. The intro stays as written; its "Deliver the full scope that was agreed." is also a rule. The five one-bullet sections become the `rules` part and a `rationale` part, and are removed.

**promoted** (5 rules):
- "Deliver the full scope that was agreed." → `should-deliver-full-agreed-scope`: "SHOULD deliver the full scope that was agreed."
- "If something genuinely should be deferred, say so explicitly and get agreement — surface it as a note (...), do not bury it." → `should-surface-deferrals-for-agreement`: "If something genuinely should be deferred, SHOULD say so explicitly and get agreement — surface it as a note (the same way scope-discipline notes adjacent issues); SHOULD NOT bury it."
- ""Out of scope" is a decision the user makes with you, not one you make on their behalf." → `should-leave-scoping-out-to-the-user`: ""Out of scope" SHOULD be a decision the user makes with you, not one you make on their behalf." (a statement read as SHOULD; with `must-not-silently-drop-request-parts` beside it, a judge may read it as MUST)
- "Re-reading the request before pausing avoids stalling work that was meant to proceed." → `should-reread-request-before-pausing`: "SHOULD re-read the request before pausing: re-reading before pausing avoids stalling work that was meant to proceed."
- "When you invoke YAGNI to not build something, name what you are skipping and why, so the choice is visible." → `should-name-what-yagni-skips`: "When you invoke YAGNI to not build something, SHOULD name what you are skipping and why, so the choice is visible."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/delete-what-you-supersede

Commits `d766e719`, `452c117e` and `4aa4dc22`. The first went in before approve.py had passed; the second respelled "TODO" in a review-focus line as "to-do note" to clear the older FM-13 check; the third restores "TODO" once FM-13 was narrowed to placeholder markers, and the topic is approved with it. 21 rules; lossless: 16 moved, 0 obsolete. The intro stays as written; "Why this matters" is `rationale`, and a new `rationale` part carries the reasons that sat beside the rules. The five bulleted sections are removed.

**promoted** (12 rules):
- "Do not leave old and new side by side, and do not park the old one behind a flag that is permanently off." → `should-not-keep-old-and-new-side-by-side`: "SHOULD NOT leave old and new side by side, and SHOULD NOT park the old one behind a flag that is permanently off."
- "Do the deletion as you go, not as a cleanup pass you plan to do later." → `should-delete-as-you-go`: "SHOULD do the deletion as you go, not as a cleanup pass you plan to do later."
- "Delete the old tests with the old code, and move any behavior they pinned that still matters onto the new path." → `should-delete-old-tests-with-old-code`: "SHOULD delete the old tests with the old code, and move any behavior they pinned that still matters onto the new path."
- "Search for the old name across the whole repo, not only the files you opened." → `should-search-whole-repo-for-old-name`: "SHOULD search for the old name across the whole repo, not only the files you opened."
- "Search for the whole identifier, not a fragment." → `should-search-whole-identifier`: "SHOULD search for the whole identifier, not a fragment."
- "Finish with a final search for the old name." → `should-finish-with-final-search`: "SHOULD finish with a final search for the old name. Any remaining hit is either a missed caller or a deliberate compatibility shim."
- "A flag whose rollout is finished, or whose old branch you just removed, is an orphan. Remove the flag and the branch it guarded." → `should-remove-orphaned-flags`: "A flag whose rollout is finished, or whose old branch you just removed, is an orphan: SHOULD remove the flag and the branch it guarded."
- "Confirm with a reference search before deleting." → `should-confirm-with-reference-search`: "SHOULD confirm with a reference search before deleting."
- "Do not leave a block of old code with a note such as "kept for reference" or "old approach"." → `should-not-keep-old-code-for-reference`: "SHOULD NOT leave a block of old code with a note such as "kept for reference" or "old approach"."
- "If the reasoning behind the old approach matters, write it as a sentence in a comment and delete the code." → `should-record-old-reasoning-as-a-sentence`: "If the reasoning behind the old approach matters, SHOULD write it as a sentence in a comment and delete the code."
- "When a change alters what a value, function or field holds, rename it to match." → `should-rename-when-meaning-changes`: "When a change alters what a value, function or field holds, SHOULD rename it to match."
- "After you change a type or a behavior, reread the names that touch it, ..." → `should-reread-touching-names`: "After you change a type or a behavior, SHOULD reread the names that touch it, including parameter names, variable names, file names and test names."

"A rename is a change to every caller, so apply the rename rule above in the same change." is a sub-bullet of `must-update-every-caller` (it adds no level of its own).

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions** (R4, left unfixed): three plain imperatives, promoted to SHOULD as the brief directs, restate a MUST beside them, so the topic now states one requirement at two levels.
- `should-not-keep-old-and-new-side-by-side` ("SHOULD NOT leave old and new side by side") against `must-delete-replaced-implementation` ("you MUST delete the one it replaces in the same change").
- `should-remove-orphaned-flags` ("SHOULD remove the flag and the branch it guarded") against `must-delete-unreferenced-things` ("anything that nothing references MUST go: ... feature flags").
- `should-not-keep-old-code-for-reference` ("SHOULD NOT leave a block of old code with a note") against `must-delete-not-comment-out` ("Code you no longer need MUST be deleted, not commented out").

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/dependency-injection

Commit `1c074190`. 8 rules; lossless: 6 moved, 0 obsolete. The intro keeps its statement paragraph; its bullets become rules, and the C# block becomes an `examples` part.

**promoted** (6 rules):
- "Constructor injection via `Microsoft.Extensions.DependencyInjection`." → `should-use-constructor-injection`: "SHOULD use constructor injection via `Microsoft.Extensions.DependencyInjection`." (the sentence also stays in the intro)
- "`Transient` for lightweight stateless services" → `should-use-transient-for-stateless-services`: "`Transient` SHOULD be used for lightweight stateless services."
- "`Scoped` for per-request services" → `should-use-scoped-for-per-request-services`: "`Scoped` SHOULD be used for per-request services."
- "`Singleton` for thread-safe shared state" → `should-use-singleton-for-shared-state`: "`Singleton` SHOULD be used for thread-safe shared state."
- "Use `IOptions<T>` / `IOptionsSnapshot<T>` for configuration binding" → `should-bind-configuration-with-ioptions`: "SHOULD use `IOptions<T>` / `IOptionsSnapshot<T>` for configuration binding."
- "Keep registrations in `Add*()` extension methods for modularity" → `should-register-in-add-extension-methods`: "SHOULD keep registrations in `Add*()` extension methods for modularity."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/file-paths

Commit `9027c6f9`. 2 rules; lossless: 0 moved, 0 obsolete. Both rules are the intro's two MUST sentences, verbatim, so nothing at the base is missing and the folder has no `lossless.json`. The intro keeps them as its statement; the Python block becomes an `examples` part.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/hilt-dependency-injection

Commit `323463e5`. 28 rules; lossless: 24 moved, 0 obsolete. The intro keeps its first sentence as the statement; its two SHOULD sentences become rules. The scope table stays as a `how-to` part ("Scope to the right component") without its bullets. Setup, constructor injection, Jetpack integration, testing and anti-patterns become rules plus a `rationale` part, and are removed.

**promoted** (21 rules):
- "Use **KSP** (`com.google.devtools.ksp`) for the Hilt compiler, not the legacy KAPT." → `should-use-ksp-not-kapt`: "SHOULD use **KSP** (...) for the Hilt compiler, not the legacy KAPT."
- "Apply the `com.google.dagger.hilt.android` Gradle plugin and add `hilt-android` plus the compiler via `ksp(...)`." → `should-apply-hilt-gradle-plugin`: "SHOULD apply the ... Gradle plugin and add `hilt-android` plus the compiler via `ksp(...)`."
- "Annotate the `Application` subclass with `@HiltAndroidApp`." → `should-annotate-application-with-hiltandroidapp`: "The `Application` subclass SHOULD be annotated with `@HiltAndroidApp`."
- "Annotate Android entry points (...) needing field injection with `@AndroidEntryPoint`." → `should-annotate-entry-points-with-androidentrypoint`: "Android entry points (`Activity`, `Fragment`, `Service`) needing field injection SHOULD be annotated with `@AndroidEntryPoint`."
- "Use a `@Module` with `@Provides` only for types you do not own (third-party, builders) or interfaces." → `should-use-provides-only-for-unowned-types`: "SHOULD use a `@Module` with `@Provides` only for types you do not own (third-party, builders) or interfaces."
- "Bind an interface to its implementation with `@Binds` in an `abstract` module — it generates less code than `@Provides`." → `should-bind-interfaces-with-binds`: "SHOULD bind an interface ... — it generates less code than `@Provides`."
- "Install every module into a component with `@InstallIn(...)`." → `should-install-every-module`: "SHOULD install every module into a component with `@InstallIn(...)`."
- "Choose the **narrowest** component that fits the binding's lifetime." → `should-choose-narrowest-component`: "SHOULD choose the **narrowest** component that fits the binding's lifetime."
- "Scope only stateful, expensive-to-build, or app-shared instances." → joined to `should-not-apply-singleton-just-in-case`: "`@Singleton` **SHOULD NOT** be applied for performance "just in case." SHOULD scope only stateful, expensive-to-build, or app-shared instances." (one rule: the lossless clause reader reads the two source sentences as one clause)
- "Annotate ViewModels with `@HiltViewModel` and an `@Inject constructor`." → `should-annotate-viewmodels-with-hiltviewmodel`: "SHOULD annotate ViewModels with `@HiltViewModel` and an `@Inject constructor`."
- "inject `SavedStateHandle` for navigation/saved args" → `should-inject-savedstatehandle`: "SHOULD inject `SavedStateHandle` for navigation/saved args."
- "Do not construct these ViewModels manually." → `should-not-construct-hilt-viewmodels-manually`: "SHOULD NOT construct these ViewModels manually."
- "For Compose, retrieve them with `hiltViewModel()` (...)." → `should-use-hiltviewmodel-in-compose`: "For Compose, SHOULD retrieve them with `hiltViewModel()` (`androidx.hilt:hilt-navigation-compose`)."
- "Annotate `CoroutineWorker`/`Worker` subclasses with `@HiltWorker`." → `should-annotate-workers-with-hiltworker`: "SHOULD annotate `CoroutineWorker`/`Worker` subclasses with `@HiltWorker`."
- "Inject `HiltWorkerFactory` into the `Application` and wire it through ..." → `should-wire-hiltworkerfactory`: "SHOULD inject `HiltWorkerFactory` into the `Application` and wire it through a custom `WorkManager` `Configuration` (or the `Configuration.Provider` on the `Application`)."
- "Use `hilt-android-testing` with `kspTest`/`kspAndroidTest`." → `should-use-hilt-android-testing`: "SHOULD use `hilt-android-testing` with `kspTest`/`kspAndroidTest`."
- "Annotate tests with `@HiltAndroidTest` and drive injection with `HiltAndroidRule`." → `should-drive-tests-with-hiltandroidrule`: "SHOULD annotate tests with `@HiltAndroidTest` and drive injection with `HiltAndroidRule`."
- "Replace bindings in tests with `@TestInstallIn` or `@BindValue` rather than mutating production modules." → `should-replace-test-bindings-without-mutating-modules`: "SHOULD replace bindings in tests with `@TestInstallIn` or `@BindValue` rather than mutating production modules."
- "Do not inject the Hilt-managed graph by passing `Context` around to build objects manually — that defeats the framework." → `should-not-build-objects-from-passed-context`: "SHOULD NOT inject the Hilt-managed graph by passing `Context` around to build objects manually — that defeats the framework."
- "Do not field-inject where constructor injection is possible; reserve field injection for framework-instantiated entry points." → `should-not-field-inject-where-constructor-possible`: "SHOULD NOT field-inject where constructor injection is possible; SHOULD reserve field injection for framework-instantiated entry points."
- "Do not create god modules. Split modules by feature and install them into the narrowest applicable component." → `should-not-create-god-modules`: "SHOULD NOT create god modules; SHOULD split modules by feature and install them into the narrowest applicable component."

"This is the root of the dependency graph and **MUST** exist exactly once." keeps its MUST as `must-have-exactly-one-hiltandroidapp`: "The `@HiltAndroidApp` application, the root of the dependency graph, **MUST** exist exactly once."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored. (The "Anti-patterns" section was a list of don'ts for the writer, not a reviewer checklist, so it became rules.)

**contradictions**: none within the topic. See `code-for-the-ai-reader` for its tension with DI wiring.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/linting

Commit `8225de4a`. 22 rules; lossless: 7 moved, 0 obsolete. The intro keeps its first MUST sentence as the statement; its other sentences become rules, and its copy of the platform table is dropped (the "Platform linters" part holds the same table). The folded copy's `introduction` part (a second H1, "Linting from day one", and one paragraph) is removed; its paragraph goes to a `rationale` part. The Swift, Kotlin, TypeScript and C# parts stay verbatim as `how-to`, and rules are drawn from their instructions. "What linting verifies that tests don't" is `rationale`.

`cookr roles lossless` refuses `obsolete` for any sentence of the topic's own base, so two leftovers of the fold were moved instead: the heading "# Linting from day one" maps to the rationale line "Lint from day one.", and "See the implementing copy of this guideline for platform-specific setup details." (this folder *is* the implementing copy) maps to a reworded pointer in "Platform linters": "See the Swift, Kotlin, TypeScript and C# parts of this guideline, the implementing copy, for platform-specific setup details."

**promoted** (12 rules):
- "during rapid prototyping, committing without lint-gating every commit is acceptable" → `may-skip-lint-gating-while-prototyping`: "During rapid prototyping, committing without lint-gating every commit MAY be done; it is acceptable."
- "**During development** — as part of the build or pre-commit hook" (under the lead-in "Linting MUST run as part of the automated verification process:") → `must-run-lint-during-development`: "During development, linting MUST run as part of the build or pre-commit hook." (takes the lead-in's MUST)
- "[SwiftLint] with `.swiftlint.yml` at project root. Enable `strict` mode. Add as SPM plugin or Xcode build phase." → `should-use-swiftlint-strict`: "Swift SHOULD use SwiftLint with `.swiftlint.yml` at project root, with `strict` mode enabled, added as an SPM plugin or Xcode build phase."
- "[swift-format] for auto-formatting." → `should-format-swift-with-swift-format`: "Swift SHOULD use swift-format for auto-formatting."
- "Use [ktlint] for both linting and formatting. Configure via `.editorconfig` at project root. Add as a Gradle plugin (...)." → `should-use-ktlint`: "Kotlin SHOULD use ktlint for both linting and formatting, configured via `.editorconfig` at project root and added as a Gradle plugin (`org.jlleitschuh.gradle.ktlint`)."
- "[ESLint] with `eslint.config.js`. Use `eslint-config-prettier` to avoid conflicts with the formatter." → `should-use-eslint-with-prettier-config`: "TypeScript SHOULD use ESLint with `eslint.config.js`, and `eslint-config-prettier` to avoid conflicts with the formatter."
- "[Prettier] with `.prettierrc` for auto-formatting." → `should-format-typescript-with-prettier`: "TypeScript SHOULD use Prettier with `.prettierrc` for auto-formatting."
- "[Stylelint] with `.stylelintrc.json` for CSS linting." → `should-lint-css-with-stylelint`: "SHOULD use Stylelint with `.stylelintrc.json` for CSS linting."
- "Add as `package.json` scripts and pre-commit hooks." → `should-add-lint-scripts-and-hooks`: "TypeScript linting and formatting SHOULD be added as `package.json` scripts and pre-commit hooks."
- "[`.editorconfig`] at repo root for all code style rules." → `should-keep-style-rules-in-editorconfig`: "C# SHOULD keep all code style rules in an `.editorconfig` at repo root."
- "Enable Roslyn analyzers in `.csproj`:" (and its XML) → `should-enable-roslyn-analyzers`: "C# SHOULD enable Roslyn analyzers in `.csproj` (`EnforceCodeStyleInBuild` true, `AnalysisLevel` `latest-recommended`)."
- "Use `dotnet format` CLI for auto-fixing." → `should-auto-fix-with-dotnet-format`: "C# SHOULD use the `dotnet format` CLI for auto-fixing."
- "Supplement with [Roslynator] or [Meziantou.Analyzer] for additional rules." → `should-supplement-with-extra-analyzers`: "C# SHOULD supplement with Roslynator or Meziantou.Analyzer for additional rules."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `must-run-lint-in-build-or-pre-commit` ("Linting MUST run as part of the build or pre-commit process") and `must-run-lint-during-development` ("During development, linting MUST run as part of the build or pre-commit hook") state one requirement twice, from the intro and from "When to run"; both kept, left unfixed. `may-skip-lint-gating-while-prototyping` sits beside `must-run-lint-in-build-or-pre-commit`: if lint runs in the pre-commit process, every commit is lint-gated, so the prototyping allowance and the MUST pull against each other; left unfixed.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/naming

Commit `514ff058`. 8 rules; lossless: 7 moved, 0 obsolete. The intro keeps its statement sentence; its bullets become rules (the five MUST bullets gain only a closing period).

**promoted** (3 rules):
- "Use .NET's established casing conventions consistently: ..." → `should-use-dotnet-casing-consistently`: "SHOULD use .NET's established casing conventions consistently: `PascalCase` for public symbols, `camelCase` for locals, and `_camelCase` for private fields." (the sentence also stays in the intro)
- "`I` prefix for interfaces (e.g., `IDisposable`)" → `should-prefix-interfaces-with-i`: "Interfaces SHOULD take the `I` prefix (e.g., `IDisposable`)."
- "Use `var` when the type is apparent from the right side of the assignment" → `should-use-var-when-type-apparent`: "SHOULD use `var` when the type is apparent from the right side of the assignment."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none. (`must-pascal-case-types-and-members` and `must-pascal-case-constants` both name constants; they agree.)

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/no-external-dependencies-in-core-librari

Commit `7f396178`. 1 rule; lossless: 0 moved, 0 obsolete (every sentence kept verbatim, so no `lossless.json`). The intro keeps its statement sentence ("`roadmap_lib` uses the standard library only."), which is also the rule's sub-bullet; the MUST NOT sentence is the rule, and the reason sentence is the `rationale` part.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/nullable-reference-types

Commit `6b7ce8b9`. 5 rules; lossless: 3 moved, 0 obsolete. The intro keeps its statement paragraph; its bullets become rules, and its C# sample moves verbatim to an `examples` part.

**promoted** (3 rules):
- "Treat warnings as design signals — `string` means non-null, `string?` means nullable." → `should-treat-nullable-warnings-as-design-signals`: "SHOULD treat warnings as design signals — `string` means non-null, `string?` means nullable." (the sentence also stays in the intro)
- "Use `required` properties and constructor parameters for non-null initialization" → `should-use-required-for-non-null-init`: "SHOULD use `required` properties and constructor parameters for non-null initialization."
- "Use `[NotNull]`, `[MaybeNull]`, `[NotNullWhen]` from `System.Diagnostics.CodeAnalysis` for contracts the compiler cannot infer" → `should-annotate-contracts-compiler-cannot-infer`: "SHOULD use `[NotNull]`, `[MaybeNull]`, `[NotNullWhen]` from `System.Diagnostics.CodeAnalysis` for contracts the compiler cannot infer."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/scope-discipline

Commit `c0509d01`. 7 rules; lossless: 6 moved, 0 obsolete. The intro keeps its statement ("Every task has a boundary. Stay inside it."). The "Before starting", "During work" and "Recognizing scope creep" parts become rules and are removed; the "do not refactor …" example sentence and the "A note like …" sentence are kept verbatim as sub-bullets of the rules they illustrate, and the five creep signals are kept verbatim as sub-bullets. "Why this matters" stays verbatim as `rationale`.

**promoted** (5 rules):
- "Stay inside it." → `should-stay-inside-task-boundary`: "Every task has a boundary. You SHOULD stay inside it." (also stays in the intro)
- "If the request is ambiguous or could be interpreted broadly, ask before assuming broad scope." → `should-ask-before-assuming-broad-scope`: "If the request is ambiguous or could be interpreted broadly, you SHOULD ask before assuming broad scope."
- "For multi-repo work, confirm which repository before making changes." → `should-confirm-repository-for-multi-repo-work`: "For multi-repo work, you SHOULD confirm which repository before making changes."
- "**note them** for the user but MUST NOT fix them" → `must-note-but-not-fix-out-of-scope-issues`: "If you discover issues outside the stated scope — broken imports, outdated comments, missing error handling — you SHOULD note them for the user but MUST NOT fix them." (the "note" half promoted to SHOULD; the MUST NOT kept)
- "Watch for these signals that scope is expanding:" → `should-watch-for-scope-creep-signals`: "You SHOULD watch for these signals that scope is expanding:" (signals kept as sub-bullets)

The sub-bullet "If asked to fix a bug, fix that bug — do not refactor surrounding code, …" is not promoted to a rule of its own: it stays verbatim under `must-modify-only-what-was-requested`, as the example of that MUST.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored. ("Recognizing scope creep" is written for the worker, "Watch for …", not for a reviewer, so it became a rule rather than the review-focus part.)

**contradictions**: `should-stay-inside-task-boundary` is a SHOULD ("Stay inside it.") while `must-modify-only-what-was-requested` makes the same boundary a MUST ("Only what was requested MUST be modified."); left unfixed.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/shared-components-and-tiers

Commit `4f1b4996`. 21 rules; lossless: 23 moved, 0 obsolete. The intro stays verbatim (its statement and its context sentences). The five section parts ("Search before you write", "The lowest tier that can hold it", "Dependencies point downward", "Features live in shared tiers, apps are shells", "Organize into encapsulated directories") become rules and are removed; their explanatory sentences are kept verbatim, either as rule sub-bullets or in a new `rationale` part keyed by rule name. "Why this matters" stays verbatim as `rationale`.

**promoted** (20 rules; every bullet but the one MUST NOT had no keyword):
- "Build upward from the most basic shared pieces, and treat each assembly as a shared piece in its own right." → `should-build-upward-from-shared-pieces`: "You SHOULD build upward from the most basic shared pieces, and treat each assembly as a shared piece in its own right." (also stays in the intro)
- "Where it does not, apply them by judgment." → `should-apply-by-judgment-without-declared-tiers`: "Where a repo declares its tiers (…), the tools can check these rules; where it does not, you SHOULD apply them by judgment." (also stays in the intro)
- "Before creating a source file or a new component, look for what already exists: …" → `should-search-before-creating`: "Before creating a source file or a new component, you SHOULD look for what already exists: the repo's tier table, its list of shared exports, and a text search for the concept under several names." ("Search for "button" and "control", …" kept verbatim as its sub-bullet)
- "If something close exists, extend or reuse it. Build a new one only when you can say why the existing one cannot serve." → `should-reuse-before-building-new`: "If something close exists, you SHOULD extend or reuse it, and build a new one only when you can say why the existing one cannot serve."
- "A new file in a shared tier is allowed, and is how the tier grows." → `may-add-new-file-to-shared-tier`: "A new file in a shared tier MAY be added: it is allowed, and is how the tier grows."
- "Check that it does not duplicate an existing component under a different name." → `should-check-new-shared-file-for-duplicates`: "For a new file in a shared tier, you SHOULD check that it does not duplicate an existing component under a different name."
- "Say what you reused, and what you chose not to reuse and why." → `should-say-what-was-reused`: "You SHOULD say what you reused, and what you chose not to reuse and why."
- "Place each piece in the lowest tier whose dependencies it can live with." → `should-place-in-lowest-tier`: "You SHOULD place each piece in the lowest tier whose dependencies it can live with." (next sentence kept verbatim as its sub-bullet)
- "Do not create a new tier, framework or target to hold a feature." → `should-not-create-tier-for-feature`: "You SHOULD NOT create a new tier, framework or target to hold a feature." ("Adding one is a decision for the project owner." kept as its sub-bullet)
- "Ask of each piece: could a command-line tool link this without the application?" → `should-ask-if-cli-could-link-it`: "You SHOULD ask of each piece: could a command-line tool link this without the application?"
- "If it reads an application settings singleton or an app-only type, pass that value in as a parameter, and the piece moves down." → `should-pass-app-values-as-parameters`: "If a piece reads an application settings singleton or an app-only type, you SHOULD pass that value in as a parameter, and the piece moves down."
- "When a lower tier needs something from above, invert the dependency: …" → `should-invert-upward-dependencies`: "When a lower tier needs something from above, you SHOULD invert the dependency: define a protocol or callback in the lower tier and let the higher tier supply it."
- "A cycle between tiers means the shared part belongs in a tier below both. Extract it rather than allowing the cycle." → `should-extract-shared-part-of-cycle`: "A cycle between tiers means the shared part belongs in a tier below both; you SHOULD extract it rather than allowing the cycle."
- "A feature's models, service protocol, client, storage, logic and views go into the repo's existing shared tiers." → `should-put-feature-pieces-in-shared-tiers`: "A feature's models, service protocol, client, storage, logic and views SHOULD go into the repo's existing shared tiers." (next sentence kept as its sub-bullet)
- "What legitimately stays in an application: the entry point, config files, and aggregation code, …" → `may-keep-entry-point-and-glue-in-app`: "An application MAY keep what legitimately stays in it: the entry point, config files, and aggregation code, meaning menu assembly, dependency wiring, and thin adapters that bind a shared protocol to that application's data or transport."
- "Split a feature by what each piece needs. Models and pure logic go to the foundation, …" → `should-split-feature-by-need`: "You SHOULD split a feature by what each piece needs: models and pure logic go to the foundation, persistence to the storage tier, views to the UI tier, transport clients to the IPC tier, and only the glue stays in the app."
- "Every file lives inside a directory that names its purpose and belongs to a declared tier. Do not leave source files strewn at the top level of a repo or package." → `should-keep-every-file-in-a-tier-directory`: "Every file SHOULD live inside a directory that names its purpose and belongs to a declared tier, and source files SHOULD NOT be left strewn at the top level of a repo or package."
- "Keep a directory cohesive: …" → `should-keep-directories-cohesive`: "You SHOULD keep a directory cohesive: what is inside changes together and is reached through a small public surface." ("Details that other code should not touch stay inside it." kept as its sub-bullet)
- "Group by concept, not by file type, so a reader finds a feature in one place." → `should-group-by-concept`: "You SHOULD group by concept, not by file type, so a reader finds a feature in one place."
- "When a path belongs to no declared tier, move the file into one. Do not add a tier just to hold it." → `should-move-untiered-file-into-a-tier`: "When a path belongs to no declared tier, you SHOULD move the file into one, and SHOULD NOT add a tier just to hold it."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `should-not-create-tier-for-feature` ("SHOULD NOT create a new tier … to hold a feature") and `should-move-untiered-file-into-a-tier` ("SHOULD NOT add a tier just to hold it") say the same thing twice from two sections; both kept, left unfixed. The guideline's dependency rule is a MUST NOT while the placement rule that drives it, `should-place-in-lowest-tier`, is a SHOULD, as the source wording carried; left as written.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/shell-scripts

Commit `60003a2a`. 13 rules; lossless: 15 moved, 0 obsolete. The intro keeps both MUST sentences (they are also the first two rules). The first "Portability" part becomes rules, with its explanatory sentences kept verbatim as sub-bullets; the second "Portability" part (`portability-2`, a checklist of what a correct script shows) is the review-focus part, its sentences kept verbatim and each keyed to the rule it checks, with lines added for the rules it does not cover.

**promoted** (11 rules):
- "Declare the shell in the shebang and write to that shell's rules." → `should-declare-shell-in-shebang`: "You SHOULD declare the shell in the shebang and write to that shell's rules."
- "Use `#!/usr/bin/env bash` (or zsh) only when you need those features, and then do not call the script with `sh`." → `should-use-bash-or-zsh-only-when-needed`: "You SHOULD use `#!/usr/bin/env bash` (or zsh) only when you need those features, and then SHOULD NOT call the script with `sh`."
- "Quote every expansion and use `setopt`-independent forms so the script behaves the same under either." → `should-use-setopt-independent-forms`: "You SHOULD quote every expansion and use `setopt`-independent forms so the script behaves the same under either zsh or bash."
- "A script does not need it and must not depend on it. Start background work with `&` and collect it with `wait`; never rely on `fg` or `bg` in a script." → `must-not-depend-on-job-control`: "A script does not need `set -m` job control and MUST NOT depend on it; it SHOULD start background work with `&` and collect it with `wait`, and MUST NOT rely on `fg` or `bg` in a script." (lower-case "must not" read as MUST NOT; "never" as MUST NOT; "Start …" as SHOULD)
- "Check the commands that matter explicitly with `|| exit` or an `if`." → `should-check-important-commands-explicitly`: "You SHOULD check the commands that matter explicitly with `|| exit` or an `if`, because `set -e` is not a general error handler."
- "Give optional values a default with `${name:-default}`." → `should-default-optional-values`: "You SHOULD give optional values a default with `${name:-default}`."
- "Older `sh` implementations may lack it, so test for it or avoid it in `#!/bin/sh` scripts." → `should-test-for-pipefail-or-avoid-it`: "Older `sh` implementations may lack `set -o pipefail`, so you SHOULD test for it or avoid it in `#!/bin/sh` scripts."
- "Quote every expansion: `"$var"`, `"$@"`." → `should-quote-every-expansion`: "You SHOULD quote every expansion: `"$var"`, `"$@"`."
- "Never build a command in a string and run it with `eval`." → `must-not-eval-built-strings`: "You MUST NOT build a command in a string and run it with `eval`."
- "Use `trap` for cleanup. `trap 'cleanup' EXIT` runs when the shell exits; trap `INT` and `TERM` too if the script must clean up on a signal." → `should-trap-for-cleanup`: "You SHOULD use `trap` for cleanup: `trap 'cleanup' EXIT` runs when the shell exits; trap `INT` and `TERM` too if the script must clean up on a signal."
- "Put a time limit on any command that can hang with `timeout …` (GNU coreutils). … Use `-k` to send a follow-up kill, and note that `timeout` is not part of POSIX and may be absent on macOS; check for it, or do the work in Python." → `should-time-limit-hanging-commands`: "You SHOULD put a time limit on any command that can hang with `timeout [options] duration command [arg]...` (GNU coreutils), use `-k` to send a follow-up kill, and, since `timeout` is not part of POSIX and may be absent on macOS, check for it, or do the work in Python."

**bars**: `look-for` moved (from the `portability-2` checklist; lines added for `must-main-only-call-functions`, `must-keep-scripts-composable-and-testable` and `should-use-bash-or-zsh-only-when-needed`, and its two two-rule lines split at the sentence), `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `should-use-setopt-independent-forms` ("Quote every expansion and use `setopt`-independent forms …") and `should-quote-every-expansion` ("Quote every expansion: …") both require quoting every expansion; kept, left unfixed. The checklist line "it does not trap `KILL` or `STOP`" reads as a requirement, while the source's rule text only says those signals "cannot be trapped"; left as written.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/type-hints

Commit `2f9baf90`. 2 rules; lossless: 0 moved, 0 obsolete (both rules keep the intro's sentences verbatim, so no `lossless.json`). The intro is unchanged.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `must-keep-python-39-compatibility` offers `from __future__ import annotations` as the 3.9 route while noting "`list[str]` requires 3.9+"; on 3.9 itself both forms work, so the example's "requires 3.9+" adds nothing for the 3.9 floor it sets. Left as written.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/typescript-strictness

Commit `3bc4b8fa`. 17 rules; lossless: 23 moved, 0 obsolete. The intro stays verbatim. "Baseline (table stakes)", "Optional, situational flags", "Adopt incrementally on existing code" and "FORECAST — not yet relied upon as shipped" become rules (bold markers around RFC keywords dropped) and are removed; descriptive sentences are kept as rule sub-bullets. "Recommended near-defaults" keeps only its flag table, as `how-to`. The incremental-adoption reason and the principle link go to a `rationale` part. Seven `moved` entries cover sentences that differed from the base only by bold markers.

**promoted** (11 rules):
- "Configure `tsconfig.json` so the compiler catches the errors it is capable of catching" → `should-configure-tsconfig-to-catch-errors`: "You SHOULD configure `tsconfig.json` so the compiler catches the errors it is capable of catching." (also stays in the intro)
- "adopt the stricter flags deliberately rather than all at once" → `should-adopt-stricter-flags-deliberately`: "You SHOULD adopt the stricter flags deliberately rather than all at once." (also stays in the intro)
- "Use a narrowly-scoped `// @ts-expect-error` (with a reason) for the rare unavoidable case …" → `should-use-scoped-ts-expect-error`: "You SHOULD use a narrowly-scoped `// @ts-expect-error` (with a reason) for the rare unavoidable case so the suppression fails loudly if the underlying type later changes."
- "Enable these on greenfield projects; they close gaps `strict` alone leaves open." → folded into `should-enable-recommended-near-defaults` (already SHOULD): "New projects SHOULD enable `noUncheckedIndexedAccess` and `verbatimModuleSyntax`: enable these on greenfield projects; they close gaps `strict` alone leaves open."
- "Enable when modeling APIs where "absent" and "present but undefined" differ." → `should-enable-exact-optional-property-types-when-absent-differs`: "You SHOULD enable `exactOptionalPropertyTypes` (TS 4.4) when modeling APIs where "absent" and "present but undefined" differ; it adds real friction with loosely-typed third-party shapes, so it is opt-in, not a baseline."
- "Enable it when files are run via native type-stripping (…) so the source contains no non-erasable syntax." → `should-enable-erasable-syntax-only-for-type-stripping`: "You SHOULD enable `erasableSyntaxOnly` (TS 5.8) when files are run via native type-stripping (…) so the source contains no non-erasable syntax."
- "Pair it with `verbatimModuleSyntax`." → `should-pair-erasable-syntax-only-with-verbatim-module-syntax`: "You SHOULD pair `erasableSyntaxOnly` with `verbatimModuleSyntax`."
- "Turn on `strict` first; land that as its own change." → `should-turn-on-strict-first`: "On existing code, you SHOULD turn on `strict` first, and land that as its own change."
- "Enable one stricter flag at a time (…), fixing the fallout before moving on." → `should-enable-one-stricter-flag-at-a-time`: "You SHOULD enable one stricter flag at a time (…), fixing the fallout before moving on."
- "Treat the following as roadmap/proposed behavior. Do **not** write configs or guidance that assume it as current." → `should-not-assume-forecast-behavior-is-current`: "You SHOULD treat the forecast behavior below as roadmap/proposed behavior, and SHOULD NOT write configs or guidance that assume it as current."
- "As of this writing, confirm actual release state against the official [TypeScript blog] and [microsoft/typescript-go] before depending on it." → `should-confirm-native-compiler-release-state`: "As of this writing, you SHOULD confirm the actual release state of the native Go compiler and the TypeScript 7.0 line against the official `[TypeScript blog](…)` and `[microsoft/typescript-go](…)` before depending on it."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `must-set-strict` and `must-keep-setting-strict-explicitly` both require `"strict": true` (one for new projects, one until strict-by-default ships); kept, left unfixed. `should-not-enable-every-flag-in-one-sweep` is addressed to "Agents", while the rules beside it are addressed to anyone; left as written.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/use-roadmaplib

Commit `35a88428`. 2 rules; lossless: 0 moved, 0 obsolete (both rules keep the intro's MUST sentences verbatim, so no `lossless.json`). The intro is unchanged.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/value-objects

Commit `41721fda`. 4 rules; lossless: 3 moved, 0 obsolete. The intro stays verbatim. "When to introduce one" becomes a rule whose three criteria and closing sentence ("A primitive with none of these does not need wrapping …") are kept verbatim as sub-bullets; "How to build one" becomes three rules; both parts are removed. "Per language" stays verbatim as `how-to`.

**promoted** (3 rules):
- "Introduce a value object when a primitive meets any of these (and not before — see yagni):" → `should-introduce-value-object-when-criteria-met`: "You SHOULD introduce a value object when a primitive meets any of these (and not before — see yagni):"
- "Make it immutable with value equality (two value objects with the same contents are equal)." → `should-be-immutable-with-value-equality`: "A value object SHOULD be immutable with value equality (two value objects with the same contents are equal)."
- "Keep it small and focused on the single concept it represents." → `should-keep-value-object-small-and-focused`: "A value object SHOULD be kept small and focused on the single concept it represents."

`must-validate-at-construction` keeps its sentence verbatim ("Validate at construction and reject invalid input there (parse, don't validate) — a constructed instance MUST be known-valid."); its MUST governs it, so it is not counted as promoted.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/verification-harness

Commit `279fbb78`. 17 rules; lossless: 17 moved, 0 obsolete. The intro stays verbatim. The five section parts become rules (bold markers around RFC keywords dropped; 11 of the `moved` entries cover sentences that differ from the base only by those markers) and are removed. The enforcement-level table becomes a `how-to` part, "Enforcement levels". The two explanatory paragraphs (error messages are part of the interface; prompt text is advisory, with the Anthropic quote) go to a `rationale` part keyed by rule name. The "MUST NOT block on style nitpicks" sentence ("They **MUST NOT** …") becomes its own rule with "Gates" for "They".

**promoted** (5 rules):
- "Wire the command into the project so the agent can discover it (e.g., …)." → `should-wire-command-for-discovery`: "You SHOULD wire the command into the project so the agent can discover it (e.g., a documented `verify`/`lint`/`test` entry point referenced in agent-readable docs)."
- "Choose the weakest level that holds:" → `should-choose-weakest-enforcement-level-that-holds`: "You SHOULD choose the weakest enforcement level that holds: in-prompt, per-session, or deterministic gate."
- "Start with the cheapest check that catches a real failure, then add cases as concrete failure patterns emerge." → `should-start-with-cheapest-check`: "You SHOULD start with the cheapest check that catches a real failure, then add cases as concrete failure patterns emerge."
- "Do **NOT** pre-build an exhaustive suite up front (YAGNI)." → `should-not-prebuild-exhaustive-suite`: "You SHOULD NOT pre-build an exhaustive suite up front (YAGNI)." (the capital NOT is emphasis, not an RFC keyword, so a plain "do not" reads as SHOULD NOT)
- "When a new class of agent error appears, encode a check for it so the harness — not a human — catches the recurrence next time." → `should-encode-check-for-new-error-class`: "When a new class of agent error appears, you SHOULD encode a check for it so the harness — not a human — catches the recurrence next time."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `should-choose-weakest-enforcement-level-that-holds` (SHOULD pick the weakest level) sits beside `must-gate-correctness-deterministically` (MUST use the strongest, a deterministic gate, for correctness of unattended or merged changes); the MUST settles the overlap for that case, but the two pull in opposite directions; left unfixed. `must-gate-correctness-deterministically` reads "MUST be enforced by a deterministic gate (…), MUST NOT rely on prompt instructions alone" with no conjunction between its halves, as the source has it; left as written.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/visual-studio-project-files

Commit `34f05f0d`. 18 rules; lossless: 8 moved, 0 obsolete. The intro stays verbatim. The topic held two folded copies: the implementing sections ("SDK-style projects", "Shared properties", "Central package management", "Solution files", "Why this matters") and a reviewing copy ("Introduction", "Project structure", "Shared properties", "Packages", "Solutions", "Why this matters"). The implementing sections become rules and are removed, with their explanatory sentences kept verbatim as sub-bullets. The reviewing copy's checklist sentences are kept verbatim as the review-focus part, each keyed to the rule it checks, with its "Review project-file changes against …" sentence as the part's opening line; its duplicate H1 matches the intro's. Both "Why this matters" parts stay verbatim as `rationale` (the second headed "Why review checks these items").

**promoted** (3 rules):
- "Convert it." → `must-not-hand-edit-old-style-projects`: "Code MUST NOT hand-edit the old-style project format, and SHOULD convert it."
- "`Directory.Build.targets` is imported late and is the place for logic that must see the project's final values." → `should-put-late-logic-in-directory-build-targets`: "Logic that must see the project's final values SHOULD go in `Directory.Build.targets`." (the source sentence kept as its sub-bullet)
- "Use `BaseOutputPath`." → `must-not-set-outdir`: "Code MUST NOT set `OutDir` to change output folders, because it bypasses the per-project subfolders; it SHOULD use `BaseOutputPath`."

Split without promotion: "`VersionOverride` … MUST be used only for a documented exception, and a project MAY set `CentralPackageVersionOverrideEnabled` to `false` to forbid it." → `must-use-version-override-only-for-documented-exception` and `may-forbid-version-override`; "There SHOULD be one solution per deployable unit, and it MUST list every project, so a clean checkout builds." → `should-have-one-solution-per-deployable-unit` and `must-list-every-project-in-solution`.

**bars**: `look-for` moved (from the folded reviewing copy; lines added for `must-use-sdk-style-csproj`, `must-not-hand-edit-old-style-projects`, `should-set-implicit-usings-explicitly`, `should-put-late-logic-in-directory-build-targets`, `may-forbid-version-override`, `should-have-one-solution-per-deployable-unit` and `must-list-every-project-in-solution`; the checklist line "CI sets `ContinuousIntegrationBuild`. Output folders use `BaseOutputPath`, not `OutDir`." split at the sentence into two rules' lines), `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: the checklist line "Every `VersionOverride` has a reason." and the rule "MUST be used only for a documented exception" agree in aim, but a reason in the change is not the same as a documented exception; left unfixed.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/xcode-project-hygiene

Commit `2e57c1cc`. 25 rules; lossless: 24 moved, 0 obsolete. The intro stays verbatim (its statement is also named as a rule). The topic held two folded copies: the implementing sections ("Build settings live in xcconfig files", "Targets and schemes", "Entitlements", "Info.plist", "Signing", "Project generators", "Why this matters") and a reviewing copy ("Introduction", "Build settings", "Schemes and targets", "Entitlements", "Info.plist", "Signing", "Generated projects", "Why this matters"). The implementing sections become rules and are removed, explanatory sentences kept verbatim as sub-bullets. The reviewing copy's checklist sentences and its opening "Review project-file changes against …" paragraph are kept verbatim as the review-focus part, each line keyed to the rule it checks; its duplicate H1 matches the intro's. Both "Why this matters" parts stay verbatim as `rationale` (the second headed "Why review checks these items").

**promoted** (23 rules; only `must-share-and-check-in-schemes` and `must-include-privacy-usage-descriptions` carried a keyword):
- "An Xcode project is source code. Treat its settings, schemes and plists the way you treat any other file: small, reviewable in a diff, and defined once." → `should-treat-project-files-as-source`: "An Xcode project is source code; you SHOULD treat its settings, schemes and plists the way you treat any other file: small, reviewable in a diff, and defined once."
- "Put build settings in `.xcconfig` files, not in the project editor's Build Settings tab." → `should-put-build-settings-in-xcconfig`: "You SHOULD put build settings in `.xcconfig` files, not in the project editor's Build Settings tab."
- "Keep one shared file for settings common to every target and one per configuration or target for the differences." "Add only the settings you want to change." → `should-keep-shared-and-per-config-xcconfigs`: "You SHOULD keep one shared file for settings common to every target and one per configuration or target for the differences, and add only the settings you want to change."
- "Leave the target-level Build Settings tab empty for any setting an xcconfig already owns, or the target value silently wins." → `should-leave-target-level-settings-empty`: "You SHOULD leave the target-level Build Settings tab empty for any setting an xcconfig already owns, or the target value silently wins."
- "Create the file with "Configuration Settings File" and deselect all targets so Xcode does not embed it in the bundle." → `should-create-xcconfig-without-targets`: "You SHOULD create the file with "Configuration Settings File" and deselect all targets so Xcode does not embed it in the bundle."
- "Look up each setting name in the build settings reference before you use it." "Do not guess a name; an unknown setting is ignored without an error." → `should-look-up-setting-names`: "You SHOULD look up each setting name in the build settings reference before you use it, and SHOULD NOT guess a name; an unknown setting is ignored without an error."
- "Add one only for a capability the app uses, and review every added key as a security change." → `should-add-entitlements-only-for-used-capabilities`: "You SHOULD add one entitlement only for a capability the app uses, and review every added key as a security change."
- "Keep one `.entitlements` file per target and configuration need (for example a sandboxed macOS app and its helper), referenced through the `CODE_SIGN_ENTITLEMENTS` setting." → `should-keep-one-entitlements-file-per-need`: "You SHOULD keep one `.entitlements` file per target and configuration need (for example a sandboxed macOS app and its helper), referenced through the `CODE_SIGN_ENTITLEMENTS` setting."
- "Never copy an entitlements file from another app wholesale." → `must-not-copy-entitlements-wholesale`: "You MUST NOT copy an entitlements file from another app wholesale."
- "Keep the Info.plist small." → `should-keep-info-plist-small`: "You SHOULD keep the Info.plist small."
- "Prefer build-setting substitution (`$(PRODUCT_NAME)`, `$(MARKETING_VERSION)`) over literals, so a version or name is set once in the xcconfig." → `should-prefer-build-setting-substitution`: "You SHOULD prefer build-setting substitution (`$(PRODUCT_NAME)`, `$(MARKETING_VERSION)`) over literals, so a version or name is set once in the xcconfig."
- "Remove keys for features the app no longer has." → `should-remove-keys-for-removed-features`: "You SHOULD remove Info.plist keys for features the app no longer has."
- "Where the repository already uses XcodeGen (a `project.yml` spec), treat the spec as the source and the generated `.xcodeproj` as an output: regenerate it, do not hand-edit it, and either ignore it in version control or verify in CI that it matches the spec." → `should-treat-xcodegen-spec-as-source`: "Where the repository already uses XcodeGen (a `project.yml` spec), you SHOULD treat the spec as the source and the generated `.xcodeproj` as an output: regenerate it, do not hand-edit it, and either ignore it in version control or verify in CI that it matches the spec."
- "XcodeGen's spec points targets at xcconfig files through its `configFiles` option and at settings through its `settings` key; keep real values in the xcconfig and use the spec for structure." → `should-keep-real-values-in-xcconfig-with-xcodegen`: "XcodeGen's spec points targets at xcconfig files through its `configFiles` option and at settings through its `settings` key; you SHOULD keep real values in the xcconfig and use the spec for structure."
- "Do not introduce a generator into a repository that has none as part of an unrelated change." → `should-not-introduce-generator-in-unrelated-change`: "You SHOULD NOT introduce a generator into a repository that has none as part of an unrelated change."
- "Put the team ID and signing style in the xcconfig." → `should-put-team-and-signing-style-in-xcconfig`: "You SHOULD put the team ID and signing style in the xcconfig."
- "Use automatic signing for local development and an explicit, documented identity for release builds." → `should-use-automatic-local-explicit-release-signing`: "You SHOULD use automatic signing for local development and an explicit, documented identity for release builds."
- "Never check in a certificate, a private key or a provisioning profile." → `must-not-check-in-signing-secrets`: "You MUST NOT check in a certificate, a private key or a provisioning profile."
- "One scheme per thing a person builds, runs or tests." → `should-have-one-scheme-per-buildable-thing`: "There SHOULD be one scheme per thing a person builds, runs or tests."
- "Delete schemes that no longer build." → `should-delete-dead-schemes`: "You SHOULD delete schemes that no longer build."
- "Name targets and schemes after what they produce." "Do not leave `Untitled`, a copied target's `copy` suffix or a stale product name." → `should-name-targets-after-products`: "You SHOULD name targets and schemes after what they produce, and SHOULD NOT leave `Untitled`, a copied target's `copy` suffix or a stale product name."
- "Keep test targets separate from app targets, and set each target's deployment target explicitly in the xcconfig, not by default." → `should-separate-test-targets`: "You SHOULD keep test targets separate from app targets."; `should-set-deployment-target-explicitly`: "You SHOULD set each target's deployment target explicitly in the xcconfig, not by default."

**bars**: `look-for` moved (from the folded reviewing copy; lines added for `should-treat-project-files-as-source`, `should-keep-shared-and-per-config-xcconfigs`, `should-create-xcconfig-without-targets`, `should-have-one-scheme-per-buildable-thing`, `should-delete-dead-schemes`, `should-separate-test-targets`, `should-keep-one-entitlements-file-per-need`, `should-keep-info-plist-small`, `should-use-automatic-local-explicit-release-signing`, `should-keep-real-values-in-xcconfig-with-xcodegen` and `should-not-introduce-generator-in-unrelated-change`; the checklist line "No leftover `copy`, `Untitled` or dead scheme or target." is keyed to `should-name-targets-after-products`), `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none found. The reviewing copy's "Every added or changed entitlement key has a reason in the change description" asks for more than the rule "review every added key as a security change" (a stated reason in the change description); recorded, left unfixed.

**unfinished**: none.

## cookbook/guidelines/implementing/code-quality/yaml-frontmatter

Commit `e1677a08`. 2 rules; lossless: 0 moved, 0 obsolete (both rules and the parser sentence, now the first rule's sub-bullet, are verbatim). The intro stays verbatim, since its statement is what approve.py's GF-01 reads.

**promoted**: none (both requirements carried MUST / MUST NOT).

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.
