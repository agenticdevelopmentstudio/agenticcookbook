"""Config-driven index regeneration.

Each index config in references/index-configs/*.yaml declares:

    name: <human label>
    strategy: flat | use_case | triggers
    applies_when:
        path_exists: <relative path, e.g. "guidelines">
    target_dir: <relative path walked by the strategy>
    output: <relative output file>
    # strategy-specific keys follow

Engine flow per config: check applies_when; if matched, ask the strategy to
render output text; write/skip-if-unchanged. Strategies are pure functions of
config + cookbook root + filesystem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from ..core.deps import require

yaml = require("yaml")

from . import flat, triggers, use_case  # noqa: E402

STRATEGIES = {
    "flat": flat,
    "use_case": use_case,
    "triggers": triggers,
}


@dataclass
class IndexResult:
    name: str
    strategy: str
    status: str  # "written" | "unchanged" | "skipped"
    output: str = ""
    reason: str = ""
    counts: dict = field(default_factory=dict)


def _applies(applies_when: dict | None, root: Path) -> tuple[bool, str]:
    if not applies_when:
        return True, ""
    path_exists = applies_when.get("path_exists")
    if path_exists:
        p = root / path_exists
        if not p.exists():
            return False, f"missing dir: {path_exists}"
    return True, ""


def load_configs(configs_dir: Path) -> list[dict]:
    if not configs_dir.is_dir():
        return []
    configs = []
    for p in sorted(configs_dir.glob("*.yaml")):
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict) and data.get("strategy") in STRATEGIES:
            data["_path"] = str(p)
            configs.append(data)
    return configs


def _undated(text: str) -> list[str]:
    return [line for line in text.splitlines() if not line.startswith("modified:")]


def render(config: dict, root: Path, today: date | None = None) -> tuple[str, dict]:
    """The index text for `config`. When only the `modified:` stamp would
    change, the existing text is returned, so a new day alone is no change."""
    text, counts = STRATEGIES[config["strategy"]].generate(
        config, root, today=today or date.today())
    out = root / config["output"]
    if out.exists():
        existing = out.read_text(encoding="utf-8")
        if _undated(existing) == _undated(text):
            return existing, counts
    return text, counts


def run_one(config: dict, root: Path, today: date | None = None) -> IndexResult:
    name = config.get("name", config.get("_path", "<unnamed>"))
    strategy_name = config["strategy"]
    ok, reason = _applies(config.get("applies_when"), root)
    if not ok:
        return IndexResult(name=name, strategy=strategy_name, status="skipped", reason=reason)

    text, counts = render(config, root, today=today)

    output_path = root / config["output"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and output_path.read_text(encoding="utf-8") == text:
        return IndexResult(
            name=name, strategy=strategy_name, status="unchanged",
            output=str(output_path.relative_to(root)), counts=counts,
        )

    output_path.write_text(text, encoding="utf-8")
    return IndexResult(
        name=name, strategy=strategy_name, status="written",
        output=str(output_path.relative_to(root)), counts=counts,
    )


def run_all(configs_dir: Path, root: Path, today: date | None = None) -> list[IndexResult]:
    return [run_one(c, root, today=today) for c in load_configs(configs_dir)]
