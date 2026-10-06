# Cookbook project format

- **Date:** 2026-10-05
- **Status:** draft — being settled type by type with Mike
- **Supersedes:** the identity, attribution and part-file layout of
  `2026-10-03-artifact-source-folder.md`

## Model

Everything lives in a **project**. A project holds artifacts — principles, guidelines,
ingredients and recipes. Each artifact is one directory, is one thing, and compiles to one
skill. An artifact holds only the content that makes it unique; anything shared across the
project (creator, attribution, license) is defined once at the project level.

Artifacts refer to each other **by id**, never by path. The project index maps each id to the
artifact's local path, so moving a directory breaks nothing. A recipe declares the recipes and
ingredients it is made of, but they are not inside it: they live elsewhere in the project and
are found through the index. Each artifact is encapsulated and independent.

There is one project format. A project's `structure.kind` says what it is: `library` for a
collection that does not build one specific thing (this repo's `cookbook/`), `app` for one
that does (what `cookbook-project.schema.json` used to describe separately, folded in as a
kind).

## The project

```
cookbook/
  cookbook.json      manifest: name, kind, version, creator, attribution, license
  README.md          optional: describes what is in the project
  ATTRIBUTION.md     the project's single attribution file
  LICENSE            the project's single license
  index.json         id → local path, for every artifact
  research/          research material artifacts can cite
  principles/  guidelines/  ingredients/  recipes/
```

## Identity: rdid

An artifact's id is a reverse-domain id, not a UUID, and replaces the old path-based `domain`
(a website lookup by id replaces domain URLs):

```
<creator>.<type>.<domain>.<more specific slugs as appropriate>.<name>

<creator>.recipe.app.lifecycle
<creator>.ingredient.ui.components.status-bar
<creator>.guideline.testing.test-pyramid
<creator>.principle.simplicity          principles have no domain
```

- **`<creator>`** is user-defined in `cookbook.json`. It only has to be unique, or at least
  unique in the user's environment. Attribution is defined in the same place.
- **Source** artifacts carry the local part only (`recipe.app.lifecycle`); the creator is the
  project's.
- **Compiled** output carries full rdids everywhere. Consuming tools never assemble an id.

## Common: `artifact.json`

Every artifact directory has one. Only what is unique to the artifact:

| Field | Notes |
|---|---|
| `id` | local rdid; its first segment is the type, so there is no separate `type` field |
| `title`, `summary` | |
| `version`, `status`, `created`, `modified` | |
| `platforms`, `tags` | |
| `depends-on`, `related` | ids, resolved through the project index |
| `references` | structured entries — see below |
| `skill` | `names_hosts`, `routes`, only when set |

Gone from every artifact: the UUID, `domain`, `type`, `author`, `copyright`, `license`,
`language` and the approval stamp.

### References

An array. Each entry is either a source or a pointer into the project's `research/`:

```json
"references": [
  {"title": "Simple Made Easy", "author": "Rich Hickey", "year": 2011,
   "url": "https://…", "note": "the simple-vs-easy distinction"},
  {"research": "research.simplicity-sources"}
]
```

### Content layout

`artifact.json` sits at the top of the directory. Where a type has several content files,
they go in descriptive category folders, so the directory reads as one artifact at a glance
and never as a collection of siblings.

Every artifact directory, whatever its type:

```
<artifact>/
  artifact.json      common fields (+ the type's own)
  <type>.md          the shared, neutral content: principle.md, guideline.md, …
  history.md         Change History: | Version | Date | Summary |
  platforms/         optional: how the content is applied per target platform
    swift.md  kotlin.md  typescript.md  windows.md …
  ai/                optional: wording additions per AI vendor and model
    anthropic/claude-opus-5-5.md  openai/gpt-5-codex.md …
```

### Platform and host tuning

Every artifact type may vary along two axes:

- **Platform** — the same content applied to a target: SwiftUI's
  `\.accessibilityReduceMotion` vs Android's `animator_duration_scale`. `platforms/<name>.md`.
- **AI vendor / model** — the same instruction worded for the model that reads it:
  `ai/<vendor>/<model>.md`, e.g. `ai/anthropic/claude-opus-5-5.md`. Its body is appended to the
  shared content; an optional YAML frontmatter block overrides skill frontmatter keys (e.g. a
  shorter `description`). The file name is the vendor's model id. The path, not a filename
  marker, says what it is, and no file is ever named `claude.md` (which a case-insensitive
  filesystem would make `CLAUDE.md`). Replaces cookr's `hosts/*.add.md|yaml`.
- **Group files** cover more than one model, marked by an `-all` suffix so they never collide
  with a model id: `claude-all.md` (every Claude model), `claude-opus-all.md` (every Opus).
  cookr stacks what exists, broadest first — for Opus 5.5:
  `claude-all.md` + `claude-opus-all.md` + `claude-opus-5-5.md`. Every level is optional.

  ```
  ai/
    anthropic/
      claude-all.md
      claude-opus-all.md
      claude-opus-5-5.md
      claude-haiku-all.md
    openai/
      gpt-5-codex.md
  ```

cookr compiles one skill per target: shared content + the consumer's platform file + the model
addition. Both folders are optional; an artifact with no variation has neither.

The axes are **independent**: there is no combined platform × model file. A Swift skill for
Haiku is the shared content + `platforms/swift.md` + the Haiku `ai/` files.

## Principle

```
simplicity/
  artifact.json      common fields + `when`
  principle.md       the principle, written as skill instructions for an agent
  history.md         Change History
```

- **Written for agents.** Everything in the cookbook is for agents, so a principle is written
  once, in skill wording: `when` (in `artifact.json`) is the trigger that becomes the skill's
  description; `principle.md` tells the agent when it applies, what to check, and what to do.
- **References:** MUST have at least one, SHOULD have several.
- **History** stays its own file: `| Version | Date | Summary |` (attribution is the
  project's, so there is no author column).

## Guideline

Proposed, not yet settled:

```
accessibility/
  artifact.json      common fields + `when`
  guideline.md       the guideline as skill instructions; supporting sections
                     (requirements, common violations, checklist, review signals…) are headings
  history.md
  platforms/         when it has platform-specific application
```

- Written once in skill wording, like a principle.
- Today's layout spreads one guideline across sibling files (`intro.md`, `swift.md`,
  `kotlin.md`, …) that read as a collection; under this layout they become `guideline.md` and
  `platforms/`.

## Ingredient

To be settled.

## Recipe

To be settled.
