---
name: grow-cookbook
version: "1.4.46"
description: "Add or rewrite cookbook guidelines from research, one area at a time: plan the area, research each topic, write it with cited rules, review, integrate."
argument-hint: "<plan|research|write|review|integrate> <area> [--workspace <dir>] [--topic <name>]"
allowed-tools: Read, Glob, Grep, Edit, Write, Agent, Skill, Bash(PYTHONPATH=*), Bash(myteams *), Bash(git *), Bash(python3 *), Bash(~/.cache/grow-cookbook/cookr-venv/bin/python *), Bash(date *), Bash(mkdir *), Bash(cat *), Bash(cp *), Bash(mv *), Bash(rm *)
---

# Grow Cookbook v1.4.46

The procedure for adding to the cookbook: an area is planned, each topic in it
is researched, written as a roled guideline whose every rule cites its
research, reviewed by someone who did not write it, and integrated. Every
artifact is written from research on its topic, never from what we already
know, from the devteam's text, or from memory.

Who does what (cookr, the teams, the helper scripts, the other skills) is in
[references/tools.md](references/tools.md); read it before stage 1.

Each stage below gives its purpose, its steps as commands, and what decides
the next step; its rules, edge cases and file formats are in its reference
file, numbered as here, which it says to read before running it. A run of
all five on one topic: [references/example.md](references/example.md).

## COOKR_PY

`$COOKR_PY` is the Python that runs cookr: Python 3.11 or later that imports
`rich`, `questionary` and `yaml` (pyyaml). A plain `python3` often lacks them.
Set it once, at startup (step 1 below):
- `python3`, when `python3 -c "import rich, questionary, yaml"` exits 0;
- otherwise `~/.cache/grow-cookbook/cookr-venv/bin/python`, made once with:
  ```
  python3 -m venv ~/.cache/grow-cookbook/cookr-venv
  ~/.cache/grow-cookbook/cookr-venv/bin/python -m pip install rich questionary pyyaml
  ```

Shell variables do not carry from one command to the next, so write its value,
the path itself, wherever a command below says `$COOKR_PY`. Every cookr command
and every example below runs under it. The helper scripts in
`${CLAUDE_SKILL_DIR}/scripts/` need only the standard library and run under it too. `speciality_reference.py` is
not one of them: it is the devteam's, at `<devteam>/speciality_reference.py` (`<devteam>`: the agenticdevteam
checkout two folders above `<repo>`, run_gaps.py's `--devteam` default; 1.4.43, G274). Stage 1 starts with
`devteam_checkout.py --repo <repo>`, which prints `<devteam>`, or, with no such checkout, exits 2 with one
plain message naming what stage 1 needs; pass `--devteam <checkout>` to it and to `run_gaps.py` for a
checkout elsewhere (1.4.45). Stages 2 to 5 need no devteam checkout. One python, `$COOKR_PY`,
runs every script, the devteam's included; a brief naming another venv for it changes nothing (G278); a plain `python3` without cookr fails `run_gaps.py` with "Unknown option: -P" or "No module named", and each script then names `$COOKR_PY` (1.4.42, G269).

## Startup

grow-cookbook v1.4.46

If `$ARGUMENTS` is `--version`, respond with exactly `grow-cookbook v1.4.46` and stop.

1. Check `$COOKR_PY`:
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/check_cookr_python.py
   ```
   It prints JSON `{"python", "version", "missing", "too_old", "ok"}`. **When
   it exits 2, stop**: say "COOKR_PY (`<python>`) cannot run cookr: it
   cannot import `<missing>`" (or "it is Python `<version>`; cookr needs 3.11
   or later"), give the two set-up lines under *COOKR_PY*, and do nothing
   else.

Parse `$ARGUMENTS`:
- `<stage>`: `plan`, `research`, `write`, `review` or `integrate`. With no
  stage, print the five stages below and the area's status (below), then stop.
- `<area>`: the area's path below `cookbook/guidelines/`, e.g.
  `implementing/feature-management`.
- `--workspace <dir>`: where the stage files live. Default:
  `docs/grow-cookbook/` in this repo.
- `--topic <name>`: run stages 2–5 on one topic of the area only.

`<repo>` is this cookbook checkout's root, the checkout this skill lives in:
`git -C ${CLAUDE_SKILL_DIR} rev-parse --show-toplevel`. That gives the
cookbook from any current directory, even one inside another repo that
holds the cookbook as a submodule; a bare `git rev-parse --show-toplevel`
would give that outer repo. Pass `--repo <repo>` to every script (`repo_path.py`).
Every stage reads and writes files under `A = <workspace>/areas/<area>/`, and a
topic's files under `A/topics/<topic>/`. `A` is always an absolute path (a
relative `<workspace>` is relative to the current directory, as any file
argument is; with no `--workspace` it is `<repo>/docs/grow-cookbook`), so
every `A/...` in a command below names the same file whatever the current
directory. A stage reads only the files the
stages before it wrote, so any stage can be re-run alone. A stage whose input
file is missing stops and names the stage that writes it.

**The cookr this skill runs** is this checkout's own, never an installed one:

```
PYTHONPATH=<repo>/skills/cookr/cli $COOKR_PY -P -m cookr -p <repo> <command>
```

Below, `cookr <command>` always means that whole line. cookr may be run from any
directory: an artifact path below, relative to `<repo>`, resolves against the `-p <repo>`
the line carries, and an absolute path works too. Any other file argument, such
as `roles gaps --against <file>`, resolves against the current directory like
any command's file argument, which is why `A` is absolute.

**Where the area stands.** Before every stage, run
```
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/stage_status.py --area <area> --workspace <workspace> --repo <repo>
```
**When it exits 2, stop** and show its message: `<repo>` holds no cookbook
(no `cookbook/` or no `skills/cookr/SKILL.md`), so `<repo>` was derived
wrongly. It prints JSON:
- `cookr`: this checkout's cookr version (from `skills/cookr/SKILL.md`) and
  whether it is at least 0.21.4. **When `cookr.ok` is false, stop**: say
  "this checkout's cookr is `<version>`; /grow-cookbook needs 0.21.4 or later"
  and do nothing else. An older cookr has no `roles gaps`, which stage 1
  measures with, and before 0.19.5 no Research check, so `validate` would
  pass research that is missing, and no `validate --research`, which stage 2
  ends with. Before 0.21.0, `validate` flags as the owner's every rule citing
  any claim of an unsupported or contradicted verdict, not only its prior
  claim, and `roles lossless` reports `---` lines and a repeated title as
  lost sentences. Before 0.21.3, `roles lossless` has no `--retarget` and
  does not refuse a second retarget (0.21.1 ignores a `retargeted` record
  outright), so stage 5's one-retarget guarantee would be absent; before
  0.21.4, `--retarget` accepts targets that trip, spending the one retarget
  on them.
- whether the plan exists, and whether its approval is `current` (it names
  the plan's `git hash-object` and `reference-hash`, A/reference.json's, 1.4.30).
- per topic: its `artifact` (below), which stage files exist, the `next`
  stage it owes, its review `rounds`, the copies to `fold` in stage 5, and
  the findings for the `owner` once its rounds are spent (for an
  integrated topic, the findings siblings routed to its `integrate.md`, each
  `from <sibling>'s review: <finding>`). Until the plan
  exists every topic's `next` is `plan`, and until its approval is current,
  `approve`: no topic owes research before then. A topic the plan lists as
  `merged` into a folder of another area has `merged` set to that folder,
  `next` null and `why` `merged into <folder>`: it owes nothing in this
  area, not approval and not research (stage 1 below).

A stage that is not the topic's `next`, or an earlier one being re-run, is a re-run: say so before starting.

**`<artifact>`** is the topic's `artifact` in that JSON: its source folder, relative to `<repo>`. Stage 1 records it in the plan's *Proposed topics* table, so a topic folded into another area's topic or created under another area is found where the plan put it. A topic the plan does not place is `cookbook/guidelines/<area>/<topic>`.

## The four questions

Every topic's research answers these four questions, each as its own section (R10 of the finish-the-cookbook-roles plan, verbatim):

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

The devteam's text and the existing artifact are inputs to check against the research, never a source in themselves.

## Stage 1: Plan the area

Measure what the area lacks against the devteam's specialities and propose its topics to the owner. **Before running stage 1, read [references/stage-1.md](references/stage-1.md).**

1. Measure the gaps. Every command that writes a file runs under `write_on_success.py`, never a `>` redirect, except a script that writes its own files: `run_gaps.py`, `mark.py`, `stage_status.py --first-check` and `--record-others --write` (G267).
   1. The area's reference files, once per area:
      ```
      $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/devteam_checkout.py --repo <repo>
      mkdir -p A/reference A/gaps
      $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py A/reference.json -- $COOKR_PY <devteam>/speciality_reference.py --area <area> --worklist <workspace>/worklist.json --workspace <workspace> --out A/reference
      ```
   2. The specialities with no topic yet:
      ```
      $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py A/unmeasured.json -- $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/unmeasured.py --area <area> --workspace <workspace> --reference A/reference.json --repo <repo>
      ```
      and each building speciality, quoted once and marked by area, then run
      again with `--marks A/building-<name>.json` into `A/building-<name>-quoted.json` (an exit 0 whose one stderr line says "marks kept (sentences unchanged)" leaves the marked file as it was, 1.4.37, G168; `--quiet` on the `--marks` run leaves `markdown` out; an exit 2 from the template keeps the marked file, which it cannot read; stage-1.md *A re-run*):
      ```
      $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py A/building-<name>.json -- $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/quote_building.py --area <area> --speciality <speciality> --file <file> --repo <repo> --keep A/building-<name>.json
      ```
      Quote all it lists: `building`, `marked_here`, `mark_conflicts` (step 1.2 of stage-1.md; set a mark with `mark.py`); name each `unread_marks` file to the owner under **Owner questions**. On exit 2 with `unplaced` rows, stop the stage and name each speciality and its `why` to the owner.
   3. Each existing topic, against every speciality it stands on, less `survivor_elsewhere` rows: `run_gaps.py` builds and runs each `cookr roles gaps <topic-folder> --against ... --json` into `A/gaps/<topic>.json` (a re-run clears only the stale files it wrote itself, never R9's `new-<name>.json`, which stay hand-built):
      ```
      $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/run_gaps.py --area <area> --workspace <workspace> --repo <repo> --hints
      ```
      `home_guess` and `gap_candidates` are an advisory guess; the plan names each home: each building sentence is judged once, at its home topic, each of `unmeasured_sentences` by hand (stage-1.md step 1.3): its `measured_pieces` are never a verdict on the sentence. `--hints` adds `paraphrase_hints.py`'s advisory ranking, over every measured topic where no home is guessed. An R9 measure (`new-<name>.json`, stage-1.md step 1.3) is stamped with `scripts/r9_stamp.py <file> --repo <repo>` right after it is written; `r9_stale` lists one whose reference or survivor folder changed since, and holds the area at plan (G94).
   4. On exit 2 from `speciality_reference.py`, `run_gaps.py` or `cookr roles gaps`, fix the name, the pool or the path, never the topic. A `stale_reference` row stops approval (`reference_format.py`, 1.4.27), approved or not (1.4.28): rewrite A/reference (step 1.1, then steps 1.2 and 1.3), re-run step 4 and hand the plan back to the owner.
2. Classify each topic by research type, and name each topic's research-bar question under **Owner questions**, even "no escalation"; `plan_sections` lists each topic none names (stage-1.md step 2, G116, G128).
3. Write `A/area-plan.md` (`scripts/plan_skeleton.py --area <area> --workspace <workspace> --repo <repo>` prints its headings with each digest line in place, read-only, G181): **Topics**, **Gaps**, **Missing subjects**, **Overlaps** (with the area's `copy_check.py` output) and its `--digest` line (G133), **Proposed topics** (the `| Topic | Action | Artifact | Why |` table), **Research questions**, **Owner questions** and **Step-4 re-check**, listing every `stage_status.py` `incoming` merge and carrying its research questions; `run_gaps.py` figures are cited from `A/run_gaps.json`.
4. Re-run `unmeasured.py` and `stage_status.py` (stage-1.md step 4), with `run_gaps.py`, read-only (`--check` on `unmeasured.py` and `run_gaps.py`), `run_gaps.py --check --hints --digest` recorded and run again as the hand-off check, a change re-run, `run_gaps.py --check-homes --area <area>` and `--check-verdicts --area <area>` run too (1.4.43, G273, G280), as stage-1.md step 4 and its re-run checklist say. `--keys` (or `--summary`) on each script prints the shapes; the library `json_keys.py` does it, it has no command line (G135). Then hand `A/area-plan.md` to the owner and stop. **Next:** stage 2, only once
   the owner approves, recorded in `A/approval.md` as `- plan: area-plan.md, git hash-object <hash>, reference-hash <reference_hash>`: copy `reference_hash` from `stage_status.py`, never compute it by hand; it is withheld while any reference is stale (1.4.31).
   An edited plan, or one approved under an older reference format or other rows, needs a new approval.

## Prompts and helper scripts

Every prompt this skill dispatches is a template in
`${CLAUDE_SKILL_DIR}/scripts/prompts/`, filled by
`${CLAUDE_SKILL_DIR}/scripts/write_brief.py`, never written out by hand:

```
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py prompt <name> --repo <repo> --cookr-py $COOKR_PY --set key=value ...
```

Dispatch the printed text exactly as it is; an unfilled placeholder exits 2
naming it. The filler, the template per stage and each helper script's job
are in [references/tools.md](references/tools.md): read it before running a
stage's first prompt or script.

## Stage 2: Research each topic

Research each topic on the four questions, verify its rules, and check the
contested claims independently. **Before running stage 2, read
[references/stage-2.md](references/stage-2.md).** Stop unless
`stage_status.py`'s `approval` is `current`.

Topics may be researched in parallel, one topic per dispatch: each dispatch
writes only its own topic's files. Steps 0–7 run in order within a topic.

0. Record the topic's base commit, before anything is written, unless
   `base.txt` exists already:
   ```
   git -C <repo> rev-parse HEAD > A/topics/<topic>/base.txt
   ```
1. Write `research-brief.md`.
2. Run the research. First check whether the research team can run:
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/team_probe.py researchteam
   ```
   It prints `{"ok", "why", "python", "missing"}`.
   - **If `ok` is true**, run the team on the brief in the foreground, follow
     each `__MYTEAMS_NEXT__` line until `__MYTEAMS_DONE__`, and save the final
     report to `team-run.md`:
     ```
     myteams researchteam research "$(cat A/topics/<topic>/research-brief.md)" --step
     ```
   - **If `ok` is false**, say its `why` once and dispatch one fresh Opus
     Agent with the `research` prompt; save the reply to `agent-run.md`:
     ```
     $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py prompt research --repo <repo> --cookr-py $COOKR_PY --set artifact=<artifact> --set topic_dir=A/topics/<topic>
     ```
3. Write `<artifact>/research/research.json`.
4. Write `<artifact>/research/research.md`.
5. If `cookbook/research-exempt.json` lists the topic, remove that entry now.
6. Second check. List the claims it covers:
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/apply_second_check.py <repo>/<artifact> --list
   ```
   dispatch one fresh Agent that did not run the research with the
   `second-check` prompt, its `claims` that list:
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py prompt second-check --repo <repo> --cookr-py $COOKR_PY --set artifact=<artifact> --set "claims=<the list>"
   ```
   write the reply to `second-check.md`, then apply it by script, never by
   hand:
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/apply_second_check.py <repo>/<artifact> A/topics/<topic>/second-check.md
   ```
   On exit 2, stop and report its output.
7. Check the research alone, before any rule cites it:
   ```
   cookr validate --research <artifact>
   ```
   It must print `Research passed.` On a finding, correct the file it names
   and run it again. **Next:** stage 3.

## Stages 3 and 4: one topic at a time

Stages 3 and 4 run **one topic at a time, in the order of the plan's
*Proposed topics* table**: a topic is written and reviewed to the end of
stage 4 (a pass, or its rounds spent) before the next topic's stage 3
starts. No topic is written while a sibling it may cite is half-written.

A finding about a sibling topic (another artifact than the one under
review, named by the reviewer) never goes to this topic's author:
- the sibling has not passed stage 4: append it to the sibling's
  `write-brief.md` under `## From <this topic>'s review`, for its next round
  (creating the brief if the sibling has not reached stage 3; its `write`,
  and a `write --restart`, keep the section);
- the sibling has passed stage 4: copy it to the sibling's `integrate.md`
  under `## From <this topic>'s review`, as `- R<n>.<m>: <finding>` (the id
  not bold; a `write --restart` keeps the section). If the sibling is not
  yet integrated, its stage 5 step 2 gives the owner the section; if the
  sibling is integrated, `stage_status.py` lists each finding in a `## From`
  section of an integrated topic's `integrate.md` in that topic's `owner`,
  as `from <this topic>'s review: <finding>`, since no stage of that topic
  runs again. *What reaches the owner*, below, says when they are handed
  over.
The next scoped round rules such a finding `routed`, naming the sibling,
which closes it in this topic.

**What reaches the owner.** This is the one statement of it; stage 4's
`next: stop` points here. When a topic stops at `next: stop`, none of this
topic's own findings goes to the owner, but a finding it routed to an
integrated sibling still does, through that sibling's `owner` items in
`stage_status.py`. So when this topic's stage 4 ends, however it ends (`next: stop`
included), give the owner every `owner` item of an integrated sibling,
verbatim. And when the area's last topic in plan order has ended, run
`stage_status.py` and give the owner every topic's `owner` items, verbatim,
whatever any topic's outcome: the area's end hand-off collects them all,
including a routed finding whose routing topic was the last to run.

## Stage 3: Write each topic

Write the topic from its research as a roled guideline whose every rule
cites a claim. **Before running stage 3, read
[references/stage-3.md](references/stage-3.md).**

Round 1 runs steps 1–8. A later round runs only steps 4–8: stage 4's count
step (its `write_brief.py append`) or stage 5's lossless recorder (its
`write_brief.py lossless`) has already put the round's findings in the brief.
It keeps `base.txt`, `current.md` and the brief, and never compiles the
artifact again, which now holds the failed draft.

1. Make sure the base is recorded (stage 2 step 0 records it), unless
   `base.txt` exists already:
   ```
   git -C <repo> rev-parse HEAD > A/topics/<topic>/base.txt
   ```
2. For an existing topic, unless `current.md` exists already, compile its
   current text into the workspace, never into the repo, run from `<repo>`
   (`--out` mirrors the artifact's path below it):
   ```
   cookr compile <artifact> --out A/topics/<topic>/compiled
   mv A/topics/<topic>/compiled/<artifact>.md A/topics/<topic>/current.md
   ```
   Stage 1 never compiles into the cookbook: to read a topic's text it
   runs the same `cookr compile <artifact> --out <scratchpad>/<area, / as -->-compiled`
   and reads the copy there (1.4.37, G167).
3. The write brief, by script:
   - round 1 (the `write-brief` template, filled from the topic):
     ```
     $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py write A/topics/<topic> --repo <repo> --cookr-py $COOKR_PY --artifact <artifact> --kind "<new topic | existing topic, its current text in A/topics/<topic>/current.md>"
     ```
   - each later round: nothing to run; `write` refuses a re-run (exit 4).
   - after stage 5 sent a research finding back to stage 2: run `write`
     again with `--restart` (exit 5: the research cannot be read, nothing
     has moved).
4. Run the guideline author. First check whether the cookbook team can run:
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/team_probe.py cookbookteam
   ```
   - **If `ok` is true**, run it on the brief in the foreground, follow each
     `__MYTEAMS_NEXT__` line until `__MYTEAMS_DONE__`, and copy the file its
     final report names to `A/topics/<topic>/draft.md`:
     ```
     myteams cookbookteam guideline new "$(cat A/topics/<topic>/write-brief.md)" --step
     ```
   - **If `ok` is false**, say its `why` once and dispatch one fresh Opus
     Agent with the `author` prompt:
     ```
     $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py prompt author --repo <repo> --cookr-py $COOKR_PY --set artifact=<artifact> --set topic_dir=A/topics/<topic>
     ```
5. Put the draft in the topic's source folder, then delete the doc (a new
   topic: `cookr convert` without `--update`):
   ```
   cp A/topics/<topic>/draft.md <repo>/<artifact>.md
   cookr convert --update <artifact>.md
   rm <repo>/<artifact>.md
   ```
6. Give every part but `intro` and `history` its role, one `--part` per part:
   ```
   cookr roles set <artifact> --part <part>=<role> [--part <part>=<role>]...
   ```
7. Check the draft against the owner list:
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/owner_list.py <repo>/<artifact> --draft A/topics/<topic>/draft.md --out A/topics/<topic>/owner-list.md
   ```
   Exit 1 sends the draft back to step 4; it never goes to review.
8. `cookr roles check <artifact>` must report no finding. **Next:** stage 4.

## Stage 4: Review each topic

Review the draft by a fresh agent that wrote none of it, round by round.
**Before running stage 4, read [references/stage-4.md](references/stage-4.md).**

A topic has **at most 3 review rounds**, plus one for each lossless failure
stage 5 records. A lossless failure gets exactly one round, whether the topic
has rounds left under the cap or has spent them: if that round fails, the
topic stops. Round 1 is a full review; each later round is a scoped
re-review of what changed.

1. Write the round's review prompt (round 1 `review-full`, later
   `review-scoped`):
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py review A/topics/<topic> --repo <repo> --cookr-py $COOKR_PY --artifact <artifact>
   ```
2. Dispatch one fresh Agent that wrote none of the topic and reviewed no
   earlier round of it (`subagent_type: general-purpose`, `model: opus`),
   with the text of `review-prompt.md` exactly. It writes `review.md`, done
   when it ends with `verdict: pass` or `verdict: fail`.
3. Count the round:
   ```
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py append A/topics/<topic>
   $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/review_findings.py status A/topics/<topic>
   ```
   This is the one place `append` runs. `status`'s `next` decides:
   - `next: integrate` (the verdict is `pass` and no lint error stands): on
     to stage 5.
   - `next: write` (a failed verdict or a lint error, below the cap): route
     each sibling finding as above, then stage 3's next round for this
     topic, then this stage again.
   - `next: owner` (round 3 failed, no lint error standing): copy every
     finding still open, with its round history, to `integrate.md` under
     `## For the owner` (`owner` looks for an id it has already recorded
     only inside `## For the owner`, so a sibling's routed finding with the
     same id never hides this topic's):
     ```
     $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/review_findings.py owner A/topics/<topic>
     ```
     and go on to stage 5, **unless** a `cookr validate` failure or a
     `cookr roles check` finding stands: that stops the topic. Say which,
     with its output verbatim.
   - `next: stop`: the topic stops; none of this topic's own findings goes
     to the owner (a finding it routed to an integrated sibling still does:
     see *What reaches the owner*). Say `why`
     (a lint error standing at round 3, the round a lossless failure opened
     failing, or a second lossless failure) with the review's `## Lint` or
     the open findings verbatim.

## Stage 5: Integrate each topic

Prove nothing the topic held is lost, then validate, bump and add the
artifact. **Before running stage 5, read
[references/stage-5.md](references/stage-5.md).** Stop unless
`review_findings.py status` says `next: integrate`, or `next: owner` and its
open findings are in `integrate.md`.

1. Nothing the topic held is lost. The orchestrator writes the accounting;
   one fresh judge rules on it.
   1. Run the check, with `--copy <folder>` for each folder in the topic's
      `fold`:
      ```
      cookr roles lossless <artifact> --base $(cat A/topics/<topic>/base.txt) [--copy <folder>]...
      ```
      Exit 0: on to step 2.
   2. On exit 1 with `missing` sentences, write `<repo>/<artifact>/lossless.json`
      yourself, then tune the targets until no tripwire fails:
      ```
      cookr roles lossless <artifact> --base <base> [--copy <folder>]... --draft
      ```
   3. For entries unjudged or stale, dispatch one fresh Opus judge that wrote
      none of the topic, with the `lossless-judge` prompt:
      ```
      $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py prompt lossless-judge --repo <repo> --cookr-py $COOKR_PY --set artifact=<artifact> --set base=<base> --set "copies=<' --copy <folder>' per fold, or empty>" --set "last_run=<the last run's output>"
      ```
   4. One retarget (at most 3 targets), by cookr, never by hand, then a fresh judge as in step 3:
      ```
      cookr roles lossless --retarget <artifact> --entry <n> --to <name> [--to <name>]...
      ```
   5. A hard failure: save the last run's JSON output to
      `A/topics/<topic>/lossless-run.json` and record it by script, never by
      hand:
      ```
      $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_brief.py lossless A/topics/<topic> --report A/topics/<topic>/lossless-run.json
      ```
      Then stage 3's next round, stage 4 as a scoped round, then step 1
      again; `review_findings.py status` decides: `next: integrate` runs
      step 1 again, `next: stop` stops the topic. A lossless failure never
      goes to the owner.
2. `cookr validate` must pass, its Research section included. Copy every
   `owner-decides` warning into `integrate.md` under `## For the owner`, and
   give the owner that list, with every `## From <topic>'s review` section in
   `integrate.md`, when the stage ends. On a failure on this topic,
   fix the cause in the stage that owns it; on one it did not touch, run
   `/repair-cookbook`; if it still fails, stop and report the output verbatim.
3. `cookr bump <artifact> --summary "<what changed>"`: the version,
   `modified` and Change History that stages 3 and 4 left alone.
4. `/add-artifact <artifact>`: lint, approval, the index, the counts. Tell it
   to run cookr exactly as `PYTHONPATH=<repo>/skills/cookr/cli $COOKR_PY -P -m cookr -p <repo>`,
   with the path of `$COOKR_PY` written out.
5. Last, add the line `integrated: <today>` to `integrate.md`. Only that
   line marks the topic integrated for `stage_status.py`; an `integrate.md`
   holding only findings for the owner does not.

## Guards

- **This checkout's cookr, 0.21.4 or later.** Never an installed `cookr`.
- **Research first.** No rule is written that cites no claim, and no claim is
  taken from the devteam's text, the existing artifact, or memory.
- **The owner approves the area plan** before any research, and decides each
  rule in `owner-list.md`.
- **One topic per research dispatch.** A topic's research never borrows another's run.
  Topics may be researched in parallel; stages 3 and 4 take one topic at a
  time, in the plan's order.
- **The research is fixed after stage 2.** A rule's citations are
  authoritative; the author never edits research, and prior rule names never
  change.
- **At most 3 review rounds**, plus one per lossless failure; a lossless
  failure gets exactly one round, under the cap or past it. Round 1 is
  full, later rounds scoped; after round 3 the open findings go to the owner
  in `integrate.md`, unless a lint error (`review_findings.py` reads `## Lint`'s
  closing `lint: clean|fail <n>` line; a missing one is an error) or a `cookr validate`/`roles check` failure stands, which stops
  the topic. A lossless failure is never handed to the owner: if the round
  it opened fails, the topic stops.
- **Scripts do the bookkeeping.** Prompts are filled by `write_brief.py`;
  the second check is applied by `apply_second_check.py`; rounds are counted
  by `review_findings.py`; a lossless failure is recorded by
  `write_brief.py lossless`. Never redo one of these by hand.
- **Reviewer and writer differ.** Stage 2's second check, stage 4's review
  and stage 5's lossless judge are each done by a fresh agent that did not
  do the work it checks.
- **The exemption list only shrinks.**
- **A failing tool stops the stage.** Report its output verbatim and the stage
  it stopped; never do the team's or cookr's work by hand instead. The two
  fallbacks are the only exceptions: when `team_probe.py` says a team
  cannot run, stage 2's research and stage 3's guideline author are each one
  Opus Agent with the prompt `write_brief.py` fills.
