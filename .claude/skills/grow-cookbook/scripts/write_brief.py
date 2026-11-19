#!/usr/bin/env python3
"""Fill the skill's prompts and keep a topic's write brief, round by round.

    python3 write_brief.py prompt <name> --repo R --cookr-py P [--today D] [--set k=v ...]
    python3 write_brief.py write  <topic-dir> --repo R --cookr-py P --artifact A [--kind K] [--today D] [--restart]
    python3 write_brief.py append <topic-dir>
    python3 write_brief.py review <topic-dir> --repo R --cookr-py P --artifact A [--today D]
    python3 write_brief.py lossless <topic-dir> --report <roles-lossless-output.json>

Every prompt the skill dispatches is a template in prompts/ with `{{name}}`
placeholders; this fills it. Each fill carries today's date, the privacy line
and the exact cookr line (`PYTHONPATH=<repo>/skills/cookr/cli <python> -P -m cookr
-p <repo>`); `{{criteria}}` is prompts/criteria.md, the review criteria, filled
in place. A placeholder left unfilled is an error (exit 2), never a blank.

`write` builds <topic-dir>/write-brief.md: the criteria verbatim, the strength
rule, the verdicts, the second check's corrections per claim (the `- correction:`
lines apply_second_check.py writes), the frontmatter rule and the owner list
(owner_list.py), with absolute paths. It runs in round 1 only: once the topic
dir holds a `review-<N>.md` or a `lossless-<N>.md`, `write` refuses (exit 4,
naming the file), since rebuilding the brief would drop the `## Round <N>
findings` and `## Lossless failure after round <N>` sections. With
`--restart` (after stage 5 sent a research finding back to stage 2) it first
moves the stopped run whole into a new `run-<k>/` subfolder (k the next free
number): every file and folder at the topic's top level but the inputs in
RESTART_KEEPS (base.txt, current.md, stage 2's research-brief.md,
team-run.md, agent-run.md and second-check.md, a research/ folder, earlier
run-<k>/ folders and dotfiles), so review-N.md, lossless-N.md, draft-N.md,
diff-N.md, disputes.md (its ids belong to the old run), draft.md, review.md,
integrate.md, owner-list.md, the filled prompts, lossless-run.json and any
log all go; write-brief.md stays, rebuilt, its `## From` sections kept.
integrate.md goes whole (its `## For the owner` findings carry the old run's
round ids, and its `integrated:` line the old run's end), but every
`## From <topic>'s review` section in it (a finding a sibling's review routed
there) is written back to a new top-level integrate.md, so it still reaches
the owner. Then
it writes as usual: the topic starts again at round 1 and keeps its earlier
runs. Everything
`write` reads (research.json, the owner list, second-check.md) is read
before anything moves: a failure (exit 5) moves nothing. `write` keeps every
`## From <topic>'s review` section already in write-brief.md (a finding a
sibling's review routed here), verbatim, at the end of the rebuilt brief.

`append`, run after each review, saves draft.md as draft-N.md and review.md as
review-N.md (N = the round) and appends `## Round N findings` to the brief:
each finding with its id (R<N>.<n>) and any new disputes.md lines. The same
review twice is no new round. A round past the cap is refused (exit 3): after
round 3 open findings go to the owner (review_findings.py owner). The cap is
3 plus one round per recorded lossless failure.

`lossless`, run on a hard failure of stage 5's `cookr roles lossless` (its
JSON output saved to a file), records the failure: each failed account and
each missing sentence becomes a finding `L<N>.<n>` (N the review rounds so
far) in <topic-dir>/lossless-<N>.md, and the brief gets `## Lossless failure
after round N` listing them. The failure opens one round past the cap: the
author fixes it, and the next scoped review, which lists it among the open
findings, rules on it. Run twice on the same report it changes nothing; a
report with no failure is refused (exit 1).

`review` writes <topic-dir>/review-prompt.md for the next round: round 1 the
full review, from round 2 the scoped re-review, given the earlier review-N.md
files, disputes.md, the findings still open and the diff from the last draft
(written to diff-N.md).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import apply_second_check  # noqa: E402
import owner_list  # noqa: E402
import review_findings  # noqa: E402

PROMPT_DIR = HERE / "prompts"
PROMPTS = ("research", "second-check", "write-brief", "author", "review-full", "review-scoped",
           "lossless-judge")
PRIVACY = ("Privacy: put no personal names, email addresses or project details in any web "
           "search or fetch; search for the topic only.")
FRONTMATTER = ("updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` "
               "to match the new text, and leaves `version`, `modified` and Change History to "
               "stage 5's `cookr bump`.")
_SLOT = re.compile(r"\{\{([a-z_]+)\}\}")


class Unfilled(ValueError):
    """A template placeholder with no value."""


class TooManyRounds(RuntimeError):
    """A review round past review_findings.MAX_ROUNDS."""


class AlreadyWritten(RuntimeError):
    """`write` run on a topic whose rounds have begun."""


class Unreadable(RuntimeError):
    """Something `write` reads is missing or malformed."""


_from_sections = review_findings.from_sections   # a `## From <topic>'s review` section, verbatim


def cookr_line(repo: str, cookr_py: str) -> str:
    return f"PYTHONPATH={repo}/skills/cookr/cli {cookr_py} -P -m cookr -p {repo}"


def common(repo: str, cookr_py: str, today: str | None = None, **extra) -> dict:
    return {"repo": repo, "cookr": cookr_line(repo, cookr_py), "privacy": PRIVACY,
            "today": today or _dt.date.today().isoformat(),
            "max_rounds": str(review_findings.MAX_ROUNDS), **extra}


def fill(name: str, values: dict) -> str:
    text = (PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8")
    if "{{criteria}}" in text:
        text = text.replace("{{criteria}}", (PROMPT_DIR / "criteria.md").read_text(encoding="utf-8").rstrip("\n"))
    missing = sorted({m for m in _SLOT.findall(text) if m not in values})
    if missing:
        raise Unfilled(f"{name}: unfilled {', '.join(missing)}")
    return _SLOT.sub(lambda m: str(values[m.group(1)]), text)


def _research(repo: str, artifact: str) -> dict:
    return json.loads((Path(repo) / artifact / "research" / "research.json").read_text(encoding="utf-8"))


def _corrections(tdir: Path) -> tuple[str, str]:
    """The second check's corrections, split: claims it refuted (criteria 3:
    they cannot carry MUST), and claims that only lost a citation (still
    supported; their strength is unchanged)."""
    check = tdir / "second-check.md"
    blocks = apply_second_check.parse(check.read_text(encoding="utf-8")) if check.exists() else []
    refuted = [f"- {b['id']}: {b['correction']}" for b in blocks
               if "correction" in b and apply_second_check.is_refuted(b)]
    dropped = [f"- {b['id']}: {b['correction']}" for b in blocks
               if "correction" in b and not apply_second_check.is_refuted(b)]
    return "\n".join(refuted) or "none", "\n".join(dropped) or "none"


# What `write --restart` leaves at a topic's top level: its inputs, which
# stage 2 (re)wrote or stage 3 keeps for every run (base.txt, current.md), and
# write-brief.md, which `write` rebuilds in place keeping its `## From`
# sections. Everything else there is the stopped run's and moves; integrate.md's
# `## From` sections (ROUTED) are then written back to the top level.
RESTART_KEEPS = ("base.txt", "current.md", "research-brief.md", "team-run.md", "agent-run.md",
                 "second-check.md", "research", "write-brief.md")
ROUTED = "integrate.md"
_RUN_DIR = re.compile(r"^run-\d+$")
_INTEGRATED = re.compile(r"(?m)^integrated:.*(?:\n|$)")   # the stopped run's end, never routed


def restart(tdir: Path) -> Path | None:
    """Move the stopped run whole into a new run-<k>/ (k the next free
    number): every file and folder at the topic's top level except
    RESTART_KEEPS, the run-<k>/ folders and dotfiles. The numbered round
    files, disputes.md (its ids belong to the old run), draft.md, review.md,
    integrate.md, owner-list.md, the filled prompts, lossless-run.json and
    any log all go. Then only what sibling topics routed to integrate.md (its
    `## From <topic>'s review` sections, verbatim) is written back to a new
    top-level integrate.md; the run's own `## For the owner` and its
    `integrated:` line stay in run-<k>/. None when there is nothing to move."""
    files = sorted(p for p in tdir.iterdir()
                   if p.name not in RESTART_KEEPS and not p.name.startswith(".")
                   and not (p.is_dir() and _RUN_DIR.match(p.name)))
    if not files:
        return None
    k = 1
    while (tdir / f"run-{k}").exists():
        k += 1
    run = tdir / f"run-{k}"
    run.mkdir()
    for p in files:
        p.rename(run / p.name)
    moved = run / ROUTED
    routed = _from_sections(moved.read_text(encoding="utf-8")) if moved.is_file() else []
    if routed:
        body = "\n".join(_INTEGRATED.sub("", s).rstrip("\n") + "\n" for s in routed)
        (tdir / ROUTED).write_text(f"# Integrate: {tdir.name}\n\n{body}", encoding="utf-8")
    return run


def write(tdir: Path, repo: str, cookr_py: str, artifact: str, kind: str = "existing",
          today: str | None = None, restart_run: bool = False) -> Path:
    started = [p for stem in ("review", "lossless") for _, p in _saved(tdir, stem)]
    if started and not restart_run:
        raise AlreadyWritten(f"{started[0]} exists: `write` runs in round 1 only, and a later round runs "
                             "nothing; after stage 2 re-ran this topic's research, use `write --restart`")
    # Read and build everything first: a failure here moves and writes nothing.
    path = tdir / "write-brief.md"
    try:
        data = _research(repo, artifact)
        verdicts = "\n".join(f"- {v['rule']}: {v['verdict']} (claims: {', '.join(v.get('claims', []))})"
                             for v in data.get("verdicts", [])) or "none"
        owner = owner_list.render(tdir.name, owner_list.build(Path(repo) / artifact))
        refuted, dropped = _corrections(tdir)
        kept = _from_sections(path.read_text(encoding="utf-8")) if path.exists() else []
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        raise Unreadable(f"cannot build the brief, nothing changed: {type(e).__name__}: {e}") from e
    text = fill("write-brief", common(repo, cookr_py, today, artifact=artifact, topic=tdir.name,
                                      topic_dir=str(tdir), kind=kind, verdicts=verdicts,
                                      refuted=refuted, dropped=dropped,
                                      owner=owner.split("\n", 2)[2].strip(), frontmatter=FRONTMATTER))
    if kept:
        text = text.rstrip("\n") + "\n\n" + "\n".join(kept)
    if restart_run:
        restart(tdir)
    (tdir / "owner-list.md").write_text(owner, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    return path


def _saved(tdir: Path, stem: str) -> list[tuple[int, Path]]:
    pat = re.compile(rf"^{stem}-(\d+)\.md$")
    return sorted((int(m.group(1)), p) for p in tdir.glob(f"{stem}-*.md") if (m := pat.match(p.name)))


def append(tdir: Path) -> dict:
    review = (tdir / "review.md").read_text(encoding="utf-8")
    reviews = _saved(tdir, "review")
    if reviews and reviews[-1][1].read_text(encoding="utf-8") == review:
        return {"round": reviews[-1][0], "new": False}
    n = len(reviews) + 1
    cap = review_findings.allowed_rounds(tdir)
    if n > cap:
        raise TooManyRounds(f"round {n} is past {cap}: see review_findings.py status for the "
                            "topic's next step (owner or stop)")
    (tdir / f"review-{n}.md").write_text(review, encoding="utf-8")
    if (tdir / "draft.md").exists():
        (tdir / f"draft-{n}.md").write_text((tdir / "draft.md").read_text(encoding="utf-8"), encoding="utf-8")
    parsed = review_findings.parse(review, n)
    brief_path = tdir / "write-brief.md"
    brief = brief_path.read_text(encoding="utf-8") if brief_path.exists() else ""
    out = [f"## Round {n} findings", "",
           f"Verdict: {parsed['verdict']}. Fix each finding, or dispute it in disputes.md "
           "(`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.", ""]
    out += [f"- {f['id']}: " + f["text"].replace("\n", "\n  ") for f in parsed["findings"]] or ["none"]
    out += _lint_for_author(parsed["lint"])
    disputes = tdir / "disputes.md"
    if disputes.exists():
        new = [ln for ln in disputes.read_text(encoding="utf-8").splitlines() if ln.strip() and ln not in brief]
        if new:
            out += ["", f"Disputes so far (disputes.md):", ""] + new
    brief_path.write_text(brief.rstrip("\n") + "\n\n" + "\n".join(out) + "\n", encoding="utf-8")
    return {"round": n, "new": True, "findings": len(parsed["findings"]), "verdict": parsed["verdict"]}


def _fence(lines: list[str]) -> str:
    """A code fence no line inside can close: four backticks, or one more than
    the longest backtick run in `lines`."""
    longest = max((len(run) for l in lines for run in re.findall(r"`+", l)), default=0)
    return "`" * max(4, longest + 1)


def _lint_for_author(lint: dict) -> list[str]:
    """The round's lint result for the brief: a failed lint is the draft's to
    fix; a missing or malformed lint line is the reviewer's, not the draft's."""
    if lint["state"] == "clean":
        return []
    if lint["state"] == "fail":
        fence = _fence(lint["report"])
        return ["", f"Lint failed (`{lint['reason']}`): fix each lint error in the draft. The review's "
                "`## Lint` section:", "", fence, *lint["report"], fence]
    return ["", f"The review's lint result could not be read ({lint['reason']}). That is the reviewer's "
            "fault, not the draft's: the next review restates the lint-line rule. Leave the draft "
            "unchanged on lint grounds."]


LINT_RULE = ("Round {n}'s review did not end `## Lint` with the lint line. End `## Lint` with exactly "
             "`lint: clean` or `lint: fail <n>` as its last line, before the verdict line; a script reads "
             "only that line, and a missing or malformed one fails the round.")


def review(tdir: Path, repo: str, cookr_py: str, artifact: str, today: str | None = None) -> dict:
    reviews = _saved(tdir, "review")
    n = len(reviews) + 1
    cap = review_findings.allowed_rounds(tdir)
    if n > cap:
        raise TooManyRounds(f"round {n} is past {cap}")
    values = common(repo, cookr_py, today, artifact=artifact, topic=tdir.name, topic_dir=str(tdir),
                    max_rounds=str(cap))
    result: dict = {"round": n}
    if n == 1:
        text = fill("review-full", values)
    else:
        drafts = dict(_saved(tdir, "draft"))
        before = drafts.get(n - 1)
        old = before.read_text(encoding="utf-8").splitlines(keepends=True) if before else []
        new = (tdir / "draft.md").read_text(encoding="utf-8").splitlines(keepends=True)
        diff = tdir / f"diff-{n}.md"
        diff.write_text("".join(difflib.unified_diff(old, new, f"draft-{n - 1}.md", "draft.md")), encoding="utf-8")
        status = review_findings.status(tdir)
        opened = "\n".join(f"- {f['id']}: " + f["text"].replace("\n", "\n  ") for f in status["open"]) or "none"
        last = review_findings.parse(reviews[-1][1].read_text(encoding="utf-8"), n - 1)["lint"]
        rule = "" if last["state"] in ("clean", "fail") else "\n" + LINT_RULE.format(n=n - 1) + "\n"
        text = fill("review-scoped", {**values, "round": str(n), "diff": str(diff), "open": opened,
                                      "lint_rule": rule,
                                      "reviews": ", ".join(str(p) for _, p in reviews)})
        result["diff"] = diff
    path = tdir / "review-prompt.md"
    path.write_text(text, encoding="utf-8")
    result["prompt"] = path
    return result


LOSSLESS_CITES = ("When carrying a lost sentence into a rule, every word added to the rule must be "
                  "covered by a claim the rule cites (add the claim to its citations, at the strength "
                  "the claims allow); a lost sentence no cited claim can cover is disputed in "
                  "disputes.md instead of added uncovered.")


class NoFailure(ValueError):
    """A lossless report with nothing failed."""


def record_lossless(tdir: Path, report: dict) -> dict:
    items = [f"Lost sentence, accounted for nowhere: \"{s}\"" for s in report.get("missing", [])]
    for f in report.get("failures", []):
        where = f" (moved to {f['to']})" if f.get("to") else (
            f" (obsolete: {f['obsolete']})" if f.get("obsolete") else "")
        head = f"\"{f['sentence']}\"{where}: " if f.get("sentence") else ""
        items.append(f"Lossless failure: {head}{f.get('reason', 'failed')}")
    if not items:
        raise NoFailure("the report has no missing sentence and no failure")
    n = len(_saved(tdir, "review"))
    text = (f"# Lossless failure after round {n}\n\n`cookr roles lossless` failed hard in stage 5.\n\n"
            "## Findings\n\n" + "\n".join(f"- {i}" for i in items) + "\n")
    path = tdir / f"lossless-{n}.md"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return {"round": n, "new": False, "findings": len(items)}
    path.write_text(text, encoding="utf-8")
    parsed = review_findings.parse(text, n, prefix="L")
    brief_path = tdir / "write-brief.md"
    brief = brief_path.read_text(encoding="utf-8") if brief_path.exists() else ""
    head = f"## Lossless failure after round {n}"
    if head in brief:
        brief = brief[: brief.index(head)].rstrip("\n")
    out = [head, "", "Nothing the topic held may be lost. Restore each sentence below in the draft, "
           "or dispute it in disputes.md; the next review rules on each.", "", LOSSLESS_CITES, ""]
    out += [f"- {f['id']}: {f['text']}" for f in parsed["findings"]]
    brief_path.write_text(brief.rstrip("\n") + "\n\n" + "\n".join(out) + "\n", encoding="utf-8")
    return {"round": n, "new": True, "findings": len(items), "file": str(path)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def paths(p, topic=True):
        if topic:
            p.add_argument("topic_dir", type=Path)
        p.add_argument("--repo", required=True)
        p.add_argument("--cookr-py", default=os.environ.get("COOKR_PY"), required="COOKR_PY" not in os.environ)
        p.add_argument("--today")

    p = sub.add_parser("prompt")
    p.add_argument("name", choices=PROMPTS)
    paths(p, topic=False)
    p.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    p = sub.add_parser("write")
    paths(p)
    p.add_argument("--artifact", required=True)
    p.add_argument("--kind", default="existing")
    p.add_argument("--restart", action="store_true",
                   help="move the earlier rounds into run-<k>/ and start again at round 1")
    p = sub.add_parser("append")
    p.add_argument("topic_dir", type=Path)
    p = sub.add_parser("review")
    paths(p)
    p.add_argument("--artifact", required=True)
    p = sub.add_parser("lossless")
    p.add_argument("topic_dir", type=Path)
    p.add_argument("--report", type=Path, required=True)
    args = ap.parse_args(argv)
    # A `~` that reached here unexpanded (quoted, or an env value set in
    # quotes) is the user's home, so every path argument is expanded first.
    for name in ("topic_dir", "report"):
        if getattr(args, name, None) is not None:
            setattr(args, name, Path(os.path.expanduser(getattr(args, name))))
    if getattr(args, "repo", None):
        # The prompts carry these to a subagent that may run from anywhere: a
        # relative path, relative to this cwd, is written out absolute
        # (abspath, not resolve, so a venv's python symlink is kept). A bare
        # command name such as `python3` is left for PATH.
        args.repo = os.path.abspath(os.path.expanduser(args.repo))
        args.cookr_py = os.path.expanduser(args.cookr_py)
        if os.sep in args.cookr_py:
            args.cookr_py = os.path.abspath(args.cookr_py)
    try:
        if args.cmd == "prompt":
            extra = dict(kv.split("=", 1) for kv in args.set)
            print(fill(args.name, common(args.repo, args.cookr_py, args.today, **extra)), end="")
            return 0
        if args.cmd == "write":
            print(write(args.topic_dir.resolve(), args.repo, args.cookr_py, args.artifact, args.kind, args.today,
                        restart_run=args.restart))
            return 0
        if args.cmd == "append":
            print(json.dumps(append(args.topic_dir.resolve())))
            return 0
        if args.cmd == "lossless":
            report = json.loads(args.report.read_text(encoding="utf-8"))
            print(json.dumps(record_lossless(args.topic_dir.resolve(), report)))
            return 0
        result = review(args.topic_dir.resolve(), args.repo, args.cookr_py, args.artifact, args.today)
        print(json.dumps({k: str(v) for k, v in result.items()}))
        return 0
    except Unfilled as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except NoFailure as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except TooManyRounds as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    except AlreadyWritten as e:
        print(f"error: {e}", file=sys.stderr)
        return 4
    except Unreadable as e:
        print(f"error: {' '.join(str(e).split())}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
