"""stage_status.py: where an area stands in /grow-cookbook.

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import pytest
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import stage_status  # noqa: E402
from reference_format import REFERENCE_FORMAT as FORMAT  # noqa: E402

AREA = "implementing/data"
ROLED = [("intro", None), ("rules", "rules"), ("look-for", "review-focus"),
         ("review-bar", "review-bar"), ("build-bar", "build-bar"), ("history", None)]
CITED = "- **must-index-keys**: Every foreign key MUST have an index. (claim: fk-index)\n"
UNCITED = "- **must-index-keys**: Every foreign key MUST have an index.\n"


# Every section step 3 requires, in order (G97, 1.4.33): a fixture plan has them all.
PLAN_HEAD = ("# Plan\n\n## Topics\n\nt\n\n## Gaps\n\ng\n\n## Missing subjects\n\nNone.\n\n"
             "## Overlaps\n\no\n\n")
# Fix round 1 (1.4.36): Topics is not a table here, so the research-bar check reads
# Proposed topics; the fixture asks one research-bar question for every topic.
OWNER_Q = "1. Research bar for every topic: vendor docs?\n"
PLAN_TAIL = f"\n## Research questions\n\nq\n\n## Owner questions\n\n{OWNER_Q}\n## Step-4 re-check\n\nr\n"


def report(d: Path) -> None:
    """A/run_gaps.json as a current run saves it (G99: a plan needs one)."""
    (d / "run_gaps.json").write_text(json.dumps({"stale_reference": [], "reference_format": FORMAT}),
                                     encoding="utf-8")


def artifact(folder: Path, parts=ROLED, rules=CITED) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    manifest = [{"part": p, **({"role": r} if r else {})} for p, r in parts]
    (folder / "artifact.json").write_text(json.dumps({"meta": {}, "parts": manifest}), encoding="utf-8")
    for p, _ in parts:
        (folder / f"{p}.md").write_text(rules if p == "rules" else "\nx\n", encoding="utf-8")
    research = folder / "research"
    research.mkdir(exist_ok=True)
    (research / "research.json").write_text("{}", encoding="utf-8")
    (research / "research.md").write_text("x\n", encoding="utf-8")
    return folder


def area(repo: Path, topics: dict[str, str]) -> Path:
    """The area's workspace dir, its plan proposing `topics` {name: artifact path}, approved."""
    d = repo / "docs" / "grow-cookbook" / "areas" / AREA
    d.mkdir(parents=True)
    rows = "".join(f"| {t} | kept | `{a}` | why |\n" for t, a in topics.items())
    (d / "area-plan.md").write_text(PLAN_HEAD + "## Proposed topics\n\n| Topic | Action | Artifact | Why |\n"
                                    f"|---|---|---|---|\n{rows}" + PLAN_TAIL, encoding="utf-8")
    (d / "reference.json").write_text("[]", encoding="utf-8")
    report(d)
    approve(d)
    for t in topics:
        (d / "topics" / t).mkdir(parents=True)
        (d / "topics" / t / "second-check.md").write_text("x\n", encoding="utf-8")
    return d


def approve(d: Path, mode: str = "w", tail: str | None = None) -> None:
    """Record the plan's approval as stage 1 says: its hash and, on the same
    line, A/reference.json's (`tail`: what follows the plan's hash instead)."""
    ref = d / "reference.json"
    if not ref.is_file():
        ref.write_text("[]", encoding="utf-8")
    if tail is None:
        tail = f", reference-hash {stage_status.git_blob_hash(ref)}"
    line = f"- plan: area-plan.md, git hash-object {stage_status.git_blob_hash(d / 'area-plan.md')}"
    with open(d / "approval.md", mode, encoding="utf-8") as f:
        f.write(line + tail + "\n")


def stamped(d: Path, n: int = 1, fmt: int | None = FORMAT) -> None:
    """Write A/reference.json with `n` rows of format `fmt` (None: unstamped)."""
    rows = [{"speciality": f"data/s{i}", "topic": None, "file": f"/s{i}.txt",
             **({"format": fmt} if fmt is not None else {})} for i in range(n)]
    (d / "reference.json").write_text(json.dumps(rows), encoding="utf-8")


def cookr_skill(repo: Path, version="0.21.4") -> None:
    f = repo / "skills" / "cookr" / "SKILL.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(f'---\nname: cookr\nversion: "{version}"\n---\n', encoding="utf-8")


def run(repo: Path) -> dict:
    return stage_status.status(AREA, repo / "docs" / "grow-cookbook", repo)


def test_written_needs_the_roled_parts(tmp_path):
    cookr_skill(tmp_path)
    folder = artifact(tmp_path / "cookbook/guidelines" / AREA / "keys", parts=[("intro", None), ("rules", None),
                                                                              ("history", None)])
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    (d / "topics/keys/base.txt").write_text("abc\n", encoding="utf-8")
    (d / "topics/keys/owner-list.md").write_text("x\n", encoding="utf-8")
    t = run(tmp_path)["topics"]["keys"]
    assert t["written"] is False and t["next"] == "write"

    artifact(folder)
    t = run(tmp_path)["topics"]["keys"]
    assert t["written"] is True and t["next"] == "review"


def test_a_roled_topic_is_not_written_until_its_rules_cite_research(tmp_path):
    # The 21 data topics are roled before stage 3 ever runs on them.
    cookr_skill(tmp_path)
    artifact(tmp_path / "cookbook/guidelines" / AREA / "keys", rules=CITED + UNCITED.replace("keys", "rows"))
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    (d / "topics/keys/base.txt").write_text("abc\n", encoding="utf-8")
    (d / "topics/keys/owner-list.md").write_text("x\n", encoding="utf-8")
    assert run(tmp_path)["topics"]["keys"]["written"] is False


def test_the_artifact_path_comes_from_the_plan(tmp_path):
    # A topic folded into, or created under, another area lives where the plan says.
    cookr_skill(tmp_path)
    elsewhere = "cookbook/guidelines/implementing/storage/keys"
    artifact(tmp_path / elsewhere)
    area(tmp_path, {"keys": elsewhere})
    t = run(tmp_path)["topics"]["keys"]
    assert t["artifact"] == elsewhere
    assert t["folder"] is True and t["research"] is True


def test_a_topic_the_plan_does_not_place_defaults_to_the_area(tmp_path):
    cookr_skill(tmp_path)
    artifact(tmp_path / "cookbook/guidelines" / AREA / "rows")
    area(tmp_path, {})
    assert run(tmp_path)["topics"]["rows"]["artifact"] == f"cookbook/guidelines/{AREA}/rows"


def test_the_status_says_whether_the_repos_cookr_is_new_enough(tmp_path):
    # 0.19.3 brings `validate --research`, which stage 2 ends with; 0.19.4 lets
    # cookr run from any directory, which the skill no longer says to `cd` for;
    # 0.19.5 makes `roles check` and `validate --research` on one folder read
    # only what that folder needs, so running them at every stage stays cheap;
    # 0.20.0 brings `roles gaps`, which stage 1 measures with; 0.20.1 ends its
    # sentences at paragraphs, list items and headings, never a wrapped line;
    # 0.20.2 makes each table row its own block; 0.21.0 keeps owner_rules to
    # prior rules and ignores `---` and title headings in the lossless gate;
    # 0.21.3 writes and checks the one lossless retarget (`--retarget`), which
    # stage 5 relies on: 0.21.1 ignores a `retargeted` record; 0.21.4's
    # `--retarget` refuses targets that trip, so a bad pick spends nothing.
    cookr_skill(tmp_path, "0.21.4")
    assert run(tmp_path)["cookr"] == {"version": "0.21.4", "minimum": "0.21.4", "ok": True}
    for old in ("0.21.3", "0.21.2", "0.21.1", "0.21.0", "0.20.2", "0.19.5"):
        cookr_skill(tmp_path, old)
        assert run(tmp_path)["cookr"] == {"version": old, "minimum": "0.21.4", "ok": False}
    (tmp_path / "skills/cookr/SKILL.md").unlink()
    assert run(tmp_path)["cookr"] == {"version": None, "minimum": "0.21.4", "ok": False}


def test_every_topic_waits_for_the_plan_and_its_approval(tmp_path):
    # E1: a topic owes nothing before the plan is approved.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "approval.md").unlink()
    assert run(tmp_path)["topics"]["rows"]["next"] == "approve"
    (d / "area-plan.md").unlink()
    assert run(tmp_path)["topics"]["rows"]["next"] == "plan"


def written_topic(tmp_path: Path) -> Path:
    art = f"cookbook/guidelines/{AREA}/rows"
    artifact(tmp_path / art)
    d = area(tmp_path, {"rows": art})
    t = d / "topics" / "rows"
    for f in ("base.txt", "owner-list.md"):
        (t / f).write_text("x\n", encoding="utf-8")
    return t


def test_rounds_are_counted_and_a_third_failed_round_goes_to_the_owner(tmp_path):
    t = written_topic(tmp_path)
    fail = "## Findings\n\n- wrong\n\n## Lint\n\nlint: clean\n\nverdict: fail\n"
    for n in (1, 2):
        (t / f"review-{n}.md").write_text(fail, encoding="utf-8")
        (t / "review.md").write_text(fail, encoding="utf-8")
        got = run(tmp_path)["topics"]["rows"]
        # m3: a failed round below the cap owes the author's next round.
        assert (got["rounds"], got["next"], got["owner"]) == (n, "write", [])
    (t / "review-3.md").write_text(fail, encoding="utf-8")
    got = run(tmp_path)["topics"]["rows"]
    assert (got["rounds"], got["next"]) == (3, "integrate")
    assert got["owner"] == ["R1.1", "R2.1", "R3.1"]


def test_every_merged_copy_is_folded_whatever_its_fold_check(tmp_path):
    # 1.4.13, G16 (was E4): stage 5 passes --copy for every merged copy, not
    # only those with fold_check true: R2 keeps text that differs.
    art = f"cookbook/guidelines/{AREA}/rows"
    area(tmp_path, {"rows": art})
    ws = tmp_path / "docs" / "grow-cookbook"
    survivor = art.removeprefix("cookbook/")
    (ws / "worklist.json").write_text(json.dumps({"batches": [{"topics": [{"topic": "rows", "survivor": survivor,
        "copies": [{"folder": "guidelines/a/rows", "fold_check": True},
                   {"folder": "guidelines/b/rows", "fold_check": False},
                   {"folder": "guidelines/c/rows"}]}]}]}), encoding="utf-8")
    assert run(tmp_path)["topics"]["rows"]["fold"] == ["cookbook/guidelines/a/rows", "cookbook/guidelines/b/rows",
                                                       "cookbook/guidelines/c/rows"]
    # a copy its own area's plan keeps as an artifact of its own is not merged, so not folded
    other = ws / "areas" / "b"
    other.mkdir(parents=True)
    (other / "area-plan.md").write_text("## Proposed topics\n\n| Topic | Action | Artifact | Why |\n|---|---|---|---|\n"
                                        "| rows | kept | `cookbook/guidelines/b/rows` | own |\n", encoding="utf-8")
    assert run(tmp_path)["topics"]["rows"]["fold"] == ["cookbook/guidelines/a/rows", "cookbook/guidelines/c/rows"]
    # 1.4.14, N2: only `kept` keeps a copy out; dropped, split or new still gets the lossless check
    for action in ("dropped", "split", "new"):
        (other / "area-plan.md").write_text(
            "## Proposed topics\n\n| Topic | Action | Artifact | Why |\n|---|---|---|---|\n"
            f"| rows | {action} | `cookbook/guidelines/b/rows` | own |\n", encoding="utf-8")
        assert "cookbook/guidelines/b/rows" in run(tmp_path)["topics"]["rows"]["fold"], action


def test_a_kept_copy_another_plan_merges_in_is_a_conflict_in_both_areas_and_folded(tmp_path):
    # 1.4.15, M1': a copy one plan keeps and another merges is an owner item in
    # the merging and the target area even when the target plan names the copy
    # (the re-review's probe shape), and folded meanwhile: over-reporting beats missing.
    art = f"cookbook/guidelines/{AREA}/rows"
    copy = "cookbook/guidelines/reviewing/data/rows"
    d = area(tmp_path, {"rows": art})
    (d / "area-plan.md").write_text((d / "area-plan.md").read_text(encoding="utf-8").replace(
        "| why |", "| merges in reviewing/data/rows |", 1), encoding="utf-8")
    ws = tmp_path / "docs" / "grow-cookbook"
    artifact(tmp_path / copy)
    plan_of(ws, "reviewing/data", [("rows", "merged", art)])
    s = run(tmp_path)
    assert s["conflicts"] == [] and s["topics"]["rows"]["fold"] == [copy]   # named, nobody keeps it
    plan_of(ws, "planning/data", [("rows", "kept", copy)])
    s = run(tmp_path)
    assert s["topics"]["rows"]["fold"] == [copy]
    why = f"planning/data keeps {copy}, reviewing/data merges it into {art}"
    assert [(c["copy"], c["why"]) for c in s["conflicts"]] == [(copy, why)]
    assert stage_status.status("reviewing/data", ws, tmp_path)["conflicts"] == s["conflicts"]


def test_incoming_fold_and_conflicts_agree_on_what_is_a_merge(tmp_path):
    # 1.4.14, M4: a merged row whose copy folder does not exist is a record of
    # a move, not a merge: none of incoming, fold and conflicts lists it; once
    # the folder exists, all three do.
    art = f"cookbook/guidelines/{AREA}/rows"
    area(tmp_path, {"rows": art})
    ws = tmp_path / "docs" / "grow-cookbook"
    plan_of(ws, "reviewing/data", [("rows", "merged", art)])
    s = run(tmp_path)
    assert (s["incoming"], s["topics"]["rows"]["fold"], s["conflicts"]) == ([], [], [])
    artifact(tmp_path / "cookbook/guidelines/reviewing/data/rows")
    s = run(tmp_path)
    copy = "cookbook/guidelines/reviewing/data/rows"
    assert [i["copy"] for i in s["incoming"]] == [copy]
    assert s["topics"]["rows"]["fold"] == [copy]
    assert [c["copy"] for c in s["conflicts"]] == [copy]


def test_a_copy_another_plan_merges_in_is_folded(tmp_path):
    # 1.4.13, G16: a plan's merged row into this artifact is a merged copy too.
    art = f"cookbook/guidelines/{AREA}/rows"
    area(tmp_path, {"rows": art})
    ws = tmp_path / "docs" / "grow-cookbook"
    artifact(tmp_path / "cookbook/guidelines/reviewing/data/rows")
    plan_of(ws, "reviewing/data", [("rows", "merged", art)])
    # 1.4.14, M2: a merge record whose copy folder does not exist is not folded
    plan_of(ws, "planning/data", [("rows", "merged", art)])
    assert run(tmp_path)["topics"]["rows"]["fold"] == ["cookbook/guidelines/reviewing/data/rows"]
    # a merge within the area is a merged copy too, and no cross-area conflict
    artifact(tmp_path / f"cookbook/guidelines/{AREA}/rows-twin")
    d = ws / "areas" / AREA
    plan = (d / "area-plan.md").read_text(encoding="utf-8").replace(
        "|---|---|---|---|\n", f"|---|---|---|---|\n| rows-twin | merged | `{art}` | twin |\n", 1)
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    s = run(tmp_path)
    assert s["topics"]["rows"]["fold"] == [f"cookbook/guidelines/{AREA}/rows-twin",
                                           "cookbook/guidelines/reviewing/data/rows"]
    assert [c["topic"] for c in s["conflicts"]] == ["rows"] and [i["topic"] for i in s["incoming"]] == ["rows"]


def test_a_review_not_yet_counted_owes_the_count_step(tmp_path):
    t = written_topic(tmp_path)
    (t / "review.md").write_text("## Findings\n\n- wrong\n\nverdict: fail\n", encoding="utf-8")
    assert run(tmp_path)["topics"]["rows"]["next"] == "review"


def test_a_lint_error_at_the_cap_stops_the_topic(tmp_path):
    t = written_topic(tmp_path)
    fail = "## Findings\n\n- wrong\n\n## Lint\n\n[FAIL] L4: no approved-by\n\nlint: fail 1\n\nverdict: fail\n"
    for n in (1, 2, 3):
        (t / f"review-{n}.md").write_text(fail, encoding="utf-8")
    (t / "review.md").write_text(fail, encoding="utf-8")
    got = run(tmp_path)["topics"]["rows"]
    assert (got["next"], got["owner"], got["why"]) == ("stop", [], "a lint error stands at the round cap")


def test_a_recorded_lossless_failure_owes_a_write_and_only_a_dated_integrate_is_done(tmp_path):
    t = written_topic(tmp_path)
    ok = "## Findings\n\n- none\n\n## Lint\n\nlint: clean\n\nverdict: pass\n"
    (t / "review-1.md").write_text(ok, encoding="utf-8")
    (t / "review.md").write_text(ok, encoding="utf-8")
    (t / "integrate.md").write_text("# Integrate\n\n## For the owner\n\nnone\n", encoding="utf-8")
    assert run(tmp_path)["topics"]["rows"]["next"] == "integrate"
    (t / "lossless-1.md").write_text("## Findings\n\n- Lost sentence\n", encoding="utf-8")
    assert run(tmp_path)["topics"]["rows"]["next"] == "write"
    (t / "lossless-1.md").unlink()
    (t / "integrate.md").write_text("# Integrate\n\nintegrated: 2026-11-16\n", encoding="utf-8")
    assert run(tmp_path)["topics"]["rows"]["next"] is None


def test_a_saved_round_and_a_newer_review_owes_the_count_step(tmp_path):
    # n4: review-1 is saved; review.md is a newer review not yet counted.
    t = written_topic(tmp_path)
    (t / "review-1.md").write_text("## Findings\n\n- wrong\n\n## Lint\n\nlint: clean\n\nverdict: fail\n",
                                   encoding="utf-8")
    (t / "review.md").write_text("## Findings\n\n- other\n\n## Lint\n\nlint: clean\n\nverdict: fail\n",
                                 encoding="utf-8")
    assert run(tmp_path)["topics"]["rows"]["next"] == "review"
    (t / "review.md").write_text((t / "review-1.md").read_text(encoding="utf-8"), encoding="utf-8")
    assert run(tmp_path)["topics"]["rows"]["next"] == "write"


def test_a_dated_integrate_is_done_whatever_the_review_files_say(tmp_path):
    # N1: the trial's ab-testing: review.md passed in round 10 and was never
    # saved as review-10.md; review-1..9 failed; integrate.md is dated.
    t = written_topic(tmp_path)
    # n5: the old rounds carry `lint: clean`, so review_findings says `owner`.
    fail = "## Findings\n\n- wrong\n\n## Lint\n\nlint: clean\n\nverdict: fail\n"
    for n in range(1, 10):
        (t / f"review-{n}.md").write_text(fail, encoding="utf-8")
    (t / "review.md").write_text("## Findings\n\nnone\n\n## Lint\n\nCLEAN\n\nverdict: pass\n", encoding="utf-8")
    (t / "integrate.md").write_text("# Integrate: rows\n\nintegrated: 2026-11-16\n", encoding="utf-8")
    import review_findings
    assert review_findings.status(t)["next"] == "owner"
    got = run(tmp_path)["topics"]["rows"]
    assert (got["integrated"], got["next"], got["owner"], got["why"]) == (True, None, [], "")


def test_the_review_field_is_the_effective_verdict(tmp_path):
    # n6: a `verdict: pass` whose lint line is missing or failing is no pass.
    t = written_topic(tmp_path)
    for lint, want in (("lint: clean", ("pass", "clean")), ("lint: fail 1", ("fail", "fail")),
                       ("lint: CLEAN", ("fail", "malformed")), ("Lint: clean", ("fail", "malformed")),
                       ("all fine", ("fail", "missing"))):
        text = f"## Findings\n\nnone\n\n## Lint\n\n{lint}\n\nverdict: pass\n"
        (t / "review.md").write_text(text, encoding="utf-8")
        (t / "review-1.md").write_text(text, encoding="utf-8")
        got = run(tmp_path)["topics"]["rows"]
        assert (got["review"], got["lint"]) == want, lint
    (t / "review.md").write_text("## Findings\n\nnone\n\nverdict: pass\n", encoding="utf-8")
    (t / "review-1.md").unlink()
    got = run(tmp_path)["topics"]["rows"]
    assert (got["review"], got["lint"]) == ("fail", "no-section")


def test_relative_workspace_and_repo_from_another_cwd_match_absolute_ones(tmp_path):
    # The trial: run from the teamtesting root with --workspace and --repo
    # relative to it, the workspace outside the cookbook repo.
    import shutil
    import subprocess
    repo = tmp_path / "outer" / "external" / "cookbook"
    cookr_skill(repo)
    written_topic(repo)
    ws = tmp_path / "outer" / ".superpowers" / "sdd" / "run"
    ws.parent.mkdir(parents=True)
    shutil.move(str(repo / "docs" / "grow-cookbook"), str(ws))
    script = str(Path(stage_status.__file__))

    def cli(cwd: Path, *args: str) -> dict:
        r = subprocess.run([sys.executable, script, AREA, *args], cwd=cwd, capture_output=True, text=True, check=True)
        return json.loads(r.stdout)

    absolute = cli(tmp_path, "--workspace", str(ws), "--repo", str(repo))
    assert absolute["topics"]["rows"]["next"] == "review" and absolute["plan"] is True
    relative = cli(tmp_path / "outer", "--workspace", ".superpowers/sdd/run", "--repo", "external/cookbook")
    assert relative == absolute
    # with no --workspace it is <repo>/docs/grow-cookbook, whatever the cwd
    shutil.move(str(ws), str(repo / "docs" / "grow-cookbook"))
    inside = cli(tmp_path / "outer", "--repo", "external/cookbook")
    assert inside["topics"] == absolute["topics"] and inside["dir"] == str(repo / "docs/grow-cookbook/areas" / AREA)


def test_a_repo_with_no_cookbook_fails_loudly(tmp_path):
    # n8's probe: <repo> read from the wrong checkout (the teamtesting root)
    # gave `cookr: None` and `next: research`. It must stop, naming the cause.
    import subprocess
    good = tmp_path / "cookbook-repo"
    cookr_skill(good)
    written_topic(good)
    script = str(Path(stage_status.__file__))
    ws = str(good / "docs" / "grow-cookbook")
    for repo in ("other", "only-cookbook-dir", "only-cookr"):
        (tmp_path / repo).mkdir()
    (tmp_path / "only-cookbook-dir" / "cookbook").mkdir()
    cookr_skill(tmp_path / "only-cookr")
    for repo in ("other", "only-cookbook-dir", "only-cookr"):
        r = subprocess.run([sys.executable, script, AREA, "--workspace", ws, "--repo", str(tmp_path / repo)],
                           capture_output=True, text=True)
        assert (r.returncode, r.stdout) == (2, ""), repo
        assert "holds no cookbook" in r.stderr and str(tmp_path / repo) in r.stderr, repo
    r = subprocess.run([sys.executable, script, AREA, "--workspace", ws, "--repo", str(good)],
                       capture_output=True, text=True)
    assert r.returncode == 0 and json.loads(r.stdout)["topics"]["rows"]["next"] == "review"


def test_a_topic_merged_into_another_areas_folder_owes_nothing_here(tmp_path):
    # 1.4.7, G7: a plan row whose Action is `merged` and whose Artifact is in
    # another area runs only under the plan whose area holds that folder.
    cookr_skill(tmp_path)
    survivor = "cookbook/guidelines/implementing/storage/keys"
    artifact(tmp_path / "cookbook/guidelines" / AREA / "keys")   # this area's copy
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    plan = (d / "area-plan.md").read_text(encoding="utf-8").replace(
        "|---|---|---|---|\n", f"|---|---|---|---|\n| keys | merged | `{survivor}/` | twin |\n")
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    (d / "approval.md").unlink()
    s = run(tmp_path)
    keys = s["topics"]["keys"]
    assert keys["merged"] == survivor and keys["next"] is None and keys["why"] == f"merged into {survivor}"
    assert s["topics"]["rows"]["next"] == "approve" and s["topics"]["rows"]["merged"] is None
    # approved: the merged topic still owes no research; the area's next ignores it
    approve(d)
    s = run(tmp_path)
    assert s["topics"]["keys"]["next"] is None and s["topics"]["rows"]["next"] == "research"
    assert s["next"] == "research"
    # merged into a folder of this area: it runs here as usual
    plan = plan.replace(f"`{survivor}/`", f"`cookbook/guidelines/{AREA}/rows`")
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    approve(d)
    keys = run(tmp_path)["topics"]["keys"]
    assert keys["merged"] is None and keys["next"] == "research"
    # every topic merged elsewhere: the area owes nothing
    only = tmp_path / "only"
    cookr_skill(only)
    d = area(only, {})
    plan = (d / "area-plan.md").read_text(encoding="utf-8").replace(
        "|---|---|---|---|\n", f"|---|---|---|---|\n| keys | Merged | `{survivor}` | twin |\n")
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    approve(d)
    s = run(only)
    assert s["topics"]["keys"]["next"] is None and s["next"] is None


def test_an_integrated_topic_lists_its_routed_findings_for_the_owner(tmp_path):
    # 1.4.10, N5: a finding a sibling routed to an integrated topic's
    # integrate.md (`## From <sibling>'s review`) is an owner item, so it
    # reaches the hand-off. Shape of the trial's ab-testing/integrate.md,
    # which holds debug-mode's R1.5.
    t = written_topic(tmp_path)
    (t / "integrate.md").write_text(
        "# Integrate: rows\n\n## Step 1: cookr roles lossless\n\nexit 0\n\n"
        "## For the owner\n\nnone\n\n## Step 4: /add-artifact\n\nApproved: yes\n"
        "integrated: 2026-11-16\n\n"
        "## From debug-mode's review\n\n"
        "- R1.5: rows' artifact.json has `\"platforms\": []`; list the platforms\n"
        "  its rules cover.\n"
        "- R2.1: a second routed finding.\n\n"
        "## From storage's review\n\n```\n## not a heading\n```\n- R1.2: a third.\n",
        encoding="utf-8")
    got = run(tmp_path)["topics"]["rows"]
    assert (got["integrated"], got["next"]) == (True, None)
    assert got["owner"] == [
        "from debug-mode's review: R1.5: rows' artifact.json has `\"platforms\": []`; list the platforms "
        "its rules cover.",
        "from debug-mode's review: R2.1: a second routed finding.",
        "from storage's review: ```\n## not a heading\n```",   # 1.4.11, N6: fenced text is kept
        "from storage's review: R1.2: a third.",
    ]


def plan_of(ws: Path, area_: str, rows: list[tuple[str, str, str]], why="why") -> Path:
    d = ws / "areas" / area_
    d.mkdir(parents=True, exist_ok=True)
    body = "".join(f"| {t} | {a} | `{f}` | {why} |\n" for t, a, f in rows)
    (d / "area-plan.md").write_text(PLAN_HEAD + "## Proposed topics\n\n| Topic | Action | Artifact | Why |\n"
                                    f"|---|---|---|---|\n{body}" + PLAN_TAIL, encoding="utf-8")
    if not (d / "run_gaps.json").exists():
        report(d)
    return d


def test_a_merge_into_this_area_its_plan_does_not_list_is_a_conflict(tmp_path):
    # 1.4.13, G9: reviewing/language merges python into implementing/language,
    # whose plan lists python only as its own `kept` survivor.
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    survivor = f"cookbook/guidelines/{AREA}/python"
    area(tmp_path, {"python": survivor})
    plan_of(ws, "reviewing/data", [("python", "merged", survivor)])
    # a copy with no folder is a record of a move, nothing to merge: no conflict, not incoming
    s = run(tmp_path)
    assert s["conflicts"] == [] and s["incoming"] == []
    artifact(tmp_path / "cookbook/guidelines/reviewing/data/python")
    s = run(tmp_path)
    incoming = {"topic": "python", "plan": "reviewing/data", "copy": "cookbook/guidelines/reviewing/data/python",
                "artifact": survivor}
    assert s["incoming"] == [incoming]
    assert s["conflicts"] == [{**incoming, "why": f"the {AREA} plan does not list "
                                                  "cookbook/guidelines/reviewing/data/python"}]
    # the merging plan's own status reports the same conflict
    other = stage_status.status("reviewing/data", ws, tmp_path)
    assert other["conflicts"] == s["conflicts"] and other["incoming"] == []


def test_a_merge_the_target_plan_lists_is_no_conflict(tmp_path):
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    survivor = f"cookbook/guidelines/{AREA}/python"
    d = area(tmp_path, {"python": survivor})
    plan_of(ws, "reviewing/data", [("python", "merged", survivor)])
    artifact(tmp_path / "cookbook/guidelines/reviewing/data/python")
    original = (d / "area-plan.md").read_text(encoding="utf-8")

    def lists(why: str) -> None:
        (d / "area-plan.md").write_text(original.replace(
            "|---|---|---|---|\n", "|---|---|---|---|\n| python-review | merged | `" + survivor
            + f"` | {why} |\n", 1), encoding="utf-8")
    # 1.4.14, N1: naming a longer path is not naming the copy
    lists("merges in reviewing/data/python-typing")
    assert len(run(tmp_path)["conflicts"]) == 1
    lists("merges in reviewing/data/python")
    s = run(tmp_path)
    assert len(s["incoming"]) == 1 and s["conflicts"] == []


def test_a_merge_into_an_area_with_no_plan_yet_is_incoming_there_and_no_conflict(tmp_path):
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    plan_of(ws, "reviewing/data", [("python", "merged", f"cookbook/guidelines/{AREA}/python")])
    # 1.4.14, M3: the copy exists, so only the missing target plan rules out a conflict
    artifact(tmp_path / "cookbook/guidelines/reviewing/data/python")
    assert stage_status.status("reviewing/data", ws, tmp_path)["conflicts"] == []
    s = run(tmp_path)
    assert [i["topic"] for i in s["incoming"]] == ["python"] and s["conflicts"] == []


def test_a_target_plan_names_the_copy_short_or_full_as_a_whole_path():
    # 1.4.16, G20: stage-1.md documents `<plan>/<topic>`; a plan may also give
    # the full copy folder. Either form names it, only as a whole path (N1).
    copy = "reviewing/code-quality/bulk-operation-verification"
    names = stage_status._names
    assert names([f" x | merges in {copy} "], copy)  # the documented form alone (the shipping log's claim)
    assert names([f" x | merges in `{copy}`. "], copy)
    assert names([f" x | merges in `cookbook/guidelines/{copy}` "], copy)
    assert names([f" x | merges in cookbook/guidelines/{copy}/ "], copy)
    assert names([f" x | merges in guidelines/{copy} "], copy)   # 1.4.17, M1: the worklist's own form
    assert names([f" x | merges in `guidelines/{copy}`. "], copy)
    assert not names([f" x | merges in other/guidelines/{copy} "], copy)
    assert not names([f" x | merges in guidelines/implementing/{copy} "], copy)
    assert not names([f" x | merges in {copy}-twin "], copy)
    assert not names([f" x | merges in {copy}/part "], copy)
    assert not names([f" x | merges in other/{copy} "], copy)
    assert not names([f" x | merges in cookbook/guidelines/implementing/{copy} "], copy)


def test_two_plans_keeping_one_artifact_is_a_conflict_in_both_areas(tmp_path):
    # 1.4.16, G26: reviewing/security and implementing/security both kept
    # vulnerability-prioritization; a double run was invisible.
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    art = "cookbook/guidelines/implementing/security/vulnerability-prioritization"
    plan_of(ws, "implementing/security", [("vulnerability-prioritization", "kept", art)])
    assert stage_status.status("implementing/security", ws, tmp_path)["conflicts"] == []
    plan_of(ws, "reviewing/security", [("vulnerability-prioritization", "kept", art),
                                       ("other", "kept", "cookbook/guidelines/reviewing/security/other")])
    # 1.4.17, N4: its own fields, not a merge conflict's `plan`/`copy` in another sense
    want = [{"kind": "double-keep", "topic": "vulnerability-prioritization",
             "plans": ["implementing/security", "reviewing/security"],
             "artifact": art, "why": f"implementing/security and reviewing/security both keep {art}"}]
    assert stage_status.status("implementing/security", ws, tmp_path)["conflicts"] == want
    assert stage_status.status("reviewing/security", ws, tmp_path)["conflicts"] == want
    assert stage_status.status("shipping", ws, tmp_path)["conflicts"] == []


def test_a_merge_into_a_plan_not_yet_written_is_pending_never_clean(tmp_path, capsys):
    # 1.4.24, G47: no conflict only because the survivor's plan does not exist
    # yet read as confirmed; it is listed as pending_target, one entry per row.
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    survivor = f"cookbook/guidelines/{AREA}/python"
    plan_of(ws, "reviewing/data", [("python", "merged", survivor)])
    artifact(tmp_path / "cookbook/guidelines/reviewing/data/python")
    want = [{"kind": "merge", "topic": "python", "plan": "reviewing/data",
             "copy": "cookbook/guidelines/reviewing/data/python", "artifact": survivor,
             "why": f"the {AREA} plan does not exist yet: nothing confirms this merge"}]
    other = stage_status.status("reviewing/data", ws, tmp_path)
    assert other["conflicts"] == [] and other["pending_target"] == want
    assert "pending_target" in other["next_why"] and "python" in other["next_why"]
    assert run(tmp_path)["pending_target"] == want
    assert stage_status.main(["reviewing/data", "--workspace", str(ws), "--repo", str(tmp_path)]) == 0
    assert "pending_target" in capsys.readouterr().err
    area(tmp_path, {"python": survivor})          # the target plan now exists: a conflict, not pending
    other = stage_status.status("reviewing/data", ws, tmp_path)
    assert other["pending_target"] == [] and "pending_target" not in other["next_why"] and len(other["conflicts"]) == 1


def test_a_kept_artifact_in_an_area_with_no_plan_is_pending(tmp_path):
    # 1.4.24, G47: the double-keep check cannot run against a plan not written yet.
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    art = "cookbook/guidelines/implementing/security/vulnerability-prioritization"
    plan_of(ws, "reviewing/security", [("vulnerability-prioritization", "kept", art),
                                       ("own", "kept", "cookbook/guidelines/reviewing/security/own")])
    want = [{"kind": "keep", "topic": "vulnerability-prioritization", "plans": ["reviewing/security"],
             "artifact": art, "why": "the implementing/security plan does not exist yet: "
                                     "nothing confirms no other plan keeps it"}]
    assert stage_status.status("reviewing/security", ws, tmp_path)["pending_target"] == want
    plan_of(ws, "implementing/security", [("other", "kept", "cookbook/guidelines/implementing/security/other")])
    s = stage_status.status("reviewing/security", ws, tmp_path)
    assert s["pending_target"] == [] and s["conflicts"] == []


# 1.4.25 G75: folds no plan stands behind, new_home merges, next_why,
# specialities pointing at a copy a fold deletes.

def _worklist(ws: Path, topics: list) -> None:
    ws.mkdir(parents=True, exist_ok=True)
    (ws / "worklist.json").write_text(json.dumps({"batches": [{"topics": topics}]}), encoding="utf-8")


def test_a_worklist_fold_from_an_area_with_no_plan_is_incoming_unplanned(tmp_path):
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    survivor = f"guidelines/{AREA}/python"
    area(tmp_path, {"python": f"cookbook/{survivor}"})
    artifact(tmp_path / "cookbook/guidelines/testing/python")
    _worklist(ws, [{"topic": "python", "survivor": survivor, "copies": [{"folder": "guidelines/testing/python"}]},
                   {"topic": "py2", "survivor": survivor, "new_home": "guidelines/planning/data/py2"}])
    s = run(tmp_path)
    assert s["incoming_unplanned"] == [
        {"via": "new_home", "topic": "py2", "copy": "cookbook/guidelines/planning/data/py2",
         "survivor": f"cookbook/{survivor}", "plan": "planning/data",
         "why": "the planning/data plan does not exist yet: no plan stands behind this fold"},
        {"via": "copy", "topic": "python", "copy": "cookbook/guidelines/testing/python",
         "survivor": f"cookbook/{survivor}", "plan": "testing",
         "why": "the testing plan does not exist yet: no plan stands behind this fold"}]
    plan_of(ws, "testing", [("python", "merged", f"cookbook/{survivor}")])
    assert [r["plan"] for r in run(tmp_path)["incoming_unplanned"]] == ["planning/data"]


def test_a_new_home_merge_into_an_area_with_no_plan_is_pending_then_incoming(tmp_path):
    # implementing/documentation's docs-match-code: merged into a reviewing
    # folder through `new_home`, with no copy folder of its own.
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    survivor = f"cookbook/guidelines/{AREA}/python"
    _worklist(ws, [{"topic": "python", "survivor": survivor.removeprefix("cookbook/"),
                    "new_home": "guidelines/reviewing/data/python"}])
    plan_of(ws, "reviewing/data", [("python", "merged", survivor)])
    other = stage_status.status("reviewing/data", ws, tmp_path)
    assert [(p["kind"], p["topic"], p.get("via")) for p in other["pending_target"]] == [("merge", "python", "new_home")]
    area(tmp_path, {"python": survivor})
    s = run(tmp_path)
    assert [(i["topic"], i["plan"], i.get("via")) for i in s["incoming"]] == [("python", "reviewing/data", "new_home")]
    assert stage_status.status("reviewing/data", ws, tmp_path)["pending_target"] == []


def test_every_next_has_a_one_line_why(tmp_path):
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    s = run(tmp_path)
    assert s["next"] == "plan" and s["next_why"] == "no area-plan.md yet"
    plan_of(ws, AREA, [("python", "merged", "cookbook/guidelines/testing/python")])
    (ws / "areas" / AREA / "reference.json").write_text("[]", encoding="utf-8")   # step 1.1 writes it
    s = run(tmp_path)
    assert s["next"] == "approve" and "every row merged elsewhere: approval is a record" in s["next_why"]
    d = ws / "areas" / AREA
    approve(d)
    s = run(tmp_path)
    assert s["next"] is None and s["next_why"] == "no topic owes a stage here"
    plan_of(ws, AREA, [("keys", "kept", f"cookbook/guidelines/{AREA}/keys")])
    approve(d)
    s = run(tmp_path)
    assert s["next"] == "research" and s["next_why"] == "keys owes research"
    assert "\n" not in s["next_why"]


def test_a_speciality_pointing_at_a_copy_a_fold_deletes_is_listed(tmp_path):
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    survivor = f"guidelines/{AREA}/python"
    area(tmp_path, {"python": f"cookbook/{survivor}"})
    _worklist(ws, [{"topic": "python", "survivor": survivor, "copies": [{"folder": "guidelines/testing/python"}]}])
    (ws / "speciality-map.json").write_text(json.dumps([
        {"speciality": "lang/python", "topic": "cookbook/guidelines/testing/python"},
        {"speciality": "lang/go", "topic": "cookbook/guidelines/testing/go"},
        {"speciality": "lang/own", "topic": f"cookbook/{survivor}"}]), encoding="utf-8")
    want = [{"speciality": "lang/python", "topic": "cookbook/guidelines/testing/python",
             "survivor": f"cookbook/{survivor}",
             "why": "the fold deletes cookbook/guidelines/testing/python: who repoints the speciality "
                    "is the owner's"}]
    assert run(tmp_path)["speciality_points_at_copy"] == want
    assert stage_status.status("testing", ws, tmp_path)["speciality_points_at_copy"] == want
    assert stage_status.status("shipping", ws, tmp_path)["speciality_points_at_copy"] == []


def test_a_fold_from_a_planned_area_whose_plan_omits_it_is_incoming_unplanned(tmp_path):
    # 1.4.26 (M7): the source area has a plan, but it has no row for the
    # fold, or a row that does not merge it into this survivor: listed,
    # never lost between `incoming` and `incoming_unplanned`.
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    survivor = f"guidelines/{AREA}/python"
    area(tmp_path, {"python": f"cookbook/{survivor}"})
    artifact(tmp_path / "cookbook/guidelines/testing/python")
    _worklist(ws, [{"topic": "python", "survivor": survivor, "copies": [{"folder": "guidelines/testing/python"}]},
                   {"topic": "py2", "survivor": survivor, "new_home": "guidelines/planning/data/py2"}])
    plan_of(ws, "testing", [("other", "kept", "cookbook/guidelines/testing/other")])
    plan_of(ws, "planning/data", [("py2", "kept", "cookbook/guidelines/planning/data/py2")])
    rows = run(tmp_path)["incoming_unplanned"]
    assert [(r["via"], r["plan"], r["why"]) for r in rows] == [
        ("new_home", "planning/data", "the planning/data plan lists py2 as kept, not merged into "
                                      f"cookbook/{survivor}"),
        ("copy", "testing", "the testing plan does not list cookbook/guidelines/testing/python: "
                            "no plan row stands behind this fold")]
    plan_of(ws, "testing", [("python", "merged", f"cookbook/{survivor}")])
    plan_of(ws, "planning/data", [("py2", "merged", f"cookbook/{survivor}")])
    assert run(tmp_path)["incoming_unplanned"] == []



def test_a_stale_reference_stops_approval(tmp_path):
    # Fix round 2, R-I-1: an A/reference.json row written before reference
    # format 2 (no stamp, or an older one) is listed in `stale_reference` and
    # stops `next: approve`, as the area must be re-measured first.
    import reference_format
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "approval.md").unlink()
    (d / "reference.json").write_text(json.dumps(
        [{"speciality": "data/indexing", "topic": None, "file": "/x.txt", "format": reference_format.REFERENCE_FORMAT}]))
    s = run(tmp_path)
    assert s["stale_reference"] == [] and s["next"] == "approve"
    (d / "reference.json").write_text(json.dumps([{"speciality": "data/indexing", "topic": None, "file": "/x.txt"}]))
    s = run(tmp_path)
    assert [r["speciality"] for r in s["stale_reference"]] == ["data/indexing"]
    assert s["next"] == "plan" and s["topics"]["rows"]["next"] == "plan"
    assert s["next_why"].startswith(f"stale_reference: 1 row(s) older than reference format {FORMAT}; "), s["next_why"]


def test_a_stale_reference_after_approval_is_named_in_next_why(tmp_path):
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "reference.json").write_text(json.dumps([{"speciality": "data/indexing", "topic": None, "file": "/x.txt"}]))
    s = run(tmp_path)
    assert s["stale_reference"] and s["next_why"].startswith("stale_reference:")


def test_a_stale_reference_holds_an_approved_area_at_plan(tmp_path):
    # Fix round 3, R2-I-1: an approved plan measured on a stale reference is
    # re-measured and re-planned: `next` is plan for the area and each topic,
    # the approval stays on record as history.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    s = run(tmp_path)
    assert s["approval"] == "current" and s["next"] != "plan"
    (d / "reference.json").write_text(json.dumps([{"speciality": "data/indexing", "topic": None, "file": "/x.txt"}]))
    approve(d)          # approved over the stale rows: it still holds at plan
    s = run(tmp_path)
    assert s["approval"] == "current"
    assert s["next"] == "plan" and s["topics"]["rows"]["next"] == "plan", s
    why = s["next_why"]
    # N3-N-1 (1.4.29): plain English, one "and" a clause.
    assert why == (f"stale_reference: 1 row(s) older than reference format {FORMAT}; the plan was measured on a "
                   "stale reference: re-run steps 1.1 to 1.3, then the step-4 checks, then hand the plan back "
                   "to the owner for a new approval (the earlier approval stays on record as history)"), why


def test_a_stale_reference_holds_an_approved_area_whose_rows_all_merged_elsewhere(tmp_path):
    # Fix round 3, R2-I-1: no topic owes a stage here, yet a stale reference
    # still holds the area at `plan` (every area, approved or not).
    cookr_skill(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    d = plan_of(ws, AREA, [("python", "merged", "cookbook/guidelines/testing/python")])
    approve(d)
    assert run(tmp_path)["next"] is None
    (d / "reference.json").write_text(json.dumps([{"speciality": "data/indexing", "topic": None, "file": "/x.txt"}]))
    approve(d)          # approved over the stale rows: it still holds at plan
    s = run(tmp_path)
    assert s["approval"] == "current" and s["next"] == "plan", s
    assert "measured on a stale reference" in s["next_why"], s["next_why"]


def test_a_stale_marked_here_reference_from_run_gaps_is_seen(tmp_path):
    # Fix round 3, R2-M-2: a marked_here reference has no reference.json row;
    # run_gaps lists it stale in A/run_gaps.json, and stage_status reads it.
    import reference_format
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "approval.md").unlink()
    (d / "reference.json").write_text(json.dumps([]))
    (d / "run_gaps.json").write_text(json.dumps({"stale_reference": [
        {"speciality": "building/extra", "file": "/A/reference/building--extra.txt", "format": None,
         "want": reference_format.REFERENCE_FORMAT, "why": "any wording at all",
         "reason": reference_format.NO_WRITER}], "reference_format": reference_format.REFERENCE_FORMAT}))
    s = run(tmp_path)
    assert [r["speciality"] for r in s["stale_reference"]] == ["building/extra"]
    assert s["next"] == "plan"


def test_a_marked_here_stale_row_is_read_by_its_reason_never_its_wording(tmp_path):
    # N3-M-2 (1.4.29): the row is picked by `reason: "no_writer"`. A row
    # whose `why` holds the old phrase but has no such reason is not one, and
    # a reworded `why` changes nothing.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "reference.json").write_text(json.dumps([]))

    def report(*rows):
        (d / "run_gaps.json").write_text(json.dumps({"stale_reference": list(rows), "reference_format": FORMAT}))
        return [r["speciality"] for r in run(tmp_path)["stale_reference"]]
    row = {"speciality": "building/extra", "file": "/x.txt", "format": None, "want": FORMAT}
    assert report({**row, "why": "no speciality_reference.py to rewrite it"}) == [None]
    assert report({**row, "why": "no speciality_reference.py to rewrite it", "reason": "old_format"}) == [None]
    assert report({**row, "why": "reworded: nothing here could write the file again", "reason": "no_writer"}) == [
        "building/extra"]
    assert report({**row, "reason": "no_writer"}) == ["building/extra"]
    assert report() == []


def test_a_report_saved_under_an_older_reference_format_is_stale(tmp_path):
    # N3-I-1 (1.4.29): A/run_gaps.json records the reference format it was
    # measured under. One with none (saved before 1.4.29: a pre-1.4.27 report
    # has no `stale_reference` key either) or a lower one may rest on a stale
    # `marked_here` reference no run listed: one stale row, the area at plan.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "reference.json").write_text(json.dumps([]))
    s = run(tmp_path)
    assert s["stale_reference"] == [] and s["next"] != "plan", s      # a current report: silent
    for saved, fmt in (({"area": AREA, "topics": [], "building": []}, None),                 # pre-1.4.27
                       ({"topics": [], "stale_reference": []}, None),                        # 1.4.27, 1.4.28
                       ({"topics": [], "stale_reference": [], "reference_format": FORMAT - 1}, FORMAT - 1),
                       ({"topics": [], "stale_reference": [], "reference_format": True}, True),
                       ({"topics": [], "stale_reference": [], "reference_format": str(FORMAT)}, str(FORMAT)),
                       (["not", "a", "report"], None)):
        (d / "run_gaps.json").write_text(json.dumps(saved))
        s = run(tmp_path)
        assert len(s["stale_reference"]) == 1, (saved, s["stale_reference"])
        row = s["stale_reference"][0]
        assert (row["speciality"], row["file"], row["format"], row["want"], row["reason"]) == (
            None, str(d / "run_gaps.json"), fmt, FORMAT, "old_report"), row
        assert "run_gaps.py" in row["why"] and "step 1.3" in row["why"], row["why"]
        assert s["next"] == "plan" and s["topics"]["rows"]["next"] == "plan", s
        assert s["next_why"].startswith(f"stale_reference: 1 row(s) older than reference format {FORMAT}; ")
    (d / "run_gaps.json").write_text("{not json")       # unreadable: its format is unknown, so listed
    s = run(tmp_path)
    assert [(r["format"], r["reason"]) for r in s["stale_reference"]] == [(None, "old_report")] and s["next"] == "plan"
    for fmt in (FORMAT, FORMAT + 1):
        (d / "run_gaps.json").write_text(json.dumps({"topics": [], "stale_reference": [], "reference_format": fmt}))
        s = run(tmp_path)
        assert s["stale_reference"] == [] and s["next"] != "plan", s


def test_an_old_report_row_stands_beside_the_reference_rows(tmp_path):
    # N3-I-1: the report row adds to the A/reference.json rows, and an old
    # report's own rows (no `reason`) are covered by the report row.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "reference.json").write_text(json.dumps([{"speciality": "data/indexing", "topic": None, "file": "/x.txt"}]))
    (d / "run_gaps.json").write_text(json.dumps({"stale_reference": [
        {"speciality": "building/extra", "file": "/x.txt", "format": None, "want": FORMAT,
         "why": "no speciality_reference.py to rewrite it"}]}))
    s = run(tmp_path)
    assert [(r["speciality"], r["reason"]) for r in s["stale_reference"]] == [
        ("data/indexing", "old_format"), (None, "old_report")]
    assert s["next_why"].startswith(f"stale_reference: 2 row(s) older than reference format {FORMAT}; ")


def test_a_report_that_lists_a_stale_row_is_stale_until_run_gaps_runs_again(tmp_path):
    # N4-I-1 (1.4.30): run_gaps saves its report even when it lists old_format
    # rows (exit 1). Rewriting A/reference.json without a re-run leaves a
    # measure on the stale reference, stamped current: the report is one stale
    # row, the area at plan, until a fresh run saves a report listing none.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    stamped(d)
    approve(d)
    assert run(tmp_path)["next"] not in ("plan", "approve")
    old = {"speciality": "data/s0", "file": "/s0.txt", "format": None, "want": FORMAT, "why": "w"}
    for rows in ([{**old, "reason": "old_format"}], [old], ["not a row"],
                 [{**old, "reason": "no_writer"}, {**old, "reason": "old_format"}]):
        (d / "run_gaps.json").write_text(json.dumps({"stale_reference": rows, "reference_format": FORMAT}))
        s = run(tmp_path)
        report = [r for r in s["stale_reference"] if r["reason"] == "old_report"]
        assert len(report) == 1, (rows, s["stale_reference"])
        assert (report[0]["speciality"], report[0]["file"], report[0]["format"], report[0]["want"]) == (
            None, str(d / "run_gaps.json"), FORMAT, FORMAT), report
        assert "stale" in report[0]["why"] and "run_gaps.py" in report[0]["why"] and "step 1.3" in report[0]["why"]
        assert "older reference format" not in report[0]["why"], report[0]["why"]
        assert len(s["stale_reference"]) == len([r for r in rows if isinstance(r, dict)
                                                 and r.get("reason") == "no_writer"]) + 1
        assert s["next"] == "plan" and s["topics"]["rows"]["next"] == "plan", s
    for odd in ({"a": 1}, "x", 3, True):          # N5-M-1 (1.4.31): not a list, so what it listed is unknown
        (d / "run_gaps.json").write_text(json.dumps({"stale_reference": odd, "reference_format": FORMAT}))
        s = run(tmp_path)
        assert [(r["reason"], r["format"]) for r in s["stale_reference"]] == [("old_report", FORMAT)], (odd, s)
        assert s["next"] == "plan", (odd, s)
    for clean in ({"stale_reference": []}, {}, {"stale_reference": None}):     # lists none: nothing is stale
        (d / "run_gaps.json").write_text(json.dumps({**clean, "reference_format": FORMAT}))
        s = run(tmp_path)
        assert s["stale_reference"] == [] and s["next"] not in ("plan", "approve"), (clean, s)


def test_an_approval_names_the_reference_it_was_given_on(tmp_path):
    # N4-I-2 (1.4.30, ruling): the approval line carries `reference-hash`, the
    # git hash-object of A/reference.json. Any rewrite of the rows changes
    # the hash, so the plan goes back to the owner with nobody remembering to.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    stamped(d)
    approve(d)
    s = run(tmp_path)
    assert (s["approval"], s["approval_why"]) == ("current", None)
    assert s["reference_hash"] == stage_status.git_blob_hash(d / "reference.json")
    assert "reference_format" not in s
    assert s["next"] not in ("plan", "approve")
    stamped(d, 2)                                  # the rows are rewritten; the plan text is unchanged
    s = run(tmp_path)
    assert (s["approval"], s["approval_why"]) == ("stale", "reference_hash"), s
    assert s["next"] == "approve" and s["topics"]["rows"]["next"] == "approve"
    assert s["next_why"] == ("the approval does not name A/reference.json as it is now (no `reference-hash`, or the "
                             "file changed since, or it is missing): record a new approval naming the plan's hash "
                             "and `reference-hash <reference_hash>` on one line (the earlier approval stays on "
                             "record as history)"), s["next_why"]
    approve(d, mode="a")                           # the new approval, appended below the old one
    assert len((d / "approval.md").read_text().splitlines()) == 2
    s = run(tmp_path)
    assert (s["approval"], s["approval_why"]) == ("current", None) and s["next"] not in ("plan", "approve")
    stamped(d)                                     # back to the first text: the first line approves it again
    assert run(tmp_path)["approval"] == "current"
    (d / "reference.json").unlink()
    s = run(tmp_path)
    assert (s["approval"], s["approval_why"], s["reference_hash"]) == ("stale", "reference_hash", None)


def test_an_approval_line_with_no_reference_hash_is_stale(tmp_path):
    # N4-I-2, N4-M-1: the 1.4.29 line (`reference-format <N>`) approves
    # nothing whatever follows the word, `2.0` and `2abc` included, and
    # `approval_why` says so; a line with neither names no reference.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    for n in (FORMAT, FORMAT + 1, f"{FORMAT}.0", f"{FORMAT}abc", f": {FORMAT}"):
        for word in ("reference-format", "reference format", "Reference-Format"):
            approve(d, tail=f", {word} {n}")
            s = run(tmp_path)
            assert (s["approval"], s["approval_why"]) == ("stale", "reference_format"), (word, n, s)
            assert s["next"] == "approve"
    assert s["next_why"] == ("the approval records `reference-format`, which approves nothing since 1.4.30: record "
                             "a new approval naming the plan's hash and `reference-hash <reference_hash>` on one "
                             "line (the earlier approval stays on record as history)"), s["next_why"]
    approve(d, tail="")
    s = run(tmp_path)
    assert (s["approval"], s["approval_why"]) == ("stale", "reference_hash"), s
    approve(d, tail=", preference-format 2")
    assert run(tmp_path)["approval_why"] == "reference_hash"
    ref = stage_status.git_blob_hash(d / "reference.json")
    approve(d, tail=f", reference-format {FORMAT}, reference-hash {ref}")      # both: the hash decides
    assert run(tmp_path)["approval"] == "current"
    approve(d, tail=f", reference-format {FORMAT}, reference-hash {'0' * 40}")
    assert run(tmp_path)["approval_why"] == "reference_hash"
    approve(d, tail=f", reference-format {FORMAT}")
    approve(d, mode="a")                                                    # history above, the new line below
    assert run(tmp_path)["approval"] == "current"


def test_the_reference_hash_counts_only_on_the_line_naming_the_plans_hash(tmp_path):
    # N4-I-2: a hash recorded for another plan text, or on a line of its own,
    # approves nothing; neither does part of a hash, or a longer one.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    h = stage_status.git_blob_hash(d / "area-plan.md")
    ref = stage_status.git_blob_hash(d / "reference.json")
    record = d / "approval.md"
    record.write_text(f"- plan: {'0' * 40}, reference-hash {ref}\n- plan: {h}\n")
    assert run(tmp_path)["approval_why"] == "reference_hash"
    record.write_text(f"- plan: {h}\n- reference-hash: {ref}\n")
    assert run(tmp_path)["approval_why"] == "reference_hash"
    record.write_text(f"- plan: {'0' * 40}, reference-hash {ref}\n")
    assert run(tmp_path)["approval_why"] == "plan_changed"
    for spelling in (f"reference-hash {ref}", f"reference-hash: {ref}", f"reference hash {ref}",
                     f"Reference-Hash: {ref.upper()}", f"reference-hash `{ref}`"):
        record.write_text(f"- plan: {h}, {spelling}\n")
        assert run(tmp_path)["approval"] == "current", spelling
    for wrong in (f"reference-hash {ref[:39]}", f"reference-hash {ref}0", f"reference-hash 0{ref}",
                  f"preference-hash {ref}", f"reference-hash {h}", f"reference-hash is {ref}", ref):
        record.write_text(f"- plan: {h}, {wrong}\n")
        s = run(tmp_path)
        assert (s["approval"], s["approval_why"]) == ("stale", "reference_hash"), wrong
    record.write_text(f"- plan: {h}, reference-hash {'0' * 40}, reference-hash {ref}\n")
    assert run(tmp_path)["approval"] == "current"


def test_the_reference_hash_is_never_printed_over_a_stale_reference(tmp_path):
    # N4-I-2 (ruling): stage_status prints the hash for the owner to copy, and
    # prints none while any stale row stands, so nobody approves over one.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    stamped(d, fmt=None)
    s = run(tmp_path)
    assert s["stale_reference"] and s["reference_hash"] is None, s
    stamped(d)
    assert run(tmp_path)["reference_hash"] == stage_status.git_blob_hash(d / "reference.json")
    (d / "run_gaps.json").write_text(json.dumps({"topics": []}))            # an old report: one stale row
    s = run(tmp_path)
    assert [r["reason"] for r in s["stale_reference"]] == ["old_report"] and s["reference_hash"] is None
    report(d)
    (d / "approval.md").unlink()                    # not approved yet: the hash is there to copy
    assert run(tmp_path)["reference_hash"] == stage_status.git_blob_hash(d / "reference.json")


def test_a_recorded_format_is_a_number_never_true(monkeypatch):
    # `true` equals 1 in Python: a report saying "reference_format": true
    # must not read as current, whatever the current format is.
    import reference_format
    monkeypatch.setattr(reference_format, "REFERENCE_FORMAT", 1)
    assert reference_format.is_current(1) is True
    assert reference_format.is_current(True) is False
    assert reference_format.is_current("1") is False
    assert reference_format.is_current(None) is False


def test_the_approval_says_why_it_is_not_current(tmp_path):
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "approval.md").unlink()
    s = run(tmp_path)
    assert (s["approval"], s["approval_why"]) == ("missing", "no_record")
    assert s["next_why"] == "the plan has no approval record"
    approve(d)
    with open(d / "area-plan.md", "a", encoding="utf-8") as f:
        f.write("\nedited\n")
    s = run(tmp_path)
    assert (s["approval"], s["approval_why"]) == ("stale", "plan_changed")
    assert s["next_why"] == "the plan changed since its approval"


def test_a_reference_that_cannot_be_read_as_rows_is_stale(tmp_path):
    # N5-I-1 (1.4.31): invalid JSON, a non-list, or a list holding a non-dict
    # is one stale row. The area holds at plan, no hash is printed, and an
    # approval naming the broken file's hash is not current.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    ref = d / "reference.json"
    good = {"speciality": "data/s0", "topic": None, "file": "/s0.txt", "format": FORMAT}
    for text in ("{bad", "", "{}", '"x"', "3", "null", '["x"]', json.dumps([good, "x"]), json.dumps([good, None]),
                 json.dumps([[good]])):
        ref.write_text(text)
        approve(d)                                  # the hash of the broken file, worked out by hand
        s = run(tmp_path)
        assert [(r["speciality"], r["file"], r["format"], r["want"], r["reason"]) for r in s["stale_reference"]] == [
            (None, str(ref), None, FORMAT, "unreadable_reference")], (text, s["stale_reference"])
        why = s["stale_reference"][0]["why"]
        assert "cannot be read" in why and "step 1.1" in why, why
        assert s["reference_hash"] is None, text
        assert (s["approval"], s["approval_why"]) == ("stale", "reference_hash"), (text, s)
        assert s["next"] == "plan" and s["topics"]["rows"]["next"] == "plan", (text, s)
    ref.write_text(json.dumps([{"speciality": "data/s0", "file": "/s0.txt"}, "x"]))   # beside an unstamped row
    assert [r["reason"] for r in run(tmp_path)["stale_reference"]] == ["old_format", "unreadable_reference"]
    for text in ("[]", json.dumps([good])):          # a list of rows, each stamped: readable
        ref.write_text(text)
        approve(d)
        s = run(tmp_path)
        assert s["stale_reference"] == [] and s["approval"] == "current", (text, s)
        assert s["reference_hash"] == stage_status.git_blob_hash(ref)
    ref.unlink()                                     # a plan and no file: step 1.1 was skipped
    assert [r["reason"] for r in run(tmp_path)["stale_reference"]] == ["unreadable_reference"]


def test_an_approval_given_over_a_stale_reference_goes_plan_then_approve(tmp_path):
    # N4-I-2: the hole in 1.4.29. An approval recorded while the rows were
    # still unstamped (the hash worked out by hand) holds at plan; once the
    # rows are rewritten and re-measured the file differs, so `next` is
    # approve even though the plan text never changed.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    stamped(d, fmt=None)
    approve(d)
    s = run(tmp_path)
    assert (s["approval"], s["next"]) == ("current", "plan"), s
    stamped(d)
    s = run(tmp_path)
    assert (s["approval"], s["approval_why"], s["next"]) == ("stale", "reference_hash", "approve"), s
    approve(d, mode="a")
    s = run(tmp_path)
    assert s["approval"] == "current" and s["next"] not in ("plan", "approve")

def test_a_broken_reference_beside_an_unmeasured_file_is_stale_not_a_crash(tmp_path):
    # A real area also has A/unmeasured.json, so run_gaps.measures reads the
    # rows (stale_gaps): a string, number or list of non-dicts must hold the
    # area at plan, never raise.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "unmeasured.json").write_text(json.dumps({"building": []}))
    ref = d / "reference.json"
    good = {"speciality": "data/s0", "topic": None, "file": "/s0.txt", "format": FORMAT}
    for text in ('"x"', "3", "null", "{}", '["x"]', json.dumps([good, "x"]), json.dumps([[good]])):
        ref.write_text(text)
        s = run(tmp_path)
        assert [r["reason"] for r in s["stale_reference"]] == ["unreadable_reference"], (text, s["stale_reference"])
        assert s["next"] == "plan" and s["reference_hash"] is None, (text, s)
        assert s["stale_gaps"] == [], (text, s["stale_gaps"])


def test_a_plan_with_no_reference_file_holds_at_plan(tmp_path):
    # Step 1.1 always writes A/reference.json ([] for an area with no
    # speciality), so a plan without one skipped it: hold, never approve.
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    approve(d)
    (d / "reference.json").unlink()
    s = run(tmp_path)
    assert [r["reason"] for r in s["stale_reference"]] == ["unreadable_reference"], s["stale_reference"]
    assert "step 1.1" in s["stale_reference"][0]["why"]
    assert s["next"] == "plan" and s["reference_hash"] is None, s


def test_no_plan_and_no_reference_file_says_only_no_plan(tmp_path):
    # Before step 1.1 nothing is stale: the plan step writes both.
    d = tmp_path / "docs" / "grow-cookbook" / "areas" / AREA
    d.mkdir(parents=True)
    s = run(tmp_path)
    assert s["stale_reference"] == [] and s["next"] == "plan" and s["next_why"] == "no area-plan.md yet", s


def test_next_why_names_an_unreadable_reference_not_an_old_format(tmp_path):
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "reference.json").write_text("{bad")
    why = run(tmp_path)["next_why"]
    assert why.startswith("stale_reference: A/reference.json cannot be read as rows (re-run step 1.1); "), why
    (d / "reference.json").write_text(json.dumps([{"speciality": "data/s0", "file": "/s0.txt"}, "x"]))
    why = run(tmp_path)["next_why"]
    assert why.startswith("stale_reference: 2 row(s) (old_format, unreadable_reference); "), why


# ---- 1.4.33 (gap-fix round 8: G94-G121) ----

def test_an_r9_file_not_measured_on_the_reference_as_it_is_holds_the_area_at_plan(tmp_path):
    # G94 (Critical): an approved area whose R9 measure predates its reference
    # goes back to plan, named in next_why, until the R9 file is re-run and stamped.
    import r9_stamp
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    ref = d / "reference" / "data--x.txt"
    ref.parent.mkdir()
    ref.write_text("Index every key.\n")
    f = d / "gaps" / "new-rows.json"
    f.parent.mkdir()
    (d / "s").mkdir()
    (d / "s" / "artifact.json").write_text('{"name": "s"}')
    f.write_text(json.dumps({"folder": str(d / "s"), "references": [{"file": str(ref), "sentences": 1, "held": 0,
                                                                "lacking": 1, "lacking_sentences": ["x"]}]}))
    s = run(tmp_path)
    assert [(r["file"], r["reason"]) for r in s["r9_stale"]] == [("new-rows.json", "no_hash"),
                                                                  ("new-rows.json", "folder_no_hash")]
    assert s["next"] == "plan" and "r9_stale: 1 R9 file(s)" in s["next_why"] and "(2 row(s)" in s["next_why"], s
    assert r9_stamp.main([str(f)]) == 0
    s = run(tmp_path)
    assert s["r9_stale"] == [] and "r9_stale" not in s["next_why"]
    ref.write_text("Index every foreign key.\n")
    s = run(tmp_path)
    assert [r["reason"] for r in s["r9_stale"]] == ["changed"] and s["next"] == "plan"
    assert r9_stamp.main([str(f)]) == 0
    (d / "s" / "artifact.json").write_text('{"name": "s", "summary": "edited"}')        # review I2
    s = run(tmp_path)
    assert [r["reason"] for r in s["r9_stale"]] == ["folder_changed"] and s["next"] == "plan"


def test_an_r9_file_written_relative_to_the_repo_is_read_there(tmp_path):
    # review I2/M6 (fix round 1): stage_status passes --repo to r9_stale, so a
    # survivor folder written relative to the repo is found, not "missing".
    import r9_stamp
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    survivor = tmp_path / "cookbook" / "guidelines" / AREA / "rows"
    survivor.mkdir(parents=True)
    (survivor / "artifact.json").write_text('{"name": "rows"}')
    ref = d / "reference" / "data--x.txt"
    ref.parent.mkdir()
    ref.write_text("Index every key.\n")
    f = d / "gaps" / "new-rows.json"
    f.parent.mkdir()
    f.write_text(json.dumps({"folder": f"cookbook/guidelines/{AREA}/rows", "references": [
        {"file": str(ref), "sentences": 1, "held": 0, "lacking": 1, "lacking_sentences": ["x"]}]}))
    assert r9_stamp.main([str(f), "--repo", str(tmp_path)]) == 0
    assert run(tmp_path)["r9_stale"] == []
    (survivor / "artifact.json").write_text('{"name": "rows", "summary": "edited"}')
    assert [r["reason"] for r in run(tmp_path)["r9_stale"]] == ["folder_changed"]


def test_a_plan_with_no_saved_report_is_held_at_plan(tmp_path):
    # G99 (1.4.33): a plan beside no A/run_gaps.json (saved before 1.4.26, or
    # never run) has figures no saved report vouches for: one old_report row,
    # the area at plan; no plan yet, no row.
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    assert run(tmp_path)["stale_reference"] == []
    (d / "run_gaps.json").unlink()
    s = run(tmp_path)
    assert [(r["file"], r["format"], r["reason"]) for r in s["stale_reference"]] == [
        (str(d / "run_gaps.json"), None, "old_report")], s["stale_reference"]
    assert "no A/run_gaps.json" in s["stale_reference"][0]["why"] and "run_gaps.py" in s["stale_reference"][0]["why"]
    assert s["next"] == "plan" and s["reference_hash"] is None
    (d / "area-plan.md").unlink()
    assert run(tmp_path)["stale_reference"] == []


def _plan_text(d: Path) -> str:
    return (d / "area-plan.md").read_text(encoding="utf-8")


def test_plan_sections_lists_each_required_heading_missing_misspelled_or_out_of_order(tmp_path):
    # G97 (1.4.33): every section step 3 requires, spelt and ordered as it says;
    # any row holds the area at plan, approved or not.
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    s = run(tmp_path)
    assert s["plan_sections"] == [] and s["next"] == "research", s["next_why"]
    good = _plan_text(d)
    (d / "area-plan.md").write_text(good.replace(f"## Owner questions\n\n{OWNER_Q}\n", ""), encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert [(r["section"], r["found"]) for r in s["plan_sections"]] == [("Owner questions", None)]
    assert "missing" in s["plan_sections"][0]["why"]
    assert s["next"] == "plan" and s["next_why"].startswith("plan_sections: 1 row(s)"), s["next_why"]
    (d / "area-plan.md").write_text(good.replace("## Step-4 re-check", "## Step 4 re-check"), encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert [(r["section"], r["found"]) for r in s["plan_sections"]] == [("Step-4 re-check", "Step 4 re-check")]
    assert "misspelled" in s["plan_sections"][0]["why"] and s["next"] == "plan"
    swapped = good.replace("## Gaps\n\ng\n\n## Missing subjects\n\nNone.\n\n",
                           "## Missing subjects\n\nNone.\n\n## Gaps\n\ng\n\n")
    (d / "area-plan.md").write_text(swapped, encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert [r["section"] for r in s["plan_sections"]] == ["Missing subjects"]
    assert "out of order" in s["plan_sections"][0]["why"] and s["next"] == "plan"
    # a heading inside a fenced block is no section
    (d / "area-plan.md").write_text(good.replace("## Overlaps\n\no\n", "```\n## Overlaps\n```\n"),
                                    encoding="utf-8")
    approve(d)
    assert [(r["section"], r["found"]) for r in run(tmp_path)["plan_sections"]] == [("Overlaps", None)]


def test_a_missing_subject_carried_nowhere_is_a_plan_sections_row(tmp_path):
    # G105 (1.4.33): a subject whose bold lead phrase is in no Research
    # question holds the area at plan.
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    good = _plan_text(d)
    plan = good.replace("## Missing subjects\n\nNone.\n", "## Missing subjects\n\n1. **Hosting model**: x.\n"
                        "2. **Identity architecture**: y.\n").replace(
        "## Research questions\n\nq\n", "## Research questions\n\n- rows: which **hosting model** fits?\n")
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert [(r["section"], r["item"]) for r in s["plan_sections"]] == [("Missing subjects", "Identity architecture")]
    assert "carried nowhere" in s["plan_sections"][0]["why"] and s["next"] == "plan"
    (d / "area-plan.md").write_text(plan.replace("which **hosting model** fits?",
                                                 "which **hosting model** fits? **identity architecture**?"),
                                    encoding="utf-8")
    approve(d)
    assert run(tmp_path)["plan_sections"] == []


def _subject_rows(tmp_path, subjects: str, research: str, owner: str = "None.\n") -> list[tuple[str, str]]:
    """plan_sections' Missing-subjects rows, (item, why), for a plan with these three sections."""
    body = "".join(f"## {h}\n\nx\n\n" for h in ("Topics", "Gaps"))
    body += f"## Missing subjects\n\n{subjects}\n## Overlaps\n\nx\n\n## Proposed topics\n\nx\n\n"
    body += f"## Research questions\n\n{research}\n## Owner questions\n\n{owner}\n## Step-4 re-check\n\nr\n"
    plan = tmp_path / "area-plan.md"
    plan.write_text("# Plan\n\n" + body, encoding="utf-8")
    return [(r["item"], r["why"]) for r in stage_status.plan_sections(plan) if r["section"] == "Missing subjects"]


def test_a_subject_is_carried_by_its_bold_lead_phrase_verbatim_in_research_questions(tmp_path):
    # Fix round 1 (1.4.34, review I1): verbatim, case and punctuation aside
    # (G127, 1.4.36: as a whole bold span).
    rows = _subject_rows(tmp_path, "1. **Long-running operations**: polling.\n",
                         "1. rows: how are **long running operations** polled?\n")
    assert rows == []


def test_a_paraphrased_subject_is_flagged(tmp_path):
    rows = _subject_rows(tmp_path, "1. **Bulk loading and ETL**: x.\n", "1. data: how is bulk loading done?\n")
    assert [i for i, _ in rows] == ["Bulk loading and ETL"] and "carried nowhere" in rows[0][1]


def test_a_subject_named_only_under_owner_questions_is_flagged(tmp_path):
    rows = _subject_rows(tmp_path, "1. **Caching layers**: x.\n", "1. data: q?\n",
                         "1. Should **caching layers** become a topic?\n")
    assert [i for i, _ in rows] == ["Caching layers"]
    assert "named only under Owner questions" in rows[0][1] and "Research question" in rows[0][1]


def test_carried_no_host_needs_an_owner_question_too(tmp_path):
    subj = "1. **Flag cleanup**: x.\n"
    research = "1. rows: **flag cleanup** (carried, no host)\n2. other: q?\n"
    rows = _subject_rows(tmp_path, subj, research)
    assert [i for i, _ in rows] == ["Flag cleanup"] and "not under Owner questions" in rows[0][1]
    assert _subject_rows(tmp_path, subj, research, "1. A new topic for **flag cleanup**?\n") == []
    # "carried, no host" in another item of the same section is not this subject's mark
    assert _subject_rows(tmp_path, subj, "1. rows: **flag cleanup**?\n2. other: x (carried, no host)\n") == []


def test_a_no_host_mark_on_a_nested_sub_bullet_counts_with_its_subject(tmp_path):
    # Fix round 2 (1.4.35, re-review Minor 1): the mark belongs to the top-level
    # item that holds the phrase, at any depth below it; never to a sibling item.
    subj = "1. **Flag cleanup**: x.\n"
    nested = "1. rows: how is **flag cleanup** scheduled?\n   - carried, no host\n2. other: q?\n"
    rows = _subject_rows(tmp_path, subj, nested)
    assert [i for i, _ in rows] == ["Flag cleanup"] and "not under Owner questions" in rows[0][1]
    assert _subject_rows(tmp_path, subj, nested, "1. A new topic for **flag cleanup**?\n") == []
    deeper = "1. rows: x\n   - flag cleanup?\n     - carried, no host\n"
    assert [i for i, _ in _subject_rows(tmp_path, subj, deeper)] == ["Flag cleanup"]
    phrase_nested = "1. rows: x (carried, no host)\n   - flag cleanup?\n"
    assert [i for i, _ in _subject_rows(tmp_path, subj, phrase_nested)] == ["Flag cleanup"]
    sibling = "1. rows: **flag cleanup**?\n2. other: y\n   - carried, no host\n"
    assert _subject_rows(tmp_path, subj, sibling) == []
    under_heading = "### rows\n\n1. flag cleanup?\n\n### other\n\n- carried, no host\n"
    assert _subject_rows(tmp_path, subj, under_heading) == []


def test_a_bold_lead_of_non_ascii_letters_is_matched_and_never_skipped(tmp_path):
    # Fix round 2 (1.4.35, re-review Minor 2): non-ASCII letters stay in the key;
    # a bold lead with no letter or digit at all is its own row, never skipped.
    assert _subject_rows(tmp_path, "1. **Ünïcode façades**: x.\n", "1. rows: **ünïcode façades**?\n") == []
    rows = _subject_rows(tmp_path, "1. **Ünïcode façades**: x.\n", "1. rows: **unicode facades**?\n")
    assert [i for i, _ in rows] == ["Ünïcode façades"] and "carried nowhere" in rows[0][1]
    assert [i for i, _ in _subject_rows(tmp_path, "1. **日本語**: x.\n", "1. rows: other?\n")] == ["日本語"]
    assert _subject_rows(tmp_path, "1. **日本語**: x.\n", "1. rows: **日本語**?\n") == []
    rows = _subject_rows(tmp_path, "1. **—**: x.\n", "1. rows: anything\n")
    assert [i for i, _ in rows] == ["—"] and "no letter or digit" in rows[0][1]


def test_every_subject_without_a_bold_lead_is_a_no_bold_lead_row(tmp_path):
    rows = _subject_rows(tmp_path, "1. Identity architecture\n- audit trails\n* **Sharding**: x.\n",
                         "1. rows: identity architecture? audit trails? **sharding**?\n")
    assert [i for i, _ in rows] == ["Identity architecture", "audit trails"]
    assert all("no bold lead phrase" in w for _, w in rows)


def test_research_and_owner_questions_are_searched_apart(tmp_path):
    # a phrase must never match across the join of the two sections
    rows = _subject_rows(tmp_path, "1. **Data sync**: x.\n", "1. rows: data\n", "sync: q?\n")
    assert [i for i, _ in rows] == ["Data sync"]


# ---- gapfix9 (1.4.36) ----

def test_a_bold_span_in_a_loose_paragraph_is_named_but_not_carried(tmp_path):
    # Fix round 1 (gapfix9 review 5): a bold span carries only inside a list
    # item; in a loose paragraph under Research questions it is named only.
    subj = "1. **Long-running operations**: polling.\n"
    rows = _subject_rows(tmp_path, subj, "How are **long-running operations** polled?\n\n1. rows: q?\n")
    assert [i for i, _ in rows] == ["Long-running operations"] and "named but not carried" in rows[0][1], rows
    assert _subject_rows(tmp_path, subj, "1. rows: how are **long-running operations** polled?\n") == []


def test_a_plain_mention_is_named_but_not_carried_and_a_bold_span_or_whole_item_carries(tmp_path):
    # G127 (1.4.36): a carry is the bold lead phrase as a whole bold span, or a
    # whole list item; a plain mention is "named but not carried".
    subj = "1. **Long-running operations**: polling.\n"
    rows = _subject_rows(tmp_path, subj, "1. rows: how are long running operations polled?\n")
    assert [i for i, _ in rows] == ["Long-running operations"] and "named but not carried" in rows[0][1]
    assert _subject_rows(tmp_path, subj, "1. rows: how are **long-running operations** polled?\n") == []
    assert _subject_rows(tmp_path, subj, "1. rows: q?\n   - Long-running operations\n") == []


def test_a_phrase_only_inside_a_longer_phrase_is_not_carried(tmp_path):
    subj = "1. **Hooks**: x.\n"
    rows = _subject_rows(tmp_path, subj, "1. rows: how are **git hooks and triggers** set up?\n")
    assert [i for i, _ in rows] == ["Hooks"] and "carried" in rows[0][1]
    rows = _subject_rows(tmp_path, subj, "1. rows: **hooks**? \n", "1. Hooks for **pre-commit hooks**?\n")
    assert rows == []


def test_a_phrase_in_a_heading_is_not_carried(tmp_path):
    subj = "1. **Image optimization**: x.\n"
    rows = _subject_rows(tmp_path, subj, "### **Image optimization**\n\n1. rows: q?\n")
    assert [i for i, _ in rows] == ["Image optimization"]
    rows = _subject_rows(tmp_path, subj, "### Image optimization\n\n1. rows: q?\n")
    assert [i for i, _ in rows] == ["Image optimization"]


def test_a_bold_led_paragraph_and_a_second_bold_phrase_are_each_checked(tmp_path):
    # G126 (1.4.36): a bold-led paragraph in Missing subjects is a row ("not a
    # list item"); a second bold phrase in one item is checked as a subject;
    # a trailing `.` or `:` is never part of the reported item.
    subj = "1. **Caching.** x, and **Sharding**: y.\n\n**Audit trails**: z.\n"
    rows = _subject_rows(tmp_path, subj, "1. rows: **caching**?\n")
    assert [i for i, _ in rows] == ["Sharding", "Audit trails"], rows
    assert "not a list item" in rows[1][1]
    rows = _subject_rows(tmp_path, "1. **Caching:** x.\n", "1. rows: q?\n")
    assert [i for i, _ in rows] == ["Caching"]


def test_every_topic_without_a_research_bar_owner_question_is_a_row(tmp_path):
    # G128 (1.4.36): one plan_sections row per topic of the Topics table that
    # no "research bar" Owner question names; one naming every topic covers all.
    body = "## Topics\n\n| Topic | Artifact |\n|---|---|\n| `swift-testing` | x |\n| **ui-tests** | y |\n\n"
    body += "".join(f"## {h}\n\nx\n\n" for h in PLAN_SECTIONS_MIDDLE)
    plan = tmp_path / "area-plan.md"

    def rows(owner: str) -> list:
        plan.write_text(f"# Plan\n\n{body}## Owner questions\n\n{owner}\n## Step-4 re-check\n\nr\n", encoding="utf-8")
        return [(r["section"], r["item"]) for r in stage_status.plan_sections(plan) if r.get("item")]
    assert rows("None.\n") == [("Owner questions", "swift-testing"), ("Owner questions", "ui-tests")]
    assert rows("1. Research bar for swift-testing: peer-reviewed?\n") == [("Owner questions", "ui-tests")]
    assert rows("1. **Research bar.** One bar for every topic: vendor docs?\n") == []
    assert rows("1. swift-testing: ui-tests too?\n") == [("Owner questions", "swift-testing"),
                                                        ("Owner questions", "ui-tests")]


def _bar_plan(tmp_path, topics: str, proposed: str, owner: str = "None.\n") -> list[tuple]:
    """plan_sections' research-bar rows, (section, item, why), for a plan with these sections."""
    body = f"## Topics\n\n{topics}\n## Gaps\n\nx\n\n## Missing subjects\n\nNone.\n\n## Overlaps\n\nx\n\n"
    body += f"## Proposed topics\n\n{proposed}\n## Research questions\n\nq\n\n"
    body += f"## Owner questions\n\n{owner}\n## Step-4 re-check\n\nr\n"
    plan = tmp_path / "area-plan.md"
    plan.write_text("# Plan\n\n" + body, encoding="utf-8")
    return [(r["section"], r.get("item"), r["why"]) for r in stage_status.plan_sections(plan)
            if "research-bar" in r["why"] or "research bar" in r["why"]]


def test_a_list_form_topics_section_falls_back_to_proposed_topics_then_one_row(tmp_path):
    # Fix round 1 (gapfix9 review I2): Topics with no table reads Proposed
    # topics' Topic column; with neither, one row, never a silent pass.
    listed = "- swift-testing\n- ui-tests\n"
    proposed = ("| Topic | Action | Artifact |\n|---|---|---|\n| swift-testing | kept | `a` |\n"
                "| `ui-tests` | new | `b` |\n")
    assert [i for _, i, _ in _bar_plan(tmp_path, listed, proposed)] == ["swift-testing", "ui-tests"]
    assert [i for _, i, _ in _bar_plan(tmp_path, listed, proposed, "1. Research bar for ui-tests: x?\n")] == [
        "swift-testing"]
    rows = _bar_plan(tmp_path, listed, "None.\n")
    assert len(rows) == 1 and "Topics lists no table the research-bar check can read" in rows[0][2], rows
    assert _bar_plan(tmp_path, listed, "None.\n", "1. Research bar for every topic: x?\n") == []


def test_every_topic_with_an_exception_or_a_name_after_it_does_not_cover_every_topic(tmp_path):
    # Fix round 1 (gapfix9 review I2): "every/each/all topics" covers all only
    # when no topic name and no except / but / other than follows it; a name
    # after the exception word is never counted as asked.
    table = "| Topic | Artifact |\n|---|---|\n| swift-testing | x |\n| ui-tests | y |\n"
    both = ["swift-testing", "ui-tests"]
    for q in ("1. Research bar for all topics except ui-tests: vendor docs?\n",
              "1. Research bar for every topic but swift-testing: vendor docs?\n",
              "1. Research bar for each topic other than ui-tests: vendor docs?\n"):
        assert [i for _, i, _ in _bar_plan(tmp_path, table, "x\n", q)] == both, q
    q = "1. Research bar for every topic: swift-testing peer-reviewed?\n"
    assert [i for _, i, _ in _bar_plan(tmp_path, table, "x\n", q)] == ["ui-tests"]
    assert _bar_plan(tmp_path, table, "x\n", "1. Research bar for every topic: vendor docs?\n") == []


def test_a_topic_name_annotated_in_parentheses_matches_its_bare_name(tmp_path):
    # Fix round 1 (gapfix9 sweep): Topics rows such as "test-adequacy (new)"
    # are named in questions without the note; the note is not the name.
    table = ("| Topic | Artifact |\n|---|---|\n| test-adequacy (new) | x |\n"
             "| ui-composition-and-state (new, proposed here) | y |\n| ui-tests | z |\n")
    q = "1. Research bar per topic: test-adequacy, ui-composition-and-state: no escalation.\n"
    assert [i for _, i, _ in _bar_plan(tmp_path, table, "x\n", q)] == ["ui-tests"]


def test_a_copies_only_topic_owes_no_research_bar_question(tmp_path):
    # Fix round 1 (gapfix9 review 6): a topic merged into another area is run
    # under the survivor's plan, whose research bar governs: no row for it.
    d, _ = _copies_area(tmp_path)
    fresh = f"| fresh | kept | `cookbook/guidelines/{AREA}/fresh` | why |\n"
    plan = _plan_text(d).replace(OWNER_Q, "None.\n").replace("| rows | merged |", fresh + "| rows | merged |")
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert [r.get("item") for r in s["plan_sections"]] == ["fresh"], s["plan_sections"]


PLAN_SECTIONS_MIDDLE = ("Gaps", "Missing subjects", "Overlaps", "Proposed topics", "Research questions")


def test_a_research_bar_row_holds_the_area_at_plan(tmp_path):
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    plan = _plan_text(d).replace(OWNER_Q, "None.\n").replace("## Topics\n\nt\n", "## Topics\n\n| Topic | x |\n|---|---|\n| rows | y |\n")
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert [r.get("item") for r in s["plan_sections"]] == ["rows"] and s["next"] == "plan"
    assert "research bar" in s["plan_sections"][0]["why"]
    (d / "area-plan.md").write_text(plan.replace("## Owner questions\n\nNone.\n",
                                                 "## Owner questions\n\n1. Research bar, rows: x?\n"), encoding="utf-8")
    approve(d)
    assert run(tmp_path)["plan_sections"] == []


def _copies_area(tmp_path: Path) -> tuple[Path, Path]:
    """An area whose plan merges one copy into a survivor elsewhere, with a worklist."""
    cookr_skill(tmp_path)
    surv = "cookbook/guidelines/implementing/other/rows"
    d = area(tmp_path, {"rows": surv})
    plan = _plan_text(d).replace("| rows | kept |", "| rows | merged |")
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    artifact(tmp_path / surv)
    artifact(tmp_path / f"cookbook/guidelines/{AREA}/rows")
    ws = tmp_path / "docs" / "grow-cookbook"
    (ws / "worklist.json").write_text(json.dumps({"batches": []}), encoding="utf-8")
    approve(d)
    return d, tmp_path / surv


def test_a_missing_or_stale_copy_check_digest_holds_the_area_at_plan(tmp_path):
    # G133 (1.4.36): the plan records copy_check.py's digest under Overlaps;
    # a missing or changed one is a stale_copy_check row, held at plan.
    import copy_check
    d, surv = _copies_area(tmp_path)
    ws = tmp_path / "docs" / "grow-cookbook"
    s = run(tmp_path)
    assert [r["recorded"] for r in s["stale_copy_check"]] == [None] and s["next"] == "plan", s["stale_copy_check"]
    line = copy_check.digest(copy_check.check(AREA, ws, tmp_path))
    assert line.startswith(f"copy_check.py {AREA}: copies 1; ") and "; result " in line
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Overlaps\n\no\n", f"## Overlaps\n\no\n\n{line}\n"),
                                    encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert s["stale_copy_check"] == [] and s["next"] != "plan", s["next_why"]
    (surv / "rules.md").write_text("- **changed**: x\n", encoding="utf-8")
    s = run(tmp_path)
    assert [r["recorded"] for r in s["stale_copy_check"]] == [line] and s["next"] == "plan"
    assert s["stale_copy_check"][0]["current"] != line and "stale_copy_check" in s["next_why"]


def test_an_area_with_no_copies_and_no_worklist_owes_no_copy_check_digest(tmp_path):
    cookr_skill(tmp_path)
    area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    assert run(tmp_path)["stale_copy_check"] == []


def _other_plan(tmp_path: Path, name: str, text: str = "# Other\n") -> Path:
    p = tmp_path / "docs" / "grow-cookbook" / "areas" / name / "area-plan.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_a_cited_plan_changed_since_its_recorded_hash_is_listed_never_held(tmp_path):
    # G134 (1.4.36): other_plans_changed, advisory: each other plan this plan
    # cites whose hash differs from the one in Step-4 re-check, or, with none
    # recorded, listed `unrecorded` (G152, 1.4.37: never cleared by mtime).
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    a = _other_plan(tmp_path, "reviewing/sec")
    b = _other_plan(tmp_path, "planning/ui")
    _other_plan(tmp_path, "planning/uix")                    # cited nowhere: never listed
    rec = f"- `reviewing/sec/area-plan.md {stage_status.git_blob_hash(a)}`\n"     # G191: backticked
    rec_b = f"- `planning/ui/area-plan.md {stage_status.git_blob_hash(b)}`\n"
    plan = _plan_text(d).replace("## Overlaps\n\no\n", "## Overlaps\n\nSee reviewing/sec and planning/ui.\n")
    (d / "area-plan.md").write_text(plan.replace("## Step-4 re-check\n\nr\n",
                                                 f"## Step-4 re-check\n\n{rec}{rec_b}"), encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert s["other_plans_changed"] == [] and s["next"] == "research"
    a.write_text("# Other, changed\n", encoding="utf-8")
    (d / "area-plan.md").write_text(_plan_text(d).replace(rec_b, ""), encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert [(r["plan"], r["recorded"]) for r in s["other_plans_changed"]] == [
        ("planning/ui", None), ("reviewing/sec", rec.split()[-1].strip("`"))]
    assert s["other_plans_changed"][1]["current"] == stage_status.content_hash(a)   # G186
    assert s["next"] == "research"                           # advisory: never held
    keyed = stage_status.output_keys(s)
    assert keyed["other_plans_changed"] == s["other_plans_changed"]


def test_a_plan_cited_by_its_areas_path_is_listed_and_a_bare_word_is_not(tmp_path):
    # Fix round 1 (gapfix9 review 4): `areas/<name>/area-plan.md` cites a plan;
    # a single-segment name cites only as a path (`<name>/`, `areas/<name>`)
    # or in backticks, never as a plain English word.
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    for name in ("reviewing/sec", "shipping", "testing", "storytelling"):
        _other_plan(tmp_path, name)
    text = ("See areas/reviewing/sec/area-plan.md. Shipping and testing are plain words here.\n"
            "Also `storytelling`.\n")
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Overlaps\n\no\n", f"## Overlaps\n\n{text}"),
                                    encoding="utf-8")
    approve(d)
    assert [r["plan"] for r in run(tmp_path)["other_plans_changed"]] == ["reviewing/sec", "storytelling"]
    (d / "area-plan.md").write_text(_plan_text(d).replace("plain words here", "in shipping/area-plan.md"),
                                    encoding="utf-8")
    approve(d)
    assert [r["plan"] for r in run(tmp_path)["other_plans_changed"]] == ["reviewing/sec", "shipping", "storytelling"]


def test_keys_print_the_rows_of_every_hold_never_a_count(tmp_path, capsys):
    # G138 (N17, 1.4.36): --keys prints plan_sections, stale_reference,
    # r9_stale, stale_copy_check and other_plans_changed whole; --rows K one key.
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    (d / "area-plan.md").write_text(_plan_text(d).replace(f"## Owner questions\n\n{OWNER_Q}\n", ""), encoding="utf-8")
    ws = tmp_path / "docs" / "grow-cookbook"
    (tmp_path / "cookbook").mkdir()
    assert stage_status.main(["--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--keys"]) == 0
    out = json.loads(capsys.readouterr().out)
    full = run(tmp_path)
    for k in ("plan_sections", "stale_reference", "r9_stale", "stale_copy_check", "host_check"):
        assert out[k] == full[k], k
    # G219 (1.4.39): other_plans_changed is counted under --keys; --rows prints it
    assert out["other_plans_changed"] == ({"rows": len(full["other_plans_changed"]),
                                           "plans": [r["plan"] for r in full["other_plans_changed"]]}
                                          if full["other_plans_changed"] else [])
    assert out["topics"] == {"keys": ["rows"]}
    assert stage_status.main([AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--rows", "topics"]) == 0
    assert json.loads(capsys.readouterr().out) == {"topics": full["topics"]}


def test_the_digest_is_one_line_that_does_not_read_the_plans_own_record(tmp_path, capsys):
    # G137 (1.4.36): --digest prints one line to record in Step-4 re-check;
    # recording it leaves it unchanged.
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    ws = tmp_path / "docs" / "grow-cookbook"
    (tmp_path / "cookbook").mkdir()
    args = [AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--digest"]
    assert stage_status.main(args) == 0
    line = capsys.readouterr().out.strip()
    assert line.startswith(f"stage_status.py {AREA}: next research; ") and "\n" not in line and "; result " in line
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Step-4 re-check\n\nr\n",
                                                          f"## Step-4 re-check\n\n{line}\n"), encoding="utf-8")
    approve(d)
    assert stage_status.main(args) == 0
    assert capsys.readouterr().out.strip() == line


def test_a_copy_only_plans_question_its_survivor_plan_lacks_is_listed(tmp_path):
    # G130 (1.4.36): survivor_carries, advisory: each Research question of a
    # copy-only plan whose first 60 characters no survivor plan holds.
    d, _ = _copies_area(tmp_path)
    q1 = "1. rows: which retry budget do clients keep when the server says 429?\n"
    q2 = "2. rows: how is idempotency keyed on a retried POST across regions?\n"
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Research questions\n\nq\n",
                                                          f"## Research questions\n\n{q1}{q2}"), encoding="utf-8")
    _other_plan(tmp_path, "implementing/other", f"# Survivor\n\n## Research questions\n\n{q1}")
    s = run(tmp_path)
    assert [r["survivors"] for r in s["survivor_carries"]] == [["implementing/other"]]
    assert "idempotency" in s["survivor_carries"][0]["question"]


# --- gapfix10 (1.4.37) ---------------------------------------------------------------------------


def _copy_plan(tmp_path: Path, research: str, survivor: str | None, owner: str = "None.\n") -> dict:
    """status() of a copy-only plan (its one topic merged into implementing/other) whose
    Research questions are `research`; the survivor's plan holds `survivor` under its
    Research questions (no survivor plan when None)."""
    d, _ = _copies_area(tmp_path)
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Research questions\n\nq\n",
                                                          f"## Research questions\n\n{research}")
                                    .replace(f"## Owner questions\n\n{OWNER_Q}", f"## Owner questions\n\n{owner}"),
                                    encoding="utf-8")
    if survivor is not None:
        _other_plan(tmp_path, "implementing/other",
                    f"# Survivor\n\n## Research questions\n\n{survivor}\n## Owner questions\n\nNone.\n")
    return run(tmp_path)


def test_survivor_carries_keys_on_the_lead_bold_span_without_its_carry_note(tmp_path):
    # G150 (N1): the subject is the item's lead bold span, a "(carried ...)" or
    # "(hosted ...)" note stripped; the survivor carries it when the whole span
    # is a bold span or list item in its Research or Owner questions.
    q = "1. **Plurals and message formatting** (carried, no host: implementing/other owns it): which ICU form?\n"
    s = _copy_plan(tmp_path, q, "1. **Plurals and message formatting** (hosted here in strings): ICU?\n")
    assert s["survivor_carries"] == [], s["survivor_carries"]
    # the note inside the bold span is stripped too
    q = "1. **Plurals and message formatting (carried, no host)**: which ICU form?\n"
    (tmp_path / "two").mkdir()
    s = _copy_plan(tmp_path / "two", q, "1. **Plurals and message formatting**: ICU?\n")
    assert s["survivor_carries"] == [], s["survivor_carries"]


def test_survivor_carries_a_span_only_inside_a_longer_phrase_does_not_clear_it(tmp_path):
    q = "1. **Plurals** (carried, no host): which ICU form?\n"
    s = _copy_plan(tmp_path, q, "1. **Plurals and message formatting**: ICU?\n")
    assert [(r["subject"], r["survivors"]) for r in s["survivor_carries"]] == [
        ("Plurals", ["implementing/other"])], s["survivor_carries"]


def test_survivor_carries_names_only_the_survivor_the_item_names(tmp_path):
    # G150 (N1): with two owners, an item naming one lists only that one.
    d, _ = _copies_area(tmp_path)
    second = f"| cols | merged | `cookbook/guidelines/planning/third/cols` | why |\n"
    artifact(tmp_path / "cookbook/guidelines/planning/third/cols")
    artifact(tmp_path / f"cookbook/guidelines/{AREA}/cols")
    q = ("1. **Plurals** (carried, no host: implementing/other): ICU?\n"
         "2. **Grapheme clusters** (carried, no host): segmenting?\n")
    (d / "area-plan.md").write_text(_plan_text(d).replace("| rows | merged |", second + "| rows | merged |")
                                    .replace("## Research questions\n\nq\n", f"## Research questions\n\n{q}"),
                                    encoding="utf-8")
    _other_plan(tmp_path, "implementing/other", "# S\n\n## Research questions\n\n1. x\n")
    _other_plan(tmp_path, "planning/third", "# T\n\n## Owner questions\n\n- **Grapheme clusters**\n")
    rows = run(tmp_path)["survivor_carries"]
    assert [(r["subject"], r["survivors"]) for r in rows] == [
        ("Plurals", ["implementing/other"]), ("Grapheme clusters", ["implementing/other"])], rows


def test_carries_asked_lists_on_the_survivor_each_subject_a_copy_plan_asks_it_to_carry(tmp_path):
    # G151 (N2): advisory on the survivor's side, never a hold; --keys prints the rows.
    _copy_plan(tmp_path, "1. **Plurals** (carried, no host: implementing/other): ICU?\n", None)
    ws = tmp_path / "docs" / "grow-cookbook"
    surv = _other_plan(tmp_path, "implementing/other", "# S\n\n## Research questions\n\n1. q\n")
    s = stage_status.status("implementing/other", ws, tmp_path)
    assert [(r["plan"], r["subject"]) for r in s["carries_asked"]] == [(AREA, "Plurals")], s["carries_asked"]
    assert stage_status.output_keys(s)["carries_asked"] == s["carries_asked"]
    surv.write_text("# S\n\n## Research questions\n\n1. **Plurals**: which ICU form?\n", encoding="utf-8")
    assert stage_status.status("implementing/other", ws, tmp_path)["carries_asked"] == []


def test_a_cited_plan_with_no_recorded_hash_is_listed_unrecorded_whatever_its_mtime(tmp_path):
    # G152 (N3): no mtime test: a cited plan with no recorded hash stays listed.
    import os
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    b = _other_plan(tmp_path, "planning/ui")
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Overlaps\n\no\n", "## Overlaps\n\nSee planning/ui.\n"),
                                    encoding="utf-8")
    approve(d)
    t = (d / "area-plan.md").stat().st_mtime
    os.utime(b, (t - 100, t - 100))
    rows = run(tmp_path)["other_plans_changed"]
    assert [(r["plan"], r["recorded"]) for r in rows] == [("planning/ui", None)], rows
    assert "unrecorded" in rows[0]["why"]


def _git_ws(tmp_path: Path) -> Path:
    import subprocess
    ws = tmp_path / "docs" / "grow-cookbook"
    subprocess.run(["git", "init", "-q", str(ws)], check=True)
    return ws


def test_a_rewritten_sibling_names_its_changed_sections_and_leaves_the_digest(tmp_path, capsys):
    # G153 (N4): other_plans_changed, survivor_carries and carries_asked are out
    # of the digest; each other_plans_changed row names the sections that changed
    # since the recorded hash when git still holds that text, else "unknown".
    import subprocess
    cookr_skill(tmp_path)
    (tmp_path / "cookbook").mkdir(exist_ok=True)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    ws = _git_ws(tmp_path)
    sib = _other_plan(tmp_path, "planning/ui", "# UI\n\n## Topics\n\nt\n\n## Gaps\n\ng\n")
    h = subprocess.run(["git", "-C", str(ws), "hash-object", "-w", str(sib)], capture_output=True, text=True,
                       check=True).stdout.strip()
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Overlaps\n\no\n", "## Overlaps\n\nSee planning/ui.\n")
                                    .replace("## Step-4 re-check\n\nr\n",
                                             f"## Step-4 re-check\n\n- `planning/ui/area-plan.md {h}`\n"),
                                    encoding="utf-8")
    approve(d)
    args = [AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--digest"]
    assert stage_status.main(args) == 0
    line = capsys.readouterr().out.strip()
    sib.write_text("# UI\n\n## Topics\n\nt\n\n## Gaps\n\ng, rewritten\n", encoding="utf-8")
    rows = run(tmp_path)["other_plans_changed"]
    assert [(r["plan"], r["sections"]) for r in rows] == [("planning/ui", ["Gaps"])], rows
    assert stage_status.main(args) == 0
    assert capsys.readouterr().out.strip() == line
    other = _other_plan(tmp_path, "planning/sec", "# Sec\n")
    (d / "area-plan.md").write_text(_plan_text(d).replace("See planning/ui.", "See planning/ui and planning/sec.")
                                    .replace(f"{h}`\n", f"{h}`\n- `planning/sec/area-plan.md {'0' * 40}`\n"),
                                    encoding="utf-8")
    approve(d)
    rows = run(tmp_path)["other_plans_changed"]
    assert {r["plan"]: r["sections"] for r in rows}["planning/sec"] == "unknown", rows
    assert other.is_file()


def test_the_record_of_a_nested_plan_never_stands_for_a_shorter_one(tmp_path):
    # G154 (N5): `implementing/testing/area-plan.md H1` is no record of `testing`.
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    t = _other_plan(tmp_path, "testing", "# T\n")
    it = _other_plan(tmp_path, "implementing/testing", "# IT\n")
    h_t, h_it = stage_status.git_blob_hash(t), stage_status.git_blob_hash(it)
    rec = f"- `testing/area-plan.md {h_t}`\n- `implementing/testing/area-plan.md {h_it}`\n"
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Overlaps\n\no\n",
                                                          "## Overlaps\n\nSee `testing` and implementing/testing.\n")
                                    .replace("## Step-4 re-check\n\nr\n", f"## Step-4 re-check\n\n{rec}"),
                                    encoding="utf-8")
    approve(d)
    assert run(tmp_path)["other_plans_changed"] == []


def test_editing_only_the_step4_section_leaves_the_digest_unchanged(tmp_path, capsys):
    # G155, G183 (N6, N34): the digest reads nothing of Step-4 re-check: recording
    # hashes and the digest line itself there never moves it.
    cookr_skill(tmp_path)
    (tmp_path / "cookbook").mkdir(exist_ok=True)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    sib = _other_plan(tmp_path, "planning/ui")
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Overlaps\n\no\n", "## Overlaps\n\nSee planning/ui.\n"),
                                    encoding="utf-8")
    approve(d)
    import os
    t = (d / "area-plan.md").stat().st_mtime
    os.utime(sib, (t + 100, t + 100))     # BASE listed a newer, unrecorded plan until its hash was recorded
    ws = tmp_path / "docs" / "grow-cookbook"
    args = [AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--digest"]
    assert stage_status.main(args) == 0
    line = capsys.readouterr().out.strip()
    rec = f"- `planning/ui/area-plan.md {stage_status.git_blob_hash(sib)}`\n- {line}\n"
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Step-4 re-check\n\nr\n", f"## Step-4 re-check\n\n{rec}"),
                                    encoding="utf-8")
    approve(d)
    assert stage_status.main(args) == 0
    assert capsys.readouterr().out.strip() == line


def test_a_wrapped_line_or_a_code_span_starting_with_bold_is_no_paragraph_row(tmp_path):
    # G165 (N16): only a paragraph's first line can be bold-led; code spans are stripped.
    subj = "1. **Caching**: x\nand more words\n**Sharding** wraps here, still item one.\n\n`**Audit**` is code.\n"
    assert _subject_rows(tmp_path, subj, "1. rows: **caching**?\n") == []
    # bold inside a code span within an item is code, never a second subject
    assert _subject_rows(tmp_path, "1. **Caching**: see `**Audit**` in code.\n", "1. rows: **caching**?\n") == []


def test_a_code_span_inside_a_bold_subject_stays_part_of_it(tmp_path):
    # G165 (N16), found on the workspace run: only a code span holding bold is
    # dropped; `ContentProvider` inside a bold subject stays, so the carried
    # subject still matches its Research question.
    subj = "12. **Scoping `ContentProvider` (and file-sharing) permissions**: x\n"
    q = "5. **Scoping `ContentProvider` (and file-sharing) permissions** (carried, no host): y?\n"
    own = "- **Scoping `ContentProvider` (and file-sharing) permissions**: a new topic?\n"
    assert _subject_rows(tmp_path, subj, q, own) == []
    rows = _subject_rows(tmp_path, "Intro line.\n\n**Audit trails**: z.\n", "1. q\n")
    assert [i for i, _ in rows] == ["Audit trails"]


def test_a_second_table_under_topics_adds_no_topics(tmp_path):
    # G166 (N17): only the first table under Topics names topics.
    table = ("| Topic | Artifact |\n|---|---|\n| swift-testing | x |\n\nCounts:\n\n| Speciality | n |\n|---|---|\n"
             "| security/authz | 3 |\n")
    rows = _bar_plan(tmp_path, table, "x\n")
    assert [i for _, i, _ in rows] == ["swift-testing"], rows
    assert "one top-level item per topic, naming the topic" in rows[0][2]


# --- gapfix10b (1.4.38) --------------------------------------------------------------------------

_ASK = "1. **Plurals and message formatting** (carried, no host: implementing/other): which ICU form?\n"
_LEADS = [" (hosted here in strings): ICU?", ": which ICU form?", ". Which ICU form?", ", and which ICU form?",
          " — which ICU form?", " - which ICU form?", ""]


@pytest.mark.parametrize("tail", _LEADS)
@pytest.mark.parametrize("marker", ["6. ", "- ", "6. **"])
def test_survivor_carries_a_plain_numbered_lead_clears_the_row(tmp_path, marker, tail):
    # G184 (1.4.38): the survivor carries the subject as the lead of a list
    # item, its text starting with the whole phrase and a boundary.
    lead = "Plurals and message formatting" + ("**" if marker.endswith("**") else "")
    s = _copy_plan(tmp_path, _ASK, f"{marker}{lead}{tail}\n")
    assert s["survivor_carries"] == [], s["survivor_carries"]


def test_a_lead_ends_at_a_boundary_or_the_items_end():
    # G184 (1.4.38): the matcher itself; bold markers are no part of the phrase.
    k = "plurals and message formatting"
    assert stage_status._leads("Plurals and message formatting", k)
    assert stage_status._leads("**Plurals and message formatting (hosted here)**: ICU?", k)
    assert not stage_status._leads("Plurals and message formatting rules", k)
    assert not stage_status._leads("Plurals and message formatting-rules", k)


@pytest.mark.parametrize("survivor", [
    "6. Plurals and message formatting rules: which ICU form?\n",
    "6. Plurals and message formatting-rules: which ICU form?\n",
    "6. Plurals and message formattings, ICU?\n",
    "6. The plurals and message formatting (hosted): ICU?\n",
    "### Plurals and message formatting (hosted here)\n\n6. which ICU form?\n",
    "### Plurals and message formatting\n",
])
def test_survivor_carries_a_longer_phrase_or_a_heading_does_not_clear_it(tmp_path, survivor):
    # G184 (1.4.38): a phrase that only starts a longer one, or a heading, carries nothing.
    s = _copy_plan(tmp_path, _ASK, survivor)
    assert [(r["subject"], r["kind"]) for r in s["survivor_carries"]] == [
        ("Plurals and message formatting", "subject")], s["survivor_carries"]


@pytest.mark.parametrize("label", ["Best practices", "Known solutions", "Platform guidelines",
                                   "The expert's view", "**Best practices:**"])
def test_a_research_label_row_is_tagged_and_still_listed(tmp_path, label):
    # G185 (1.4.38): an item led by a research label stays listed, tagged
    # research_label; a subject row is tagged subject; --keys shows the kind.
    sep = " " if label.endswith(":**") else ": "
    q = f"1. {label}{sep}what should a reviewer check (implementing/other)?\n" + _ASK.replace("1.", "2.", 1)
    s = _copy_plan(tmp_path, q, "1. x\n")
    rows = s["survivor_carries"]
    # G214 (1.4.39): subject rows print first, research_label rows after
    assert [r["kind"] for r in rows] == ["subject", "research_label"], rows
    assert rows[0]["subject"] == "Plurals and message formatting"
    assert stage_status.output_keys(s)["survivor_carries"] == rows


def test_a_label_word_that_only_starts_a_longer_lead_is_a_subject(tmp_path):
    q = "1. Best practices for plural forms (carried, no host: implementing/other)?\n"
    rows = _copy_plan(tmp_path, q, "1. x\n")["survivor_carries"]
    assert [r["kind"] for r in rows] == ["subject"], rows


@pytest.mark.parametrize("survivor,left", [
    ("6. Plurals and message formatting (hosted here in strings): ICU?\n", []),
    ("6. Plurals and message formatting rules: which ICU form?\n", ["subject"]),
    ("### Plurals and message formatting\n", ["subject"]),
])
def test_carries_asked_uses_the_same_matcher(tmp_path, survivor, left):
    # G184/G185 (1.4.38): carries_asked reads the survivor through the same matcher, with the kind.
    q = "1. Best practices: which ICU form (implementing/other)?\n" + _ASK.replace("1.", "2.", 1)
    _copy_plan(tmp_path, q, None)
    ws = tmp_path / "docs" / "grow-cookbook"
    _other_plan(tmp_path, "implementing/other",
                f"# S\n\n## Research questions\n\n{survivor}\n## Owner questions\n\nNone.\n")
    s = stage_status.status("implementing/other", ws, tmp_path)
    assert [r["kind"] for r in s["carries_asked"]] == left + ["research_label"], s["carries_asked"]   # G214
    assert stage_status.output_keys(s)["carries_asked"] == s["carries_asked"]


@pytest.mark.parametrize("q,survivor,kind", [
    ("1. **Best practices**: which ICU form (implementing/other)?\n",
     "1. Best practices: which ICU form?\n", "research_label"),
    ("1. Best practices: which ICU form (implementing/other)?\n",
     "1. Best practices: which ICU form (implementing/other)?\n", "research_label"),
    ("1. **Missing subjects** (carried, no host): for **Swift isolation**, which checks?\n",
     "5. Missing subjects (*Missing subjects* 9): for Swift, which checks?\n", "subject"),
])
def test_a_label_or_section_name_lead_is_never_cleared(tmp_path, q, survivor, kind):
    # G185 (1.4.38): a research label or a plan section name names no subject;
    # its row stays listed whatever the survivor holds, on both sides.
    s = _copy_plan(tmp_path, q, survivor)
    assert [r["kind"] for r in s["survivor_carries"]] == [kind], s["survivor_carries"]
    ws = tmp_path / "docs" / "grow-cookbook"
    asked = stage_status.status("implementing/other", ws, tmp_path)["carries_asked"]
    assert [r["kind"] for r in asked] == [kind], asked


def test_a_heading_neither_carries_nor_names_a_subject(tmp_path):
    # G184 (1.4.38): _split, shared by _chunks and _carried, leaves a heading's
    # text out of every chunk, so a heading does not even name the subject.
    rows = _subject_rows(tmp_path, "1. **Image optimization**: x.\n", "### Image optimization\n\n1. rows: q?\n")
    assert [i for i, _ in rows] == ["Image optimization"] and "carried nowhere" in rows[0][1], rows


# --- gapfix11 (1.4.39) ---------------------------------------------------------------------------


def _append(p: Path, text: str) -> None:
    p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")


def _citing_pair(tmp_path: Path) -> tuple[Path, Path, Path]:
    """This area's plan (A) citing planning/ui, and planning/ui's plan (B) citing A; (A, B, workspace)."""
    cookr_skill(tmp_path)
    (tmp_path / "cookbook" / "guidelines" / AREA).mkdir(parents=True, exist_ok=True)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    a = d / "area-plan.md"
    a.write_text(_plan_text(d).replace("## Overlaps\n\no\n", "## Overlaps\n\nSee planning/ui.\n"), encoding="utf-8")
    approve(d)
    b = _other_plan(tmp_path, "planning/ui",
                    f"# UI\n\n## Overlaps\n\nSee {AREA}.\n\n## Research questions\n\n1. q?\n\n## Step-4 re-check\n\nr\n")
    return a, b, tmp_path / "docs" / "grow-cookbook"


def test_recording_each_others_content_hash_settles_the_cycle(tmp_path):
    # G186 (L1, 1.4.39): other_plans_changed compares a content hash, the plan
    # with its Step-4 re-check section removed: recording A's hash in B, then
    # B's in A, leaves both rows clear.
    a, b, ws = _citing_pair(tmp_path)
    row = run(tmp_path)["other_plans_changed"][0]
    assert f"`planning/ui/area-plan.md {row['current']}`" in row["why"], row
    _append(a, f"- `planning/ui/area-plan.md {row['current']}`\n")
    rows_b = stage_status.status("planning/ui", ws, tmp_path)["other_plans_changed"]
    assert [r["plan"] for r in rows_b] == [AREA], rows_b
    _append(b, f"- `{AREA}/area-plan.md {rows_b[0]['current']}`\n")
    assert run(tmp_path)["other_plans_changed"] == []
    assert stage_status.status("planning/ui", ws, tmp_path)["other_plans_changed"] == []
    # a change outside Step-4 re-check in B re-lists B in A
    b.write_text(b.read_text(encoding="utf-8").replace("1. q?", "1. q, changed?"), encoding="utf-8")
    rows = run(tmp_path)["other_plans_changed"]
    assert [(r["plan"], r["recorded"]) for r in rows] == [("planning/ui", row["current"])], rows


def test_an_old_whole_file_hash_counts_until_the_plan_changes(tmp_path):
    # G186 (L1): a hash recorded before 1.4.39 (git hash-object of the whole
    # file) stays current while the cited plan is unchanged.
    a, b, _ = _citing_pair(tmp_path)
    _append(a, f"- `planning/ui/area-plan.md {stage_status.git_blob_hash(b)}`\n")
    assert run(tmp_path)["other_plans_changed"] == []
    b.write_text(b.read_text(encoding="utf-8").replace("1. q?", "1. q, changed?"), encoding="utf-8")
    assert [r["plan"] for r in run(tmp_path)["other_plans_changed"]] == ["planning/ui"]


def test_only_backticked_step4_lines_are_records_and_the_last_wins(tmp_path):
    # G191 (L6, 1.4.39): a hash is read only from a Step-4 line holding
    # `<area>/area-plan.md <40-hex>` in backticks; of several, the last (the
    # last `### ` subsection's) wins. A prose line or an un-backticked one is
    # no record, and the row says the un-backticked one is not read.
    a, b, _ = _citing_pair(tmp_path)
    good = run(tmp_path)["other_plans_changed"][0]["current"]
    old = "1" * 40
    _append(a, f"### On 1.4.38\n\n- `planning/ui/area-plan.md {good}`\n\n"
               f"The 1.4.36 plan recorded planning/ui/area-plan.md {old} here.\n")
    assert run(tmp_path)["other_plans_changed"] == []
    _append(a, f"\n### On 1.4.39\n\n- `planning/ui/area-plan.md {old}`\n")
    assert [r["recorded"] for r in run(tmp_path)["other_plans_changed"]] == [old]
    text = a.read_text(encoding="utf-8").split("## Step-4 re-check")[0]
    a.write_text(text + f"## Step-4 re-check\n\n- planning/ui/area-plan.md {good}\n", encoding="utf-8")
    rows = run(tmp_path)["other_plans_changed"]
    assert [r["recorded"] for r in rows] == [None] and "not read" in rows[0]["why"], rows


def test_record_others_snapshots_a_plan_so_an_untracked_change_names_its_sections(tmp_path, capsys):
    # G193 (L8, 1.4.39): --record-others saves each cited plan as
    # A/other-plans/<plan, / as -->.<hash>.md and prints the lines to record;
    # a later row diffs against that snapshot, git or not.
    a, b, ws = _citing_pair(tmp_path)
    args = ["--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path)]
    assert stage_status.main(args + ["--record-others"]) == 0
    out = capsys.readouterr().out
    h = run(tmp_path)["other_plans_changed"][0]["current"]
    assert out.strip() == f"- `planning/ui/area-plan.md {h}`", out
    assert (a.parent / "other-plans" / f"planning--ui.{h}.md").is_file()
    _append(a, out)
    assert run(tmp_path)["other_plans_changed"] == []
    b.write_text(b.read_text(encoding="utf-8").replace("1. q?", "1. q, changed?"), encoding="utf-8")
    rows = run(tmp_path)["other_plans_changed"]
    assert [(r["plan"], r["sections"]) for r in rows] == [("planning/ui", ["Research questions"])], rows


def test_each_row_says_where_this_plan_cites_the_plan_and_its_question_numbers(tmp_path):
    # G194 (L9), G211 (L26, 1.4.39): `cited_at` lists the plan's lines naming
    # the other plan; `question_cites` those that also cite its question numbers.
    a, b, _ = _citing_pair(tmp_path)
    a.write_text(a.read_text(encoding="utf-8").replace(
        "See planning/ui.\n", "See planning/ui.\nplanning/ui Research questions 6-8 carry it.\n"), encoding="utf-8")
    lines = a.read_text(encoding="utf-8").splitlines()
    at = [i + 1 for i, x in enumerate(lines) if "planning/ui" in x]
    _append(a, "- `planning/ui/area-plan.md " + "0" * 40 + "`\n")      # a Step-4 record is no citation
    rows = run(tmp_path)["other_plans_changed"]
    assert rows[0]["cited_at"] == at and rows[0]["question_cites"] == [at[1]], rows
    assert f"cited at {stage_status.line_ranges(at)}" in rows[0]["why"]


def _cited_plan_with_questions(tmp_path: Path, cite_line: str) -> tuple[Path, Path, Path]:
    """_citing_pair whose planning/ui plan has three Research items and two Owner items, this plan citing
    them in `cite_line`, the snapshot of planning/ui recorded in this plan's Step-4 re-check."""
    a, b, ws = _citing_pair(tmp_path)
    b.write_text("# UI\n\n## Research questions\n\n### t\n\n1. **Alpha** (missing subject 1): a?\n"
                 "2. **Beta** (missing subject 2): b?\n3. **Gamma** (missing subject 3): c?\n\n"
                 "## Owner questions\n\n1. **Alpha** owner call?\n2. **Beta** owner call?\n\n"
                 "## Step-4 re-check\n\nr\n", encoding="utf-8")
    a.write_text(a.read_text(encoding="utf-8").replace("See planning/ui.\n", "See planning/ui.\n" + cite_line + "\n"),
                 encoding="utf-8")
    (line,) = stage_status.record_others(AREA, ws)
    _append(a, line + "\n")
    return a, b, ws


def test_a_cited_question_number_whose_lead_changed_is_a_cite_moved_row_that_holds_at_plan(tmp_path):
    # G232 (L10), G245 (L23): the plan cites "question 2" of planning/ui; planning/ui then puts a new item
    # first, so question 2 is Alpha, not Beta: a cite_moved row, `next` plan; an unmoved cite gives none.
    a, b, ws = _cited_plan_with_questions(tmp_path, "planning/ui question 2 and owner question 1 carry it.")
    approve(a.parent)
    assert run(tmp_path)["cite_moved"] == [] and run(tmp_path)["next"] != "plan"
    b.write_text(b.read_text(encoding="utf-8").replace(
        "1. **Alpha** (missing subject 1)", "1. **New** (missing subject 0): n?\n2. **Alpha** (missing subject 1)", 1),
        encoding="utf-8")
    s = run(tmp_path)
    [row] = s["cite_moved"]
    assert (row["plan"], row["cite"], row["was"], row["now"]) == ("planning/ui", "question 2", "Beta", "Alpha"), row
    assert row["why"].startswith("cite 2: was 'Beta', now 'Alpha'") and "in planning/ui" in row["why"]
    assert s["next"] == "plan" and "cite_moved" in s["next_why"]


def test_a_cite_by_owner_question_its_question_or_topic_pair_is_read_and_one_naming_the_area_without_a_path(tmp_path):
    # G232 (L10): "owner question N" reads the owner list; "topic 1-3" the third item of the first group.
    # gapfix13 (G258): the `<name> plan` alias takes the exact area name only.
    a, b, ws = _cited_plan_with_questions(tmp_path, "The planning/ui plan: owner question 2 and topic 1-3 carry it.")
    approve(a.parent)
    assert run(tmp_path)["cite_moved"] == []
    b.write_text(b.read_text(encoding="utf-8").replace("2. **Beta** owner call?", "2. **Other** owner call?")
                 .replace("3. **Gamma**", "3. **Delta**"), encoding="utf-8")
    rows = run(tmp_path)["cite_moved"]
    assert sorted((r["cite"], r["was"], r["now"]) for r in rows) == [
        ("owner question 2", "Beta", "Other"), ("topic 1-3", "Gamma", "Delta")], rows


def test_record_others_write_replaces_the_record_lines_of_the_last_subsection_atomically(tmp_path, capsys):
    # G236 (L14, 1.4.40): --record-others --write puts the printed lines into the last `### ` subsection of
    # Step-4 re-check (a stale record of the plan replaced in place), a second run changes nothing, other text is
    # byte-identical; with no `### ` subsection it refuses and writes nothing.
    a, b, ws = _citing_pair(tmp_path)
    old = "## Step-4 re-check\n\nr\n"
    assert old in a.read_text(encoding="utf-8")
    args = [AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--record-others", "--write"]
    before = a.read_text(encoding="utf-8")
    assert stage_status.main(args) == 2 and a.read_text(encoding="utf-8") == before
    assert "no `### ` subsection" in capsys.readouterr().err
    stale = "- `planning/ui/area-plan.md " + "0" * 40 + "`\n"
    a.write_text(before.replace(old, "## Step-4 re-check\n\n### Round 1\n\nkeep me\n" + stale + "\n### Round 2\n\n"
                                + stale + "tail line\n"), encoding="utf-8")
    pre = a.read_text(encoding="utf-8")
    assert stage_status.main(args) == 0
    h = stage_status.content_hash_of(b.read_text(encoding="utf-8"))
    head, _, last = pre.partition("### Round 2\n")      # only the last subsection's record is replaced
    want = head + "### Round 2\n" + last.replace(stale, f"- `planning/ui/area-plan.md {h}`\n")
    assert a.read_text(encoding="utf-8") == want
    assert stage_status.main(args) == 0 and a.read_text(encoding="utf-8") == want
    assert not list(a.parent.glob("*.tmp*"))
    assert run(tmp_path)["other_plans_changed"] == []


def _hosting_plan(tmp_path: Path, research: str, owner: str = OWNER_Q, merged: str | None = None,
                  titles: dict | None = None) -> dict:
    """status() of a plan whose topics are rendering-strategy, design-tokens,
    cache-keys and cache-eviction (titled as their folders say), with these
    Research questions and Owner questions."""
    cookr_skill(tmp_path)
    titles = titles or {"rendering-strategy": "Rendering strategy", "design-tokens": "Design tokens",
                        "cache-keys": "Cache keys", "cache-eviction": "Cache eviction policy",
                        "data-keys": "Data keys"}
    d = area(tmp_path, {t: f"cookbook/guidelines/{AREA}/{t}" for t in titles})
    for t, title in titles.items():
        f = artifact(tmp_path / f"cookbook/guidelines/{AREA}/{t}")
        (f / "artifact.json").write_text(json.dumps({"meta": {"title": title}, "parts": []}), encoding="utf-8")
    plan = _plan_text(d).replace("## Research questions\n\nq\n", f"## Research questions\n\n{research}")
    plan = plan.replace(f"## Owner questions\n\n{OWNER_Q}", f"## Owner questions\n\n{owner}")
    if merged:
        plan = plan.replace(f"| {merged} | kept | `cookbook/guidelines/{AREA}/{merged}`",
                            f"| {merged} | merged | `cookbook/guidelines/implementing/other/{merged}`")
        artifact(tmp_path / f"cookbook/guidelines/implementing/other/{merged}")
    (d / "area-plan.md").write_text(plan, encoding="utf-8")
    approve(d)
    return run(tmp_path)


def test_host_check_lists_a_host_sharing_no_specific_word_and_a_no_host_subject_that_shares_one(tmp_path):
    # G188 (L3), G208 (L23, 1.4.39): a generic word ("strategy") or an area
    # word ("data") never hosts; a No-host subject sharing a specific word
    # (a stem: "tokens" / "token") has a host. Both hold the area at plan.
    research = ("### rendering-strategy\n\n1. Best practices: x?\n"
                "2. **UI testing strategy** (missing subject 9), carried,\n   no host: which tests?\n"
                "3. **Rendering on watches** (missing subject 2), carried, no host: which?\n\n"
                "### data-keys\n\n1. **Data lineage**, carried, no host: x?\n\n"
                "### No host\n\n1. **Token naming** (missing subject 4), carried, no host: which?\n"
                "2. **Navigation maps**, carried, no host: x?\n")
    s = _hosting_plan(tmp_path, research)
    got = {(r["subject"], r["host"]): r["why"] for r in s["host_check"]}
    assert set(got) == {("UI testing strategy", "rendering-strategy"), ("Data lineage", "data-keys"),
                        ("Token naming", None)}, s["host_check"]
    assert "design-tokens" in got[("Token naming", None)] and s["next"] == "plan"
    assert "host_check" in s["next_why"]


def test_host_check_a_tie_names_every_tying_topic_and_goes_under_owner_questions(tmp_path):
    # G209 (L24, 1.4.39): with a tie the subject names every tying topic and
    # is under Owner questions; a topic sharing more words is the host.
    research = "### cache-keys\n\n1. **Cache warming**, carried, no host: x?\n"
    s = _hosting_plan(tmp_path / "a", research)
    assert [(r["subject"], r["host"]) for r in s["host_check"]] == [("Cache warming", "cache-keys")]
    assert "cache-eviction" in s["host_check"][0]["why"], s["host_check"]
    research = "### cache-keys, cache-eviction\n\n1. **Cache warming**, carried, no host: x?\n"
    s = _hosting_plan(tmp_path / "b", research, OWNER_Q + "2. **Cache warming**: a topic?\n")
    assert s["host_check"] == [], s["host_check"]
    research = "### cache-keys\n\n1. **Cache key rotation**, carried, no host: x?\n"
    s = _hosting_plan(tmp_path / "c", research)
    assert s["host_check"] == [], s["host_check"]
    research = "### cache-keys\n\n1. **Cache eviction policy tuning**, carried, no host: x?\n"
    s = _hosting_plan(tmp_path / "d", research)
    assert [r["subject"] for r in s["host_check"]] == ["Cache eviction policy tuning"]
    assert "cache-eviction" in s["host_check"][0]["why"]


def test_host_check_runs_on_every_hosted_subject_not_only_a_carried_no_host_one(tmp_path):
    # G228 (L6, 1.4.40): a bold-led subject hosted in an ordinary topic that shares no word with it is a row;
    # one hosted where a word is shared is clean; a subject led by a research label is skipped.
    research = ("### rendering-strategy\n\n1. **Token naming** (missing subject 4): which names?\n"
                "2. **Best practices**: what do experts say?\n\n### design-tokens\n\n"
                "1. **Token naming** (missing subject 4): which names?\n")
    s = _hosting_plan(tmp_path, research)
    assert [(r["subject"], r["host"]) for r in s["host_check"]] == [("Token naming", "rendering-strategy")], \
        s["host_check"]
    assert "design-tokens" in s["host_check"][0]["why"] and s["next"] == "plan"


def test_host_check_drops_a_word_every_topic_folder_shares_and_does_not_tie_on_it(tmp_path):
    # G229 (L7): `checklist` in every folder name names no coverage: dropped from subject and topic words.
    titles = {"skill-checklist": "Skill checklist", "agent-checklist": "Agent checklist",
              "rule-checklist": "Rule checklist"}
    research = "### skill-checklist\n\n1. **Checklist severity** (missing subject 1), carried, no host: x?\n"
    s = _hosting_plan(tmp_path, research, titles=titles)
    [row] = s["host_check"]
    assert row["shares"] == {} and "tie" not in row["why"], row


def test_host_check_needs_two_shared_stems_or_one_that_is_a_word_of_the_folder_name(tmp_path):
    # G229 (L7): one shared title word that is not part of the folder name hosts nothing; a folder word does.
    research = ("### cache-eviction\n\n1. **Policy exceptions** (missing subject 1): x?\n"
                "2. **Eviction order** (missing subject 2): x?\n"
                "3. **Policy eviction exceptions** (missing subject 3): x?\n")
    s = _hosting_plan(tmp_path, research)
    assert [r["subject"] for r in s["host_check"]] == ["Policy exceptions"], s["host_check"]


def test_specific_words_drops_cross_choos_target_agent_and_keeps_a_slash_pair_whole():
    # G229 (L7), G241: the four words join GENERIC; `A/B` is one token `ab`.
    assert stage_status.specific_words("Cross-platform choosing target agents", "x/y") == {"platform"}
    assert "ab" in stage_status.specific_words("A/B testing", "x/y")
    assert stage_status.specific_words("caching and cache", "x/y") == {"cach"}


def test_the_generic_words_stage_1_prints_are_the_scripts_generic_list():
    # G241 (L19): stage-1.md's list is generated from stage_status.GENERIC, and states the stem rule.
    doc = (Path(__file__).resolve().parent.parent / "references" / "stage-1.md").read_text(encoding="utf-8")
    m = re.search(r"GENERIC words \(stage_status\.GENERIC\): ([^\n]+?)\.\n", doc)
    assert m, "stage-1.md prints no `GENERIC words (stage_status.GENERIC): ...` line"
    assert set(m.group(1).split(", ")) == set(stage_status.GENERIC)
    for phrase in ("two shared stems", "whole word of the topic's folder name", "A/B", "led by a research label"):
        assert phrase in doc, phrase


def test_host_check_a_merged_copy_never_hosts(tmp_path):
    # G162 within the host check (1.4.39).
    research = "### design-tokens\n\n1. **Token naming**, carried, no host: x?\n"
    s = _hosting_plan(tmp_path, research, merged="design-tokens")
    assert [(r["subject"], r["host"]) for r in s["host_check"]] == [("Token naming", "design-tokens")]
    assert "merged" in s["host_check"][0]["why"]


def test_shared_no_host_lists_each_other_plan_carrying_the_same_subject_unhosted(tmp_path, capsys):
    # G190 (L5, 1.4.39): advisory; case-folded and stem-matched; --keys prints the rows.
    research = "### No host\n\n1. **Full-text search**, carried, no host: x?\n2. **Sharding**, carried, no host\n"
    s = _hosting_plan(tmp_path, research)
    assert s["shared_no_host"] == []
    (tmp_path / "cookbook").mkdir(exist_ok=True)
    _other_plan(tmp_path, "planning/data", "# D\n\n## Research questions\n\n### No host\n\n"
                                           "1. **Full-text Searching** (carried, no host): y?\n")
    _other_plan(tmp_path, "planning/other", "# O\n\n## Research questions\n\n### keys\n\n"
                                            "1. **Sharding**, carried, no host: y?\n")
    s = run(tmp_path)
    assert [(r["plan"], r["subject"]) for r in s["shared_no_host"]] == [("planning/data", "Full-text search")]
    ws = tmp_path / "docs" / "grow-cookbook"
    assert stage_status.main(["--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--keys"]) == 0
    assert json.loads(capsys.readouterr().out)["shared_no_host"] == s["shared_no_host"]


def test_shared_no_host_says_whether_the_owner_questions_name_the_other_plan_and_the_subject(tmp_path):
    # G244 (L22, 1.4.40): the row stays listed, with named_in_owner true once an Owner question names both.
    research = "### No host\n\n1. **Full-text search**, carried, no host: x?\n"
    owner = OWNER_Q + "2. Does planning/data settle full-text search for both plans?\n"
    s = _hosting_plan(tmp_path, research, owner=owner)
    (tmp_path / "cookbook").mkdir(exist_ok=True)
    _other_plan(tmp_path, "planning/data", "# D\n\n## Research questions\n\n### No host\n\n"
                                           "1. **Full-text search** (carried, no host): y?\n")
    [row] = run(tmp_path)["shared_no_host"]
    assert row["named_in_owner"] is True and "named_in_owner" in row["why"]
    d = tmp_path / "docs" / "grow-cookbook" / "areas" / AREA / "area-plan.md"
    d.write_text(d.read_text(encoding="utf-8").replace("planning/data settle", "the other plan settle"),
                 encoding="utf-8")
    assert [r["named_in_owner"] for r in run(tmp_path)["shared_no_host"]] == [False]


def _settled_copy_plan(tmp: Path, research: str) -> dict:
    """_copy_plan with the copy_check.py digest recorded, so nothing else holds it at plan."""
    import copy_check
    _copy_plan(tmp, research, None)
    d, ws = tmp / "docs" / "grow-cookbook" / "areas" / AREA, tmp / "docs" / "grow-cookbook"
    line = copy_check.digest(copy_check.check(AREA, ws, tmp))
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Overlaps\n\no\n", f"## Overlaps\n\no\n\n{line}\n"),
                                    encoding="utf-8")
    approve(d)
    return run(tmp)


def test_a_subject_carry_row_holds_next_at_plan_and_a_label_row_does_not(tmp_path):
    # G214 (L29, 1.4.39): survivor_carries and carries_asked rows of kind
    # `subject` hold next at plan; research_label rows stay advisory and print last.
    s = _settled_copy_plan(tmp_path, "1. Best practices: which ICU form (implementing/other)?\n")
    assert [r["kind"] for r in s["survivor_carries"]] == ["research_label"]
    assert s["next"] != "plan", s["next_why"]
    (tmp_path / "two").mkdir()
    s = _settled_copy_plan(tmp_path / "two", "1. Best practices: which ICU form (implementing/other)?\n"
                                             "2. **Plurals** (carried, no host: implementing/other): ICU?\n")
    assert [r["kind"] for r in s["survivor_carries"]] == ["subject", "research_label"], s["survivor_carries"]
    assert s["next"] == "plan" and "survivor_carries: 1 subject row" in s["next_why"], s["next_why"]
    ws = tmp_path / "two" / "docs" / "grow-cookbook"
    _other_plan(tmp_path / "two", "implementing/other", "# S\n\n## Research questions\n\n1. q\n")
    o = stage_status.status("implementing/other", ws, tmp_path / "two")
    assert [r["kind"] for r in o["carries_asked"]] == ["subject", "research_label"], o["carries_asked"]
    assert o["next"] == "plan" and "carries_asked: 1 subject row" in o["next_why"], o["next_why"]
    assert "1 research_label row" in o["next_why"]


def test_stale_pointer_lists_a_plan_line_citing_a_folded_copy(tmp_path):
    # G216 (L31, 1.4.39): advisory: a topic path the plan cites that the
    # worklist folds, or a plan merges, into a survivor it does not name there.
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    ws = tmp_path / "docs" / "grow-cookbook"
    (ws / "worklist.json").write_text(json.dumps({"batches": [{"topics": [
        {"topic": "backup", "survivor": "guidelines/implementing/data/backup",
         "copies": [{"folder": "guidelines/shipping/backup"}]}]}]}), encoding="utf-8")
    (d / "area-plan.md").write_text(_plan_text(d).replace(
        "## Gaps\n\ng\n", "## Gaps\n\n- shipping/backup holds restore drills.\n\n- shipping/backup is now "
                          "implementing/data/backup.\n"), encoding="utf-8")
    approve(d)
    s = run(tmp_path)
    assert [(r["pointer"], r["survivor"], r["section"]) for r in s["stale_pointer"]] == [
        ("shipping/backup", "implementing/data/backup", "Gaps")], s["stale_pointer"]
    assert "stale_pointer" not in s["next_why"] and "stale_pointer" not in stage_status.DIGEST_KEYS   # advisory


def _folded_plan(tmp_path: Path, gaps: str, reference: list | None = None) -> dict:
    """status() of a plan whose Gaps section is `gaps`, the worklist folding shipping/backup into
    implementing/data/backup."""
    cookr_skill(tmp_path)
    d = area(tmp_path, {"rows": f"cookbook/guidelines/{AREA}/rows"})
    ws = tmp_path / "docs" / "grow-cookbook"
    (ws / "worklist.json").write_text(json.dumps({"batches": [{"topics": [
        {"topic": "backup", "survivor": "guidelines/implementing/data/backup",
         "copies": [{"folder": "guidelines/shipping/backup"}]}]}]}), encoding="utf-8")
    if reference is not None:
        (d / "reference.json").write_text(json.dumps(reference), encoding="utf-8")
    (d / "area-plan.md").write_text(_plan_text(d).replace("## Gaps\n\ng\n", "## Gaps\n\n" + gaps), encoding="utf-8")
    approve(d)
    return run(tmp_path)


def test_stale_pointer_reads_a_list_item_whole_and_accepts_a_word_saying_the_copy_is_folded(tmp_path):
    # G234 (L12, 1.4.40): the copy and the survivor on adjacent wrapped lines of one bullet are clean; a line
    # holding `folded`, `fold` or `merged into` beside the copy is clean; a bare copy still flags, with the matched
    # text and its column.
    s = _folded_plan(tmp_path, "- shipping/backup holds drills; see\n  implementing/data/backup for them.\n"
                               "- shipping/backup is folded away.\n- shipping/backup was merged into it.\n"
                               "- shipping/backup holds restore drills.\n")
    [row] = s["stale_pointer"]
    assert (row["pointer"], row["line"], row["matched"], row["column"]) == (
        "shipping/backup", row["line"], "shipping/backup", 3), row
    assert "folded" in row["why"] and "merged into" in row["why"] and "whole list item" in row["why"], row["why"]


def test_stale_pointer_skips_a_speciality_id_a_fold_list_and_a_quoted_line(tmp_path):
    # G235 (L13, 1.4.40): a backticked token naming one of this plan's specialities is no folder use; neither is a
    # list item under an intro that says the copies are folded, nor a `>` quoted line; the folder use still flags.
    gaps = ("- The speciality `shipping/backup` reads it.\n- shipping/backup holds drills.\n\n"
            "The copies this plan folds are:\n\n- shipping/backup\n\n> shipping/backup quoted Why cell\n")
    s = _folded_plan(tmp_path, gaps, reference=[{"speciality": "shipping/backup", "file": "x"}])
    assert [(r["line"], r["column"]) for r in s["stale_pointer"]] == [(s["stale_pointer"][0]["line"], 3)], s
    assert len(s["stale_pointer"]) == 1


def test_rows_takes_several_keys_and_keys_counts_other_plans_changed(tmp_path, capsys):
    # G219 (L34, 1.4.39): --rows a,b prints each key; --keys prints
    # other_plans_changed as its count and plan names.
    a, b, ws = _citing_pair(tmp_path)
    args = ["--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path)]
    assert stage_status.main(args + ["--rows", "next,other_plans_changed"]) == 0
    out = json.loads(capsys.readouterr().out)
    full = run(tmp_path)
    assert out == {"next": full["next"], "other_plans_changed": full["other_plans_changed"]}
    assert stage_status.main(args + ["--keys"]) == 0
    assert json.loads(capsys.readouterr().out)["other_plans_changed"] == {"rows": 1, "plans": ["planning/ui"]}


def test_rows_of_another_scripts_key_names_that_script(tmp_path, capsys):
    # G220 (L35, 1.4.39).
    a, b, ws = _citing_pair(tmp_path)
    args = ["--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path)]
    assert stage_status.main(args + ["--rows", "held_by_wording"]) == 2
    assert "run_gaps.py" in capsys.readouterr().err
    assert stage_status.main(args + ["--rows", "home_recorded"]) == 2
    err = capsys.readouterr().err
    assert "run_gaps.py" in err and "home_unguessed" in err, err


def test_the_digest_is_followed_by_the_advisory_counts_on_stderr(tmp_path, capsys):
    # G195 (L10, 1.4.39): after the digest, one stderr line counts the advisory lists it leaves out.
    a, b, ws = _citing_pair(tmp_path)
    assert stage_status.main(["--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--digest"]) == 0
    c = capsys.readouterr()
    assert "host_check 0" in c.out
    assert "advisory (not in the digest): other_plans_changed 1; survivor_carries 0; carries_asked 0" in c.err, c.err


def _held_report(d, rows):
    (d / "run_gaps.json").write_text(json.dumps({"stale_reference": [], "reference_format": FORMAT,
                                                 "held_by_wording": rows}), encoding="utf-8")


def test_a_reset_verdict_is_a_stale_verdicts_row_that_holds_at_plan_and_clears_when_rejudged(tmp_path, capsys):
    # G251 (1.4.41): a held_by_wording row with `verdict_was` and no `verdict` is a stale_verdicts row; `next` is
    # plan, `next_why` says it, --keys prints the row; a row with a current verdict (re-recorded) clears it.
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    assert run(tmp_path)["stale_verdicts"] == [] and run(tmp_path)["next"] != "plan"
    reset = {"id": "sp:1@keys", "speciality": "sp", "n": 1, "topic": "keys", "text": "Do x.", "verdict_was": "not",
             "verdict_why": "the piece or the topic sentence changed since the verdict was recorded"}
    _held_report(d, [reset, {"id": "sp:2@keys", "speciality": "sp", "n": 2, "topic": "keys", "text": "Do y.",
                              "verdict": "held"}])
    s = run(tmp_path)
    [row] = s["stale_verdicts"]
    assert (row["id"], row["verdict_was"]) == ("sp:1@keys", "not") and row["topic"] == "keys", row
    assert s["next"] == "plan" and "stale_verdicts" in s["next_why"]
    cookr_skill(tmp_path)
    (tmp_path / "cookbook").mkdir(exist_ok=True)
    args = ["--area", AREA, "--workspace", str(tmp_path / "docs" / "grow-cookbook"),
            "--repo", str(tmp_path), "--keys"]
    assert stage_status.main(args) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["stale_verdicts"][0]["id"] == "sp:1@keys", shown["stale_verdicts"]
    _held_report(d, [{**reset, "verdict": "not"}])
    s = run(tmp_path)
    assert s["stale_verdicts"] == [] and s["next"] != "plan"


def test_stale_pointer_reads_only_cites_never_prose_a_bold_heading_or_a_table_cell_of_more_than_the_path(tmp_path):
    # gapfix13 (G258, 1.4.42): a cite is the copy's folder in a list item, as a whole table cell or as a link
    # target (tools.md); an explaining paragraph, a whole-bold heading paragraph, a `#` heading and a table cell
    # holding more than the path are not read. The list item, the whole cell and the link still flag.
    gaps = ("We moved what shipping/backup said into the survivor.\n\n**shipping/backup drills**\n\n"
            "### shipping/backup\n\n| folder | note |\n|---|---|\n| x | the `shipping/backup` row |\n"
            "| `shipping/backup` | drills |\n\nSee [drills](cookbook/guidelines/shipping/backup).\n\n"
            "- shipping/backup holds drills.\n")
    s = _folded_plan(tmp_path, gaps)
    lines = gaps.splitlines()
    want = sorted(i for i, x in enumerate(lines) if x.startswith("| `shipping") or x.startswith("See [")
                  or x.startswith("- shipping"))
    base = s["stale_pointer"][0]["line"] - want[0]
    assert sorted(r["line"] - base for r in s["stale_pointer"]) == want, s["stale_pointer"]


def test_cite_moved_reads_question_numbers_split_by_a_slash_or_or(tmp_path):
    # gapfix13 (G258, 1.4.42): "its Research question 1/2" and "questions 1 or 2" cite 1 and 2; renumbering
    # planning/ui's questions moves both.
    a, b, ws = _cited_plan_with_questions(tmp_path, "planning/ui: its Research question 2/3 carry it.")
    approve(a.parent)
    assert run(tmp_path)["cite_moved"] == []
    b.write_text(b.read_text(encoding="utf-8").replace(
        "1. **Alpha** (missing subject 1)", "1. **New** (missing subject 0): n?\n2. **Alpha** (missing subject 1)", 1),
        encoding="utf-8")
    rows = run(tmp_path)["cite_moved"]
    assert sorted((r["was"], r["now"]) for r in rows) == [("Beta", "Alpha"), ("Gamma", "Beta")], rows


def test_the_name_plan_alias_matches_only_the_exact_area_name(tmp_path):
    # gapfix13 (G258, 1.4.42): "the ui plan" no longer cites planning/ui; "the planning/ui plan" does, and a
    # one-segment area is cited by "the brainstorming plan".
    a, b, ws = _citing_pair(tmp_path)
    a.write_text(a.read_text(encoding="utf-8").replace("See planning/ui.\n", "See the ui plan.\n"), encoding="utf-8")
    _other_plan(tmp_path, "brainstorming", "# B\n")
    assert [r["plan"] for r in run(tmp_path)["other_plans_changed"]] == []
    a.write_text(a.read_text(encoding="utf-8").replace("See the ui plan.\n", "See the brainstorming plan.\n"),
                 encoding="utf-8")
    assert [r["plan"] for r in run(tmp_path)["other_plans_changed"]] == ["brainstorming"]


def test_stale_verdicts_reads_the_live_held_json_not_the_reports_copy(tmp_path):
    # gapfix13 (G269, 1.4.42): a verdict re-recorded after the report was saved clears its row before any re-run;
    # a recorded verdict whose text no longer matches the row's is listed though the report showed it current.
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    reset = {"id": "sp:1@keys", "speciality": "sp", "n": 1, "topic": "keys", "text": "Do x.", "verdict_was": "not",
             "verdict_why": "changed"}
    current = {"id": "sp:2@keys", "speciality": "sp", "n": 2, "topic": "keys", "text": "Do y.", "verdict": "held"}
    _held_report(d, [reset, current])
    (d / "held.json").write_text(json.dumps({
        "sp:1@keys": {"verdict": "not", "why": "re-judged", "text": "Do x."},
        "sp:2@keys": {"verdict": "held", "why": "old", "text": "Do y, once."}}), encoding="utf-8")
    [row] = run(tmp_path)["stale_verdicts"]
    assert (row["id"], row["verdict_was"]) == ("sp:2@keys", "held") and "G159" in row["why"], row


def test_report_refresh_names_the_command_when_the_report_is_older_than_the_skill_or_its_verdicts(tmp_path):
    # gapfix13 (G269, 1.4.42): advisory; a report saved by another skill version, or older than held.json,
    # names the run that refreshes it. A current report has no row.
    import os
    from repo_path import skill_version
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    _held_report(d, [])
    [row] = run(tmp_path)["report_refresh"]
    assert "before 1.4.42" in row["why"] and "run_gaps.py --area" in row["why"] and "--hints" in row["why"], row
    rep = json.loads((d / "run_gaps.json").read_text())
    (d / "run_gaps.json").write_text(json.dumps({**rep, "skill_version": skill_version(), "area": AREA}))
    assert run(tmp_path)["report_refresh"] == []
    (d / "held.json").write_text("{}")
    t = (d / "run_gaps.json").stat().st_mtime
    os.utime(d / "held.json", (t + 5, t + 5))
    [row] = run(tmp_path)["report_refresh"]
    assert "held.json changed after it was saved" in row["why"] and f"--area {AREA} " in row["why"], row


def test_non_home_lacking_rows_are_their_own_key_printed_whole_by_keys(tmp_path, capsys):
    # gapfix13 (G256, 1.4.42): a counted, unjudged lacking piece at a topic that is not its home is its own
    # advisory key; --keys prints its rows.
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    rows = [{"id": "lacking:sp:1@keys", "topic": "keys", "home": "other"}]
    (d / "run_gaps.json").write_text(json.dumps({"stale_reference": [], "reference_format": FORMAT,
                                                 "held_by_wording": [], "non_home_lacking": rows}))
    assert run(tmp_path)["non_home_lacking"] == rows
    cookr_skill(tmp_path)
    (tmp_path / "cookbook").mkdir(exist_ok=True)
    assert stage_status.main(["--area", AREA, "--workspace", str(tmp_path / "docs" / "grow-cookbook"),
                              "--repo", str(tmp_path), "--keys"]) == 0
    assert json.loads(capsys.readouterr().out)["non_home_lacking"] == rows


def test_host_check_skips_a_section_name_or_topic_name_label_reads_a_new_heading_and_lists_a_tie(tmp_path):
    # gapfix13 (G264, 1.4.42): "**Missing subjects**" and a bold topic name leading a bullet are labels, not
    # subjects; "### cache-keys (new)" hosts in cache-keys; a tie row carries `tie` with every tying topic.
    research = ("### design-tokens\n\n1. **Missing subjects** 4 and 5: which names?\n"
                "2. **Cache keys**: what do they hold?\n\n"
                "### cache-keys (new)\n\n1. **Cache key rotation**, carried, no host: x?\n\n"
                "### cache-keys\n\n1. **Cache warming**, carried, no host: x?\n")
    s = _hosting_plan(tmp_path, research)
    rows = {r["subject"]: r for r in s["host_check"]}
    assert set(rows) == {"Cache warming"}, s["host_check"]
    assert rows["Cache warming"]["tie"] == ["cache-eviction", "cache-keys"], rows


def test_record_others_write_says_written_or_no_change_and_a_no_op_exits_0(tmp_path, capsys):
    # gapfix13 (G265, 1.4.42): --record-others --write says what it did; a run that finds every line in place
    # prints `no change` and exits 0.
    a, b, ws = _citing_pair(tmp_path)
    a.write_text(a.read_text(encoding="utf-8").replace("## Step-4 re-check\n\nr\n",
                                                       "## Step-4 re-check\n\n### On 1.4.42\n\nr\n"),
                 encoding="utf-8")
    args = [AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--record-others", "--write"]
    capsys.readouterr()
    assert stage_status.main(args) == 0
    assert "written" in capsys.readouterr().err
    after = a.read_text(encoding="utf-8")
    assert stage_status.main(args) == 0 and a.read_text(encoding="utf-8") == after
    assert "no change" in capsys.readouterr().err


def test_first_check_writes_the_three_digest_lines_in_order_saving_an_old_copy_by_the_running_version(tmp_path,
                                                                                                      capsys):
    # gapfix13 (G262, G267, 1.4.42): one command writes A/first-check.txt: the digest line of
    # `unmeasured.py --check --digest`, of `run_gaps.py --check --hints --digest` and of `stage_status.py --digest`,
    # in that order, one per line, nothing else; an old first-check.txt is first saved as
    # first-check-before-<running version>.txt, and a backup of that name already there is never overwritten.
    d = area(tmp_path, {"x": f"cookbook/guidelines/{AREA}/x"})
    ws = tmp_path / "docs" / "grow-cookbook"
    calls = []

    def runner(cmd):
        calls.append(cmd)
        name = Path(cmd[1]).name
        return 1 if name == "run_gaps.py" else 0, f"noise\n{name} digest\n", "advisory\n"

    assert stage_status.first_check(AREA, ws, tmp_path, runner) == 0
    v = stage_status.skill_version()
    want = "unmeasured.py digest\nrun_gaps.py digest\nstage_status.py digest\n"
    assert (d / "first-check.txt").read_text(encoding="utf-8") == want
    assert [Path(c[1]).name for c in calls] == ["unmeasured.py", "run_gaps.py", "stage_status.py"]
    assert [c[2:] for c in calls] == [
        ["--check", "--digest", "--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path)],
        ["--check", "--hints", "--digest", "--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path)],
        ["--digest", "--area", AREA, "--workspace", str(ws), "--repo", str(tmp_path)]]
    assert not (d / f"first-check-before-{v}.txt").exists()
    (d / "first-check.txt").write_text("old\n", encoding="utf-8")
    assert stage_status.first_check(AREA, ws, tmp_path, runner) == 0
    assert (d / f"first-check-before-{v}.txt").read_text(encoding="utf-8") == "old\n"
    assert (d / "first-check.txt").read_text(encoding="utf-8") == want
    assert stage_status.first_check(AREA, ws, tmp_path, runner) == 0      # the backup is kept as it is
    assert (d / f"first-check-before-{v}.txt").read_text(encoding="utf-8") == "old\n"
    assert not list(d.glob("*.tmp*"))


def test_first_check_writes_nothing_when_a_check_fails(tmp_path, capsys):
    d = area(tmp_path, {"x": f"cookbook/guidelines/{AREA}/x"})
    ws = tmp_path / "docs" / "grow-cookbook"
    (d / "first-check.txt").write_text("old\n", encoding="utf-8")
    assert stage_status.first_check(AREA, ws, tmp_path, lambda cmd: (2, "", "boom\n")) == 2
    assert (d / "first-check.txt").read_text(encoding="utf-8") == "old\n"
    assert "boom" in capsys.readouterr().err
    assert not list(d.glob("first-check-before-*"))


def test_short_not_owed_rows_are_an_advisory_key_read_from_the_saved_report(tmp_path):
    # gapfix13b (platform-integration#5, 1.4.42): the saved report's short_not_owed rows, never a hold.
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    rows = [{"id": "short:sp:4", "topic": "keys", "marked_for": "reviewing/data", "counted_at": ["reviewing/data"],
             "why": "x"}]
    (d / "run_gaps.json").write_text(json.dumps({"stale_reference": [], "reference_format": FORMAT,
                                                 "held_by_wording": [], "short_not_owed": rows}))
    s = run(tmp_path)
    assert s["short_not_owed"] == rows and "short_not_owed" in stage_status.ADVISORY_KEYS


def test_a_stale_verdict_row_carries_the_old_and_current_rule_text_and_the_topic_files(tmp_path):
    # gapfix13b (language#3, G269, 1.4.42): a reset row shows the piece, the rule and topic sentence the verdict
    # was recorded on and the current ones, where the rule is, and the topic files the sentences are read from
    # (each part artifact.json lists, but history); the digest is unchanged by these fields.
    cookr_skill(tmp_path)
    artifact(tmp_path / f"cookbook/guidelines/{AREA}/keys")
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    row = {"id": "sp:1@keys", "speciality": "sp", "n": 1, "topic": "keys", "text": "Index keys.",
           "topic_sentence": "Every foreign key MUST have an index.", "rule_sentence": "Keys MUST be indexed.",
           "rule_at": "rules sentence 2", "topic_hash": "new"}
    _held_report(d, [row])
    (d / "held.json").write_text(json.dumps({"sp:1@keys": {
        "verdict": "held", "why": "w", "text": "Index keys.", "topic_sentence": "Every foreign key MUST have an index.",
        "rule_sentence": "Keys SHOULD be indexed.", "topic_hash": "old"}}), encoding="utf-8")
    s = run(tmp_path)
    [r] = s["stale_verdicts"]
    assert (r["rule_sentence_was"], r["rule_sentence_now"]) == ("Keys SHOULD be indexed.", "Keys MUST be indexed."), r
    assert r["topic_sentence_was"] == r["topic_sentence_now"] == "Every foreign key MUST have an index."
    assert (r["text"], r["rule_at"]) == ("Index keys.", "rules sentence 2"), r
    base = f"cookbook/guidelines/{AREA}/keys/"
    assert r["topic_files"] == [base + p + ".md" for p in ("intro", "rules", "look-for", "review-bar", "build-bar")]
    slim = {**s, "stale_verdicts": [{k: r[k] for k in ("id", "speciality", "n", "topic", "verdict_was", "why")}]}
    assert stage_status.digest(s) == stage_status.digest(slim)


def test_a_stale_verdict_row_carries_the_severity_cell_of_its_rule_row(tmp_path):
    # gapfix14 (G279, skills-and-agents#7): the Severity of a checklist rule row, readable without opening the topic.
    cookr_skill(tmp_path)
    artifact(tmp_path / f"cookbook/guidelines/{AREA}/keys")
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    row = {"id": "sp:1@keys", "speciality": "sp", "n": 1, "topic": "keys", "text": "Index keys.",
           "topic_sentence": "t", "rule_sentence": "| C1 | Keys are indexed | FAIL |", "topic_hash": "new"}
    _held_report(d, [row])
    (d / "held.json").write_text(json.dumps({"sp:1@keys": {
        "verdict": "held", "why": "w", "text": "Index keys.", "topic_sentence": "t",
        "rule_sentence": "| C1 | Keys are indexed | WARN |", "topic_hash": "old"}}), encoding="utf-8")
    [r] = run(tmp_path)["stale_verdicts"]
    assert (r["rule_severity_was"], r["rule_severity_now"]) == ("WARN", "FAIL"), r


def test_a_tie_topic_named_in_any_case_or_before_a_hyphen_counts_and_the_row_says_what_is_missing(tmp_path):
    # gapfix13b (language#5, G209, 1.4.42): "Cache-eviction timing" names cache-eviction (case-folded; a hyphen
    # joins a word that makes no other topic's name); the row of an unsettled tie names the unnamed topics and
    # whether an Owner questions item's whole bold lead is the subject.
    owner = OWNER_Q + "2. **Cache warming**: a topic?\n"
    research = "### cache-keys\n\n1. **Cache warming**, carried, no host: Cache-eviction timing?\n"
    assert _hosting_plan(tmp_path / "a", research, owner)["host_check"] == []
    [row] = _hosting_plan(tmp_path / "b", research)["host_check"]
    assert (row["unnamed"], row["owner_item"]) == ([], False), row
    assert "whole bold lead of an Owner questions item" in row["why"], row
    research = "### cache-keys\n\n1. **Cache warming**, carried, no host: x?\n"
    [row] = _hosting_plan(tmp_path / "c", research, owner)["host_check"]
    assert (row["unnamed"], row["owner_item"]) == (["cache-eviction"], True), row
    assert "cache-eviction" in row["why"]


def test_names_topic_reads_a_hyphen_joined_word_but_not_another_topics_name():
    # gapfix13b (language#5, 1.4.42)
    tw = {"swift": {}, "swift-concurrency": {}, "objective-c": {}}
    assert stage_status.names_topic("Objective-C Swift-import annotations", "swift", tw)
    assert stage_status.names_topic("Objective-C Swift-import annotations", "objective-c", tw)
    assert not stage_status.names_topic("uses swift-concurrency only", "swift", tw)
    assert not stage_status.names_topic("swiftly", "swift", tw)


def test_a_stale_report_names_its_stale_views_and_the_refresh_command_in_the_digest_line(tmp_path):
    # gapfix14 (G291, implementing-internationalization#2: the first-check line read stale_verdicts 0 while a
    # re-measure showed 4): a report older than a hand hold (mark.py --hold) is stale too; the row names the views
    # read from it, and the digest line says so with the one command that refreshes it.
    import os
    from repo_path import skill_version
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    _held_report(d, [])
    rep = json.loads((d / "run_gaps.json").read_text())
    (d / "run_gaps.json").write_text(json.dumps({**rep, "skill_version": skill_version(), "area": AREA}))
    s = run(tmp_path)
    assert s["report_refresh"] == [] and "report_refresh" not in stage_status.digest(s)
    (d / "hand_holds.json").write_text("{}")
    t = (d / "run_gaps.json").stat().st_mtime
    os.utime(d / "hand_holds.json", (t + 5, t + 5))
    s = run(tmp_path)
    [row] = s["report_refresh"]
    assert "hand_holds.json changed after it was saved" in row["why"], row
    assert "stale_verdicts" in row["stale_views"] and "measured_total" in row["stale_views"], row
    line = stage_status.digest(s)
    assert f"report_refresh 1 (stale: {', '.join(row['stale_views'])}; refresh: $COOKR_PY run_gaps.py --area {AREA}" \
        in line and "--hints)" in line, line
    assert line.split("; result ")[1].split(";")[0] == stage_status.digest({**s, "report_refresh": []}).split(
        "; result ")[1]     # the hash is the holds' alone


def test_first_check_says_it_rewrote_first_check_txt_when_its_backup_is_already_there(tmp_path, capsys):
    # gapfix14 (G290, reviewing-language#1): "kept as it is" read as if nothing was written.
    d = area(tmp_path, {"x": f"cookbook/guidelines/{AREA}/x"})
    ws = tmp_path / "docs" / "grow-cookbook"
    (d / "first-check.txt").write_text("old\n", encoding="utf-8")
    (d / f"first-check-before-{stage_status.skill_version()}.txt").write_text("older\n", encoding="utf-8")
    assert stage_status.first_check(AREA, ws, tmp_path, lambda cmd: (0, f"{Path(cmd[1]).name} digest\n", "")) == 0
    err = capsys.readouterr().err
    assert "kept as it is" in err and "first-check.txt rewritten" in err, err


def test_record_others_write_sets_a_new_list_off_by_a_blank_line_and_a_no_op_says_the_hashes_are_current(
        tmp_path, capsys):
    # gapfix14 (G295, planning-infrastructure#4, implementing-documentation#6): a new list abutted the lead-in
    # sentence; `no change` did not say the recorded hashes are current.
    a, b, ws = _citing_pair(tmp_path)
    a.write_text(a.read_text(encoding="utf-8").replace("## Step-4 re-check\n\nr\n",
                                                       "## Step-4 re-check\n\n### On 1.4.43\n\nLead-in line.\n"),
                 encoding="utf-8")
    args = [AREA, "--workspace", str(ws), "--repo", str(tmp_path), "--record-others", "--write"]
    assert stage_status.main(args) == 0
    h = stage_status.content_hash_of(b.read_text(encoding="utf-8"))
    assert f"Lead-in line.\n\n- `planning/ui/area-plan.md {h}`\n" in a.read_text(encoding="utf-8")
    capsys.readouterr()
    assert stage_status.main(args) == 0
    assert "no change: every recorded hash is current" in capsys.readouterr().err


def test_cited_at_in_the_why_is_compressed_to_line_ranges_and_a_count(tmp_path):
    # gapfix14 (G296, implementing-performance#6): `why` printed one `line N` per cite, cut at 12 with "and more";
    # it now gives the count and runs of consecutive lines, every line covered.
    assert stage_status.line_ranges([3, 4, 5, 9, 11, 12]) == "6 lines: 3-5, 9, 11-12"
    assert stage_status.line_ranges([7]) == "1 line: 7"
    a, b, _ = _citing_pair(tmp_path)
    a.write_text(a.read_text(encoding="utf-8").replace(
        "See planning/ui.\n", "See planning/ui.\n" + "planning/ui again.\n" * 14), encoding="utf-8")
    rows = run(tmp_path)["other_plans_changed"]
    at = rows[0]["cited_at"]
    assert len(at) == 15 and f"cited at {stage_status.line_ranges(at)}" in rows[0]["why"], rows[0]["why"]
    assert "and more" not in rows[0]["why"]


def test_keys_view_gives_a_stale_verdict_rows_topic_files_as_a_count_and_rows_gives_the_paths(tmp_path, capsys):
    # gapfix14 (G298, reviewing-documentation#7): `--keys` printed every topic file on every stale_verdicts row, so
    # four rows ran to several screens; `--keys` now counts them and `--rows stale_verdicts` keeps the paths.
    cookr_skill(tmp_path)
    artifact(tmp_path / f"cookbook/guidelines/{AREA}/keys")
    d = area(tmp_path, {"keys": f"cookbook/guidelines/{AREA}/keys"})
    _held_report(d, [{"id": "sp:1@keys", "speciality": "sp", "n": 1, "topic": "keys", "text": "Index keys.",
                      "topic_sentence": "t", "rule_sentence": "Keys MUST be indexed.", "rule_at": "rules sentence 2",
                      "topic_hash": "new"}])
    (d / "held.json").write_text(json.dumps({"sp:1@keys": {"verdict": "held", "why": "w", "text": "Index keys.",
                                                           "topic_sentence": "t", "topic_hash": "old"}}),
                                 encoding="utf-8")
    args = ["--area", AREA, "--workspace", str(tmp_path / "docs" / "grow-cookbook"), "--repo", str(tmp_path)]
    capsys.readouterr()
    assert stage_status.main(args + ["--keys"]) == 0
    [row] = json.loads(capsys.readouterr().out)["stale_verdicts"]
    assert row["topic_files"] == {"files": 5, "paths": "--rows stale_verdicts"}, row
    assert stage_status.main(args + ["--rows", "stale_verdicts"]) == 0
    [row] = json.loads(capsys.readouterr().out)["stale_verdicts"]
    assert len(row["topic_files"]) == 5 and all(p.endswith(".md") for p in row["topic_files"])
