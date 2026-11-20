# Stage 1: Plan the area, in detail

The detail of SKILL.md's *Stage 1*. The commands are in SKILL.md; the steps
here are numbered as there.

## Re-run checklist

A re-run (a newer skill version, a rewritten reference, another plan's new
marks) works through this list and reads only the sections it names
(1.4.33, G119). An area with no speciality or of copies only reads *The
short path* (below) first, and skips each item marked so; a `count_only`
row (step 1.3, `home_unguessed`) is listed and counted, never judged
(1.4.37, G178, G179). With no speciality, skip items 4–6 (their commands
still run, finding nothing) and record "no speciality" under **Gaps** once;
with no R9 file, skip item 5 (1.4.39, G222). With no speciality, step 1.3's re-judging
(`held_by_wording`, `modal_differs`, `stale_verdicts`, `non_home_lacking`) is vacuous too: confirm
each is `[]` once and move on (1.4.43, G301). A re-run reads this checklist and step 1.3's G160 table
in full, the rest only by the section an item names (1.4.43, G298). Every command below is
written in full: copy it whole, `--area <area> --workspace <workspace>
--repo <repo>` included (1.4.39, G197); an unknown area, or a workspace
holding no `areas/`, exits 2 in every script (G198); each flag is its own word:
zsh passes a variable holding the flags as one word, and a script that gets one
argument holding ` --` says so in its message (1.4.40, G240). No command here
keeps a flag in a plain shell variable: zsh passes it as one word, so never `$ARGS`,
`$S/<script> $FLAGS` or `${=C}`; an exit 2 from argparse names this rule (1.4.42, G263). A single-word
path variable (`$COOKR_PY`, `$W`, `$R`) is fine; flags repeated over many calls go in a zsh array,
`flags=(--area <area> --workspace <workspace> --repo <repo>)` then `"${flags[@]}"`, or in a Python
driver (a run of `mark.py --lack` calls); the plan records each command written out whole (1.4.43,
G293). Every script takes `--area`; `unmeasured.py`, `copy_check.py` and, since 1.4.43, `run_gaps.py`
take the area positionally too (G299):
1. Back up the area's old outputs to the scratchpad under a per-area name
   carrying `<version>`, the skill version running this re-run (`grow-cookbook
   v<version>`, SKILL.md; 1.4.42, G262: one name for the checklist and any
   brief): `<scratchpad>/<prefix><area, / as -->-before-<version>/`, never inside
   `<workspace>/areas/` (*A re-run*); every scratch file's name carries the
   area, and a brief's own prefix (`<prefix>`, such as `P1r8-`) goes before
   it. The one backup allowed inside A is `A/area-plan-before-<version>.md`
   (1.4.36, G142), and item 3's `--first-check` run of `stage_status.py` saves the old
   `A/first-check.txt` as `A/first-check-before-<version>.txt` itself. A
   backup of that name already there (a second re-run at one version) is left
   as it is, never renamed, overwritten or deleted, so it keeps the outputs
   from before the first re-run at that version; back up every file under **Writes** (*Reads and writes*),
   `A/homes.json` and `A/held.json` included (1.4.37, G170). The scratch name is free beyond
   carrying the area and `<version>`: a brief's own scratch-name rule (`P1r9-<area>`, single hyphens)
   wins (1.4.43, G292). With no old `A/first-check.txt` there is nothing to back up and no
   `first-check-before-<version>.txt` (G290).
2. Run `stage_status.py --area <area> --workspace <workspace> --repo <repo> --keys`:
   each output key with its shape only. `--keys` (or `--summary`) on
   each script prints the shapes; the library `json_keys.py` does it, it has
   no command line (1.4.36, G135). An empty list prints as `[]`; a string
   prints whole (`run_gaps.py`'s `note` too); the rows of each `ROW_KEYS`
   key print whole: `plan_sections`, `stale_reference`, `r9_stale`,
   `stale_copy_check`, `other_plans_changed`, `survivor_carries`,
   `carries_asked`, `held_by_wording`, `new_keys` and `changes` (G138;
   1.4.37, G171), so `stage_status.py --keys --area <area> --workspace <workspace> --repo <repo>` prints the hold rows whole
   and can run long; every other list prints as `{"rows": N}`. `--rows KEY`
   prints one key whole, and `--rows a,b` several (`stage_status.py` and `run_gaps.py`, 1.4.39, G219; 1.4.40, G239). Read in full only the keys that hold rows.
   `stale_reference`, `r9_stale`, `stale_copy_check`, `plan_sections` and
   `host_check` hold the area at `plan`, and so does each `subject` row of
   `survivor_carries` and `carries_asked` (1.4.39, G188, G214);
   `other_plans_changed`, `shared_no_host`, `stale_pointer` and the
   `research_label` carry rows are advisory and hold nothing (1.4.36;
   1.4.37, G151; 1.4.39). Since 1.4.39 `--rows a,b` prints several keys,
   and `stage_status.py --keys --area <area> --workspace <workspace> --repo <repo>` prints `other_plans_changed` as its count
   and the plans it names (`--rows other_plans_changed` prints the rows,
   G219). Each key belongs to one script (1.4.39, G220), and `--rows KEY`
   on another script exits 2 naming the owner:
   - `stage_status.py`: `next`, `next_why`, `plan`, `approval`,
     `reference_hash`, `incoming`, `conflicts`, `pending_target`, the holds
     above and the advisory lists (`other_plans_changed` rows carry `plan`,
     `recorded`, `current`, `sections`, `cited_at`, `question_cites`, `why`;
     carry rows `kind`);
   - `unmeasured.py`: `new_topics`, `marked_here`, `mark_conflicts`,
     `against_survivor`, `survivor_elsewhere`, `unread_marks`, `building`;
   - `run_gaps.py`: `topics`, `building`, `home_measures`, `home_unguessed`
     (field `home_recorded`), `held_by_wording` (fields `id`, `text` (the
     piece; there is no `piece` key), `topic`, `topic_sentence`,
     `rule_sentence`, `topic_hash`, `modal_piece`, `modal_topic`,
     `modal_differs`, `home_topic`, `home`, `verdict`), `short_sentences`,
     `repeat_of`, `numbering_differs`, `stale_home`, and on `--check`
     `gap_total`, `new_keys` and `changes`.
3. Before any rewrite, the first check, on the saved reports: run
   `unmeasured.py --check --area <area> --workspace <workspace> --repo <repo>` and
   `run_gaps.py --check --hints --area <area> --workspace <workspace> --repo <repo>`
   (their JSON gives `new_keys` and `changes`), each again with `--digest`,
   and `stage_status.py --digest --area <area> --workspace <workspace> --repo <repo>`; one command runs the
   three `--digest` forms and writes `A/first-check.txt` (1.4.42, G267):
   `$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/stage_status.py --first-check --area <area> --workspace <workspace> --repo <repo>`.
   Its content is exactly three lines, nothing else: the digest line of the
   three commands above, each with the area's three flags: unmeasured.py with
   `--check --digest`, run_gaps.py with `--check --hints --digest` and
   stage_status.py with `--digest`, in that order (each the command's last
   stdout line; it writes nothing when one exits 2), never under
   `write_on_success.py`. An old file of another shape (four lines, a whole JSON) is backed up as it
   is; with that backup already there it says `kept as it is (first-check.txt rewritten below)`, and
   the file is rewritten all the same (1.4.43, G290). On a re-run the `run_gaps.py` line gives
   `stated S -> measured M (+D: counted_with_prior_verdict a, counted_never_judged b, verdict_changes
   c)`: `counted_never_judged` above 0 is the cue for step 1.3's per-row verdict pass (1.4.43, G300);
   `missing_subjects N` sits beside `measured_total`, never inside it (G286); `counted_rows_differ`
   names every row behind a gap between `counted_rows` and `measured_total` (`id: why`: a row marked
   for another area only, an uncounted row, a home-measure topic, G283). `--digest` is a view and
   never saves `A/run_gaps.json`; `--check` exits 1 on any change, an expected outcome (G299). Record under **Step-4 re-check** each
   digest line and each `new_keys` and `changes` row. Item 4 rewrites the
   saved reports, after which no check can show them (1.4.37, G155; step
   4, G148): `write_on_success.py` and `speciality_reference.py` warn on
   stderr when an area with a plan has no `A/first-check.txt` (1.4.39,
   G215). `run_gaps.py --check --area <area> --workspace <workspace> --repo <repo>` names each `new_keys` key on stderr
   (G218); `stage_status.py --digest --area <area> --workspace <workspace> --repo <repo>` counts the advisory lists it leaves
   out on one stderr line (G195). A digest written before 1.4.37, or before
   a version that added a hold (1.4.39 adds `host_check`), is not
   comparable: record both lines and the reason, and read the holds with
   `--keys` (G195).
4. Steps 1.1–1.3 (*A re-run*). `speciality_reference.py` says on stderr how
   many reference files the rewrite left byte-identical ("N of M files
   byte-identical to the old rewrite"); the steps still run all the same
   (the byte-identical line: skip with no speciality). A hand-read
   `A/reference/<speciality>.txt` with no `A/reference.json` row (G149) is
   rewritten by the single-speciality form,
   `$COOKR_PY <devteam>/speciality_reference.py <speciality> --out A/reference`
   (1.4.39, G221). Re-quote each building speciality with the two
   `quote_building.py` commands below, the `--marks` run without `--quiet`
   (1.4.39, G196).
5. Re-run and re-stamp each R9 file (step 1.3, *A new topic's candidate
   survivor*), before step 1.3's final `run_gaps.py` run, so that run and its
   saved report see the stamps: `r9_stale` names one whose reference or
   survivor folder changed since its stamp (1.4.36, G140) (skip with no R9).
6. Re-judge each cookr `held` against *Held in other words* (G118), starting
   from `run_gaps.py`'s `held_by_wording` rows (1.4.36, G129, G132), and
   record each verdict with `mark.py --held`, or many at once with
   `--held-file` (1.4.37, G159; 1.4.39, G199), each judged by step 1.3's
   G160 table (skip with no speciality). Then run
   `run_gaps.py --area <area> --workspace <workspace> --repo <repo> --hints` once more, so the saved
   report and `stage_status.py` see the verdicts: `report_refresh` names a saved report older than
   `held.json`, `hand_lacks.json` or `hand_holds.json`, with its `stale_views` and the one `command`
   that refreshes it (1.4.43, G291, G301).
7. Re-run `copy_check.py --area <area> --workspace <workspace> --repo <repo>` and
   rewrite **Overlaps** from it, recording its `--digest` line there
   (step 3, *Overlaps*; G133). When the area has copies, read *An area of
   copies only* (step 3).
8. Rewrite the plan to the current section list (step 3), each item a newer
   step requires added and recorded as new in **Step-4 re-check**; each
   Missing subject led by a bold phrase that a Research question repeats
   verbatim (step 3, *Missing subjects*; 1.4.34); each topic's research-bar
   question under **Owner questions** (step 2; G128).
   `$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/plan_skeleton.py --area <area> --workspace <workspace> --repo <repo>`
   prints the section headings in order with each digest line in place,
   read-only (1.4.37, G181).
9. Step 4: the `--check` re-runs, each digest recorded, and the second
   `--check` after the final edit, the hand-off check, with
   `run_gaps.py --check-homes --area <area> --workspace <workspace> --repo <repo>` and
   `run_gaps.py --check-verdicts --area <area> --workspace <workspace> --repo <repo>` (step 4, 1.4.43). `next: approve` follows any rewrite of an approved plan (the
   plan changed since its approval): the owner approves it again (G301).

The commands, in full (1.4.36, G139; 1.4.39, G197); the two
`quote_building.py` lines re-quote one building speciality (item 4):
```
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py A/building-<name>.json -- $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/quote_building.py --area <area> --speciality <speciality> --file A/reference/building--<name>.txt --repo <repo> --workspace <workspace> --keep A/building-<name>.json
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py A/building-<name>-quoted.json -- $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/quote_building.py --area <area> --speciality <speciality> --file A/reference/building--<name>.txt --repo <repo> --workspace <workspace> --marks A/building-<name>.json
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/stage_status.py --area <area> --workspace <workspace> --repo <repo> --keys
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/unmeasured.py --area <area> --workspace <workspace> --repo <repo> --check --digest
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/run_gaps.py --area <area> --workspace <workspace> --repo <repo> --check --hints --digest
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/copy_check.py --area <area> --workspace <workspace> --repo <repo> --digest
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/stage_status.py --area <area> --workspace <workspace> --repo <repo> --digest
```
`unmeasured.py` reads `A/reference.json` when `--reference` is left out.

## Reads and writes

**Reads:** the area's topic folders (`cookbook/guidelines/<area>/*/artifact.json`);
`<workspace>/worklist.json` and `<workspace>/speciality-map.json` when the
workspace has them (the roles plan's worklist and speciality map).
**Writes:** `A/area-plan.md`, `A/reference.json`, `A/reference/<speciality>.txt`, `A/gaps/<topic>.json`,
`A/gaps/new-<name>.json`, `A/gaps/home--<topic>.json`, `A/run_gaps.json`,
`A/unmeasured.json`, `A/building-<name>.json`,
`A/building-<name>-quoted.json`, `A/homes.json` (`mark.py --home N=AREA:TOPIC`),
`A/held.json` (`mark.py --held`), and `A/approval.md` once the owner approves.
It also reads every other area plan in `<workspace>/areas/` and their
`building-<name>.json` marks files (step 1.2, step 3).
Stage 1 writes nothing in the cookbook. To read a topic's text whole, run
`cookr compile <artifact> --out <scratchpad>/<area, / as -->-compiled` from
`<repo>` and read the copy there (it mirrors the artifact's path), or read
the folder's `artifact.json` and part files; never a plain `cookr compile`,
which writes `<artifact>.md` into the repo (1.4.37, G167).

**`--repo`.** Every script that reads the cookbook takes `--repo <repo>`,
which must hold `cookbook/guidelines/`. Left out, a script takes the nearest
folder at or above the current directory that holds `cookbook/guidelines/`
(`repo_path.py`); run from the workspace, outside the repo, it finds none
and exits 2 asking for `--repo`, never reading a wrong cookbook. Pass
`--repo <repo>` every time (1.4.25, G76).

**Full paths.** The plan writes every folder as its full path from the repo:
`cookbook/guidelines/<area>/<topic>`. For an area under `cookbook/` (the
cookbook's own guidelines) that is `cookbook/guidelines/cookbook/<area>/<topic>`,
never `cookbook/<area>`, which is another folder (1.4.25, G92).

## The short path: two special cases

Two kinds of area need only part of this file (1.4.25, G80):
- **An area with no speciality** (every worklist topic `devteam: authored`):
  steps 1.1–1.3 produce empty output: `A/reference.json` is `[]` ("area
  has no speciality; reference is empty ([])"), `unmeasured.py` lists no
  row of its own, and `run_gaps.py` measures nothing and says why in
  `why_empty`. The run still does them all, and the plan's **Gaps** quotes
  `why_empty`. Its gaps come from the subject: **Missing subjects**, judged
  by hand against what a practitioner expects of the area, each carried
  into the **Research questions** of the topic that answers it. Read step 1
  (*A re-run*), step 1.2's `marked_here` and `mark_conflicts` items (other
  plans' marks still reach it), step 1.3's *A new topic's candidate
  survivor* (R9 in an empty area), step 2, step 3 and step 4. The plan
  records "no speciality" once, under **Gaps**, and the "N of M files
  byte-identical" line is owed only when a speciality exists (1.4.36, G141).
  It skips each re-run checklist item marked "skip with no speciality"; an
  area with no R9 file skips each marked "skip with no R9" (1.4.37, G178).
- **An area of copies only** (every topic `merged` elsewhere): steps
  1.1–1.3 still run, and their output names the survivors' plans that
  measure each speciality. Read step 3 (*An area of copies only*,
  *Incoming merges*) and step 4.

An area that is both reads the union of both lists, and each rule of
either governs (1.4.36, G141).

## Step 1: Measure the gaps

1. Measure the gaps. cookr knows no team: it measures a topic against plain
   reference text, which the devteam's `speciality_reference.py` writes.
   `<devteam>` is the devteam checkout the speciality map came from; when this
   cookbook is its `external/agenticcookbook` submodule, it is `<repo>/../..`.
   Every command that writes a file runs under
   `$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py <file> -- <command>`,
   never a `>` redirect: the file's folder must exist (`mkdir -p` it first,
   or pass `--mkdir` before the file: `write_on_success.py --mkdir <file> -- ...`;
   a missing folder exits 2 naming it, writing nothing, 1.4.37, G174), and it puts the output in
   place only when the command exits 0, so a failed command never leaves an
   empty or partial file behind. A script that writes its own files is never
   wrapped: `run_gaps.py` (`A/run_gaps.json`, `A/gaps/`), `mark.py` and
   `stage_status.py --first-check` or `--record-others --write` (1.4.42, G267). On any other exit it shows what the command
   printed, its message included, and exits with the command's code. It exits 2 when the command edited `<file>`
   in place (an editor such as `sed -i` that prints nothing): nothing is written over it, the edit stands, and one
   line says so; run an in-place edit on its own, never under this wrapper (1.4.40, G231).
   The command form is the one shown: `-- PYTHONPATH=<path> $COOKR_PY -P -m cookr ...`,
   the assignment as the first word after `--`, no `env` (a test runs this
   form; `env PYTHONPATH=...` works too but is not the form).
   Every command is shell-neutral, the same in bash and zsh: to see a
   command's exit code, end its line with `; echo exit=$?`, never
   `${PIPESTATUS[0]}` (bash only) or a pipe into `tee` (1.4.18, G43).

**A re-run.** A stage-1 re-run, a newer skill version's included,
regenerates every step-1 output: `A/reference.json` and its reference files,
`A/unmeasured.json`, every `A/gaps/*.json` and each `A/building-<name>-quoted.json`.
It keeps the marks: the template command names its own output with
`--keep A/building-<name>.json`, and when that file holds any mark and its
sentences are the new quote's, `quote_building.py` prints it unchanged, says "marks kept (sentences unchanged)" on stderr and exits 0, leaving the file
untouched (1.4.18, G38); run the `--marks` step then. The stderr is one
line: "quote_building.py: marks kept (sentences unchanged): <file> already
marks these sentences and is printed as it is; marks kept; nothing to run"
(1.4.37, G168). The `--marks` step prints one stderr line (the
sentences quoted, this area's, the problems); `--quiet` leaves `markdown`
out of its JSON (1.4.37, G168), so a re-run never passes it: the quoted
file must stay byte-identical, and `--quiet` exits 2 when
`A/building-<name>-quoted.json` already holds `markdown` (1.4.39, G196).
When the speciality's text changed, it
writes the new template keeping each mark whose sentence is unchanged, and
lists every mark it dropped in `dropped` (and on stderr): mark the new
sentences, and say in the plan which marks were dropped. The `--marks` step
exits 2 on a sentence unmarked. A `--keep` file it cannot read is an exit 2 too, writing nothing: fix or
remove the file, then re-run.
A re-quote carries each mark by its sentence's text, never by its number.
Since 1.4.24 a sentence no longer ends after `e.g.`, `i.e.`, `etc.`, `vs.` or
`cf.`, nor inside an open parenthesis (G54), so an older marks file may
renumber: a new sentence that rejoins old pieces carries every area their
marks named (`joined`), and a mark it cannot carry is listed in `dropped`.
To see this before writing, run the template command with `--check` beside
`--keep A/building-<name>.json`: it writes nothing and prints `renumbered`,
`changed`, `old_count`, `new_count`, `joined`, `lost` and `kept` (exit 0
unchanged, 1 renumbered or a mark lost). `renumbered` is true for an append
too (the count changes); `changed` numbers each new sentence whose text is
new; `kept` is true when no mark is lost. The rewritten
`A/building-<name>-quoted.json` may differ from the old one by `topics`
alone (G77): that is expected, no change of marks (1.4.33, G111).
Re-mark each `lost` sentence with `mark.py`.
Clear `A/gaps/` before step 1.3 by running `run_gaps.py`, never by hand:
no one types `rm` or `find` (zsh fails on an empty glob). Before it
measures, `run_gaps.py` removes only the stale gaps files it wrote itself
(every reference carries `lacking_numbers`), lists them in `cleared`, and
never removes an R9 `new-<name>.json` (1.4.24, G45). Its `home--<topic>.json`
files (step 1.3, *Measured at its home*) are its own: one this run does not
write is cleared like the rest (1.4.25, G68); the two hyphens keep it apart
from any topic's own file (1.4.26). It writes each topic's
file again, and each R9 `new-<name>.json` is re-run by
hand after it when its inputs changed (`r9_stale` names one whose reference
or survivor folder changed, G94, 1.4.34), step 1.3 *A new topic's candidate survivor*; `run_gaps.py`
lists each `new` plan row owed one with no such file in `r9_missing`, 1.4.19 M4;
none is owed for a new topic with no candidate survivor: a worklist `kind`
other than `shared-different`, 1.4.20; one is owed when its kind is
`shared-different`, or when the worklist has no entry for it, 1.4.21): a
gaps file the re-run does not write is from an older measure. `stage_status.py` and
`run_gaps.py` list each such file in `stale_gaps`; never quote or count one
(1.4.18, G32). A `stale_gaps` of `{"refused": why}` means two topics share a
basename, so no file is known current: name them apart first (1.4.19, M3).
`cleared` also lists an old-shape gaps file (no `written_by`, its
references with no `lacking_numbers`) that no topic of this run writes
(1.4.33, G110).
A plan written under an older skill version is rewritten to the current
section list (step 3); every item a newer step requires is added and
recorded as new in **Step-4 re-check** (1.4.33, G98). Back up the old
outputs to the scratchpad under a per-area name before a re-run
(`<area, / as -->-before-<version>`, the skill version running the re-run,
1.4.42, G262; every scratch file's name carrying the area), never into the
workspace; the one backup allowed inside A is `A/area-plan-before-<version>.md`
(1.4.36, G142), beside `A/first-check-before-<version>.txt`. Back up every file under **Writes**; leave an older backup as it
is (1.4.37, G170, re-run checklist item 1). `unmeasured.py` reads only the `building-*.json` directly in
an area folder (one holding `area-plan.md` or `reference.json`, in no other
such folder) and lists every other one it finds in `ignored_marks`, never
read (1.4.33, G109).

### Step 1.1: the area's reference files

1. Create the area's folders, then write the area's specialities'
   reference files, once per area:

`--area` writes only this area's specialities: those whose topic lies
under the area, those a worklist topic of the area names in its
`devteam` entries, and the building specialities a worklist `building`
entry maps to one of its topics. A topic of the area is a topic whose `survivor` or `new_home` is in the area;
a `building` entry reaches the area when its topic is in the area or is
paired (survivor and `new_home`) with one that is. Each row of `A/reference.json` is
`{"speciality", "topic", "file"}`: the speciality's own text (its
*Review focus*, *A complete review must establish* and *Build focus*,
cut at `_Cookbook guidance`) in `file`, and the topic it stands on, or
null. A roled speciality's two review sections are its topic's reviewer
pair, copied whole, not its own text: from format 3 its reference leaves
them out, holding only its other own sections, and its row's `copied` names
the two left out (1.4.46). Only this area's specialities are written (1.4.24, G57): an area
with none gets `[]`, and "area has no speciality" on stderr ("area has no
speciality; reference is empty ([])", 1.4.25, G78), exit 0.
`unmeasured.py` reads every other speciality with no topic from
`<workspace>/speciality-map.json`, so step 1.2 still tells an unplaced one
from another area's and none is hidden. One
speciality alone:
`$COOKR_PY <devteam>/speciality_reference.py data/indexing --out A/reference`.

### Step 1.2: the specialities with no topic

2. Place each speciality that has no topic yet, a row of
   `A/reference.json` whose `topic` is null. `roles gaps` cannot measure
   it: it stands on no topic, so the whole of its text is lacking.

The worklist places each one; the speciality's domain (`development`
for every speciality today) names no area, so the worklist is what
places it:
- A `building-split` speciality (its `case` in
  `<workspace>/speciality-map.json`; the roles plan's R8 splits it onto
  the existing topics it covers) goes to every area that a `building`
  entry of a `<workspace>/worklist.json` batch maps it to. That entry's
  `topic` is `guidelines/<area>/<topic>`. It is in `building`, with this
  area's topics it maps to.
- Any other goes to the area of the one worklist topic with `new: true`
  whose `devteam` entries name it. That topic's `survivor` is
  `guidelines/<area>/<topic>`. It is in `new_topics`, with that topic.

`new_topics` lists every `new` worklist topic of this area, one row per
speciality it claims, whatever that speciality's reference row says
(1.4.24, G53). A claimed speciality whose reference row names a folder
outside the area (`cookbook/principles/principle-of-least-astonishment`)
names the new topic's candidate survivor: it is the topic's R9 target
(`A/gaps/new-<name>.json`, step 1.3), never an existing topic of this area.

For each row of `new_topics`, the plan's **Gaps** section quotes the
whole of its `file`, every line, as lacking, under its new `topic`.
A `building` speciality's text spans many areas (logging, tracing,
config, containers …), so it is quoted once, whole, each sentence
marked this area's or another named area's:

writes every sentence (blank lines are not sentences) and a `marks`
map with each sentence's area null. `<name>` is the speciality's basename
(`platform-windows` for `building/platform-windows`; 1.4.24, G63). A
speciality is given as the speciality map names it (`building/platform-windows`),
in every command; `quote_building.py` exits 2 on another form, naming the
map's (`did you mean building/platform-windows?`, 1.4.42, G261). Set each to the area path, below
`cookbook/guidelines/`, the sentence is about (this area's own path for
this area's), with
`$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/mark.py --area <area> --workspace <workspace> --repo <repo> --speciality <speciality> --n <n> --to <area-path>`,
never by editing the JSON (the schema: tools.md *The marks file*). A
sentence that spans areas (a UI clause and a packaging clause) takes each:
`--to` with every area path, a list, and each area gets it in
`marked_here`; two plans conflict only when their lists name different
areas (1.4.24, G55). Many sentences are marked in one call, with
`--mark <n>=<area>[,<area>]` repeated (`<n>=` clears one), every mark
checked before any is written (1.4.25, G70; the command lines are in
tools.md *The marks file*). `mark.py` refuses (exit 2, writing nothing) a missing
file, another speciality's file, an `n` with no sentence (or given twice) and an area that
is neither a folder of the cookbook nor a planned new area: one with
`<workspace>/areas/<area>/area-plan.md`, whose folder stage 3 creates
(1.4.25, G65). `--marks` accepts the same areas. A speciality this area reaches only through a `new_home` (its
row's `by_new_home`, the worklist entry's survivor in another area): mark
each sentence for the area that holds the topics it is about, the
survivors' area, not this one for the `new_home` alone (1.4.18, G42). Save it, and run again with `--marks A/building-<name>.json`,
writing `A/building-<name>-quoted.json`.
It prints the `markdown` to quote and `this_area`, the sentences that
are this area's; it exits 2 naming any sentence unmarked or marked
with no area of the cookbook. The **Gaps** section quotes the
`markdown` under the heading "Building specialities not yet measured",
naming the speciality and its `topics` (`--marks` prints `topics`: this
area's topics the worklist maps the speciality to, as `unmeasured.json`
gives them; 1.4.25, G77). Only the `this_area`
sentences are lacking from this area: they alone go into its gaps and
its topics' research briefs. The rest stay quoted and marked, never
dropped. A speciality an area does not list is another area's to
quote. Once a worklist topic of this area lists a building speciality in
its `devteam` entries, step 1.3 measures it there as well.

`unmeasured.py` runs before step 1.3, whose gaps commands need its
`survivor_elsewhere` rows.

A plan quotes a speciality's text from `A/reference/<speciality>.txt` (or
from the `A/building-<name>-quoted.json` this plan wrote from it) only,
never from another plan's quote: another plan's file may be cut from an
older reference (1.4.25, G88). That holds for another area's building
sentence quoted for the record too: quote it, by its text, from this area's
`A/reference/<speciality>.txt` (written by `speciality_reference.py` when
missing), never from that plan's files (1.4.33, G118). A file in
`A/reference/` with no `A/reference.json` row is read by the plan only: no
script measures it, so the plan quotes it and judges it by hand, naming it
under **Gaps** (1.4.36, G149).

Building text must reach the area it belongs to. Quote, in the **Gaps**
section, everything `unmeasured.py` lists:
- each `building` row, including one reached `by_new_home` (the worklist
  entry names a `new_home` of a survivor here, or the survivor of a
  `new_home` here). A null `file` is written first with
  `$COOKR_PY <devteam>/speciality_reference.py <speciality> --out A/reference`.
  A row whose `measured_by` is empty is measured by no topic's `roles
  gaps`: say so under its quote ("never measured: no topic's `devteam`
  names it"). It is never silently skipped. A `via` mapping (the worklist
  maps it to this area's topic through another speciality, the row's `via`
  `{"speciality", "topic"}` entries) is not a measure: the row stays
  unmeasured, its text quoted whole. `run_gaps.py` (step 1.3) adds the
  building speciality's file as an `--against` at each `via` topic, so its
  sentences are measured against that topic. A `via` topic with no folder
  yet (a `new` topic: `run_gaps.py`'s `unmeasurable`) has nothing to measure
  against: the plan lists the building sentences that are its subject in
  that topic's Why cell and in its research questions, and they count as
  gaps of the new topic (1.4.18, G35).
- each `marked_here` sentence: another plan's marks file gives it to this
  area; quote it with the `plan` that marked it. It is lacking from this
  area like a `this_area` sentence. `unmeasured.py` lists each sentence
  once per (speciality, `n`), every marking plan in its `marked_by` (1.4.24,
  G49). A sentence several plans mark, or that this area's own marks file
  already marks this area's, is quoted once, naming every plan that marks it.
- each `mark_conflicts` sentence: two plans mark it for different areas
  (two lists conflict only when their areas differ, order aside).
  Quote it with every plan's mark and list it under the plan's **Owner
  questions**; the owner settles it, and the plan that loses changes its
  marks file. Every row stays listed, overlapping lists included
  (`["implementing/testing", "testing"]` against `"implementing/testing"`),
  with `agrees_for`, the areas every plan's mark names, and `differs_for`,
  the areas some plan's mark leaves out. A row whose `differs_for` does not
  name this area agrees for this area: it is an owner item, listed under
  **Owner questions**, not a blocker for this plan. One whose `differs_for`
  names this area is this plan's conflict (1.4.25, G71).
- each `mark_conflicts` row with `reason: "numbering differs"`: a stale
  marks file, two plans numbering the speciality differently. It carries
  no `agrees_for` or `differs_for`: its marks are for different sentences,
  so it is always this plan's to resolve, never read as agreement (1.4.26).
  Quote it with both plans, both `n` and the text, under **Owner questions**. The plan whose
  marks file is stale re-quotes and re-marks it (G22); until then the
  conflict stays quoted under **Owner questions**.
- each `unread_marks` file: another area's marks file that could not be
  read (its run may be mid-edit) is skipped, not fatal; name it under the
  plan's **Owner questions** and re-run this step once that run saves it.
  This area's own unreadable marks file exits 2.
- which of these is this plan's to mark (1.4.33, G117): this plan marks only
  its own marks files, `A/building-<name>.json`; a `marked_here` sentence is
  the marking plan's, and a disagreement is a `mark_conflicts` row, never a
  re-mark of another plan's file. A `marked_here` speciality with no
  `building` row here has no marks file here: quote it with
  `quote_building.py --area <area> --speciality <speciality> --file A/reference/<file>`
  once its reference is written; a `--file` not yet written exits 2 naming
  the `speciality_reference.py` command that writes it. A `mark_conflicts`
  row naming this area for a speciality with no marks file here is listed
  under **Owner questions**, never marked here. A speciality two plans
  number differently is compared by text: one row per text the plans mark
  differently, `compared: "by text"`, each plan's number in `n_by_plan`,
  listed once beside its `numbering differs` rows (1.4.33, G114).

If it exits 2 with `unplaced` rows, the worklist places no area for
those specialities (no `building` entry maps a `building-split` one;
no new row, or more than one, claims any other). This is not this
skill's to place: stop the stage, and name each speciality and its
`why` to the owner. If it exits 2 naming a file, that input is missing
or unreadable: run the roles plan step that writes it.

### Step 1.3: each existing topic

3. For each existing topic of the area, measure it against the file of
   every row whose `topic` is that topic's folder (`<topic-folder>`,
   relative to `<repo>`), except a row `unmeasured.py` (step 1.2) lists in
   `survivor_elsewhere`, and of every speciality the topic's worklist
   entry (in `<workspace>/worklist.json`, the entry whose `survivor` is the
   folder without its leading `cookbook/`) lists in its `devteam` entries,
   one `--against` per speciality, each speciality once, and of each
   building speciality whose `via` names the topic. `run_gaps.py` builds
   and runs these topic measures; never build them by hand (1.4.18, G37).
   Only R9's `new-<name>.json` measures stay hand-built (below):
```
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/run_gaps.py --area <area> --workspace <workspace> --repo <repo> --hints
```
It reads `A/reference.json`, `A/unmeasured.json`, the worklist and the plan
(a topic resolves to its plan row's Artifact, else to its worklist survivor),
runs each command under `write_on_success.py`, numbers its lacking pieces
and only then replaces `A/gaps/<topic>.json`, and prints per topic `pieces`,
`held`, `lacking` and the lacking sentence numbers with a guessed home
(`lacking_by_home_guess`), and per building speciality each sentence's
`home_guess`, `held_at` and `lacking_at`. `--hints` adds
`paraphrase_hints.py`'s top 3 to each sentence held at no measured topic,
or one with a piece not measured, whatever its measured pieces say (its own
`held_at` is always empty, 1.4.22):
at its guessed home, or, with no guess, over every measured topic
(`hints_at` says which; each hint names its `topic`; 1.4.20; a topic whose run failed is never ranked, 1.4.21). It exits
2 naming a missing input, two topics with one basename, or a failed `cookr
roles gaps` run (listed in `failed`; its previous file is kept; each
building entry then carries `partial`, naming the failed topics: its
figures are not the area's until the failure is fixed and the run repeated). `--out DIR`
writes the gaps files elsewhere, for a read-only check, and
writes a missing reference into `DIR/reference`, never `A/reference` (1.4.26).
A `marked_here` reference (it has no `A/reference.json` row) is
rewritten on every run, never reused: into `A/reference` on a run, into
`DIR/reference` with `--out DIR`, into a scratch folder under `--check`
(1.4.27); with no `speciality_reference.py` to rewrite it, the old file is
used and listed in `stale_reference`. A run that lists any `stale_reference`
saves its report and exits 1, naming each on stderr: its figures are not
the area's (1.4.28). Every report records `reference_format`, the format
it was measured under (1.4.29). `run_gaps.py` refuses before any run:
an `--out` that is the area folder, or holds it, exits 2 whatever its
spelling (a symlink, `A/.`); an `--out` that resolves to `A/gaps` is the default (1.4.27).
So does an `--out` inside the area other than `A/gaps` (or a folder below
it), such as `A/reference` or `A/topics` (1.4.28).
`A/run_gaps.json` records `hints` (whether `--hints` ran); `--check`
compares `advisory_failed` only when the saved run and the check agree on
`--hints`, and otherwise lists it in `not_compared` (1.4.27).
`run_gaps.py` saves its JSON itself as `A/run_gaps.json` when `--out` is
the default `A/gaps`, and as `DIR/run_gaps.json` with any other `--out DIR`
(1.4.26: a scratch run never overwrites the area's report), written whole or
not at all, on a run's exit 2 too, never under `--check` and never on a
refused input (exit 2 before any run); stdout carries the same JSON. The plan
cites that file for every `run_gaps.py` figure (1.4.25, G90).

**An advisory failure.** `--hints` is advisory: a hint that fails never
stops the stage. `run_gaps.py` still writes every file, lists the failure
in `advisory_failed` (`part`, `speciality`, `n`, `why`) and on stderr, and
exits as it would without it; a home guess at a topic no speciality
measures is hinted there, not a failure (G66). The plan names each
`advisory_failed` row under **Gaps**, and runs
`$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/paraphrase_hints.py A/gaps --repo <repo>`
on its own for those sentences (1.4.25, G82).

Each topic's command, for example for the `indexing` topic of `implementing/data`, which
the speciality `data/indexing` stands on, with this repo at
`/work/agenticcookbook` and the default workspace:
```
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py /work/agenticcookbook/docs/grow-cookbook/areas/implementing/data/gaps/indexing.json -- PYTHONPATH=/work/agenticcookbook/skills/cookr/cli $COOKR_PY -P -m cookr -p /work/agenticcookbook roles gaps cookbook/guidelines/implementing/data/indexing --against /work/agenticcookbook/docs/grow-cookbook/areas/implementing/data/reference/data--indexing.txt --json
```
Each file's `lacking_sentences` is the speciality's text, in its own
wording, that the topic does not hold.

**Sentences and pieces.** A gaps file's figures (`pieces`, `held`,
`lacking`, and the entries of `lacking_sentences`) count cookr's pieces,
not sentences: cookr cuts at `;` and `:` too and leaves short pieces out.
`quote_building.py` numbers sentences. The plan quotes each topic's
figures from the gaps file and says they are pieces; it names each building
sentence by its number, separately, one sentence however many pieces it
holds, and never adds pieces to sentences (1.4.25, G73).

**Short sentences.** cookr leaves a piece under six words out of the
measure, so no gaps file names it. `run_gaps.py` lists each in
`short_sentences` (`speciality`, `n`, `text`), for every speciality's file,
direct, building, R9 or home-measured. Judge each one by hand at its
topic; it counts as a gap unless held (1.4.25, G72). Each row carries
`marked_for` (the sentence's mark; this area for a direct or R9 speciality)
and `topic`: a row whose `marked_for` names other areas only is counted,
never judged; G91 outranks "judge each" (1.4.33, G101). A row with
`fragment: true` is a piece cookr cut inside a backtick span, after `vs.`,
or at a heading label's `:` (so every `kind: "label"` row is a fragment too,
and the two counts overlap): it stays listed and counted unless judged
held, and may be judged as one group with the sentence it was cut from
(1.4.33, G102). A row with `kind: "label"` is a heading label or procedure
opener: it names a part and carries no rule, so it is held when the topic
has that part, else counted once with its part (1.4.33, G103). A label
whose part the topic lacks is one gap, counted with the part's lacking
sentence when there is one (1.4.36, G144). Only `label` and `opener` rows
take this held-by-part rule; every other kind is judged as a sentence. An
`opener` is a piece starting "Review" or "Closing", or a procedure lead
(Before, After, When, Once, First, Then, Next, Finally, During, Lastly,
Afterwards) ending in a colon, such as "Before merging:"; a piece ending
in "pass" ("Run the security pass") is a `piece`, judged and counted
(1.4.37, G161). A `--check` change to a `short_sentences` row whose kind
changed carries `kind_changed` `[old, new]`: re-judge that row (1.4.37,
G180). `kind` is one of `marker`,
`cut`, `heading`, `label`, `opener` and `piece`; a piece whose kind is
uncertain is `piece`, counted, never `label` (1.4.36, G125); a bold
label needs its colon (`- **name**:` or `**name:**`), and a bold line with
no colon is a whole rule, `piece` (fix round 1). `marked_for` is
never null: it is read from every plan's marks files by the sentence's
text; `"unmarked"` when a marks file holds the speciality and none marks the
sentence, `"unknown"` when no plan has a marks file for it or the piece is
in no one sentence; either is judged here (1.4.36, G124). A row marked
for other areas only carries `count_only: true`: listed and counted, never
judged here (G123). A piece that
is only a list marker is listed in `markers`, never dropped silently.

**One numbering.** cookr cuts text at `;` and `:` as well as at sentence
ends, and drops pieces under six words, so its pieces are not
quote_building's sentences. `run_gaps.py` writes beside each reference's
`lacking_sentences` its `lacking_numbers`: the number `quote_building.py`
gives the sentence holding each piece. The plan cites a building sentence
by that number only, the one `A/building-<name>.json` uses (1.4.18, G34).
`lacking_numbers` numbers a direct speciality's pieces the same way
(1.4.33, G118).

**Counting building sentences.** Each building sentence marked for this area
(a `this_area` sentence, or a `marked_here` one) is judged once, at its home
topic: the topic whose subject it is. Lacking there (and not held in other
words) it is one gap of that topic; lacking at the other topics it was
measured against is not counted only once the home topic holds it
(`counted: false`, G250) or that row has its own verdict. The unit `run_gaps.py`
counts is the topic row, one per topic the sentence was measured at, not the
sentence (1.4.42, G256): until then a row at a topic that is not its home
counts in `measured_total`, and the skill wants that verdict. A hold recorded at the home topic clears no other row, so each
non-home row needs a per-row verdict, `mark.py --held <id> held --why "judged
at home topic <topic>"` (or `not` with a why); `non_home_lacking`
(`run_gaps.py`, advisory in `stage_status.py`) lists each one still counted.
A `short_sentences` row marked for another area only (`counted: false`) owes no verdict here;
`short_not_owed` (`run_gaps.py`, advisory in `stage_status.py`) names each one, with `counted_at` and
why (1.4.42, platform-integration#5), so the rows owing a verdict are the rest.
A continuation piece (`#2`) is a row of its own too. A sentence marked for
another area is never this area's gap, wherever it is lacking. A home-measure,
`marked_here` or `home_unguessed` sentence lacking at its home is counted once,
at the area that owns its home (`home_lacking`, ids
`home:<speciality>:<n>@<topic>`); a marking area that is not that owner lists
it with `counted: false` and `counted at <area>`. Each lacking piece of the
area's own R9 files (`r9_lacking`, ids `r9:<name>:<speciality>:<n>`) counts in
`measured_total` too (1.4.42, G254). Every hand-judged lack is a row:
`mark.py --lack <topic> --source <reference relpath>#<n> --text "<sentence>"
--why "<one line>"` records it in `A/hand_lacks.json` (`hand:<speciality>:<n>@<topic>`),
counted in `measured_total` and its topic's `topic_totals` row; a sentence a
measured row already holds is refused, naming that row, and `--held <hand id>
held --why ...` withdraws it. A gap stated only in the plan's prose, with no
row, is not allowed (1.4.42, G253). Every hand judgment at a home is recorded, held or lacking
(1.4.43, G276): a hand hold is `mark.py --hold <topic> --source <relpath>#<n> --text "<sentence>"
--why "<why quoting the topic's rule>"` (`A/hand_holds.json`; the topic may be authored-unmeasured
or have no speciality), read by `run_gaps.py` and `--check-homes` as that sentence's verdict at that
home. `--source` is the reference file below A, W or R and the sentence number, e.g.
`reference/building--platform-windows.txt#10`; `quote_building.py --area <area> --speciality <s>
--file <f> --keep /dev/null` prints each sentence with its number (G287). Several pieces of one
sentence at one topic are separate rows with `--piece <k>`; a second `--lack` on an existing id is
refused unless `--refresh`; a wrong `--text` prints the expected sentence (G285). A non-owner hold
counted elsewhere is recorded structured, `mark.py --held <id> held --counted-at <area>` (an old why
`counted at <area>` or `the owner is <area>` reads the same, G273). `mark.py --non-home-held` marks,
in one call, each non-home row whose home has a recorded verdict in any area as held `judged at home
topic <topic>`, printing the count and leaving the rest counted (G284). An R9 row and its topic row
for one piece count once, at the R9 row (`counted_at: r9`, G281); `topic_totals` follows each row's
`counted` (G284). A Missing subject is never a `--lack` row: it has no source sentence; a Research
question or `### No host` carries it, and `run_gaps.py` reports `missing_subjects` beside
`measured_total`, never inside it (G286). A `home_lacking` row carries the sentence's `text` and its
lacking `pieces` (G302); a `--home` on any row, a `home_measures` one too, adds the marks file's
`homes` key or `A/homes.json` (G287). `run_gaps.py`'s `home_guess` and
`gap_candidates` are an advisory guess; the plan names each home.
`home_guess` is a measured topic that holds the sentence, else the measured
topic sharing most of its words (at least `HOME_SHARE`, 40%), and null below
that or on a tie; `gap_candidates` are the sentences marked for this area
held at no measured topic, before the held-in-other-words notes (1.4.19,
I1). A sentence's home may be a topic it was not measured against (outside
its `via`) or a `new` topic: judge it against that topic's text, or run
`cookr roles gaps <home-folder> --against <building file> --json` into a
scratch file; at a `new` topic it is that topic's gap (G35). A sentence is
measured only when cookr measured every piece of it. A sentence
`run_gaps.py` lists in `unmeasured_sentences` has a piece cookr did not
measure (under six words, named in its `unmeasured_parts`, 1.4.20; or its
file was measured at no topic: `measured_at` is [], a row with no `via` or
only `new` ones), so no measure says it is held: judge each one by hand at
its home topic; it counts as a gap unless held (1.4.19, I2). Every
sentence not fully measured is listed in `unmeasured_sentences`, whatever
its mark, as `{"n", "marked_for"}` (1.4.24, G48, G64): `marked_for` is its
mark (an area, a list of areas, or null). Judge each whose `marked_for`
names this area, or is null (mark it first); one marked for other areas
only is listed so nothing is hidden, and is judged in the area it names.
Rows whose `marked_for` names other areas only, in an all-new or
unmeasurable area too, are not this plan's to judge, and only need a count:
the plan gives how many, never their verdicts (1.4.25, G91).
`lacking_candidates` gives each sentence held at no measured topic, or with
a piece not measured, up to 3 topic folders of the area ranked by the share
of its words they hold, every topic folder counted, an authored one no
speciality names included; with no `home_guess`, the first at `HOME_SHARE`
or more, untied, becomes it. It is advisory, like `home_guess` (1.4.24, G50).
`same_text` groups a lacking piece whose text recurs across specialities
(a closing "A review passes when ..." line in each): judge it once and
record that judgment under each speciality, which still lists it; nothing
judges it for you (1.4.24, G51). Each topic row splits its `pieces`,
`held` and `lacking` into `own` (its specialities' pieces and this area's
building pieces) and `building_marked_elsewhere` (building pieces whose
sentence is marked for other areas only), summing to the totals: the plan
quotes `own` as the topic's figure (1.4.24, G52). `own` and
`building_marked_elsewhere` count pieces, like every gaps-file figure,
whatever a key's name says (1.4.33, G118). Each lacking piece counts where
it stands: `repeat_of` lists, within one speciality, each lacking sentence
that restates an earlier one (the same text, or most of its words; the
shape of `same_text`); the plan notes it "repeat of <n>" and still counts
it (1.4.33, G104). A row for sentences 1 and 2 (a speciality's own
Review focus and its restatement, which every direct speciality has)
carries `review_focus_pair: true`, tagged, never skipped, only when the
reference opens with that Review focus: a format-3 roled reference leaves
its copied Review focus out (its `A/reference.json` row's `copied` names
it), so its sentences 1 and 2 are other text, never tagged, and each counts
as a gap like any other (1.4.46); its `pieces`
name each sentence's text and the topics it is counted at, so the pair is
judged once as review procedure (*Review-procedure sentences*; 1.4.36, G146). A sentence
measured in part keeps its measured pieces' verdicts under `measured_pieces`
(and `home_guess`) beside its `unmeasured_parts`, so the hand judge sees
both; it is never a `gap_candidates` entry (1.4.21). `measured_pieces` is
not a verdict on the sentence: its `held_at` and `lacking_at` cover the
measured pieces only (1.4.23). The sentence's own `held_at` and `lacking_at`
stay empty, its `by_hand` says it is judged by hand, and a
`lacking_by_home_guess` row for it carries `measured: false`. Never record
such a sentence as held from `measured_pieces`: it is not held until judged
by hand (1.4.22). A building entry may carry `unplaced_pieces`: a piece
cookr did not measure that no sentence holds; judge each one by hand too
(1.4.21). A measured piece no one sentence holds is never dropped either: it
is listed there with its verdict (1.4.22). `unmeasured_sentences` and
`unplaced_pieces` are fields of each `building` entry, not top-level keys
of the report (1.4.37, G178). The entries are each an object:
`text`, `measured`, `verdict`, `topic`, `sentences`. A piece cookr did not
measure is listed once, `verdict` and `topic` null; a measured one once per
measured topic, `verdict` `lacking` at each `topic` where cookr listed it
lacking, else `held` (1.4.23). `sentences` numbers each sentence the piece
could belong to: each carries the piece in its `unplaced_parts`, is listed
in `unmeasured_sentences` and has no verdict of its own, so judge it by hand
with the piece. With `sentences` [] no sentence can be chosen: judge the
piece by hand alone, at its home topic. A topic row's `unplaced` counts its
lacking pieces with no number (a null in `lacking_numbers`). The **Gaps**
section records, per building speciality, each counted sentence's number and
home topic, and the count per topic (1.4.18, G33).

**Measured at its home.** Every building sentence whose home is
unmeasured, marked for any area (each `home_measures` sentence carries
`marked_for`; rows marked elsewhere are counted, never judged, G91; 1.4.33,
G100): one whose `home_guess` is a topic its file was not measured at (most often a topic no
speciality names), and each sentence of a `marked_here` speciality with no
building row, is measured at its home by `run_gaps.py` itself, into
`A/gaps/home--<topic>.json`: one of its own files, cleared like the rest,
never an R9 `new-<name>.json`. A missing reference is written into
`A/reference/` first by `<devteam>/speciality_reference.py` (`--devteam`,
default `<repo>/../..`). `home_measures` lists each home: `topic`,
`folder`, `gaps_file`, `specialities`, and each sentence's verdict there
(`lacking`, `held`, or `not measured`: a piece under six words, or a home
file with no row for that reference, which the row names in
`unmeasured_references`; judge either by hand). A sentence whose home cannot
be guessed is in `home_unguessed`, every building sentence with no
`home_guess` and no measured-topic home, whatever the reason (1.4.33, G95):
record its home with `mark.py --home` (below) and judge it by hand. A
`count_only` row (below) is listed and counted whether or not a home is
recorded: recording one is optional, needs no judgment, and a recorded one
shows `home_recorded` and stays listed (1.4.37, G157; 1.4.39, G206). A guessed home carries
`home_shared_words`, the words the sentence shares with it, so the guess is
checked at a glance (1.4.33, G121). A `home_unguessed` row marked for
other areas only is tagged `count_only`, listed, never removed (G123).
Record the home the plan names with
`$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/mark.py --area <area> --workspace <workspace> --repo <repo> --speciality <s> --home N=TOPIC`
(alone on its call; `N=AREA:TOPIC` for a home in another area, kept in
`A/homes.json`, the area known and the topic one of its topics; `N=`
clears either), then re-run step 1.3 so `home_recorded` is saved in
`A/run_gaps.json`: the run reads the marks file and `A/homes.json` and
lists the sentence's home as `home_recorded`, the row kept (1.4.36, G145;
1.4.37, G156, G177). `--home` needs `--speciality` (1.4.39, G204); the
same-area form writes the building marks file's `homes`, the cross-area
form `A/homes.json`; a sentence holds one home, a new one replacing it. A
home is recorded for any building sentence of the saved `A/run_gaps.json`: one in
`home_unguessed`, in `home_measures`, or with a `home_guess`; a recorded home
replaces the guess as the sentence's `home_topic` (1.4.40, G230). A
sentence the report lists nowhere exits 2 naming that. A recorded home moves no
figure by itself (`measured_total` is the lacking pieces of each topic);
the hold or lack at the home topic does, through a recorded verdict. A `not` on
a held row makes the same sentence `lacking` in its `home_measures` row at that topic
(`verdict_by` names the row), so the figure is counted once (1.4.40, G246). A recorded
home that names no topic (a bare name an older version kept for another
area's topic, or an `A/homes.json` value not in `AREA:TOPIC` form) is a
`stale_home` row, on stderr too, in `run_gaps.py` and `quote_building.py`
(`--keep` or `--marks`): re-record it with `--home N=AREA:TOPIC` (1.4.39,
G205). A sentence
lacking at every topic it was measured at says so in its `why`
("measured, lacking at every topic it was measured at (...)"): name its
home by hand, never leave it unplaced. A
`marked_here` row is matched by its text, not its number alone: when the
reference's sentence `n` is another text (the marks file numbered an older
reference), the row is in `numbering_differs` with the text `now` at `n`,
`found_at` and `measured_as` (the one sentence its text names, or null:
then it is not measured). Re-quote that plan's marks (G22); until then,
judge a null `measured_as` by hand and list it under **Owner questions**
(1.4.26). Such a row is in `home_unguessed` too ("numbering differs: …"):
judge it by hand or re-mark it, as every other sentence there (1.4.27). A
row two marking plans hold is listed and measured once (1.4.27). No hand-run scratch measure is needed
for these (1.4.25, G68).

**A speciality two plans measure.** A speciality one plan claims for a
`new` topic (`new_topics`) and another measures at its own topic
(`documentation/instruction-files`) is counted by each plan at its own
topics only. A sentence counted in both is named in both plans, each
naming the other, never dropped from either (1.4.25, G85).

**A speciality stale against its topic.** A speciality whose text is out of
date against its topic, or contradicts it (a meta field the topic dropped,
such as template-conformance's `domain`; a ratio the topic rejects, such as
test-pyramid's), is counted by the measure all the same. The plan raises,
under **Owner questions**, a question that names the contradiction: which text says what, and
which the research must settle (1.4.25, G86). A sentence both this rule and
*Review-procedure sentences* (G41) touch: G41 decides whether it counts,
and this owner question is raised all the same (1.4.33, G118).

**A topic measured in another plan.** A topic whose plan row is `merged`
with its Artifact folder in another area is measured against that folder,
by the plan that runs it: that folder's area. `run_gaps.py` lists it in
`measured_elsewhere` and does not run it; this plan's **Gaps** section
records "measured in <plan>" for it and does not count it (1.4.18, G36).
Every plan row `merged` with its Artifact in another area is listed there,
whatever its speciality (`specialities` [] when none of this area names
it; 1.4.24, G46). With no topic to measure, `why_empty` says why ("area has
no speciality", every topic merged or measured elsewhere); the **Gaps**
section quotes it. A topic no row names has no
gaps file, and the plan's **Gaps** section says so.

**A run before the plan.** Before `A/area-plan.md` exists, `run_gaps.py`
resolves topics through the worklist alone, so it may measure a topic the
plan will not own (its `new_home` in another area). Its figures stand only
until the plan is written: the step-4 `--check` re-run settles which topics
are this area's (1.4.24, G63).

**A speciality on a copy.** When a speciality's topic is a copy (the
worklist names another `survivor` for it), it is measured in the
survivor's area plan, against the survivor, never in the copy's plan.
`unmeasured.py` (step 1.2, run first) lists them: `against_survivor` rows are this
area's to measure, each with an `--against` on its survivor's gaps
command (a null `file` is written first with
`$COOKR_PY <devteam>/speciality_reference.py <speciality> --out A/reference`);
`survivor_elsewhere` rows are skipped here (the survivor's plan measures them), and the **Gaps** section
names each with the survivor's area that measures it.

**Held in other words.** `roles gaps` matches wording, not subject. After
it, note under each lacking sentence whether the topic holds it in other
words, holds it partly, or does not hold it. Only the partly held and
not held sentences count as gaps in the plan; the held-in-other-words
ones stay quoted, with that note. Run
`$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/paraphrase_hints.py A/gaps --repo <repo>` first:
for each lacking sentence it lists the topic sentences with the highest
word overlap (top 3, each with a score), the ones to read first. It is
advisory: its output never decides held or not held, and the plan judges
each sentence itself. A cookr `held` that rests on wording only (the topic
uses the words, not the rule) is overturned by hand: quote both texts, note
it "held in wording only: not held", and count it (1.4.33, G118).
`run_gaps.py` lists every piece cookr holds at a measured topic or at its
home in `held_by_wording` (`speciality`, `n`, `text`, `topic`,
`marked_for`, `number_differs`): re-judge each row, first those with
`number_differs: true` (a numeral the topic's text never says); none is
filtered (1.4.36, G132). Each row also carries `topic_sentence`, the
topic's sentence nearest the piece (the one to compare first), and `id`,
`<speciality>:<n>@<topic>` (`#2` and on for a repeat). Since 1.4.39 each
row also carries `rule_sentence` (the topic sentence holding the piece, else its nearest
heading's scope: never a neighbour or the topic summary, 1.4.40, G227), `nearest_modal_sentence`,
`topic_hash` (the topic's whole text),
`modal_piece` (the strongest RFC 2119 word of the piece), `modal_piece_all`, `modal_sentence` (the modal
of the building sentence the piece was cut from, 1.4.40, G223), `modal_topic` (the weakest word of
`rule_sentence`: MUST, with `modal_topic_implied`, for a sentence that opens with a verb and holds none),
`modal_differs` (the topic's rule is weaker than the piece's modal, else its sentence's, else MUST), and
`home_topic` and `home` (whether the topic is the sentence's home), `counted` (false when this row is no home
of the sentence and the home topic holds it, 1.4.40, G250) (G201,
G202). Record the verdict
with `$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/mark.py --area <area> --workspace <workspace> --repo <repo> --held <id> held|not`
(alone on its call; `A/held.json`, never edited by hand, 1.4.42, G255), or many with `--held-file FILE`, a JSON
object `{"<id>": "held"|"not"}` (or `{"<id>": {"verdict": ..., "why": ...}}`), one unknown id or verdict writing none;
it prints `{file, verdicts, changed: N}`, the ids only with `--verbose` (1.4.40, G243)
(1.4.39, G199). Since 1.4.40 `--held` takes any row id of `held_by_wording`, `lacking_pieces`
(`lacking:<speciality>:<n>@<topic>`: `held`, the plan holds the piece in other words, or `not` with a
why, the lack confirmed, 1.4.42, G255), `home_lacking`, `r9_lacking`, `hand_lacks` and
`short_sentences` (`short:<speciality>:<n>`: `held` or `not`), each with `--why "<one line>"` where a
lacking piece is `held` or a short sentence is `not`; a hand judgment that moves the total is recorded this
way and run_gaps applies it (G225, G226, G233): the next run gives the row `verdict`
while the piece, `topic_sentence`, `rule_sentence` and `topic_hash` are
those it was judged on, else `verdict_was` and `verdict_why`: judge it
again (any rule of the topic changing resets it; a verdict recorded before
1.4.39 keeps its verdict, `verdict_unpinned`, until re-recorded, G202). The row is
listed either way (1.4.37, G159). A reset verdict never lowers a total (1.4.41,
G251): a row with `verdict_was` and no `verdict` counts lacking, as a `not` does, until
`mark.py --held` records a new verdict on the current text: a reset `not` stays lacking and a reset
`held` is lacking until judged again, so a reset can only raise `measured_total`. `stage_status.py`
lists each such row in `stale_verdicts` (read from the saved `A/run_gaps.json`; a hold: `next` stays at
`plan`; `--keys` prints its rows; re-run step 1.3 after re-recording to clear it)). Each row carries what to judge it again on (1.4.42, language#3): the piece
(`text`), the rule and topic sentence the verdict was recorded on (`rule_sentence_was`,
`topic_sentence_was`) and the current ones (`rule_sentence_now`, `topic_sentence_now`), `rule_at`, and
`topic_files`, the topic's part files the sentences are read from: read those, no compile is needed. A `not` verdict counts the piece lacking
in the saved figures (the topic's `held`, `lacking`, `own`, its
reference's, `not_held_by_verdict`), and `run_gaps.py --check` lists a
plan whose `This area's gaps: N` differs from the measured total in
`gap_total` (advisory). The unit (1.4.40, G225, G226, G233): the plan states
`This area's gaps: N`, N being `measured_total`, the sum of every topic's `own.lacking` after every
recorded verdict, in pieces, plus each short sentence judged `not` held; a plan with no lacking pieces
states `This area's gaps: 0`. The accepted form, exactly (1.4.42, G259; step 3): `This area's gaps: N` on a
line of its own, N a number; allowed are a leading list dash, bold around the label (`**This area's gaps:** N`),
around the whole line (`**This area's gaps: N**`) or around N, and a final full stop; nothing else on the
line. Only a line giving this area's gaps a number is read as a stated line; prose naming them
without one is not (1.4.43, G294). An old plan's duplicate stated line is removed, leaving one. The `gap_total` row quotes the line it read and this form. A `(run_gaps M; K by hand)` form, any other wording of the line, and a plan
with lacking pieces and no such line are `gap_total` rows too; a hand judgment never goes in the line as a
"by hand" term, it is a recorded verdict. `--check` reports a verdict that moved the total in `gap_total`
and `verdict_changes` (`{id, kind, was, now, total_delta}`), and `--digest` prints `gap_total_rows N;
measured_total M` (1.4.40, G247).

The G160 table (1.4.37, G160; 1.4.39, G187, G200): each verdict is a hand
verdict by these cases, and no owner question overrides it:

| Case | Verdict |
|---|---|
| The topic sentence contradicts the building sentence | `not`; the contradiction goes under **Gaps** |
| The topic's rule is weaker than the piece's: MUST, NEVER, ALWAYS or a build failure against SHOULD, MAY, CONSIDER or Prefer; `Do NOT` against `SHOULD NOT`; an unconditional rule against one with an exception (`modal_differs: true` flags the modal cases; a text holding several modals reads its strongest on the piece side and its weakest on the topic side, so a mismatch is reported, 1.4.40, G227) | `not`: count it. A weaker modal is never `held` |
| The piece has no modal word (`modal_piece: null`) | it takes the modal of the building sentence it was cut from (`modal_sentence`); only when neither has one is it a MUST: a piece from a "Prefer" sentence against a "Prefer" topic is `held`, the same piece from a sentence with no modal against a SHOULD topic is `not` (1.4.40, G223) |
| The topic sentence is a checklist row | its Severity cell is its modal: FAIL is MUST, WARN is SHOULD, INFO is MAY; a row with no Severity cell reads as its words do; `rule_sentence` is that row, never the whole table (1.4.40, G224) |
| The topic sentence opens with a verb and holds no modal (`Validate every token.`, an imperative) | it reads as a MUST (`modal_topic_implied: true`): a piece with a SHOULD is `held`, a piece with a MUST is `held` too; example row: `Validate every token.` |
| The topic sentence has no finite verb (a heading, a label, a fragment such as `Token validation`) | judged against `rule_sentence`, the nearest sentence holding a modal word (1.4.40, G249); example row: `Token validation` -> its section's rule |
| The hold is at a topic that is not the sentence's home (`home_topic: false`) | `not`, unless the home topic holds it too |
| `topic_sentence` is a heading, a fragment or an example | judge against `rule_sentence`, the neighbouring rule |
| A `count_only` row (marked for other areas only) | no verdict owed; it is counted |
| `modal_differs: true` | `not`: the modal case above, never `held` (1.4.42, G260) |
| The piece is a cut fragment (cookr cut it at `;` or `:`) | judge the whole building sentence it was cut from against `rule_sentence`: `held` only when the rule states the fragment's part, else `not` |
| The piece or `topic_sentence` opens with a label lead-in (`**Note:**`, `Example:`) | read past the label; the label is never the rule |
| A multi-clause piece (several requirements joined by `and`, `;` or a list) | `held` only when every clause is stated at an equal or stronger modal by some sentence of the same topic, `rule_sentence` or another: record it with `mark.py --held <id> held --clause "<clause>" --cites "<topic sentence>"`, one pair per clause (a cited sentence weaker than the piece's modal is refused, 1.4.43, G280); one clause missing is `not` |
| A tool or library list (`use X, Y or Z`) | `held` only when the topic states each item; each item is a `--clause` (1.4.43, G280) |
| A summary paragraph (several requirements in one sentence or paragraph) | `held` only when the topic states each clause; one `--clause`/`--cites` pair per clause (1.4.43, G280) |
| A flat clause, then a MAY or SHOULD clause, in one sentence | the flat clause is judged by its own modal (MUST with none), never by the later clause's (1.4.43, G280) |
| A negated lowercase modal (`no X may`, `must never`, `may not`), or a modal inside a relative clause or a quoted example (`may have bypassed`) | the first reads as MUST NOT; the second is no modal (1.4.43, G275) |
| An older plan's "held in other words" note this table overturns (a weaker modal, a non-home hold) | the table wins: record `not` with `--why "G160 overturns the <version> hold: <reason>"`; the old note is history |

`rule_sentence` is the one sentence (or checklist row) holding the piece, its
place named in `rule_at` (`<part> sentence N`, plus ` row <id>` for a table
row): of the topic's sentences sharing the piece's words within 85% of the
best match, the one with the strongest modal, so a checklist row with a FAIL
beats a WARN row and the sentence holding the piece beats a longer one sharing
its nouns; a whole table is never a rule (1.4.42, G260). `preferred`,
`preferably` and `optionally` are modals (SHOULD, SHOULD, MAY); `respect`,
`honor`, `favor`, `support` and `emit` open an imperative.

A gaps folder that does not exist is an exit 2:
fix the path.

**Review-procedure sentences.** A sentence about how to review (evidence
units such as `__evidence__`, finding formats, what a report records) is no
rule a writing-side topic can hold. Note it "not held: review procedure":
it stays quoted, does not count as a gap, and stage 3 routes it to the
area's review-focus. This applies to writing-side topics only: in a
`reviewing/` area a finding format or report rule is something the topic
holds, so lacking it is a gap, counted like any other (1.4.18, G41).

**A circular measure.** A speciality whose text restates its topic (or
the topic's copy) measures circularly: a 100% held from it says nothing
was lost on fold, and nothing about whether the topic is correct. Both cases
are circular: a speciality that restates the topic itself, and one that
restates a copy merged into the topic (measured against the survivor, so
its held share need not be 100%). For each such speciality the **Gaps**
section says it is circular and what the measure does and does not show:
it shows which of the speciality's sentences the topic holds (and, for a
copy's speciality, what the fold must still carry); it does not show that
the topic is correct or complete.

**A new topic's candidate survivor (R9).** Measuring a `new` topic's
candidate text against an existing survivor writes `A/gaps/new-<name>.json`,
`<name>` being the new topic, under `write_on_success.py` like any gaps file:
`... A/gaps/new-<name>.json -- cookr roles gaps <survivor-folder> --against A/reference/<speciality>.txt --json`.
In full, run from `<repo>`, `A` written as its absolute path
(`<workspace>/areas/<area>`, so `--against` is absolute), `<survivor-folder>`
relative to the repo and `<speciality-file>` the reference file's name
(`/` as `--`: `data--indexing.txt`) (1.4.37, G173):
```
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py A/gaps/new-<name>.json -- PYTHONPATH=<repo>/skills/cookr/cli $COOKR_PY -P -m cookr -p <repo> roles gaps <survivor-folder> --against A/reference/<speciality-file> --json
```
`env PYTHONPATH=<repo>/skills/cookr/cli $COOKR_PY -P -m cookr ...` after the
`--` works too.
The plan quotes its counts from that file. `run_gaps.py` lists in
`r9_targets` each new topic's candidate survivor outside the area, with the
`out` file it owes, and never measures that folder as a topic of this area
(1.4.24, G53). Right after writing or re-running an R9 file, stamp it:
`$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/r9_stamp.py A/gaps/new-<name>.json --repo <repo>`
records the `git hash-object` hash of each reference it was measured against
(`reference_hashes`) and the hash of the survivor folder's `artifact.json`
and `*.md` files (`folder_hash`, 1.4.34; never written by hand). A relative
path resolves against the area folder and the folders above it up to the
workspace's, then `--repo` (so pass it: a survivor `folder` written relative
to the repo, as the R9 command writes it, is found only there; 1.4.35), never
the cwd. `run_gaps.py` (a run and `--check`) and
`stage_status.py` list an R9 file whose hash is missing or differs from its
reference or survivor folder now in `r9_stale` (`folder_changed` when
another area's stage 4/5 rewrote the survivor), as is one with no `folder`
or an empty `references` list (`unreadable`); each holds the area at `plan`:
re-run that R9 measure, then stamp it again (1.4.33, G94; 1.4.34). Run
the R9 command from the repo with the survivor folder written relative to
the repo; each `r9_stale` row's `why` names the fix. A saved-report view
(`--keys`, `--summary`, `--digest` without `--check`) prints the report and
does not repeat its `r9_stale` stderr (1.4.36, G140).
- A `new` topic the plan proposes with no worklist row takes as its
  candidate survivor the nearest existing artifact by `paraphrase_hints.py`
  and the home guess (`lacking_candidates`); the plan names it in the Why
  cell, and its R9 measure is run against it (1.4.24, G62).
- In an area with no topic folder (empty, or all `new`), the candidate
  survivor is chosen from the whole cookbook: search it (`grep -ril` over
  `<repo>/cookbook/`) for the topic's subject, and the plan names how it was
  chosen, the search and the hits weighed (1.4.25, G87).
- A `-windows` or client variant the worklist makes `new` while
  `A/reference.json` measures its speciality on the base topic takes the
  base topic's measure as its gap count, and the plan says so.
- A variant that restates its base topic's text is a split-or-merge
  question: the plan hands it to the owner and does not decide it, listing it under
  **Owner questions**.

### Step 1.4: exits

4. If `speciality_reference.py` exits 2, it names a speciality that does
   not exist, or one found in more than one domain with both folders:
   fix the name or the pool. If `cookr roles gaps` exits 2, it names the
   path that is wrong: fix the path, never the topic. If `run_gaps.py`
   exits 2, it names the input, the basename clash or the failed topic,
   or lists a topic folder that cannot be read in `unplaced`. An `unplaced`
   exit 2 still wrote every other gaps file and printed the JSON: keep
   them. List each `unplaced` topic under **Owner questions** and judge it
   by hand; never plan on as if the topic did not exist.

## Step 2: Classify each topic

2. Classify each topic by research type before anything else, with the three
   lenses of `guidelines/researching/process/research-type-taxonomy`
   (intent, domain, method). The type picks the sources and the bar; most
   cookbook topics are *Technology / software* or *How-to / troubleshooting*.
   An R8 checklist topic (the worklist `kind` `checklist`) is *Technology /
   software*, intent *Evaluate* (1.4.24, G62).
   A topic the taxonomy does not name takes the nearest type (1.4.25, G81):
   writing craft is *How-to / troubleshooting*; ML or LLM evaluation is
   *Technology / software*, intent *Evaluate*, with the *Scientific /
   empirical* and *Statistical* bars for each metric claim; a method topic
   resting on psychology findings spans *How-to / troubleshooting* and
   *Scientific / empirical*. For a topic outside software, question 3
   (*Platform guidelines*) means the method owners, the published style
   guides and the standards bodies the topic touches. Whether a topic's
   research bar escalates is the owner's question: name it under **Owner
   questions**; plans do not escalate on "acted on" alone until the owner rules.
   Every plan names the question for each topic, even when the answer is "no
   escalation" (1.4.33, G116): a top-level item under **Owner questions**
   that says "research bar" and names the topic (as the **Topics** table
   names it), or one that names every, each or all topics with no topic
   name and no "except", "but" or "other than" after that phrase (such a
   question names only the topics it names before the exception word).
   `plan_sections` lists each topic of the **Topics** table that no such
   question names, and holds the area at `plan` (1.4.36, G128). With no
   table under **Topics** the topics are **Proposed topics**' `Topic`
   column (a trailing note such as "(new)" is no part of a name); with
   neither, one row says "Topics lists no table the
   research-bar check can read" (fix round 1). Only a section's first table
   is read; a later table under **Topics** or **Proposed topics** names no
   topics (1.4.37, G166). A topic merged into another
   area owes no question here: the survivor's research bar governs a copy,
   and `plan_sections` lists no research-bar row for it (fix round 1).

## Step 3: The area plan

3. Write `A/area-plan.md` with these sections, in order, each a `## `
   heading spelled as here (every folder a full path, *Full paths* above).
   `stage_status.py`'s `plan_sections` lists each one missing, misspelled or
   out of order, and holds the area at `plan` while it lists any (1.4.33, G97):
   - **Topics:** every topic in the area, from the worklist rows and the
     speciality map (each topic's path, survivor, copies, the specialities on
     it), and its research type. Every merged copy is folded into its
     survivor and checked lossless at stage 5 (`--copy`), whatever its
     worklist `fold_check`; `stage_status.py` lists them as the topic's
     `fold`. A copy is not folded only when a plan keeps it as an artifact
     of its own (Action `kept`; a `dropped`, `split` or `new` row still folds).
     A copy one plan keeps and another merges is a conflict (`stage_status.py`
     reports it in both the merging and the target area, even when the
     target plan names the copy), and is folded until the owner settles it. Say so for each copy, folded or not.
     A worklist copy's `fold_check: false` is superseded by this rule (1.4.15):
     it does not keep the copy from folding. On a `merged` row of this plan
     whose Artifact lies in another area (`next` null, `merged into <folder>`),
     `fold` names the copy that the survivor's area folds, not this one.
     An artifact two plans both keep (Action `kept`) is a conflict too:
     `stage_status.py` reports it in each keeping area, an owner item,
     with `kind: double-keep` and every keeping plan in `plans` (no single
     `plan` or `copy`, as a merge conflict has). The plan whose area holds
     the kept folder runs the topic; the other plan's row stays until the
     owner retires it, and the later plan names the double-keep under its
     **Owner questions**. A kept twin is researched on its own and never borrows its twin's research
     (1.4.25, G83).
   - **Gaps:** from `A/gaps/<topic>.json`, each speciality's text the cookbook lacks,
     quoted, with the topic it belongs to; for each new topic, the whole
     text of every speciality it claims; and, under "Building specialities
     not yet measured", the whole text of every building speciality the
     worklist maps to this area (step 1.2).
   - **Missing subjects:** what a practitioner would expect this area to
     cover and it lacks, each a numbered item led by a bold phrase naming
     the subject (`1. **Flag cleanup**: ...`). Carry each subject by writing
     its bold lead phrase verbatim (case and punctuation aside) in the
     **Research question** that carries it, in the topic that answers it; a
     paraphrase is no carry. A subject no topic answers is carried, no host:
     its phrase appears verbatim under **Owner questions** as a candidate
     `new` topic, and in **Research questions** (the nearest topic's, or
     under `### No host`: the host rule below) in an
     item marked "carried, no host": the mark goes in the same list item as
     the phrase, on its line or on a sub-bullet under it, never in a sibling
     item (1.4.35). A bold lead names the subject in words (non-ASCII letters
     count; a lead with no letter or digit is its own row). `plan_sections` (no fuzzy match;
     Research and Owner questions searched apart) lists each subject whose
     phrase is in no Research question ("carried nowhere", or "named only
     under Owner questions"), each "carried, no host" item whose phrase is
     not under Owner questions, and each top-level numbered or `-` item with
     no bold lead ("no bold lead phrase"); a re-run fixes each by rewriting
     the plan (1.4.33, G105; 1.4.34).
     The format (1.4.36, G126, G127): each subject is a numbered item whose
     bold lead is on its first line; a bold-led paragraph that is no list
     item is flagged ("not a list item"); every bold phrase of an item is
     checked, a second one as a subject of its own ("a second bold phrase
     of the item ..."). A carry is the phrase as a whole bold span inside a
     list item, or as a whole list item, inside **Research questions** (or
     **Owner questions**); a phrase inside a longer phrase, in plain text or
     in bold in a loose paragraph is no carry ("named but not carried"),
     and a heading never counts (fix round 1). Bold inside a code span is
     code, never a subject (a code span with no bold in it, such as
     `ContentProvider` inside a bold subject, stays part of it); only a paragraph's first line (after a blank
     line) can be bold-led (1.4.37, G165).
     The host rule (1.4.36, G130, G131): a topic hosts a subject only when one
     of its four research questions states what to do about the subject,
     not merely names it or its method (1.4.37, G162): "compare the cache
     libraries' eviction policies" hosts *cache eviction*; "covers
     caching" does not. Else the subject has no host: carry it as its own
     numbered item, after the four, in the topic sharing the most content
     words of its title with it, never in a merged copy, marked "carried,
     no host", and name it under **Owner questions**. Stop-words (and, of,
     the, for, in, with, a) and the words of the area's own name
     (`testing`, `ui`) never count as shared (1.4.37, G164). With no shared
     content word the subject goes in no topic, never the first one: carry
     it as an item under a closing `### No host` heading of **Research
     questions**, marked "carried, no host", and name it under **Owner
     questions** (1.4.37, G164). A subject a topic answers only in part
     (some of the subject's questions it leaves unanswered: "covers
     retries, not idempotency keys") is carried to that topic, its item
     asking the unanswered questions, AND named under **Owner questions**
     (1.4.37, G162). When in doubt, no host.
     Since 1.4.39 the shared word must be specific (G188, G209): words are
     compared lower-cased on a simple stem (a trailing `s`, `es`, `ing` or
     `ed` dropped: `column`/`columns`, `test`/`testing`); stop-words, every
     segment of the area's path, and the generic words strategy, design,
     management, pattern(s), guideline(s), practice(s), approach,
     system(s), framework(s), general, basics, overview and quality never
     count. A topic's title is its folder name and its artifact title, both.
     Since 1.4.40 (G228, G229, G241) the host rule runs on every bold-led
     subject hosted anywhere (an item led by a research label is no
     subject and is skipped); a topic shares only with two shared stems,
     or one that is a whole word of the topic's folder name; a word every
     topic folder name of the plan holds (`checklist` in skill-checklist,
     agent-checklist) never counts; a one-letter pair around a slash
     (A/B) is one word (`ab`), so A/B testing matches ab-testing.
     GENERIC words (stage_status.GENERIC): agent, approach, approaches, based, basic, basics, choose, configuration, cross, design, designs, driven, framework, frameworks, general, guideline, guidelines, manage, management, overview, overviews, pattern, patterns, practice, practices, quality, strategies, strategy, system, systems, target.
     With a tie the subject names every tying topic in one item (any case; a hyphen may join a
     word, so Swift-import names swift, never another topic's name such as swift-concurrency) and is
     the whole bold lead of an item under **Owner questions**; the row's `unnamed` and `owner_item`
     say which half is missing (1.4.42, language#5). `stage_status.py`'s `host_check` (a hold at
     `plan`) lists a hosted subject whose topic shares no specific word and
     a `### No host` subject that does share one (G208); its advisory
     `shared_no_host` lists each other plan whose `### No host` carries the
     same subject (G190); its row stays listed and says `named_in_owner: true`
     once an Owner question names that plan and the subject (1.4.40, G244). When several rules meet one subject, G162 goes
     first (a merged copy never hosts), then G164 (no shared word: `### No
     host`), and a G163 carry ask is written inside that `### No host` item,
     naming the survivor on its first line (G210). The `### No host` fix, whole (1.4.43, G297): move
     the item under `### No host`, remove the topic's own question 5 when it carried the subject,
     renumber the Research questions, name the survivor on the item's first line, and name the
     subject under **Owner questions**; with a tie, the item in the host topic carries the tie text.
     A carry summary is a table, never a list of bold-led bullets (those read as hosted subjects);
     a merged copy never hosts. The order, and which wins
     (1.4.42, G264): (1) a merged copy never hosts; (2) `host_check`'s
     shared-word test decides whether a topic may host at all: a topic sharing
     no specific word is never the host, whatever its questions say; (3) among
     topics that pass (2), G162 and the four research questions decide: the
     host is the topic one of whose four questions states what to do about the
     subject, and a topic answering it only in part carries it there, asking
     the unanswered questions; (4) a subject no topic passes goes under `###
     No host`, named under **Owner questions** with the topic that answers it
     in part. A tie in (2) is a `host_check` row with `tie` naming every tying
     topic: host it in the one whose question states what to do, and name the
     others in one Owner question with the subject. `host_check` reads as a
     subject only a bold lead that is neither a plan section name
     (**Missing subjects**) nor a topic of the plan (a bold topic name leading
     a bullet is a label), and reads `### <topic> (new)` as `<topic>`. Moving a subject
     renumbers Research questions: re-check every plan whose
     `other_plans_changed` row's `question_cites` names this plan's numbers
     (G211). The checker reads these forms only (G212): a list item starts
     with `N.`, `N)`, `-` or `*`; a subject's bold lead sits whole on the
     item's first line; a plan is named on the first line of a carry, with
     no `/` before its name; a bold lead in a plain paragraph is no subject.
   - **Overlaps:** topics whose rules cover the same ground, quoting both.
     Run `$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/copy_check.py --area <area> --workspace <workspace> --repo <repo>`
     and list its output here: for each merged copy, every part, meta
     (`references`, version) and link that differs from its survivor, and
     every cookbook file that links the copy's UUID (`linked_by`). A worklist
     `identical: true` does not make a copy the same as its survivor. The
     fold must carry everything it names: the copy's extra references and
     links into the survivor, and each `linked_by` link retargeted to the
     survivor, since folding deletes the copy (1.4.24, G58).
     Each row's `direction` is `out` (the copy is in this area) or `in` (a
     worklist copy from any area, planned or not, whose survivor is here).
     An owner-recorded `twin_differs` is reported first (`copy_says`,
     `survivor_says`); meta `triggers` and `platforms` are compared, and
     every other top-level key of `artifact.json` (`top`). `linked_by_folded`
     flags each linking file that is itself a copy being folded, a worklist
     copy or a `merged` copy of any area's plan (1.4.26): its link is
     retargeted in the fold that keeps its text. Where the worklist says
     `identical` or `exact` but `copy_check.py` lists a difference,
     copy_check wins: the plan carries its differences (1.4.25, G74).
     Stamps are never carried: `synced` and the meta `approved-by`,
     `approved-date` and `modified` are listed under `stamps`, never make a
     copy not `identical`, and the survivor keeps its own (1.4.33, G106).
     `history` and `intro` differences are listed apart, in
     `parts.differ_uncarried`: a fold never pastes them in (the survivor's
     history gets its own bump line), but judge whether the copy's intro
     says anything the survivor lacks. A row with `kept: true` is a twin its
     own plan keeps, listed, not folded. In every diff line `-` is the
     survivor and `+` the copy (1.4.37, G175). `--summary` prints the names of what
     differs only, no diff lines (1.4.33, G107), and drops each empty field
     (1.4.37, G175); its meta rows are
     `{key, copy, survivor}`, each value cut to 80 characters, and
     `differ_uncarried` rows are `{part, first_line}`, the first diff line
     (1.4.36, G143). Record `copy_check.py --area <area> ... --digest` (one line:
     the counts and the result's hash) under **Overlaps**, after the
     section's rows, as the line it prints (1.4.37, G176):
     ```
     ## Overlaps

     - <each copy_check row the fold must carry>

     copy_check.py <area>: copies N; identical N; moved N; unreadable N; twin_differs N; differ_uncarried none; result <sha12>
     ```
      `stage_status.py`
     lists `stale_copy_check` when the recorded line is missing (the area has
     copies) or differs from a fresh run, and holds the area at `plan`
     (1.4.36, G133).
   - **Proposed topics:** a table, under the heading `## Proposed topics`,
     with exactly these columns:
     ```
     | Topic | Action | Artifact | Why |
     |---|---|---|---|
     | feature-flags | kept | `cookbook/guidelines/implementing/feature-management/feature-flags` | one line |
     ```
     The table's order is the order stages 3 and 4 take the topics in.
     `Topic` is the name stages 2–5 take as `--topic`; `Action` is `kept`,
     `merged`, `split`, `new` or `dropped`; `Artifact` is the source folder
     the topic is written to, relative to the repo, even when it lies outside
     the area (a topic merged into another, or a new one placed elsewhere).
     `stage_status.py` reads `<artifact>` from this column, and `Action`
     too: a merged topic is researched, written and reviewed only under the
     plan whose area holds its Artifact folder. A `merged` row whose
     `Artifact` lies in another area is a record here, never run here:
     `stage_status.py` reports it `merged into <folder>`, owing nothing in
     this area, not approval and not research, and it runs under that
     folder's area plan, where it is a topic of its own.
   - **Research questions:** for each proposed topic, the four questions
     (SKILL.md, *The four questions*) made specific to it (which platforms, which solutions to compare).
     Each incoming merge's research questions (below) are carried into the
     questions of the topic it merges into.
   - **Owner questions:** every item this file sends to the owner, in one
     place: each `mark_conflicts` row, `conflicts`, `pending_target`,
     `incoming_unplanned` and `speciality_points_at_copy` row, `unplaced` topic,
     `unread_marks` file, double-keep, contradiction and research-bar
     question, each citing the plan body it rests on (1.4.25, G79).
   - **Step-4 re-check:** what step 4's re-checks printed, and every change
     since step 1.2 or step 3, each with what the plan did about it.

   **An area of copies only.** When every topic of the area is `merged`
   elsewhere, the plan still has every section: its **Gaps** is a table
   naming each speciality and the survivor's plan that measures it; its
   **Research questions** are reviewer-side only. The copy-only plan writes
   them in its own plan and records the survivor's plan as carrying them;
   when the survivor's plan was written first and omits them, that goes
   under **Owner questions** (1.4.25, G84). Its **Gaps** quotes the
   survivor's figures as "recorded, not counted", figures read from the
   survivor's plan at its recorded hash (the survivor's `area-plan.md` and
   files, each `git hash-object` recorded in Step-4 re-check; 1.4.37,
   G182), and names the
   survivor's research-bar question (step 2) under **Owner questions**
   (1.4.33, G115). G118's rule against quoting another plan's figures
   makes one exception here: the G115 figures, quoted from the survivor's
   files (`A/gaps/`, `A/run_gaps.json` of the survivor's area) with each
   file's `git hash-object` (1.4.36, G136). `stage_status.py` lists in
   `survivor_carries` (advisory) each research question this plan records
   the survivor's plan as carrying that the survivor's plan does not
   carry; a new carry is an item under **Owner questions** naming the
   survivor's plan, and the plan names the survivor's research bar
   (1.4.36, G130). A subject is keyed by its item's lead bold span, a
   trailing "(carried ...)" or "(hosted ...)" note stripped (no lead bold:
   the whole item); the survivor carries it when that whole span is a bold
   span or a whole list item in its Research or Owner questions; only the
   survivors the item names are checked, every owner when it names none
   (1.4.37, G150). It also carries it as the lead of a list item there:
   the item's text, after its `1.` or `-` marker and any bold markers,
   starts with the whole phrase (case and punctuation aside) followed by
   ` (`, `:`, `.`, `,`, ` —`, ` -` or the item's end, as in
   `6. Plurals and message formatting (hosted here in ...)`. A phrase that
   only starts a longer one ("Plurals and message formatting rules") and a
   heading carry nothing (1.4.38, G184). An item led by a research label
   ("Best practices:", "Known solutions:", "Platform guidelines:", "The
   expert's view:") stays listed with `kind` `research_label`; every other
   row has `kind` `subject`; no row is dropped, and a row led by a research
   label or by a plan section name ("Missing subjects") is never cleared,
   since such a lead names no subject: carry its subjects under their own
   bold names (1.4.38, G185). The
   survivor's plan sees each such ask in its own `carries_asked`
   (advisory: `plan`, `question`, `subject`, `kind`), read by the same
   matcher, until it carries the subject (1.4.37, G151; 1.4.38). A
   `subject` row of either list holds `next` at `plan`; `research_label`
   rows stay advisory, printed after the `subject` rows, and N label rows
   left is the clean end state (1.4.39, G213, G214). When the survivor's plan does not yet carry
   a subject, the end state is: name it under **Owner questions**, report
   `next: plan`, and hand the open `subject` row to the controller, who runs
   the survivor's plan; this plan's approval waits on it (1.4.40, G242). A plan line citing a
   folded or merged copy is a `stale_pointer` row (advisory; only a cite is
   read, tools.md *Cites*: a prose paragraph, a heading or a table cell holding
   more than the path never is, 1.4.42, G258), naming the
   survivor: cite the survivor, or say the copy is `folded` or `merged into`
   it on the same list item or paragraph (wrapped lines joined); a backticked
   speciality id, a list under a line saying the copies are folded and a `>`
   quoted line are skipped, and each row gives the matched text and its
   column (1.4.39, G216; 1.4.40, G234, G235). Every topic here is a merged copy,
   so "never in a merged copy" leaves a no-host subject no topic: it goes
   to the survivor's plan as a carry ask (a Research question naming the
   survivor, marked "carried, no host") and is listed under this plan's
   **Owner questions** (1.4.37, G163). It still needs the owner's
   approval, as a record. An area the fold empties lists the subjects it
   would miss under **Owner questions**; it never proposes `new` topics on its own
   (1.4.24, G60).

   **Another plan's figures and questions.** Never quote another plan's
   figure: it may be stale; cite that plan by name and quote this plan's own
   files only. An owner question one plan raised is carried out by that plan
   once the owner answers, and a later plan records the answer; an item
   recorded as new since step 1.2 stays in **Step-4 re-check**, marked
   settled or open, never dropped (1.4.33, G118).

   **Plans written in parallel.** Merges and marks read other plans that
   may still be changing. When one batch plans both a merging area and its
   survivor's area, run the survivor's area plan first. A merged copy's own
   plan (a copy-only plan aside, above) writes no research questions for it
   when the survivor's plan writes them; it records which plan does. When
   two areas in one batch merge into each other, neither can go first:
   re-run step 4 in both once both plans exist (1.4.25, G89). Whatever timing missed, step 4 catches:
   `stage_status.py`'s `pending_target` (a merge or keep whose target area has
   no plan yet: never clean), the `--check` re-runs, and a final sweep of
   every area once all plans are written (1.4.24, G61). The controller
   runs that sweep: a last `stage_status.py` over every area after all plans
   are written, each area's `other_plans_changed` and `carries_asked` read
   and settled (1.4.37, G153). `other_plans_changed` lists a cited plan
   whose hash differs from the one recorded (its `<area>/area-plan.md`
   path matched whole, never the tail of a longer path, G154) with
   `sections`, the `## ` sections whose text changed since that hash (or
   `"unknown"` when neither git nor an `A/other-plans/` snapshot holds it,
   1.4.39, G193), and lists one with no recorded
   hash as `unrecorded`, whatever its age: record its hash to clear it
   (1.4.37, G152, G153). Neither list, nor `survivor_carries`, is in the
   `stage_status.py` digest, so a sibling's rewrite never moves this plan's
   digest (1.4.37, G153).

   **Incoming merges.** Before writing the plan, read every existing plan's
   `merged` rows that point at this area's folders: `stage_status.py`'s
   `incoming`. Only a copy whose folder exists, or that is a worklist
   `new_home`, is listed there; a merged row naming a folder that does not
   exist, and is no `new_home`, records a move, not a merge,
   and `incoming`, `fold` and `conflicts` all leave it out. A copy reached
   through a `new_home` (no folder of its own) is a merge: `pending_target`
   in the merging plan while this area has no plan, `incoming` here once it
   has one, each row with `via: new_home`. List each under **Proposed topics** by naming `<plan>/<topic>`
   in the Why cell of the row of the topic it merges into (`merges in
   reviewing/language/python`), and carry its plan's research questions for it into this plan's
   **Research questions**. `stage_status.py` reads only the cells of the
   **Proposed topics** table's rows: name the copy in the Why cell of the
   survivor's row, as `<plan>/<topic>` or as the full
   `cookbook/guidelines/<plan>/<topic>`, a whole path (`<plan>/<topic>-typing`
   or `<plan>/<topic>/part` is another path); the worklist's `guidelines/<plan>/<topic>` names it too. A name in the prose or in the
   **Topics** table does not count. A plan that does not list one disagrees with
   the merging plan: `stage_status.py` reports it in `conflicts` (from
   either plan) as an owner item, and the plan hands it to the owner
   under its **Owner questions** rather than settling it.

   **Folds no plan stands behind.** `incoming_unplanned` lists each worklist
   fold into this area from an area with no plan yet, or whose plan has no
   row for it or a row that does not merge it into this survivor (1.4.26)
   (`via` `copy`, its folder existing, or `new_home`), with the plan and its
   `why`: name each in the
   survivor's Why cell like an incoming merge, and under **Owner questions**
   until that plan exists. `speciality_points_at_copy` lists each
   speciality-map row whose topic is a copy a fold deletes: who repoints the
   speciality is the owner's, so name each under **Owner questions**.
   `next_why` says in one line why the area's `next` is what it is ("every
   row merged elsewhere: approval is a record"), led by the `pending_target`
   note when any row waits on a plan (1.4.25, G75).
   `stale_reference` (1.4.27) lists each `A/reference.json` row written
   before the current reference format (`reference_format.py`; format 2
   takes *Standing focus* and *Tidy focus*, 1.4.26; format 3 leaves out a
   roled skill's copied review sections, 1.4.46): its file is not in the
   sections the measure reads now (an older file may lack some, or hold
   copied review text it must not count), so the area is never measured
   against it as if current.
   `stage_status.py`, `unmeasured.py --check` and `run_gaps.py` (exit 1, a
   run and `--check` alike) list it; `stage_status.py` also lists
   a `marked_here` reference `A/run_gaps.json` lists stale (one no
   `speciality_reference.py` could rewrite, 1.4.28), and `A/run_gaps.json`
   itself when it was saved under an older reference format, or none (its
   `reference_format` is missing or lower than the current one, or the file
   cannot be read; 1.4.29): a `marked_here` reference has no stamp of its
   own, so a report from before the current format may rest on a stale one
   that no run listed. That row's `speciality` is null and its `file` is
   the report; re-running `run_gaps.py` (step 1.3) saves the report again
   and clears it. The same row stands for a report saved while it listed a
   stale row (an `"old_format"` row, or one with no `reason`; 1.4.30):
   rewriting `A/reference.json` without re-running `run_gaps.py` leaves a
   measure on the stale reference. A plan with no `A/run_gaps.json` gets
   such a row too: step 1.3 never ran or its report is gone, so re-run it
   (1.4.33, G99); an area with neither gets none. Each
   row names its `reason` (`"old_format"`, `"no_writer"`, `"old_report"`);
   scripts read that field, never the wording of `why` (1.4.29).
   An `A/reference.json` that cannot be read as a list of rows (invalid
   JSON, not a list, or holding a row that is not an object), or absent
   beside an `area-plan.md` (step 1.1 always writes one, `[]` for an area
   with no speciality; 1.4.32), is one row,
   `reason` `"unreadable_reference"` (1.4.31): no `reference_hash` is
   printed and no approval of it is current. A saved report whose
   `stale_reference` is not a list is an `"old_report"` row too.
   A stale reference
   holds the area and each topic at `next: plan`, approved or not (1.4.28):
   the plan was measured on it. `next_why` leads with it: rewrite `A/reference` (step 1.1, then steps 1.2 and 1.3) and re-measure,
   re-run step 4, and hand the plan back to the owner for a new approval.
   A plan approved under an older reference format is no longer approved:
   the approval names the `git hash-object` of `A/reference.json` (1.4.30),
   and rewriting the rows changes it. Once the reference is current again,
   `approval` reads `stale` with `approval_why` `"reference_hash"`, and
   `next` is `approve`. The
   earlier approval is not deleted: the approval stays on record as history,
   and no stage runs on the old figures.

## Step 4: The owner's approval

4. Other plans may change while this one is written: their marks feed
   `marked_here` and `mark_conflicts`, their merges feed `incoming` and
   `conflicts`. Immediately before the hand-off, re-check with
   `unmeasured.py --area <area> --workspace <workspace> --repo <repo> --reference A/reference.json --check`,
   `run_gaps.py --area <area> --workspace <workspace> --repo <repo> --check --hints`
   and `stage_status.py`, each with `--repo <repo>`, and
   `$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/run_gaps.py --check-homes --workspace <workspace> --repo <repo>`
   (read-only, the whole workspace: each home-measure sentence lacking at its home and
   counted in no area or in more than one, and each sentence two areas record different homes
   for; a sentence its owner holds at its home is never listed; each row names the owner, the
   home topic, the owner's verdict and the `mark.py` command that settles it; exit 1 if any row,
   1.4.42, G254; with `--area <area>` only the rows touching the area, the exit covering those,
   1.4.43, G273, G282), and
   `$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/run_gaps.py --check-verdicts --area <area> --workspace <workspace> --repo <repo>`
   (read-only: one piece at one topic with different verdicts in different areas, a structured
   `counted_at` hold left out; exit 1 if any row; 1.4.43, G280). Each `--check` writes nothing: it compares a fresh
   result with the saved `A/unmeasured.json`, `A/run_gaps.json` or `A/gaps/` files and prints
   every change (`marked_here`, `mark_conflicts`, the `building` entry
   fields `unmeasured_sentences` and `unplaced_pieces`, topics and counts), exit 0 unchanged, 1 changed, so the
   saved files and the hand-built R9 files stay (1.4.24, G45).
   Without `--hints` or `--no-hints`, `run_gaps.py --check` runs as the saved
   report ran (its `hints`) and prints `hints` and `hints_from`; a write run
   with neither keeps the saved report's `hints` (1.4.36, G122). A
   `not_compared` row is never clean: re-run step 1.3 so both ran alike,
   then check again (1.4.33, G96). On a change, re-run the step that writes
   the file: `unmeasured.py` with
   `$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/write_on_success.py A/unmeasured.json -- $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/unmeasured.py --area <area> --workspace <workspace> --reference A/reference.json --repo <repo>`,
   and step 1.3 with `run_gaps.py --area <area> --workspace <workspace> --repo <repo> --hints`,
   whose stdout may be discarded: it saves `A/run_gaps.json` itself
   (1.4.33, G113). **Step-4 re-check** records each check's result in one
   line: `run_gaps.py ... --check --hints --digest` prints it (the verdict,
   exit, each list's count, `not_compared`, hints, the saved report's hash).
   After the plan's final edit run the checks once more: that last check
   is the hand-off check, and its digest is the one recorded as the
   hand-off (1.4.33, G120; 1.4.37, G183). Record the first check's digest
   line too (re-run checklist item 3, run on the saved reports before any
   rewrite, 1.4.37, G155); when the hand-off line differs from it, the
   change is recorded and re-checked.
   `unmeasured.py --check --digest` and `stage_status.py --digest` print
   one line the same way (1.4.36, G137). The `run_gaps.py` line recorded is
   the `--check --hints --digest` form; `plan_skeleton.py` prints the saved
   report's form (`saved report; ...`) and, since 1.4.40, the `--check --hints
   --digest` line beside it (G248): record the check's line, not the saved
   one, and keep the skeleton's lines of the
   other three scripts (1.4.39, G217). The `stage_status.py` digest is
   `next` and the holds (`plan_sections`, `stale_reference`, `r9_stale`,
   `stale_copy_check`, and since 1.4.39 `host_check`, since 1.4.40 `cite_moved`, since 1.4.41 `stale_verdicts`, so every older
   digest line differs once) only: the Step-4 re-check section and the advisory
   lists are left out, so recording the line never changes it (1.4.37,
   G153, G183). Record the first check's `new_keys`, `changes` and
   `cleared` (re-run checklist item 3), then re-run step 1.3 so the saved
   report carries every key; an empty new key is no change (1.4.36, G148).
   In **Step-4 re-check** record each other plan this plan cites as a
   backticked line `` `<area>/area-plan.md <40-hex hash>` ``, the only form
   read (1.4.39, G191); when several lines name one plan, the one in the
   LAST `### ` subsection of Step-4 re-check wins. The hash is the plan's
   content hash: the git blob hash of its text with its whole `## Step-4
   re-check` section removed, so recording hashes never changes one and two
   plans citing each other settle (1.4.39, G186); each row's `current` is
   it, and `stage_status.py --record-others` prints every line to record (with
   `--write` it puts them into the last `### ` subsection of Step-4 re-check,
   replacing the line that records the same plan, atomically; it refuses a
   plan with no such subsection, and a second run changes nothing, 1.4.40,
   G236; write this run's `### On <version>` subsection first, since the
   lines go into whichever `### ` subsection is last, and make `--record-others
   --write` the plan's last edit; it says `written` or, when every line is
   already in place, `no change: every recorded hash is current`, exit 0: an expected outcome, 1.4.42,
   G265; a new list after prose gets a blank line before it, an older subsection's hash list stays as
   history, only the last `### ` subsection being read, and the `stage_status.py` hand-off digest is
   taken after the write, which changes its `result` hash, 1.4.43, G295) and
   saves each cited plan as `A/other-plans/<plan>.<hash>.md`, so a later
   row names the `sections` that changed even for a plan git does not track
   (G193). A recorded whole-file `git hash-object` of the plan as it is now
   counts as current too, until the plan changes. Record the hashes last,
   immediately before the final `stage_status.py` check; re-read what each
   cited plan says about this area, and name a plan still being rewritten
   under **Owner questions** instead of chasing it (1.4.39, G192).
   `stage_status.py` lists in
   `other_plans_changed` (advisory, rows always printed) each cited plan
   whose hash differs from the recorded one, or, with none recorded, whose
   file is newer than this plan; re-read it (1.4.36, G134). It reflects
   sibling plans other sessions edit while this run is open, so it can rise
   and fall: re-run `--record-others --write` once at the end, as the last
   edit, then `stage_status.py` once more, and report that final value, rows
   included; never chase a plan still changing (1.4.42, G266). Each row says
   where this plan cites it (`cited_at`, its line numbers; the `why` gives them as a count and
   ranges, 1.4.43, G296) and which of
   this plan's question numbers the cited plan names (`question_cites`); an
   `unrecorded` row means read it and record it, even when nothing in it
   concerns this area (1.4.39, G194, G211). The row's `why` says "in the cited
   plan", and `sections` names the cited plan's sections that changed (1.4.40,
   G245). `cite_moved` (a hold at `plan`, in the digest) lists a question
   number this plan cites (`question N`, `owner question N`, `its question N`,
   `RQ N`, `topic N-M`, on a line naming the plan's path or "the <area> plan" with
   the area's exact name, never its last segment alone, 1.4.42, G258) whose lead phrase in the cited plan's snapshot differs from today's:
   `cite N: was '<lead>', now '<lead>'` (1.4.40, G232). `cite_moved` reads numbered cites only: a
   topic-named cite, or an Owner-question bullet naming the cited plan's question, is checked by
   hand, and a line citing this plan's own question is worded so (`This plan's Owner question 4`)
   (1.4.43, G296). A plan is cited
   by its area as a whole path (`areas/` before it allowed); a
   single-segment area (`shipping`) only as `shipping/`, `areas/shipping` or
   in backticks, never as a plain word (fix round 1). `--keys`,
   `--summary` and `--digest` without `--check` read the saved
   `A/run_gaps.json` and write nothing, never a re-run: after
   `mark.py --held` or `--home` they say "read saved report, not re-run"
   on stderr, naming each marks file newer than the report, until step
   1.3's `run_gaps.py --hints` runs again (1.4.39, G207); with no saved report they exit 2
   naming step 1.3's command; `--rows KEY` prints one key whole (1.4.36,
   G122, G138). `--check --out DIR` with no `DIR/run_gaps.json` exits 2,
   naming the file (1.4.37, G172).
   `run_gaps.py --check` compares every key of the saved `A/run_gaps.json`
   (`measured_elsewhere`, `why_empty`, `r9_missing`, `building` with its
   entry fields `unmeasured_sentences` and `unplaced_pieces`, `short_sentences`, `home_measures`, `numbering_differs`,
   `advisory_failed` (1.4.26) and the rest; a missing one is a change; a key
   the saved file lacks whose fresh value is empty is no change, listed in
   `new_keys` on both `--check`s, while a non-empty new key is a change,
   1.4.34) and counts any non-empty `would_clear` as a
   change, so step 4 needs no `--out` scratch run. `--check --out DIR` compares `DIR/run_gaps.json`,
the report a run with that `--out` saves, never `A/run_gaps.json`; its
output names the file as `report` (1.4.27). `unmeasured.py --check`
   names the file it compared as `saved_file`; it writes nothing (1.4.25, G67). `run_gaps.py
   --check` exits 2 on any `unplaced` topic, new or unchanged: keep the
   saved files, list each such topic under **Owner questions** and judge it
   by hand; never plan on as if it did not exist. Compare
   them with what the plan quotes; on a change, re-run the step that writes
   the file, then the plan. A `pending_target` entry is never clean: name it
   under **Owner questions** until its target area's plan exists (G47). The plan records every change since step
   1.2 or step 3 (a new or gone `marked_here`, `mark_conflicts`, `incoming` or
   `conflicts` row) in its **Step-4 re-check** section, and each one the
   owner must settle under its **Owner questions**. A `marked_here` row that
   agrees with this plan's own marks (the same sentence marked this area's
   in its marks file) is listed once, naming both plans: it is no owner
   item; only a mark that disagrees is (1.4.18, G39). Then re-read each owner
   question against the plan body it cites, and rewrite or drop any the body
   no longer bears out (1.4.18, G40). Re-read each one against the plans
   that now exist as well: a question that rested on another plan not
   existing, or asked for an action that plan has since taken, is rewritten
   or dropped, and the change recorded in **Step-4 re-check** (1.4.33, G118). Then hand `A/area-plan.md` to
   the owner and stop. Stage 2 starts only when the
   owner approves. Record the approval, and any changes the owner asks for,
   in `A/approval.md`: `approved-by`, `date`, and the plan's git hash
   (`git hash-object A/area-plan.md`) with the hash of the reference the
   plan was measured on (`git hash-object A/reference.json`), both on one
   line (1.4.30):
   `- plan: area-plan.md, git hash-object <hash>, reference-hash <reference_hash>`.
   Copy `reference_hash` from `stage_status.py`, never compute it by hand; it is withheld while any reference is stale (1.4.31).
   The script hashes the file's raw bytes, and a plain `git hash-object`
   can differ where git filters line endings. `stage_status.py` prints no `reference_hash` while `stale_reference` lists any row,
   so no plan is approved over a stale reference. `approval` is `current`
   only when `reference-hash`, with the hash of `A/reference.json` as it is
   now, sits on the line that names the plan's hash; a hash on a line of
   its own, or beside another plan hash, approves nothing. `approval_why`
   says why an approval is not current: `"no_record"`, `"plan_changed"`,
   `"reference_hash"` (no reference hash on that line, or the file changed
   since) or `"reference_format"` (the line records `reference-format <N>`,
   the 1.4.29 form, which approves nothing since 1.4.30). An edited plan
   needs a new approval, and so does one whose `A/reference.json` was
   rewritten since: a format bump forces that rewrite.
   Add the new approval as a new entry below the old one. The earlier
   approval stays in `A/approval.md` as history: never rewrite or delete it.
