"""Flat-list index strategy.

Walks `target_dir`, lists every artifact as a bullet linking to the file (relative
to the index output), grouped by immediate subdir.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from ..core.scheme import index_domain
from ._shared import (
    cookbook_name,
    iter_artifacts,
    merge_index_frontmatter,
    render_frontmatter,
    title_of,
)


def generate(config: dict, root: Path, today: date) -> tuple[str, dict]:
    target = root / config["target_dir"]
    output = root / config["output"]
    files = iter_artifacts(target)

    by_subdir: dict[str, list[Path]] = {}
    flat_files: list[Path] = []
    for f in files:
        rel = f.relative_to(target)
        if len(rel.parts) == 1:
            flat_files.append(f)
        else:
            by_subdir.setdefault(rel.parts[0], []).append(f)

    fm_data = merge_index_frontmatter(
        output,
        title=config.get("title", f"{target.name.title()} Index"),
        domain=index_domain(root, output, f"{cookbook_name(root)}/{target.name}/index"),
        summary=config.get("summary", f"Index of {target.name}."),
        today=today,
    )

    lines = [render_frontmatter(fm_data).rstrip("\n"), ""]
    lines.append(f"# {fm_data['title']}")
    lines.append("")
    if config.get("description"):
        lines.append(config["description"])
        lines.append("")
    lines.append(f"Total: {len(files)} artifacts.")
    lines.append("")

    output_parent = output.parent
    for f in flat_files:
        rel = _relpath(f, output_parent)
        lines.append(f"- [{title_of(f)}]({rel})")
    if flat_files and by_subdir:
        lines.append("")

    for sub in sorted(by_subdir):
        lines.append(f"## {sub.replace('-', ' ').replace('_', ' ').title()}")
        lines.append("")
        for f in sorted(by_subdir[sub]):
            rel = _relpath(f, output_parent)
            lines.append(f"- [{title_of(f)}]({rel})")
        lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    counts = {"total": len(files), "subdirs": len(by_subdir), "flat": len(flat_files)}
    return text, counts


def _relpath(target: Path, base: Path) -> str:
    import os
    return os.path.relpath(target, base)
