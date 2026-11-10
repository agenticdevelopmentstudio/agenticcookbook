"""`cookr check` — the recipe work a change set still owes (spec section 7).

`--staged` checks the staged set, `--branch` (the default) the branch diff from
its merge base plus the working tree. With no base branch it checks the
uncommitted changes and skips the version-bump rule. `--hook` is what the Claude
Code hook runs: findings print as one message and exit 2; a clean check is
silent, exit 0. Without `--hook` it prints a table and exits 1 on findings.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from rich.markup import escape

from ..core import changes as git_changes
from ..core.hookcheck import Finding, analyze, base_index_at, ordered, staged_divergence
from ..core.index import current_index
from ..core.links import resolver_for
from ..core.versions import GitError, base_ref
from .inventory import require_config

NAME = "check"
HELP = "List the recipe work a change set still owes (the check behind the cookr hook)."

CAP = 15
HEADER = "cookr: recipe work to do before this lands:"
PROCEDURE = ("Do this work now and continue; do not stop to ask. "
             "(cookr scope shows the full picture.)")


def register(parser: argparse.ArgumentParser) -> None:
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--staged", action="store_true", help="Check the staged set.")
    mode.add_argument("--branch", action="store_true",
                      help="Check the branch diff plus the working tree (the default).")
    parser.add_argument("--hook", action="store_true",
                        help="Hook output: one message, exit 2 on findings, silent when clean.")
    parser.add_argument("--json", action="store_true", help="Emit the findings as JSON.")


def hook_message(findings: list[Finding]) -> str:
    lines = [HEADER, *(f"  - {f.message}" for f in findings[:CAP])]
    if len(findings) > CAP:
        lines.append(f"  … and {len(findings) - CAP} more")
    lines.append(PROCEDURE)
    return "\n".join(lines) + "\n"


def _say(text: str) -> None:
    """Hook output: plain text on stderr, which Claude Code shows on a blocking exit."""
    sys.stderr.write(text)


def _fail(args, ctx, message: str) -> int:
    if args.hook:
        _say(f"cookr: {message}\n")
        return 2
    ctx.ui.error(escape(message))
    return 1


def run(args, ctx) -> int:
    if args.hook and ctx.config is None and not ctx.config_error:
        return 0                                  # not a cookr repo: nothing to check
    if not require_config(ctx):
        return 2
    cfg = ctx.config
    index = current_index(cfg.cookbook_dir)
    try:
        base = base_ref(cfg.repo_root)
        if args.staged:
            found = git_changes.staged(cfg.repo_root)
        elif base:
            found = git_changes.branch(cfg.repo_root, base)
        else:
            found = git_changes.uncommitted(cfg.repo_root)
        if not base and not args.hook:
            ctx.ui.warn("no base branch found (origin/main, main); version bumps were not "
                        "checked")
        # The index as the change set started from it: HEAD for a staged check.
        base_index = base_index_at(cfg, "HEAD" if args.staged else (base or "HEAD"))
        result = analyze(cfg, index, resolver_for(cfg, index), found, base, base_index)
        if args.staged:
            result.findings = ordered(result.findings + staged_divergence(
                cfg, index, base_index, found))
    except GitError as e:
        return _fail(args, ctx, f"git failed, so the change set is unknown: {e}")

    findings = result.findings
    if args.json:
        sys.stdout.write(json.dumps([asdict(f) for f in findings], indent=2) + "\n")
        return 2 if args.hook and findings else (1 if findings else 0)
    if args.hook:
        if findings:
            _say(hook_message(findings))
            return 2
        return 0
    for line in result.unreachable:
        ctx.ui.warn(escape(line))
    if not findings:
        ctx.ui.ok("Nothing to do: every change is covered.")
        return 0
    ctx.ui.table(["kind", "subject", "to do"],
                 [[f.kind, escape(f.subject), escape(f.message)] for f in findings])
    return 1
