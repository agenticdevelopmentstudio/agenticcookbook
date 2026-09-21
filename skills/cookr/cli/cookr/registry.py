"""Auto-discover modules in `cookr.modules`.

A module is a file under `cookr/modules/` (or a package with an __init__)
exposing NAME, HELP, register(subparsers) and run(args, ctx).
"""

from __future__ import annotations

import importlib
import pkgutil
from types import ModuleType


def discover() -> list[ModuleType]:
    from . import modules as modules_pkg

    found = []
    for info in pkgutil.iter_modules(modules_pkg.__path__):
        if info.name.startswith("_"):
            continue
        mod = importlib.import_module(f"cookr.modules.{info.name}")
        if all(hasattr(mod, attr) for attr in ("NAME", "HELP", "register", "run")):
            found.append(mod)
    return sorted(found, key=lambda m: m.NAME)
