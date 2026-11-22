# Stage 3: Write each topic, in detail

The detail of SKILL.md's *Stage 3*. The commands are in SKILL.md; the steps
here are numbered as there.

## Reads and writes

**Reads:** `A/area-plan.md`, `<artifact>/research/`, `A/topics/<topic>/second-check.md`,
and, from round 2, `A/topics/<topic>/review.md`.
**Writes:** `A/topics/<topic>/base.txt`, `A/topics/<topic>/write-brief.md`,
`A/topics/<topic>/owner-list.md`, `A/topics/<topic>/current.md` (an existing
topic only), `A/topics/<topic>/draft.md`, `A/topics/<topic>/disputes.md` (when
the author disputes a finding), and the artifact folder.

## Step 1: The base

1. Make sure the base is recorded (stage 2 step 0 records it). Unless
   `base.txt` exists already (a re-run keeps the first one):

A base taken after the write would hold the new text, and stage 5's
lossless check would compare the topic with itself.

## Step 2: The current text

2. For an existing topic, unless `current.md` exists already (a re-run keeps
   the first one), compile its current text and move it into the workspace:

## Step 3: The write brief

3. The write brief, by script:
- round 1:

  It writes `write-brief.md` and `owner-list.md`. The brief carries, up
  front, the review criteria (`prompts/criteria.md`) word for word; the
  strength rule: each rule at the strength of the weakest claim it cites,
  with the criteria's item 3, its one source, on which claims cannot
  carry MUST; every verdict; the second check's corrections, per claim,
  split into refuted claims and claims that only lost a citation; the
  frontmatter rule (the author updates `summary`, 160 characters or
  fewer, `tags`, `platforms` and `related` to match the new text, and
  leaves `version`, `modified` and Change History to stage 5's
  `cookr bump`); and the owner list. `write` keeps every `## From
  <topic>'s review` section already in the brief (a finding a sibling's
  review routed here), verbatim, at the end of the rebuilt brief.
- each later round: nothing to run. Stage 4's count step (step 3) ran
  `append`, which put `## Round <N> findings` in the brief, or stage 5's
  `lossless` put `## Lossless failure after round <N>` there. `write`
  refuses a re-run: once the topic holds a `review-<N>.md` or a
  `lossless-<N>.md` it exits 4 naming that file, since a rebuilt brief
  would drop those sections.
- after stage 5 sent a research finding back to stage 2: run `write`
  again with `--restart`. It moves the stopped run whole into a new
  `run-<k>/` subfolder (k the next free number): the numbered
  `review-<N>.md`, `lossless-<N>.md`, `draft-<N>.md` and `diff-<N>.md`,
  `disputes.md` (its ids belong to the old run), and every other file the
  stages wrote at the topic's top level, such as `draft.md`, `review.md`,
  `owner-list.md`, `review-prompt.md`, `author-prompt.md`,
  `lossless-judge-prompt.md`, `lossless-run.json` and any log. Only the
  topic's inputs stay (`RESTART_KEEPS` in `write_brief.py`): `base.txt`,
  `current.md`, stage 2's `research-brief.md`, `team-run.md`,
  `agent-run.md` and `second-check.md`, a `research/` folder, and
  `write-brief.md`, which it rebuilds. `integrate.md` moves whole; then
  only what sibling topics routed to `integrate.md` stays: its `## From
  <topic>'s review` sections are written back to a new top-level
  `integrate.md`. The stopped run's own `## For the owner` and its
  `integrated:` line stay in `run-<k>/` (round ids restart per run, so a
  run's owner findings live with that run). It then writes the brief
  and owner list afresh from the new research, keeping the `## From
  <topic>'s review` sections; the topic starts again at round 1 and keeps
  its earlier runs. It reads the research before it moves anything: when
  the research cannot be read it exits 5 and nothing has moved. `review_findings.py status` reads
  only the topic folder's top level.

### The owner list

**The owner list** (`owner-list.md`, from `owner_list.py`) holds (a)
every prior rule whose verdict is `unsupported` or `contradicted`, with
its prior text, and (b) every `open_questions` entry of the research.
Being on it exempts only the rule's wording from review, nothing else.
A prior rule with no RFC keyword is named as such: the author keeps its
text word for word and may put one lead-in in front of it carrying the
keyword the old text implied ("In TypeScript, the panel MUST be reached
this way:"); that lead-in is the one change the reviewer accepts.

## Step 4: The guideline author

4. Run the guideline author. First check whether the cookbook team can run:

- **If `ok` is true**, run it on the brief in the foreground:

  Follow each `__MYTEAMS_NEXT__` line until `__MYTEAMS_DONE__`. Its final
  report names the file it wrote; copy that file to
  `A/topics/<topic>/draft.md`. If the report names no file, stop and
  report it verbatim.
- **If `ok` is false**, say its `why` once (never install into the team's
  environment), and dispatch the guideline author as one fresh Agent
  instead (`subagent_type: general-purpose`, `model: opus`), with the
  `author` prompt:

  If `~/.myagenticteams/cookbookteam/install/team-leads/guideline-author.md`
  does not exist, stop and say so.

The author writes only `draft.md`, and `disputes.md` to dispute a
finding (`- <id>: <why, citing the claim or rule>`): a disputed finding is
not obeyed; the next review rules on it. The author edits no research,
no owner list and no other topic.

## Step 5: The draft into the source folder

5. Put the draft in the topic's source folder, then delete the doc:
   - an existing topic:
     ```
     cp A/topics/<topic>/draft.md <repo>/<artifact>.md
     cookr convert --update <artifact>.md
     rm <repo>/<artifact>.md
     ```
   - a new topic:
     ```
     cp A/topics/<topic>/draft.md <repo>/<artifact>.md
     cookr convert <artifact>.md
     rm <repo>/<artifact>.md
     ```

## Step 6: Part roles

6. Give every part but `intro` and `history` its role, one `--part` per part.
   The part names are the section headings as kebab-case file names; list
   them with `$COOKR_PY -c "import json; print([p['part'] for p in json.load(open('<repo>/<artifact>/artifact.json'))['parts']])"`.
   Each role is the one the gf-roled-parts table in
   `cookbook/guidelines/cookbook/authoring/guideline-formatting/rules.md` gives what
   the part holds (`rules`, `how-to`, `examples`, `review-focus`,
   `review-bar`, `build-bar`, `rationale` or `references`). For example, a
   topic whose parts are `intro`, `rules`, `covering-indexes`,
   `partial-indexes`, `what-a-reviewer-looks-for`,
   `a-complete-review-must-establish`, `a-build-must-establish`,
   `rationale`, `references` and `history`:
   ```
   cookr roles set <artifact> \
     --part rules=rules \
     --part covering-indexes=how-to \
     --part partial-indexes=examples \
     --part what-a-reviewer-looks-for=review-focus \
     --part a-complete-review-must-establish=review-bar \
     --part a-build-must-establish=build-bar \
     --part rationale=rationale \
     --part references=references
   ```

## Step 7: The owner-list check

7. Check the draft against the owner list:

Each prior rule is `verbatim`, `lead-in` (listed in owner-list.md, the
change the reviewer accepts), `reworded` or `dropped`. Exit 1 (a rule
reworded or dropped) sends the draft back to step 4 with that problem
appended to the brief; it never goes to review.
