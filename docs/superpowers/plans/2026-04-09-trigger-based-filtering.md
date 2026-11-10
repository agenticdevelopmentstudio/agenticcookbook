> [!WARNING]
> **ARCHIVED — HISTORICAL RECORD, NOT CURRENT.** Captured 2026-11-10. This document reflects a
> past state or decision and may no longer describe how things work. Do not treat it as live
> documentation.

# Trigger-Based Guideline Filtering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the cookbook's 141 guidelines discoverable by AI agents through activity-based trigger tags, plus address three smaller feedback items (linting timing, top-10 shortlist, AI/ML guidelines).

**Architecture:** Add a `triggers` field to guideline frontmatter. Build a Python script that generates `index/triggers.yaml` — a flat lookup from trigger name to guideline paths. Create two new AI/ML guidelines, a top-10 shortlist document, and clarify the linting guideline's timing language.

**Tech Stack:** Markdown (YAML frontmatter), Python (index generator), YAML (trigger index)

**Source:** `docs/feedback/cookbook-review-2026-04-08.md`

---

## File Structure

### New files

| File | Responsibility |
|------|---------------|
| `index/triggers.yaml` | Flat trigger → guideline-paths lookup (generated, not hand-edited) |
| `scripts/generate-trigger-index.py` | Reads all guideline frontmatter, builds `index/triggers.yaml` |
| `introduction/trigger-guide.md` | Documents the trigger system: canonical triggers, usage for agents, escalating checkpoint pattern |
| `guidelines/observability/ai-provider-observability.md` | New guideline: structured logging for AI API calls |
| `guidelines/networking/ai-cost-management.md` | New guideline: cost control for AI-powered systems |
| `introduction/top-10-guidelines.md` | Curated shortlist of highest-signal guidelines |

### Modified files

| File | Change |
|------|--------|
| `guidelines/code-quality/linting.md` | Change "from day one" / "from initial generation" timing to "before the first PR" |
| `introduction/conventions.md` | Add `triggers` field to frontmatter spec |
| `compliance/artifact-formatting/guideline-formatting.md` | Add compliance check for `triggers` field |
| All 141 `guidelines/**/*.md` files | Add `triggers:` field to frontmatter |
| `index.md` | Add entries for new files |
| `README.md` | Update guideline count, mention trigger system |
| `.claude/CLAUDE.md` | Update guideline count in Cookbook Artifacts table |

---

## Canonical Trigger Taxonomy

These are the trigger values used across all guidelines. Each trigger represents an activity or context where an agent should consult guidelines.

| Trigger | When it fires |
|---------|--------------|
| `writing-tests` | Writing or modifying tests |
| `error-handling` | Adding try/except, catch, error paths |
| `new-module` | Creating a new file, module, or package |
| `api-integration` | Calling external APIs (REST, GraphQL, gRPC) |
| `ai-api-integration` | Calling AI/ML provider APIs specifically |
| `data-modeling` | Defining types, schemas, database tables |
| `database-operations` | Writing queries, migrations, transactions |
| `ui-implementation` | Building UI components or layouts |
| `authentication` | Implementing auth flows, tokens, sessions |
| `input-handling` | Processing user input, form data, file uploads |
| `networking` | HTTP clients, WebSockets, retry logic, caching |
| `concurrency` | Threads, async/await, locks, queues |
| `logging` | Adding log statements, analytics events |
| `security-review` | Reviewing code for security concerns |
| `performance-optimization` | Optimizing hot paths, queries, rendering |
| `accessibility` | Screen readers, keyboard nav, contrast, Dynamic Type |
| `internationalization` | Localization, RTL, locale formatting |
| `feature-flags` | Adding or managing feature flags |
| `platform-integration` | Deep links, notifications, widgets, sharing |
| `code-review` | Reviewing code quality, structure, patterns |
| `pre-commit` | Final check before committing code |
| `pre-pr` | Final check before opening a pull request |
| `dependency-management` | Adding, updating, or auditing dependencies |
| `configuration` | App settings, environment config, build config |
| `offline-support` | Offline-first patterns, sync, conflict resolution |
| `skill-authoring` | Writing Claude Code skills, rules, or agents |
| `recipe-authoring` | Writing or modifying cookbook recipes |
| `schema-design` | Designing database schemas, migrations |

---

## Task 1: Define Trigger Convention in Conventions Doc

**Files:**
- Modify: `introduction/conventions.md` (frontmatter field definitions, around lines 43-92)

- [ ] **Step 1: Add `triggers` field to the frontmatter field definitions table**

In `introduction/conventions.md`, add a new row to the Field Definitions table after the `approved-date` row:

```markdown
| `triggers` | Guideline only | Activity or context tags that make this guideline relevant to an AI agent. Empty list `[]` if not yet classified. Values from the canonical trigger taxonomy in `introduction/trigger-guide.md`. |
```

- [ ] **Step 2: Add `triggers` to the frontmatter YAML example block**

In the YAML example block at the top of the File Format section, add after `approved-date`:

```yaml
triggers: []
```

- [ ] **Step 3: Bump version to 1.5.0, update modified date to 2026-04-09**

- [ ] **Step 4: Add Change History entry**

```markdown
| 1.5.0 | 2026-04-09 | Mike Fullerton | Add triggers field for guideline-type artifacts |
```

- [ ] **Step 5: Commit and push**

```bash
git add introduction/conventions.md
git commit -m "feat: add triggers field to guideline frontmatter convention"
git push
```

---

## Task 2: Write the Trigger Guide Document

**Files:**
- Create: `introduction/trigger-guide.md`

- [ ] **Step 1: Create the trigger guide**

Create `introduction/trigger-guide.md` with full frontmatter (UUID, domain `agenticdevelopercookbook://introduction/trigger-guide`, type `reference`, version `1.0.0`, status `draft`). Content sections:

**## Purpose** — Explain why triggers exist: 141 guidelines are too many to load into agent context. Triggers let agents query by activity to get ~10-20 relevant guidelines instead of all 141.

**## Canonical Triggers** — Table with all 28 triggers from the taxonomy above. Columns: Trigger, When It Fires, Example Guidelines. List 2-3 example guideline paths per trigger.

**## Usage Pattern for AI Agents** — The 4-step escalating checkpoint pattern from the feedback doc:
1. Principles — always loaded (small, universal)
2. Trigger-filtered guidelines — loaded on demand by current activity
3. Pre-commit checklist — mandatory ~10 rules before every commit
4. Pre-PR audit — broader set before opening a PR

**## Querying Triggers** — Show how to use `index/triggers.yaml`:
```yaml
# index/triggers.yaml structure
writing-tests:
  - guidelines/testing/test-pyramid.md
  - guidelines/testing/properties-of-good-tests.md
  - guidelines/testing/unit-test-patterns.md
  ...
```

**## Adding Triggers to a Guideline** — Show the frontmatter field, explain 1-5 triggers per guideline, link to conventions.md.

**## Change History** — Standard table.

- [ ] **Step 2: Commit and push**

```bash
git add introduction/trigger-guide.md
git commit -m "docs: add trigger guide documenting the trigger-based filtering system"
git push
```

---

## Task 3: Build the Trigger Index Generator Script

**Files:**
- Create: `scripts/generate-trigger-index.py`

- [ ] **Step 1: Write the generator script**

Create `scripts/generate-trigger-index.py`. The script:

1. Walks all `guidelines/**/*.md` files (skip INDEX.md, index.md, references.md)
2. Parses YAML frontmatter from each file (use `yaml.safe_load` on the text between `---` delimiters)
3. Extracts the `triggers` list (skip files with no triggers or empty list)
4. Builds a dict: `{trigger_name: [sorted list of file paths relative to repo root]}`
5. Sorts triggers alphabetically
6. Writes `index/triggers.yaml` with a header comment:
```yaml
# Auto-generated by scripts/generate-trigger-index.py
# Do not edit manually — regenerate with: python scripts/generate-trigger-index.py
# Generated: YYYY-MM-DD HH:MM:SS
```
7. Prints a summary: total guidelines processed, guidelines with triggers, unique triggers found, output path

Edge cases:
- If `index/` directory doesn't exist, create it
- If a guideline has a trigger not in the canonical list, print a warning but still include it
- Handle missing `triggers` field gracefully (treat as empty)

```python
#!/usr/bin/env python3
"""Generate index/triggers.yaml from guideline frontmatter triggers fields."""

import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml


def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    return yaml.safe_load(text[3:end]) or {}


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    guidelines_dir = repo_root / "guidelines"
    output_path = repo_root / "index" / "triggers.yaml"

    skip_names = {"INDEX.md", "index.md", "references.md"}
    trigger_map: dict[str, list[str]] = defaultdict(list)
    total = 0
    with_triggers = 0

    for md_file in sorted(guidelines_dir.rglob("*.md")):
        if md_file.name in skip_names:
            continue
        total += 1
        fm = parse_frontmatter(md_file)
        triggers = fm.get("triggers", [])
        if not triggers:
            continue
        with_triggers += 1
        rel_path = str(md_file.relative_to(repo_root))
        for trigger in triggers:
            trigger_map[trigger].append(rel_path)

    # Sort triggers and their guideline lists
    sorted_map = {k: sorted(v) for k, v in sorted(trigger_map.items())}

    output_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    header = (
        f"# Auto-generated by scripts/generate-trigger-index.py\n"
        f"# Do not edit manually — regenerate with: python scripts/generate-trigger-index.py\n"
        f"# Generated: {now}\n\n"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.dump(sorted_map, f, default_flow_style=False, sort_keys=False)

    unique_triggers = len(sorted_map)
    print(f"Processed {total} guidelines")
    print(f"  With triggers: {with_triggers}")
    print(f"  Unique triggers: {unique_triggers}")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script to verify it works (will produce an empty index since no guidelines have triggers yet)**

```bash
python scripts/generate-trigger-index.py
cat index/triggers.yaml
```

- [ ] **Step 3: Add `index/triggers.yaml` to `.gitignore` (it's generated)**

Append to `.gitignore`:
```
# Generated trigger index
index/triggers.yaml
```

- [ ] **Step 4: Commit and push**

```bash
git add scripts/generate-trigger-index.py .gitignore
git commit -m "feat: add trigger index generator script"
git push
```

---

## Task 4: Add Triggers to All 141 Guidelines

This is the largest task. It modifies every guideline file to add a `triggers:` field to the frontmatter.

**Files:**
- Create: `scripts/add-triggers-to-guidelines.py` (one-time migration script)
- Modify: All 141 `guidelines/**/*.md` files

The trigger assignment follows this mapping. Each guideline category has a primary trigger plus specific overrides per file.

- [ ] **Step 1: Write the migration script**

Create `scripts/add-triggers-to-guidelines.py` — a Python script that:

1. Reads each guideline's frontmatter
2. Assigns triggers based on a mapping dict defined in the script
3. The mapping dict maps guideline domain → list of triggers
4. Inserts the `triggers:` field after `approved-date:` in the frontmatter
5. Bumps the patch version (e.g., 1.0.0 → 1.0.1)
6. Updates the `modified` date to 2026-04-09
7. Adds a Change History row: `| X.Y.Z | 2026-04-09 | Mike Fullerton | Add trigger tags |`
8. Writes the file back

The mapping dict should be comprehensive. Here is the category-level default mapping:

```python
CATEGORY_DEFAULTS = {
    "testing": ["writing-tests"],
    "security": ["security-review"],
    "ui": ["ui-implementation"],
    "networking": ["networking", "api-integration"],
    "accessibility": ["accessibility", "ui-implementation"],
    "internationalization": ["internationalization"],
    "concurrency": ["concurrency"],
    "logging": ["logging"],
    "feature-management": ["feature-flags"],
    "code-quality": ["code-review", "pre-commit"],
    "database-design": ["database-operations", "schema-design"],
    "skills-and-agents": ["skill-authoring"],
    "codebase-decomposition": ["code-review", "new-module"],
    "recipe-quality": ["recipe-authoring"],
    "platform": ["platform-integration"],
    "platform/windows": ["platform-integration", "ui-implementation"],
    "language/python": ["new-module"],
    "language/swift": ["ui-implementation"],
    "language/kotlin": ["ui-implementation"],
    "language/csharp": ["new-module"],
}
```

Plus file-level overrides for guidelines that need more specific triggers:

```python
FILE_OVERRIDES = {
    # Testing
    "guidelines/testing/test-pyramid.md": ["writing-tests", "pre-pr"],
    "guidelines/testing/test-doubles.md": ["writing-tests"],
    "guidelines/testing/unit-test-patterns.md": ["writing-tests"],
    "guidelines/testing/flaky-test-prevention.md": ["writing-tests", "pre-pr"],
    "guidelines/testing/mutation-testing.md": ["writing-tests", "pre-pr"],
    "guidelines/testing/security-testing.md": ["writing-tests", "security-review"],
    "guidelines/testing/test-data.md": ["writing-tests", "data-modeling"],
    "guidelines/testing/properties-of-good-tests.md": ["writing-tests", "code-review"],
    "guidelines/testing/property-based-testing.md": ["writing-tests"],
    "guidelines/testing/post-generation-verification.md": ["pre-commit", "code-review"],
    "guidelines/testing/the-testing-workflow.md": ["writing-tests", "pre-pr"],
    "guidelines/testing/testing.md": ["writing-tests", "pre-pr"],

    # Security
    "guidelines/security/input-validation.md": ["input-handling", "security-review", "api-integration"],
    "guidelines/security/authentication.md": ["authentication", "security-review"],
    "guidelines/security/authorization.md": ["authentication", "security-review"],
    "guidelines/security/token-handling.md": ["authentication", "security-review"],
    "guidelines/security/secure-storage.md": ["security-review", "data-modeling"],
    "guidelines/security/transport-security.md": ["networking", "security-review"],
    "guidelines/security/cors.md": ["networking", "security-review", "api-integration"],
    "guidelines/security/content-security-policy.md": ["security-review", "ui-implementation"],
    "guidelines/security/dependency-security.md": ["dependency-management", "security-review"],
    "guidelines/security/privacy.md": ["security-review", "data-modeling"],
    "guidelines/security/sensitive-data.md": ["security-review", "logging"],
    "guidelines/security/security-headers-checklist.md": ["security-review", "pre-pr"],

    # Networking
    "guidelines/networking/api-design.md": ["api-integration", "new-module"],
    "guidelines/networking/caching.md": ["networking", "performance-optimization"],
    "guidelines/networking/error-responses.md": ["api-integration", "error-handling"],
    "guidelines/networking/offline-and-connectivity.md": ["offline-support", "networking"],
    "guidelines/networking/pagination.md": ["api-integration", "data-modeling"],
    "guidelines/networking/rate-limiting.md": ["api-integration", "networking"],
    "guidelines/networking/retry-and-resilience.md": ["networking", "error-handling"],
    "guidelines/networking/timeouts.md": ["networking", "api-integration"],
    "guidelines/networking/real-time-communication.md": ["networking", "concurrency"],

    # Code quality
    "guidelines/code-quality/linting.md": ["pre-commit", "new-module"],
    "guidelines/code-quality/atomic-commits.md": ["pre-commit"],
    "guidelines/code-quality/scope-discipline.md": ["code-review", "new-module"],
    "guidelines/code-quality/bulk-operation-verification.md": ["code-review", "pre-commit"],

    # Logging
    "guidelines/observability/logging.md": ["logging", "new-module", "error-handling"],
    "guidelines/observability/analytics.md": ["logging", "ui-implementation"],

    # UI
    "guidelines/ui/layout.md": ["ui-implementation"],
    "guidelines/ui/color.md": ["ui-implementation"],
    "guidelines/ui/typography.md": ["ui-implementation"],
    "guidelines/ui/spacing.md": ["ui-implementation"],
    "guidelines/ui/animation-motion.md": ["ui-implementation", "accessibility"],
    "guidelines/ui/form-design.md": ["ui-implementation", "input-handling"],
    "guidelines/ui/feedback-patterns.md": ["ui-implementation", "error-handling"],
    "guidelines/ui/always-show-progress.md": ["ui-implementation", "networking"],
    "guidelines/ui/data-display.md": ["ui-implementation", "data-modeling"],
    "guidelines/ui/iconography.md": ["ui-implementation"],
    "guidelines/ui/previews.md": ["ui-implementation"],
    "guidelines/ui/platform-design-languages.md": ["ui-implementation", "platform-integration"],
    "guidelines/ui/visual-hierarchy.md": ["ui-implementation"],
    "guidelines/ui/touch-click-targets.md": ["ui-implementation", "accessibility"],

    # Feature management
    "guidelines/feature-management/feature-flags.md": ["feature-flags", "new-module"],
    "guidelines/feature-management/ab-testing.md": ["feature-flags", "logging"],
    "guidelines/feature-management/debug-mode.md": ["feature-flags", "logging"],

    # Concurrency
    "guidelines/concurrency/concurrency.md": ["concurrency", "performance-optimization"],
    "guidelines/concurrency/immutability.md": ["concurrency", "data-modeling"],

    # Internationalization
    "guidelines/internationalization/localization.md": ["internationalization", "ui-implementation"],
    "guidelines/internationalization/rtl-support.md": ["internationalization", "ui-implementation"],

    # Accessibility
    "guidelines/accessibility/accessibility.md": ["accessibility", "ui-implementation", "pre-pr"],

    # Database design — all get database-operations + schema-design by default,
    # plus specific overrides
    "guidelines/data/sqlite-best-practices.md": ["database-operations", "schema-design"],
    "guidelines/data/indexing.md": ["database-operations", "performance-optimization", "schema-design"],
    "guidelines/data/query-optimization.md": ["database-operations", "performance-optimization"],
    "guidelines/data/transactions-and-concurrency.md": ["database-operations", "concurrency"],
    "guidelines/data/backup-and-recovery.md": ["database-operations", "configuration"],
    "guidelines/data/schema-evolution.md": ["database-operations", "schema-design"],
    "guidelines/data/sync-engine-design.md": ["offline-support", "database-operations"],
    "guidelines/data/sync-protocol.md": ["offline-support", "networking", "database-operations"],
    "guidelines/data/sync-schema-design.md": ["offline-support", "schema-design"],
    "guidelines/data/sync-tooling.md": ["offline-support", "dependency-management"],
    "guidelines/data/offline-first-architecture.md": ["offline-support", "database-operations"],
    "guidelines/data/conflict-resolution.md": ["offline-support", "database-operations"],

    # Language-specific
    "guidelines/language/python/type-hints.md": ["new-module", "code-review"],
    "guidelines/language/python/database.md": ["database-operations"],
    "guidelines/language/python/web-services.md": ["api-integration", "new-module"],
    "guidelines/language/python/file-paths.md": ["new-module"],
    "guidelines/language/python/yaml-frontmatter.md": ["data-modeling", "configuration"],
    "guidelines/language/python/shell-scripts.md": ["new-module", "configuration"],
    "guidelines/language/python/deterministic-ids.md": ["data-modeling"],
    "guidelines/language/python/no-external-dependencies-in-core-librari.md": ["dependency-management", "new-module"],

    # Platform integration
    "guidelines/platform/deep-linking.md": ["platform-integration", "configuration"],
    "guidelines/platform/notifications.md": ["platform-integration", "ui-implementation"],
    "guidelines/platform/background-tasks.md": ["platform-integration", "concurrency"],
    "guidelines/platform/search-integration.md": ["platform-integration"],
    "guidelines/platform/widgets-and-glanceable-surfaces.md": ["platform-integration", "ui-implementation"],
    "guidelines/platform/share-and-inter-app-data.md": ["platform-integration"],
    "guidelines/platform/handoff-and-continuity.md": ["platform-integration", "offline-support"],
    "guidelines/platform/shortcuts-and-automation.md": ["platform-integration", "configuration"],

    # Skills and agents
    "guidelines/skills-and-agents/authoring-skills-and-rules.md": ["skill-authoring"],
    "guidelines/skills-and-agents/performance.md": ["skill-authoring", "performance-optimization"],
    "guidelines/skills-and-agents/agent-checklist.md": ["skill-authoring", "pre-pr"],
    "guidelines/skills-and-agents/skill-checklist.md": ["skill-authoring", "pre-pr"],
    "guidelines/skills-and-agents/rule-checklist.md": ["skill-authoring", "pre-pr"],
}
```

The script logic:
1. For each guideline file, check FILE_OVERRIDES first. If found, use those triggers.
2. Otherwise, derive triggers from CATEGORY_DEFAULTS based on the file's parent directory.
3. Insert `triggers:` field into frontmatter after `approved-date:` line.
4. Bump patch version.
5. Update `modified` date.
6. Append Change History row.

```python
#!/usr/bin/env python3
"""One-time migration: add triggers field to all guideline frontmatter."""

import re
import sys
from pathlib import Path

import yaml

# ... CATEGORY_DEFAULTS and FILE_OVERRIDES dicts as above ...

def add_triggers_to_file(path: Path, triggers: list[str], repo_root: Path) -> bool:
    """Add triggers field to a guideline file. Returns True if modified."""
    text = path.read_text(encoding="utf-8")
    if "triggers:" in text.split("---")[1] if text.startswith("---") else "":
        return False  # Already has triggers

    # Parse frontmatter boundaries
    first_end = text.index("---", 3)
    frontmatter_text = text[3:first_end]
    body = text[first_end + 3:]

    # Insert triggers after approved-date line
    triggers_yaml = "triggers:\n" + "".join(f"  - {t}\n" for t in triggers)
    if "approved-date:" in frontmatter_text:
        frontmatter_text = frontmatter_text.replace(
            "approved-date:",
            "approved-date:",
            1,
        )
        # Insert after the approved-date line
        lines = frontmatter_text.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith("approved-date:"):
                new_lines.append(triggers_yaml.rstrip())
        frontmatter_text = "\n".join(new_lines)
    else:
        frontmatter_text = frontmatter_text.rstrip() + "\n" + triggers_yaml

    # Bump patch version
    fm = yaml.safe_load(frontmatter_text)
    old_version = fm.get("version", "1.0.0")
    parts = old_version.split(".")
    parts[2] = str(int(parts[2]) + 1)
    new_version = ".".join(parts)
    frontmatter_text = frontmatter_text.replace(
        f"version: {old_version}", f"version: {new_version}"
    )

    # Update modified date
    frontmatter_text = re.sub(
        r"modified: \d{4}-\d{2}-\d{2}",
        "modified: 2026-04-09",
        frontmatter_text,
    )

    # Add change history row
    history_row = f"| {new_version} | 2026-04-09 | Mike Fullerton | Add trigger tags |"
    if "## Change History" in body:
        # Insert after the table header row (the |---|---|---|---| line)
        body = re.sub(
            r"(\|[-\s|]+\|)\n",
            r"\1\n" + history_row + "\n",
            body,
            count=1,
        )

    result = f"---\n{frontmatter_text}\n---{body}"
    path.write_text(result, encoding="utf-8")
    return True


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    guidelines_dir = repo_root / "guidelines"
    skip_names = {"INDEX.md", "index.md", "references.md"}

    modified = 0
    skipped = 0
    for md_file in sorted(guidelines_dir.rglob("*.md")):
        if md_file.name in skip_names:
            continue

        rel_path = str(md_file.relative_to(repo_root))

        # Determine triggers
        if rel_path in FILE_OVERRIDES:
            triggers = FILE_OVERRIDES[rel_path]
        else:
            # Walk parent dirs to find category default
            rel_dir = str(md_file.parent.relative_to(guidelines_dir))
            triggers = None
            while rel_dir:
                if rel_dir in CATEGORY_DEFAULTS:
                    triggers = CATEGORY_DEFAULTS[rel_dir]
                    break
                rel_dir = str(Path(rel_dir).parent) if "/" in rel_dir else ""
            if not triggers:
                print(f"  WARNING: No trigger mapping for {rel_path}")
                triggers = []

        if not triggers:
            skipped += 1
            continue

        if add_triggers_to_file(md_file, triggers, repo_root):
            modified += 1
            print(f"  ✓ {rel_path}: {triggers}")
        else:
            print(f"  - {rel_path}: already has triggers")

    print(f"\nModified: {modified}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the migration script**

```bash
python scripts/add-triggers-to-guidelines.py
```

Review the output. Spot-check 5 files across different categories to verify:
- `triggers:` field is present and correctly placed
- Version was bumped
- `modified` date updated
- Change History row added

- [ ] **Step 3: Run the trigger index generator**

```bash
python scripts/generate-trigger-index.py
```

Verify `index/triggers.yaml` contains all 28 triggers with reasonable guideline counts.

- [ ] **Step 4: Spot-check the generated index**

```bash
python -c "
import yaml
with open('index/triggers.yaml') as f:
    data = yaml.safe_load(f)
for trigger, paths in sorted(data.items()):
    print(f'{trigger}: {len(paths)} guidelines')
"
```

Each trigger should have at least 2 guidelines. No trigger should have more than 40 (that would mean the trigger is too broad).

- [ ] **Step 5: Commit and push**

```bash
git add guidelines/ scripts/add-triggers-to-guidelines.py
git commit -m "feat: add trigger tags to all 141 guidelines"
git push
```

---

## Task 5: Fix Linting Timing Language

**Files:**
- Modify: `guidelines/code-quality/linting.md`

- [ ] **Step 1: Update the linting guideline**

In `guidelines/code-quality/linting.md`, change the title and summary from "Linting from day one" / "from initial generation" to "Linting before the first PR". The guidance should clarify:

- Linting config SHOULD be set up early in the project
- Linting MUST pass before the first PR is opened
- During rapid prototyping, committing without lint-gating every commit is acceptable
- Before any PR, lint MUST be clean

Update:
- Title: `"Linting before the first PR"`
- `title:` frontmatter field
- `domain:` stays the same (path doesn't change)
- Summary: `"All projects MUST have linting configured and passing before the first pull request."`
- H1 heading: `# Linting before the first PR`
- Opening paragraph: rewrite to match the softer timing
- Bump minor version (content change): e.g., 1.0.0 → 1.1.0
- Update modified date
- Add Change History row

- [ ] **Step 2: Commit and push**

```bash
git add guidelines/code-quality/linting.md
git commit -m "docs: soften linting timing to 'before the first PR'"
git push
```

---

## Task 6: Create AI Provider Observability Guideline

**Files:**
- Create: `guidelines/observability/ai-provider-observability.md`

- [ ] **Step 1: Create the guideline**

Create `guidelines/observability/ai-provider-observability.md` with full frontmatter:
- New UUID
- domain: `agenticdevelopercookbook://guidelines/observability/ai-provider-observability`
- type: guideline
- version: 1.0.0
- status: draft
- tags: `[logging, ai, observability, llm]`
- triggers: `[ai-api-integration, logging, api-integration]`
- depends-on: `[agenticdevelopercookbook://guidelines/observability/logging]`
- references: OpenTelemetry docs, Anthropic API docs

Content requirements (the actual requirements the guideline must define):

**Summary:** Every call to an AI provider API MUST be logged with structured metadata for cost attribution, debugging, and performance monitoring.

**Requirements:**
- **structured-request-log**: Every AI API call MUST log: provider name, model ID, prompt token count, completion token count, total cost (computed from token counts × per-token price), latency (ms), HTTP status, request ID
- **prompt-tracking**: Prompt templates MUST be versioned. Logs SHOULD reference the prompt template ID and version, not the full prompt text (which may contain PII)
- **cost-attribution**: Logs MUST include a cost-attribution tag (feature name, user action, or batch job ID) so costs can be traced to their source
- **rate-limit-tracking**: Rate limit headers (remaining, reset) SHOULD be logged to enable proactive throttling
- **error-classification**: AI provider errors MUST be classified: rate-limit, context-length-exceeded, content-filter, server-error, timeout. Each category has different retry/fallback behavior.
- **no-pii-in-prompts-log**: Full prompt text MUST NOT be logged in production. Use prompt template IDs. In development/staging, full prompts MAY be logged if the environment is access-controlled.

**Change History** — Standard table.

- [ ] **Step 2: Commit and push**

```bash
git add guidelines/observability/ai-provider-observability.md
git commit -m "feat: add AI provider observability guideline"
git push
```

---

## Task 7: Create AI Cost Management Guideline

**Files:**
- Create: `guidelines/networking/ai-cost-management.md`

- [ ] **Step 1: Create the guideline**

Create `guidelines/networking/ai-cost-management.md` with full frontmatter:
- New UUID
- domain: `agenticdevelopercookbook://guidelines/networking/ai-cost-management`
- type: guideline
- version: 1.0.0
- status: draft
- tags: `[cost-management, ai, caching, rate-limiting]`
- triggers: `[ai-api-integration, networking, performance-optimization]`
- depends-on: `[agenticdevelopercookbook://guidelines/networking/caching, agenticdevelopercookbook://guidelines/networking/rate-limiting]`

Content requirements:

**Summary:** AI API calls cost $0.01–$0.10+ each. Systems MUST treat AI calls as a managed resource with budgets, caching, and fallback strategies.

**Requirements:**
- **response-caching**: Identical or semantically equivalent requests MUST be cached. Cache key includes: model, prompt template ID, template variables, temperature (if 0). Cache TTL depends on the use case.
- **cost-budgets**: Every AI-powered feature MUST define a per-user and per-request cost budget. The system MUST reject or degrade gracefully when the budget is exhausted.
- **tiered-model-selection**: Systems SHOULD route requests to the cheapest model that meets quality requirements. Example: use Haiku for classification, Sonnet for generation, Opus for complex reasoning.
- **batch-over-realtime**: Non-latency-sensitive work SHOULD use batch APIs (typically 50% cheaper) rather than real-time endpoints.
- **cost-per-request-tracking**: Every API response MUST record actual cost (input tokens × price + output tokens × price). Aggregate cost SHOULD be available per feature, per user, and per time period.
- **provider-fallback**: Systems SHOULD define fallback providers for availability and cost. If the primary provider's costs spike or availability drops, traffic can shift.
- **prompt-optimization**: Prompt length directly affects cost. Prompts SHOULD be reviewed for token efficiency. System prompts SHOULD be cached where the API supports it (e.g., Anthropic prompt caching).

**Change History** — Standard table.

- [ ] **Step 2: Commit and push**

```bash
git add guidelines/networking/ai-cost-management.md
git commit -m "feat: add AI cost management guideline"
git push
```

---

## Task 8: Create Top-10 Guidelines Shortlist

**Files:**
- Create: `introduction/top-10-guidelines.md`

- [ ] **Step 1: Create the shortlist document**

Create `introduction/top-10-guidelines.md` with full frontmatter:
- New UUID
- domain: `agenticdevelopercookbook://introduction/top-10-guidelines`
- type: reference
- version: 1.0.0
- status: draft
- summary: "The 10 highest-signal guidelines that catch 80% of issues in AI-assisted codebases."

Content: A curated list of the 10 guidelines that the feedback doc identified as having the highest signal-to-noise ratio. Selection criteria: guidelines that (a) apply universally regardless of platform, (b) catch real issues during code generation, and (c) are actionable without deep domain knowledge.

The top 10 (based on the feedback session's findings and cross-category impact):

| # | Guideline | Why it's here |
|---|-----------|--------------|
| 1 | [Test Pyramid](agenticdevelopercookbook://guidelines/testing/test-pyramid) | Prevents test-suite bloat and gives the right ratio |
| 2 | [Input Validation](agenticdevelopercookbook://guidelines/security/input-validation) | #1 security issue in generated code |
| 3 | [Properties of Good Tests](agenticdevelopercookbook://guidelines/testing/properties-of-good-tests) | AI-generated tests are often brittle — this fixes that |
| 4 | [Linting before the first PR](agenticdevelopercookbook://guidelines/code-quality/linting) | Catches style/format drift before it compounds |
| 5 | [Logging](agenticdevelopercookbook://guidelines/observability/logging) | AI agents skip logging unless told — this ensures observability |
| 6 | [Error Responses](agenticdevelopercookbook://guidelines/networking/error-responses) | Generated code often has incomplete error handling |
| 7 | [Accessibility](agenticdevelopercookbook://guidelines/accessibility/accessibility) | Never added by AI unless explicitly required |
| 8 | [Atomic Commits](agenticdevelopercookbook://guidelines/code-quality/atomic-commits) | Keeps AI-generated PRs reviewable |
| 9 | [Sensitive Data](agenticdevelopercookbook://guidelines/security/sensitive-data) | Prevents PII/secrets in logs and responses |
| 10 | [Scope Discipline](agenticdevelopercookbook://guidelines/code-quality/scope-discipline) | Prevents AI from over-engineering or scope-creeping |

Each entry should have 2-3 sentences explaining why this guideline is in the top 10 and what it catches.

**Change History** — Standard table.

- [ ] **Step 2: Commit and push**

```bash
git add introduction/top-10-guidelines.md
git commit -m "docs: add top-10 guidelines shortlist"
git push
```

---

## Task 9: Update Index, README, CLAUDE.md

**Files:**
- Modify: `index.md`
- Modify: `README.md`
- Modify: `.claude/CLAUDE.md`
- Modify: `compliance/artifact-formatting/guideline-formatting.md`

- [ ] **Step 1: Update `index.md`**

Add entries to the Introduction section table:

```markdown
| [Trigger Guide](introduction/trigger-guide.md) | Activity-based trigger system for AI agents |
| [Top 10 Guidelines](introduction/top-10-guidelines.md) | Highest-signal guidelines shortlist |
```

Update the Guidelines section description to mention trigger-based filtering is available.

Bump version, update modified date, add Change History row.

- [ ] **Step 2: Update `README.md`**

Update the guideline count from "88 files" to the actual count (currently 141 + 2 new = 143). Add a brief mention of the trigger system in the Guidelines section:

```markdown
### Guidelines (143 files)

*What rules apply when building.* Organized by topic, with [trigger-based filtering](introduction/trigger-guide.md) for AI agents.
```

- [ ] **Step 3: Update `.claude/CLAUDE.md`**

Update the Cookbook Artifacts table:

```markdown
| Guideline | 143 | `guidelines/` | Topic-organized rules for planning and implementation |
```

- [ ] **Step 4: Add compliance check for triggers field**

In `compliance/artifact-formatting/guideline-formatting.md`, add a new check:

```markdown
### gf-triggers-field

The `triggers` field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the canonical taxonomy defined in `introduction/trigger-guide.md`. Empty list `[]` is acceptable for guidelines not yet classified.

**Applies when:** always.

**Guidelines:**
- [Trigger Guide](agenticdevelopercookbook://introduction/trigger-guide)
- [Conventions](agenticdevelopercookbook://introduction/conventions)
```

Bump version, update modified date, add Change History row.

- [ ] **Step 5: Commit and push**

```bash
git add index.md README.md .claude/CLAUDE.md compliance/artifact-formatting/guideline-formatting.md
git commit -m "docs: update index, README, CLAUDE.md for trigger system and new guidelines"
git push
```

---

## Task 10: Run Approval and Final Verification

- [ ] **Step 1: Run `/approve-artifact` on each new artifact**

Run on:
- `introduction/trigger-guide.md`
- `introduction/top-10-guidelines.md`
- `guidelines/observability/ai-provider-observability.md`
- `guidelines/networking/ai-cost-management.md`

Fix any issues and re-run until all pass.

- [ ] **Step 2: Regenerate the trigger index (now includes the 2 new guidelines)**

```bash
python scripts/generate-trigger-index.py
```

- [ ] **Step 3: Verify no broken cross-references**

```bash
grep -r "agenticdevelopercookbook://" --include="*.md" | grep -v "node_modules" | head -50
```

Spot-check that all `agenticdevelopercookbook://` URIs resolve to real files.

- [ ] **Step 4: Run `/update-website`**

Sync all changes to agenticcookbookweb.

- [ ] **Step 5: Mark PR ready and merge**

```bash
gh pr ready 45
gh pr merge 45 --squash
```

- [ ] **Step 6: Clean up worktree**

```bash
cd /Users/mfullerton/projects/active/cookbook
git worktree remove .claude/worktrees/feature+trigger-based-filtering
git pull
```
