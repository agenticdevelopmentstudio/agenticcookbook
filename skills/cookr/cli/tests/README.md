# `cookr` CLI tests

```
skills/cookr/cli/tests/
  conftest.py       sys.path (cookr + cookbook) and the mini-repo fixture
  fixtures/         mini-repo: a tiny target repo with .cookr.json, sources and recipes
  unit/             in-process, no install
  functional/       subprocess against the installed `cookr` shim; skips if not on PATH
```

Run from the repo root:

```bash
python3 -m pytest skills/cookr/cli/tests/unit -q      # fast
python3 -m pytest skills/cookr/cli/tests -q           # needs ./install.sh
```
