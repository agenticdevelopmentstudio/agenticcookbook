"""Auto-discovery of cookbook modules."""

from __future__ import annotations

from cookbook.core.cliapp import discover as _discover


def discover():
    return _discover("cookbook.modules")


REQUIRED_ATTRS = ("NAME", "HELP", "register", "run")
EXPECTED_NAMES = {"create", "update", "lint", "validate", "plan"}


def test_discover_returns_all_v1_modules():
    mods = discover()
    names = {m.NAME for m in mods}
    assert EXPECTED_NAMES.issubset(names), f"missing: {EXPECTED_NAMES - names}"


def test_discover_returns_sorted():
    mods = discover()
    names = [m.NAME for m in mods]
    assert names == sorted(names)


def test_every_module_has_required_attrs():
    for mod in discover():
        for attr in REQUIRED_ATTRS:
            assert hasattr(mod, attr), f"{mod.__name__} missing `{attr}`"


def test_help_strings_are_non_empty():
    for mod in discover():
        assert isinstance(mod.HELP, str) and mod.HELP.strip()
