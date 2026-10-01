# `cookr` CLI tests

```
skills/cookr/cli/tests/
  conftest.py       sys.path (cookr + cookbook) and the mini_repo/legacy_repo fixtures
  fixtures/
    mini-repo/      a tiny library cookbook: cookbook/cookbook.json, sources, and specs
    legacy-repo/    a tiny flat .cookr.json corpus, for `cookr organize` to convert
  unit/             in-process, no install
  functional/       subprocess against the installed `cookr` shim; skips if not on PATH
```

`mini_repo` and `legacy_repo` (in `conftest.py`) each hand a test a fresh, mutable
copy of the matching fixture under `tmp_path`. Most modules (`inventory`,
`coverage`, `prompt`, `arrangement`, `relink`) work against `mini_repo`, since
they operate on an already-organized library cookbook. `cookr organize`
(`test_organize.py`, `test_modules_organize.py`) works against `legacy_repo`,
converting it into a library cookbook.

Run from the repo root:

```bash
python3 -m pytest skills/cookr/cli/tests/unit -q      # fast
python3 -m pytest skills/cookr/cli/tests -q           # needs ./install.sh
```
