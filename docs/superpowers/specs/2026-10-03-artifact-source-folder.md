# Artifact source folder — format 1

*Status:* implemented in cookr (`core/artifact.py`, `core/artifact_types.py`).
*Plan:* [compiled artifacts and skills](../plans/2026-10-03-compiled-artifacts-and-skills.md), phase P1.

A cookbook artifact (a principle, guideline, ingredient or recipe) is a
**folder of source**. Every other form is compiled from it, including the
single-file markdown `doc` that the cookbook uses today.

## Layout

```
cookbook/guidelines/implementing/data/transactions-and-concurrency/
  artifact.json                  manifest: format, meta, parts
  intro.md                       `# Title` and the statement under it
  use-wal-mode-by-default.md     one file per `## ` section, heading line excluded
  ...
  history.md                     the `## Change History` section
```

The folder takes the place of `<name>.md` and has the same path without the
`.md`. The artifact's `domain` is unchanged.

## artifact.json

```json
{
  "format": 1,
  "meta": { "id": "…", "title": "…", "type": "guideline", "…": "…" },
  "parts": [
    {"part": "intro"},
    {"part": "use-wal-mode-by-default", "heading": "Use WAL Mode by Default"},
    {"part": "history", "heading": "Change History"}
  ]
}
```

- **`format`** is `1`. A reader refuses any format it doesn't know.
- **`meta`** holds today's frontmatter fields, in the same order and with the
  same values. YAML dates become ISO strings. The required fields are listed
  in `cookbook/introduction/conventions.md`. Recipes also need `ingredients`.
  Guidelines may carry `triggers`.
- **`parts`** lists, in order, the parts that compose the body. The part
  file is `<part>.md`.
  - `heading` is the section heading exactly as written. Only the intro has
    none.
  - Part names are kebab-case slugs of their headings. `## Change History` is
    always `history`. A repeated name, or one that collides with `intro`,
    `history` or `artifact`, gets a `-2`, `-3`, … suffix.

- **`names_hosts`** is optional. It gives the reason the artifact's shared
  text names a host or model family that cookr's host manifest declares, for
  example because the artifact documents Claude Code's file layout. Without
  it, naming one fails the neutrality check (`cookr validate`), because
  host-specific wording belongs in `hosts/` additions. Edits made through the
  doc keep it.

`cookbook/reference/artifact.schema.json` is the JSON Schema for this file.

## Composing the doc

```
---
<meta as YAML>
---
<intro.md>## <heading>
<part.md>## <heading>
<part.md>…
```

- **The body is lossless.** Splitting and then composing returns the
  original body byte for byte, including blank lines, trailing whitespace and
  a missing final newline.
  - Headings inside ``` or ~~~ fences never split.
- **Only the frontmatter is normalized.** JSON keeps the values, not the
  YAML spelling, so the emitter writes a single style:
  - Key order is kept.
  - Lists are block lists, and an empty list is `[]`.
  - `title`, `summary`, `approved-by` and `approved-date` are double-quoted.
  - `created` and `modified` are bare dates.
  - Any other string is plain if YAML reads it back unchanged; otherwise it
    is double-quoted.

  These are the majority styles in the corpus. Frontmatter values are
  scalars or lists of scalars, and a nested value is refused.

All 427 artifacts in `cookbook/` round-trip under test
(`test_every_cookbook_artifact_round_trips`).

## Types

`core/artifact_types.py` declares each type's required fields and body
shape. It is derived from
`cookbook/compliance/artifact-formatting/<type>-formatting.md`, and tests fail
if it drifts from those files.

| Type | Body between intro and history |
|---|---|
| principle | free-form; the intro carries the statement |
| guideline | free-form; the intro carries the statement |
| ingredient | closed, ordered: Overview … Compliance (19 sections, 7 optional) |
| recipe | closed, ordered: Overview … Compliance (11 sections, 1 optional) |

`validate(artifact)` reports these problems:

- missing or malformed fields: UUID, semver, status, ISO dates, list fields
- an intro that does not open with `# <title>`
- a free-form type with no statement under its title
- a missing final `## Change History` table
- for closed types: missing, unknown or out-of-order sections

## Other files in the folder

A folder may hold files that `parts` does not list. The `doc` target ignores
them. These names are reserved for the later phases:

- `hosts/`: host and model tuning additions (plan §3)
- `attribution.md`
- `examples/`

## Samples

`skills/cookr/cli/tests/fixtures/artifacts/` holds one artifact of each type,
in both forms:

- `docs/`: the source `.md`
- `folders/`: the converted folder

| Type | Sample |
|---|---|
| principle | `yagni` |
| guideline | `transactions-and-concurrency` |
| ingredient | `mcp-tool` |
| recipe | `mcp-server` |

## Corpus conformance at P1

These artifacts convert and round-trip, but they do not pass `validate`:

- 12 of 13 recipes predate the recipe section order, and they lack
  `ingredients`.
- 18 of 19 ingredients are missing a section, mostly `## Compliance`.
- 8 guidelines lack a statement under the title, or have a title that differs
  from their H1.
