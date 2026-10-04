# Pre-commit integration

The `cookr` CLI exposes two hooks usable with [`pre-commit`](https://pre-commit.com/).
Both run the same Phase A deterministic checks (frontmatter, semver, UUID, link
resolution, duplicate id); the validate hook additionally diffs every `INDEX.md`
against what the indexing engine would generate now.

| Hook id            | Command                  | Purpose                                              |
|--------------------|--------------------------|------------------------------------------------------|
| `cookbook-validate`| `cookr validate`         | Phase A + index drift. Catches stale `INDEX.md`.     |
| `cookbook-lint`    | `cookr lint --no-llm`    | Phase A only. Faster; use when drift isn't a concern.|

## Setup

1. Install the CLI: clone the agenticcookbook repo and run `./install`.
   Verify with `command -v cookr`.
2. In the repo that contains your cookbook, install pre-commit
   (`pip install pre-commit`) and create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/agenticdevelopercookbook/agenticcookbook
    rev: <pin a tag or commit sha>
    hooks:
      - id: cookbook-validate
```

3. Enable: `pre-commit install`.
4. (Optional) First-time backfill: `pre-commit run --all-files`.

## Why both hooks

`cookbook-validate` is the right default. It guarantees a contributor cannot
land a stale `INDEX.md` — drift only surfaces when a new recipe is added but
`cookr update` was forgotten.

`cookbook-lint` exists for repos where drift is checked elsewhere (e.g. a CI
job runs `validate`, but the pre-commit only needs the per-file rules to stay
fast on every commit).

## Failures and fixes

Both hooks print a `fix` column under each failure row. The common cases:

- `required-field:...` or `frontmatter-present` → run `cookr update`.
- `drift` (only `validate`) → run `cookr update` to regenerate indexes.
- `link-resolves` / `domain-matches-path` → manual fix; the hint identifies
  the bad value.

The hooks always run (`always_run: true`, `pass_filenames: false`) because
drift can be invisible to git's per-file view: adding a new recipe changes
the parent `INDEX.md` even if the recipe file itself is the only thing in
the staged diff.
