# `cookbook` CLI tests

```
skills/cookbook/cli/tests/
  conftest.py            sys.path + references_dir + fixture-repo wiring
  unit/                  in-process, no install, no network — fast
  functional/            subprocess against installed `cookbook`; clones cookbook-tests
```

## Running

From the repo root:

```bash
# Unit tests only (no install, no network)
python3 -m pytest skills/cookbook/cli/tests/unit -q

# Full suite — requires `./install` first and SSH access to
# git@github.com:agenticdevelopercookbook/cookbook-tests.git
python3 -m pytest skills/cookbook/cli/tests -q
```

If `cookbook` isn't on `$PATH`, functional tests skip rather than fail. Same for fixture-backed tests when the fixture repo can't be cloned.

## Fixture repo override

```bash
COOKBOOK_TESTS_REPO=/path/to/local/cookbook-tests python3 -m pytest skills/cookbook/cli/tests
```

Useful when iterating on fixtures locally — point at the working copy instead of the remote.
