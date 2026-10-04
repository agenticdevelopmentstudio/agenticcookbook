"""The host manifest (`cookr/data/hosts.json`) and tuning targets.

A **target** names who a rendered output is for, as a dotted chain from least
to most specific:

    claude  →  claude.opus  →  claude.opus-5-5
    codex   →  codex.gpt-5  →  codex.gpt-5-codex

The host is a key of the manifest. The version is the model ID without the
host's `model_prefix`, a trailing release date (`-20251001`) or a bracketed
variant (`[1m]`), with dots made dashes so a target stays one dotted chain.
The family is the one whose `match` is the longest prefix of the version; a
model no family matches has a two-step chain.

A model the manifest does not list still resolves, so a new model gets its
family's and host's tuning before anyone adds it. `models` lists what cookr
renders ahead of time; `default_model` is what an install renders for when no
model is named.

Adding a host is a manifest entry, not code.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional

MANIFEST = Path(__file__).resolve().parent.parent / "data" / "hosts.json"

_DATE_SUFFIX = re.compile(r"-\d{8}$")
_VARIANT_SUFFIX = re.compile(r"\[[^\]]*\]$")
_SEGMENT = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class HostError(ValueError):
    """An unknown host, a malformed manifest, or a model that is not a model ID."""


@dataclass(frozen=True)
class Host:
    name: str
    skills_dir: str
    instructions_file: str
    model_prefix: str
    default_model: str
    families: dict[str, str]          # family → version prefix it matches
    models: tuple[str, ...]
    rules: dict = field(default_factory=dict)

    def version(self, model: str) -> str:
        m = model.strip().lower()
        if self.model_prefix and m.startswith(self.model_prefix):
            m = m[len(self.model_prefix):]
        m = _VARIANT_SUFFIX.sub("", m)
        m = _DATE_SUFFIX.sub("", m)
        m = m.replace(".", "-")
        if not _SEGMENT.match(m):
            raise HostError(f"{model!r} is not a model ID cookr can name a target after")
        return m

    def family(self, version: str) -> Optional[str]:
        best = None
        for name, prefix in self.families.items():
            if version.startswith(prefix) and (best is None or len(prefix) > len(self.families[best])):
                best = name
        return best

    def chain(self, model: Optional[str] = None) -> tuple[str, ...]:
        """The targets for `model` on this host, least specific first. With no
        model, just the host."""
        if model is None:
            return (self.name,)
        version = self.version(model)
        family = self.family(version)
        steps = [self.name]
        if family is not None:
            steps.append(f"{self.name}.{family}")
        steps.append(f"{self.name}.{version}")
        return tuple(dict.fromkeys(steps))

    def targets(self) -> tuple[str, ...]:
        """Every target this host renders ahead of time: the host, each
        family, and each listed model, in that order."""
        out = [self.name, *(f"{self.name}.{f}" for f in self.families)]
        out += [self.chain(m)[-1] for m in self.models]
        return tuple(dict.fromkeys(out))


def _host(name: str, data: dict) -> Host:
    try:
        return Host(
            name=name,
            skills_dir=data["skills_dir"],
            instructions_file=data["instructions_file"],
            model_prefix=data.get("model_prefix", ""),
            default_model=data["default_model"],
            families={f: v["match"] for f, v in data.get("families", {}).items()},
            models=tuple(data.get("models", [])),
            rules=dict(data.get("rules", {})),
        )
    except (KeyError, TypeError) as e:
        raise HostError(f"host {name!r} in the manifest is missing {e}") from e


def load(path: Path = MANIFEST) -> dict[str, Host]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise HostError(f"{path}: {e}") from e
    if data.get("format") != 1:
        raise HostError(f"{path}: unsupported format {data.get('format')!r}")
    return {name: _host(name, h) for name, h in data.get("hosts", {}).items()}


@lru_cache(maxsize=None)
def manifest() -> dict[str, Host]:
    return load()


def host(name: str, hosts: Optional[dict[str, Host]] = None) -> Host:
    hosts = manifest() if hosts is None else hosts
    if name not in hosts:
        raise HostError(f"unknown host {name!r} (declared: {', '.join(sorted(hosts))})")
    return hosts[name]


def host_of(target: str) -> str:
    return target.split(".", 1)[0]


def chain(host_name: str, model: Optional[str] = None,
          hosts: Optional[dict[str, Host]] = None) -> tuple[str, ...]:
    return host(host_name, hosts).chain(model)


def parse_target(spec: str, hosts: Optional[dict[str, Host]] = None) -> tuple[str, ...]:
    """The chain a target names: `claude` (its default model), `claude.opus`
    (a family) or `claude.opus-5-5` / `claude.claude-opus-5-5` (a model)."""
    name, _, rest = spec.partition(".")
    h = host(name, hosts)
    if not rest:
        return h.chain(h.default_model)
    if rest in h.families:
        return (h.name, f"{h.name}.{rest}")
    return h.chain(rest)


def names(hosts: Optional[dict[str, Host]] = None) -> tuple[str, ...]:
    """Every word that names a declared host or model family, for the
    neutrality census."""
    hosts = manifest() if hosts is None else hosts
    return tuple(dict.fromkeys([*hosts, *(f for h in hosts.values() for f in h.families)]))
