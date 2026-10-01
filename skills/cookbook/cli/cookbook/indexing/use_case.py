"""Use-case strategy: ordered top-level subdirs with descriptions.

Replicates the legacy `regenerate-guidelines-index.py` shape generically — the
ordering, descriptions, and section structure come from config, not code.
Within each use-case subdir we either flatten files or group them by category
subdirectory.

Config shape (see references-src/index-configs/guidelines.yaml):

    strategy: use_case
    target_dir: guidelines
    output: guidelines/INDEX.md
    title: "Guidelines Index"
    summary: "..."
    description: "Long-form blurb shown after the heading."
    use_cases:
      - name: planning
        description: "Architecture, data modeling, choosing patterns"
      - name: implementing
        ...
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from ..core.scheme import index_domain
from ._shared import (
    SKIP_FILENAMES,
    cookbook_name,
    extract_change_history,
    iter_artifacts,
    merge_index_frontmatter,
    render_frontmatter,
    title_of,
)


def _collect(uc_dir: Path) -> tuple[dict[str, list[Path]], list[Path]]:
    categories: dict[str, list[Path]] = {}
    flat: list[Path] = []
    for item in sorted(uc_dir.iterdir()):
        if item.is_dir():
            files = [
                md for md in sorted(item.rglob("*.md"))
                if md.name not in SKIP_FILENAMES
            ]
            if files:
                categories[item.name] = files
        elif item.is_file() and item.suffix == ".md" and item.name not in SKIP_FILENAMES:
            flat.append(item)
    return categories, flat


def generate(config: dict, root: Path, today: date) -> tuple[str, dict]:
    target = root / config["target_dir"]
    output = root / config["output"]
    use_cases: list[dict] = config.get("use_cases", [])

    # Per-use-case counts + global counts
    per_uc_counts: dict[str, int] = {}
    total_with_dupes = 0
    for uc in use_cases:
        d = target / uc["name"]
        if not d.is_dir():
            per_uc_counts[uc["name"]] = 0
            continue
        n = sum(1 for f in d.rglob("*.md") if f.name not in SKIP_FILENAMES)
        per_uc_counts[uc["name"]] = n
        total_with_dupes += n

    # Unique (by filename across the entire target tree)
    unique_names = {
        f.name for f in iter_artifacts(target)
    }
    unique = len(unique_names)

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

    # Summary table
    lines.append(f"| Use Case | {target.name.title()} | When to use |")
    lines.append("|----------|-----------|-------------|")
    for uc in use_cases:
        name = uc["name"]
        c = per_uc_counts.get(name, 0)
        anchor = f"{name}-{c}-{target.name.lower()}"
        desc = uc.get("description", "")
        lines.append(f"| [{name.title()}](#{anchor}) | {c} | {desc} |")
    lines.append("")
    lines.append(
        f"{unique} unique {target.name}, {total_with_dupes} total "
        "(with duplicates across use cases)."
    )
    lines.append("")

    # Per-use-case sections
    output_parent = output.parent
    for uc in use_cases:
        name = uc["name"]
        uc_dir = target / name
        if not uc_dir.is_dir():
            continue
        c = per_uc_counts[name]
        lines.append("---")
        lines.append("")
        lines.append(f"### {name.title()} ({c} {target.name})")
        lines.append("")

        categories, flat = _collect(uc_dir)

        for f in flat:
            rel = _relpath(f, output_parent)
            lines.append(f"- [{title_of(f)}]({rel})")

        for cat in sorted(categories):
            lines.append("")
            lines.append(f"**{cat}**")
            for f in categories[cat]:
                rel = _relpath(f, output_parent)
                lines.append(f"- [{title_of(f)}]({rel})")
        lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    history = extract_change_history(output)
    if history:
        text += "\n---\n\n" + history
    counts = {
        "per_use_case": per_uc_counts,
        "unique": unique,
        "total_with_duplicates": total_with_dupes,
    }
    return text, counts


def _relpath(target: Path, base: Path) -> str:
    import os
    return os.path.relpath(target, base)
