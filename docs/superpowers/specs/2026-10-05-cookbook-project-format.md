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
- No category folders: one content file needs none.

## Guideline

To be settled.

## Ingredient

To be settled.

## Recipe

To be settled.
