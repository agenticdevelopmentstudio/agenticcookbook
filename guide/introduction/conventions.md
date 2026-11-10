---
id: 7a3e1f2c-8b4d-4e6a-9c5f-1d2e3f4a5b6c
title: "Conventions"
type: reference
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-11-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "All conventions for file format, naming, cross-referencing, and authoring in this repository."
platforms: []
tags:
  - conventions
  - naming
  - frontmatter
  - format
depends-on: []
related: []
references:
  - https://datatracker.ietf.org/doc/html/rfc8141
  - https://go.dev/doc/modules/layout
  - https://docs.oracle.com/javase/tutorial/java/package/namingpkgs.html
  - https://maven.apache.org/guides/mini/guide-naming-conventions.html
  - https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/understanding_utis/understand_utis_conc/understand_utis_conc.html
  - https://semver.org
  - https://spdx.org/licenses/
  - https://www.dublincore.org/specifications/dublin-core/dces/
  - https://schema.org/CreativeWork
---

# Conventions

All conventions for file format, naming, cross-referencing, and authoring in this repository.

## File Format

Every markdown file starts with a YAML frontmatter block containing these fields:

```yaml
---
id: <uuid>
title: <human readable title>
type: principle | guideline | ingredient | recipe | cookbook | workflow | reference
version: 1.0.0
status: wip | draft | review | accepted | deprecated
language: en
created: YYYY-MM-DD
modified: YYYY-MM-DD
author: <name>
copyright: YYYY Mike Fullerton
license: MIT
summary: <one-line description for search and tooltips>
platforms: []
tags: []
depends-on: []
related: []
references: []
approved-by: ""
approved-date: ""
triggers: []
---
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | UUID, globally unique, stable across renames and moves. The artifact's identity: every link stores it. |
| `title` | Yes | Human-readable title |
| `type` | Yes | One of: `principle`, `guideline`, `ingredient`, `recipe`, `cookbook`, `workflow`, `reference`, `compliance` |
| `version` | Yes | Semver. Major for breaking changes, minor for new content, patch for clarifications. Immutable once on main — changes require a version bump. |
| `status` | Yes | `wip` (actively being built — LLM consumers skip this content), `draft` (complete first pass, awaiting review), `review` (ready for feedback), `accepted` (stable), `deprecated` (superseded) |
| `language` | Yes | BCP 47 language tag. Default: `en` |
| `created` | Yes | ISO 8601 date. Immutable after creation. |
| `modified` | Yes | ISO 8601 date. Updated on every change. |
| `author` | Yes | Primary author name |
| `copyright` | Yes | `YYYY Mike Fullerton` |
| `license` | Yes | SPDX license identifier. Default: `MIT` |
| `summary` | Yes | One-line description (~120 chars). Used in search results, tooltips, and index pages. |
| `platforms` | Yes | List of platforms this content applies to. Empty list `[]` if universal. Values: `swift`, `kotlin`, `typescript`, `csharp`, `python`, `windows`, `macos`, `ios`, `web` |
| `tags` | Yes | 1-5 lowercase tags for discoverability. Empty list `[]` if none. |
| `depends-on` | Yes | UUIDs of content that should be read first (see Identity below). Empty list `[]` if none. |
| `related` | Yes | UUIDs of related content ("see also"). Empty list `[]` if none. |
| `references` | Yes | External URLs referenced by this content. Empty list `[]` if none. |
| `ingredients` | Recipe only | UUIDs of the ingredients this recipe composes. Required when `type` is `recipe`. |
| `approved-by` | Yes | Approval stamp from `/approve-artifact`. Format: `"approve-artifact <version>"`. Empty string `""` if not yet approved. |
| `approved-date` | Yes | ISO 8601 date when the artifact was last approved. Empty string `""` if not yet approved. |
| `triggers` | Guideline only | Activity or context tags that make this guideline relevant to an AI agent. Empty list `[]` if not yet classified. Values from the canonical trigger taxonomy in `guide/introduction/trigger-guide.md`. |

### Source Folders

Every principle, guideline, ingredient and recipe is stored as a source folder. The single
`.md` file described above is compiled from it on demand and is never committed:

```
<name>/
  artifact.json   format, meta (the frontmatter fields above) and the ordered part list
  intro.md        the `# Title` and its statement
  <section>.md    one part per `## ` section
  history.md      the Change History section
```

`artifact.json` carries `"format": 2`. The folder is the only committed form: edit its parts
directly, or compile a doc with `cookr compile`, edit it, fold it back with
`cookr convert --update <path>`, then delete the doc. `cookr validate` fails while a compiled doc
present beside its folder disagrees with it, and a committed compiled doc fails cookr's tests.
The full format is in `docs/superpowers/specs/2026-10-03-artifact-source-folder.md`.

### Change History

Every file ends with a Change History section. `cookr bump <path> --summary "<what changed>"`
raises the version, sets `modified` and adds the row deterministically:

```markdown
## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | Name | Initial creation |
```

Each row corresponds to a version bump. Once a version is on main, it is immutable.

### Compliance Section

Recipes and guidelines include a `## Compliance` section listing the compliance checks that were evaluated and their results. Compliance checks are defined in `tbd/compliance/` — see `tbd/compliance/INDEX.md` for the full list. Each named check (`### <check-name>` in a category file) has its own UUID and rdid in `cookbook/index.json` (`adc.check.<category>.<check-name>`), so it is linked like an artifact.

**Format:**

```markdown
## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [adc.check.security.secure-log-output](cookbook:b258657f-bb73-5491-9c70-0d14afdfa6ce) | passed | Security |
| [adc.check.accessibility.keyboard-navigable](cookbook:56755f54-b31f-59aa-a77d-eeb0cd87731a) | passed | Accessibility |
```

**Rules:**
- Only list checks that are applicable — omit entire categories that don't apply
- Status values: `passed`, `failed`, `partial`
- Each check is an in-text link to its index entry: `[<check rdid>](cookbook:<check uuid>)`
- The Compliance section appears after Design Decisions and before Change History

**Architecture:** Recipes → compliance checks → guidelines → external standards. Each layer is one level of indirection. Compliance checks reference guidelines; guidelines reference external standards (OWASP, WCAG, etc.).

### Standards Alignment

This format is aligned with:
- **Dublin Core** (ISO 15836): `id` → `dc:identifier`, `title` → `dc:title`, `author` → `dc:creator`, `summary` → `dc:description`, `tags` → `dc:subject`
- **Schema.org CreativeWork**: `version`, `dateCreated`, `dateModified`, `creativeWorkStatus`, `keywords`
- **SPDX** (ISO/IEC 5962): `license` field uses SPDX identifiers
- **SemVer 2.0.0**: `version` field

## Naming

### Identity: UUIDs and rdids

**The UUID is the identity.** Every artifact has a UUID (`id`), and so does every cookbook
(`id` in `cookbook/cookbook.json`). Every link stores UUIDs. Neither a name nor a path is ever
used as identity: both can change without breaking a link.

**The rdid is a readable name**, held once in the cookbook's index next to the UUID. It has the
form `<cookbook-rdid>.<type>.<path, dotted>`:

| Source folder | rdid |
|---------------|------|
| `cookbook/principles/simplicity/` | `adc.principle.simplicity` |
| `cookbook/guidelines/testing/test-pyramid/` | `adc.guideline.testing.test-pyramid` |
| `cookbook/ingredients/ui/components/empty-state/` | `adc.ingredient.ui.components.empty-state` |
| `cookbook/recipes/ui/windows/settings-window/` | `adc.recipe.ui.windows.settings-window` |
| `tbd/compliance/security.md`, `### secure-log-output` | `adc.check.security.secure-log-output` |

This cookbook's rdid is `adc`. `cookr rename <uuid|rdid> <new-rdid>` renames an rdid: it rewrites
one index entry and refreshes the labels that show it; no link changes. `cookr id <uuid|rdid>`
looks an artifact up in either direction.

Moving an artifact takes two steps. First move its folder; skill routes follow the folder path.
Then `cookr update` records the new path, and `cookr rename` gives it the matching rdid. The rdid
never changes on its own, so a move without a rename keeps the old name.

### The Index

Each cookbook has `cookbook/cookbook.json` (`format`, `id`, `rdid`) and `cookbook/index.json`.
The index is edited only through cookr commands, never by hand. Each entry, keyed by UUID,
holds the artifact's `kind`, `rdid` and `path`, and the code that implements it:

- `cookr update` writes `rdid` and `path` from the source folders, stores authored rdids as
  UUIDs, and regenerates the INDEX pages.
- `cookr implements <uuid|rdid> <location> --platform <p>` records an implementation;
  `--remove <location>` drops one.
- `cookr confirm <uuid|rdid>` records the implementations as conforming to the artifact's
  current version.
- `cookr validate` checks that every link resolves, the index matches the folders, and
  implementations exist.

The index's `foreign` map caches the rdid of every foreign UUID this cookbook links to. The
schemas are `references/cookbook.schema.json` and `references/index.schema.json`.

### Link Forms

People and agents write rdids; cookr stores UUIDs.

| Where | Local | Foreign (another cookbook) |
|-------|-------|----------------------------|
| `depends-on`, `related`, `ingredients` | `"<artifact-uuid>"` | `"<cookbook-uuid>/<artifact-uuid>"` |
| In text | `[<rdid>](cookbook:<artifact-uuid>)` | `[<rdid>](cookbook:<cookbook-uuid>/<artifact-uuid>)` |

The in-text label is a cached rdid for the reader; cookr refreshes it on rename. An in-text link
names a whole artifact or check and carries no fragment.

### Fragments — Addressing Sections Within a Document

Use short-form `#` fragments to reference sections and items within the same document:

```
#requirements/ordered-list
#states/error
```

To point at a section of another artifact, link the artifact and name the section in prose:
`the ordered-list requirement of [adc.ingredient.ui.components.ai-chat-control](cookbook:f9f12465-9f73-40ef-b9f6-d124090781f5)`.

| Section | Fragment pattern |
|---------|-----------------|
| Overview | `#overview` |
| Requirements | `#requirements/<name>` |
| Appearance | `#appearance/<property>` |
| States | `#states/<state-name>` |
| Platforms | `#platforms/<platform>` |
| Accessibility | `#accessibility/<item>` |
| Test vectors | `#test-vectors/<id>` |
| Configuration | `#configuration/<option>` |
| Edge cases | `#edge-cases/<name>` |
| Logging | `#logging/<event>` |
| Localization | `#localization/<key>` |
| Feature flags | `#feature-flags/<flag>` |
| Analytics | `#analytics/<event>` |
| Privacy | `#privacy` |
| Ingredients | `#ingredients/<name>` |
| Integration requirements | `#integration-requirements/<name>` |
| Layout | `#layout` |
| Shared state | `#shared-state/<state>` |
| Integration test vectors | `#integration-test-vectors/<id>` |
| Design decisions | `#design-decisions/<name>` |
| Change history | `#change-history/<version>` |

### Named Requirements

Requirements use descriptive kebab-case names, not sequential numbers. Format: `**<name>**: <description>`

```markdown
- **ordered-list**: The control MUST maintain an ordered list of messages.
- **scroll-to-bottom**: The control MUST auto-scroll to the newest message.
```

Constraints:
- Names MUST be unique within the requirements section of a file
- Names MUST be kebab-case (URL-safe)
- Names SHOULD be descriptive of the requirement's subject

**Cross-referencing requirements:**

Between documents: `See the ordered-list requirement of [adc.ingredient.ui.components.ai-chat-control](cookbook:f9f12465-9f73-40ef-b9f6-d124090781f5)`

Within the same document: `Validates: #requirements/ordered-list`

### File Naming Rules

- **kebab-case** for all filenames: `file-tree-browser.md`
- **Descriptive names**: the filename describes what the thing **is**, not what it does
- **No numeric prefixes**: the path provides the hierarchy
- **`.md` extension** for all content files
- **`index.md`** for landing pages (lowercase)

### Cookbook Directory Naming

Standalone cookbook directories MUST use the suffix `-cookbook`. For a source repository named `my-app`, the cookbook directory is `my-app-cookbook/`. This distinguishes cookbooks from other directories and makes the project type immediately recognizable.

A cookbook that specifies code in its own repository (a library cookbook, `structure.kind: library`) is instead that repository's `cookbook/` directory. Its directory tree mirrors the arrangement of the code, and each spec is a source folder named by its file name alone. No spec carries a Reference Implementations table: the code that implements it is recorded in the cookbook's `index.json` with `cookr implements <uuid|rdid> <location> --platform <p>`, and `cookr confirm` marks it as conforming to the current version. A compiled doc or skill shows those rows as a derived `## Reference Implementations` section. Where the code lives is tool configuration, not part of the cookbook: the repo's `.cookr.json` lists its `roots` (`references/cookr-config.schema.json`), and `cookr coverage` reports source files under them that no spec's implementations claim. A cookbook with no code of its own (this one) has no `.cookr.json` roots.

```
my-repo/
├── .cookr.json                # roots: where the code lives (path, platform, kind, group, ignore)
├── cookbook/
│   ├── cookbook.json          # format, id, rdid; structure.kind: library
│   ├── index.json             # every artifact's UUID, rdid, path and implementations
│   └── ai-plugin-kit/
│       ├── ai-plugin/         # a source folder: artifact.json + one .md per section
│       └── models/
│           └── model-capability/
└── packages/...               # the code the implementations point at
```

```
my-app-cookbook/
├── cookbook.json
├── app/
│   └── ...specs...
└── context/
    └── ...research...
```

### Cross-Referencing

Use an in-text link for cross-document references: `See [adc.guideline.testing.test-pyramid](cookbook:f3ae65a6-f51d-4e42-8f79-fa8097dd3480)`

Use short-form fragments for within-document references: `See #requirements/ordered-list`

In the `depends-on`, `related` and `ingredients` meta fields, list UUIDs. An rdid may be written
there; `cookr update` replaces it with the UUID:

```json
"depends-on": [
  "ce2af25c-4f18-41ae-91b9-342e363449b3",
  "22729bee-7ab4-4648-aa5a-2beef067d0c3"
],
"related": ["f3ae65a6-f51d-4e42-8f79-fa8097dd3480"]
```

## Platform Notes

An ingredient or recipe carries one bullet per platform under `## Platform Notes`:
SwiftUI, Compose, React/Web, AppKit / UIKit, and WinUI 3. The **WinUI 3** bullet
is required for any recipe counted by `cookr coverage`; a recipe with an empty
WinUI 3 bullet reports as `partial`.

## RFC 2119 Keywords

Use RFC 2119 keywords for all behavioral requirements:

- **MUST** / **MUST NOT**: Absolute requirements.
- **SHOULD** / **SHOULD NOT**: Recommendations.
- **MAY**: Optional behavior.

## Template Variables

Content uses `{{placeholder}}` tokens for consumer-specific values. Never hardcode app-specific values.

| Variable | Example | Purpose |
|----------|---------|---------|
| `{{app_name}}` | `MyApp` | Application name (PascalCase) |
| `{{app_name_lower}}` | `myapp` | Application name (lowercase) |
| `{{org_package}}` | `company.myapp` | Package/bundle identifier root |
| `{{bundle_id}}` | `com.company.app` | Bundle/package identifier |
| `{{app_scheme}}` | `myapp` | URL scheme for deep links |
| `{{app_prefix}}` | `myapp` | Prefix for feature flag keys |
| `{{api_base_url}}` | `https://api.example.com` | Production API URL |
| `{{db_name}}` | `myapp.db` | Local database filename |

## Design Decisions

Any choice that affects behavior or structure must be explicitly noted and approved. Record approved decisions in the relevant file's **Design Decisions** section so all implementations stay consistent.

Format:
```markdown
**Decision**: Description of the choice.
**Rationale**: Why this choice was made.
**Approved**: yes | pending
```

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID identity, rdids and index.json replace `domain`; implementations live in index.json and code roots in `.cookr.json`; compiled docs are not committed |
| 1.7.0 | 2026-10-03 | Mike Fullerton | Source folders: artifacts are stored as folders and the .md is compiled from them |
| 1.6.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.5.0 | 2026-04-09 | Mike Fullerton | Add triggers field for guideline-type artifacts |
| 1.4.0 | 2026-04-06 | Mike Fullerton | Rename concoction to cookbook; add cookbook type to enum |
| 1.3.0 | 2026-04-05 | Mike Fullerton | Add ingredient, recipe (composition), and concoction types; rename cookbook-project to concoction |
| 1.2.0 | 2026-04-04 | Mike Fullerton | Add approved-by and approved-date frontmatter fields |
| 1.1.0 | 2026-04-02 | Mike Fullerton | Add cookbook project directory naming convention (-cookbook-project suffix) |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial consolidation from 5 separate convention files |
