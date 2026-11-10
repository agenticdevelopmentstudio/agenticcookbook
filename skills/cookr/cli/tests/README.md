# `cookr` CLI tests

```
skills/cookr/cli/tests/
  conftest.py       sys.path (cookr + cookbook) and the mini_repo/legacy_repo fixtures
  fixtures/
    mini-repo/      a tiny format-2 library cookbook: .cookr.json, cookbook/cookbook.json,
                    cookbook/index.json, sources, and source-folder specs (made by
                    upgrading v1-repo)
    v1-repo/        the same cookbook in format 1 (domains, Reference Implementations
                    sections), for `cookr upgrade`
    md-repo/        the same cookbook as plain docs with no source folders, for `cookr upgrade`
    legacy-repo/    a tiny flat .cookr.json corpus, for `cookr upgrade` to convert
    artifacts/      sample docs and the format-2 source folders they split into
  unit/             in-process, no install
  functional/       subprocess against the installed `cookr` shim; skips if not on PATH
```

`mini_repo` and `legacy_repo` (in `conftest.py`) each hand a test a fresh, mutable
copy of the matching fixture under `tmp_path`. Most modules (`inventory`,
`coverage`, `prompt`, `arrangement`, `relink`) work against `mini_repo`, since
they operate on an already-organized format-2 library cookbook. `cookr upgrade`
(`test_upgrade.py`) works against `v1-repo`, `md-repo` and `legacy_repo`, and the
organize placement it reuses (`test_organize.py`) against `legacy_repo`.

`repo_v2` (session-scoped) is a format-2 copy of this repo's own cookbook, for
the tests that read the real corpus while it is still format 1.

Run from the repo root:

```bash
python3 -m pytest skills/cookr/cli/tests/unit -q      # fast
python3 -m pytest skills/cookr/cli/tests -q           # needs ./install
```
