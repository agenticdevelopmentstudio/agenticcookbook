# Who does the work: tools, prompts and helper scripts

The detail behind SKILL.md's opening and its *Prompts and helper scripts*.

## Who does what

This skill orchestrates; the work is done by what already exists, and this
skill replaces none of it:

| Who | Does |
|---|---|
| `cookr` (this checkout's) | the gap measure (`roles gaps`), `compile`, `convert`, `roles set`, `roles check`, `roles lossless`, `validate`, `bump` |
| the devteam's `speciality_reference.py` | each speciality's own text, the gap measure's reference (*The reference text*, below) |
| `scripts/write_on_success.py` | a command's output written to its file only when the command succeeds; the file's folder must exist, or `--mkdir` (first, before the file) creates it; a missing folder, or a temp file it cannot create, is one line and exit 2 (G174, 1.4.37); a command that edited the file in place is refused, exit 2, its edit stands (G231, 1.4.40) |
| `scripts/plan_skeleton.py` | an area plan's section headings in order, with each digest line in place: `copy_check.py --digest` under Overlaps; `unmeasured.py --check --digest`, the saved `run_gaps.py --digest`, `run_gaps.py --check --hints --digest` (1.4.40, G248) and `stage_status.py --digest` under Step-4 re-check; read-only; a script with no line is named in its place and the exit is 1 (G181, 1.4.37) |
| `scripts/unmeasured.py` | the specialities with no topic, placed in their areas by the worklist; building text other plans mark for this area, and conflicting marks (each with `agrees_for` and `differs_for`, G71; a `numbering differs` row has neither, 1.4.26); specialities on copies, measured in the survivor's area; a renumbered speciality compared by text (G114); every marks file it does not read listed in `ignored_marks` (G109) |
| `scripts/` (the rest), `scripts/prompts/` | the deterministic steps and every dispatched prompt: see *Prompts and helper scripts* |
| `myagenticteams:researchteam` | the research, one topic per dispatch (an Opus Agent when `team_probe.py` says the team cannot run) |
| `myagenticteams:cookbookteam` (`guideline new`) | the guideline author (an Opus Agent when `team_probe.py` says the team cannot run) |
| `/create-artifact` | a single artifact drafted interactively, with no research |
| `/lint-artifact`, `/approve-artifact`, `/add-artifact` | lint, approval, index and counts |
| `/repair-cookbook` | a cookbook `cookr validate` cannot pass |

## The reference text

`speciality_reference.py` writes a speciality's reference, `A/reference/<speciality>.txt`
(`/` as `--`), from its `SKILL.md`: an explicit list of every own-text
section the pool holds, *Review focus*, *A complete review must establish*,
*Build focus*, *Standing focus* and *Tidy focus* (the last two in three
building specialities: documentation, hygiene, code-quality), in that order,
each cut at its own `_Cookbook guidance` (the cookbook pointers after it are
not the speciality's text), then joined. Any other `## ` section is not
taken, and never dropped silently: the row's `left_out` names it and stderr
says so (1.4.26; the pool has none today). A reference written before
1.4.26 lacks *Standing focus* and *Tidy focus*. Before 1.4.25 the joined text was cut at the first
marker, which sits inside *Review focus*, so both later sections were lost;
a reference file written before then is short (G69, G93). An area with no
speciality gets `[]` and "area has no speciality; reference is empty ([])"
(G78).

## The prompt filler

The filler puts in today's date, the privacy line (no personal names, email
addresses or project details in any web search or fetch) and the exact cookr
line, `PYTHONPATH=<repo>/skills/cookr/cli $COOKR_PY -P -m cookr -p <repo>`, so
no agent guesses the date or looks for a `cookr` on PATH. A placeholder left
unfilled is an error (exit 2, naming it): give the missing `--set`, never a
blank. Dispatch the printed text exactly as it is.

## Templates and scripts

| Template | Stage | Its `--set` values |
|---|---|---|
| `research` | 2, the research fallback | `artifact`, `topic_dir` |
| `second-check` | 2, the second check | `artifact`, `claims` |
| `write-brief` | 3 (written by `write_brief.py write`) | (filled from the topic) |
| `author` | 3, the guideline author | `artifact`, `topic_dir` |
| `review-full`, `review-scoped` | 4 (written by `write_brief.py review`) | (filled from the topic) |
| `lossless-judge` | 5, the lossless judge | `artifact`, `base`, `copies`, `last_run` |

`criteria.md` is the review criteria, filled into the write brief and both
review prompts word for word, so the author writes against exactly what the
reviewer checks.

The scripts, each with its tests beside it (`python3 -m pytest
.claude/skills/grow-cookbook/scripts`):

Run every script with absolute paths, from any directory: no script reads
the working directory. Every subprocess a script starts is isolated from it
(`-I`, or `-P` with a fixed working directory, so a `cookr` or `json.py`
where you stand is never imported), and `write_on_success.py` refuses a
relative `<out-file>` (exit 2) rather than writing wherever the caller stands
(G44, 1.4.24).

Every script that reads the cookbook takes `--repo <repo>`; without it,
`repo_path.py` finds the nearest folder at or above the current directory
that holds `cookbook/guidelines/`, and exits 2 asking for `--repo` when there
is none (from the workspace, outside the repo). Pass `--repo` every time
(G76, 1.4.25).

| Script | Does |
|---|---|
| `stage_status.py` | where the area stands: per topic its stage files, `next`, review `rounds`, the copies to `fold`, the findings for the `owner`; the area's `incoming` merges and `conflicts` (merges a plan does not list; artifacts two plans keep, `kind: double-keep`); `incoming_unplanned` (worklist folds into this area that no plan stands behind: no plan yet, or a plan with no row merging it here) and `speciality_points_at_copy` (speciality-map rows on a copy a fold deletes: the owner's); a merge through a worklist `new_home` (`via: new_home`); `next_why`, one line on why `next` is what it is (G75); `r9_stale` (G94), `plan_sections` (G97, G105; each topic with no research-bar Owner question, G128) and `stale_copy_check` (the Overlaps `copy_check.py --digest` line missing or not a fresh run's, G133), holds that keep `next` at `plan`; `other_plans_changed` (G134; `sections` changed since the recorded hash or `"unknown"`, a cited plan with no recorded hash listed `unrecorded`, the recorded path matched whole, G152–G154, 1.4.37), `survivor_carries` (G130; keyed on each item's lead bold span, its carry note stripped, only the survivors it names, G150; carried as a bold span, a whole item or an item's lead phrase, G184; each row's `kind` `research_label` or `subject`, G185, 1.4.38) and `carries_asked` (the survivor's side: each subject a copy-only plan asks this area to carry, G151, 1.4.37; same matcher and `kind`, 1.4.38), advisory, none of them in `--digest` (G153); a plan with no `A/run_gaps.json` an `old_report` row (G99); `--keys` prints each key's shape only (1.4.33), the hold and advisory lists' rows whole (G138); `--rows KEY` one key whole; `--digest` one line (`next` and the holds only; G183, 1.4.37); 1.4.39: `host_check` (a hold: a hosted subject whose topic shares no specific word with it, a `### No host` subject that shares one; stemmed, area-path and generic words never count, G188, G208, G209), `shared_no_host` (advisory: another plan's `### No host` carrying the same subject, G190), `stale_pointer` (advisory: a line citing a folded copy, G216); a `subject` carry row holds `next` at `plan` (G214); the recorded hash is the plan's content hash (its Step-4 re-check section removed), read only from a backticked `` `<area>/area-plan.md <40hex>` `` line, the last `###` subsection winning (G186, G191); `--record-others` prints the lines and snapshots each cited plan in `A/other-plans/` (G193), and with `--write` puts them into the last `###` subsection of Step-4 re-check (G236, 1.4.40); `cite_moved` (a hold, in the digest: `{plan, cite, at, was, now, why}`, G232); `stale_verdicts` (a hold, in the digest: each saved `held_by_wording` row with `verdict_was` and no `verdict`, counted lacking by `run_gaps.py` until `mark.py --held` judges it again, G251, 1.4.41); `shared_no_host` rows carry `named_in_owner` (G244); `stale_pointer` rows carry `column` and `matched` (G234, G235); rows carry `cited_at` and `question_cites` (G194, G211); `--rows a,b` (G219); `--digest` counts the advisory lists on stderr (G195); an unknown area or a workspace with no `areas/` exits 2 in every area script (G198); Missing subjects: bold in a code span is no subject (a code span holding no bold stays part of a subject), only a paragraph's first line is bold-led (G165); only a section's first table names topics (G166); the area as `--area` (the positional kept, deprecated, G169); `--first-check` writes `A/first-check.txt` (the three digest lines, saving an old one as `A/first-check-before-<version>.txt`, G262, G267); `report_refresh` names the command that refreshes a saved report older than the skill or its verdicts (G269), its `stale_views` and `command` (1.4.43, G291); `--keys` gives a `stale_verdicts` row's `topic_files` as a count (G298); `--record-others --write` sets a new list off by a blank line and a no-op says `no change: every recorded hash is current` (G295) |
| `quote_building.py` | a building speciality's text quoted once, each sentence marked by area; `--marks` prints `topics` (G77); `--keep` never lets a re-run wipe marks; unchanged sentences: exit 0, file untouched; a re-quote carries each mark by sentence text, never by number, and lists every mark it cannot carry; `--check` prints the renumbering, `changed` and `kept`, and writes nothing (G111); a `--file` not yet written exits 2 naming the command that writes it (G117); a `--speciality` the workspace's `speciality-map.json` does not name exits 2, naming any near match (G158, 1.4.37); "marks kept (sentences unchanged)" is one stderr line, and `--marks` prints one stderr line of counts, `--quiet` leaving `markdown` out (G168, 1.4.37) (stage 1) |
| `mark.py` | marks set in a plan's marks file, validated: one sentence (`--n N` with `--to AREA...` or `--clear`), or many in one call (`--mark N=AREA[,AREA]`, repeated, every mark checked before any is written, G70); an area is a cookbook folder or a planned new area (`<workspace>/areas/<area>/area-plan.md`, G65); `--home N=TOPIC` (repeatable, alone on its call; `N=` clears it) records the home the plan names for sentence N, every entry checked before any is written, read by `run_gaps.py` as `home_recorded` (G145, 1.4.36); `--home N=AREA:TOPIC` records a home in another area in `A/homes.json` (the area known, the topic one of its plan's rows or folders; no marks file needed, N checked against `A/run_gaps.json`; G156, 1.4.37); `--held ID held\|not` (alone on its call; `--speciality` not needed) records a `held_by_wording` verdict in `A/held.json` with the piece and topic sentence it was judged on (G159, 1.4.37), and since 1.4.39 its `rule_sentence` and `topic_hash` (G202); `--held-file FILE` records many (`{"<id>": "held"\|"not"}`), every id and verdict checked before any is written (G199); `--home` needs `--speciality` (G204) and takes a `home_unguessed` row of the saved `A/run_gaps.json` only, exit 2 naming where any other sentence is listed (G203); the area as `--area` (G169); never edit a marks file, `homes.json` or `held.json` by hand; 1.4.43: `--held ... --counted-at AREA` (G273), `--hold TOPIC` with `--source`, `--text`, `--why` into `A/hand_holds.json` (G276), `--lack` with `--piece K` and `--refresh` (G285), `--non-home-held` (G284), repeatable `--clause`/`--cites` pairs (G280), a `not` needs `--why` (G288), `--source` example `reference/building--platform-windows.txt#10` (G287) (stage 1) |
| `copy_check.py` | each merged copy of the area compared with its survivor, outgoing and incoming (`direction` `out` or `in`: every worklist copy whose survivor is here, from any area): an owner-recorded `twin_differs` first, parts, meta (`references`, version, `triggers`, `platforms`), other top-level keys (`top`), links, every cookbook file that links the copy's UUID, and in `linked_by_folded` each such file that is itself a copy being folded, a worklist copy or any plan's `merged` copy (G74, 1.4.26); listed under Overlaps, carried by the fold; it wins over a worklist `identical`/`exact`; stamps (`synced`, meta `approved-by`, `approved-date`, `modified`) listed under `stamps`, never a difference (G106); `history` and `intro` listed apart in `parts.differ_uncarried`; `kept` true for a twin its own plan keeps; `--summary` prints names only (G107), meta as `{key, copy, survivor}` cut to 80 characters and `differ_uncarried` as `{part, first_line}` (G143); `--digest` prints the one line the plan records under Overlaps (G133); in each diff line `-` is the survivor and `+` the copy, and `--summary` drops empty fields (G175, 1.4.37); the area as `--area` (the positional kept, deprecated, G169) (stage 1, step 3) |
| `paraphrase_hints.py` | for each lacking sentence of `A/gaps/*.json`, the topic sentences with the highest word overlap, nested and flat (`sentences`); advisory only; a `--repo` with no `cookbook/guidelines/` exits 2 (stage 1) |
| `run_gaps.py` | step 1.3's `cookr roles gaps` commands built from `A/reference.json`, `A/unmeasured.json`, the worklist and the plan, run under `write_on_success.py`; each lacking piece numbered as `quote_building.py` numbers it; per topic pieces, held, lacking; per building sentence `home_guess` and `gap_candidates`, an advisory guess (the plan names each home), and `unmeasured_sentences` (a piece not measured: judged by hand) its `measured_pieces` (never a verdict on the sentence), and `unplaced_pieces` (judged by hand): objects with `text`, `measured`, `verdict`, `topic`, `sentences`, a measured piece no sentence holds listed with its verdict, never dropped; `--hints` over every measured topic where no home is guessed; `stale_gaps`; `r9_missing` (owed R9 measures only); `unmeasured_sentences` rows carry `marked_for`; `lacking_candidates` over every topic folder of the area; `same_text`; per topic `own` and `building_marked_elsewhere`; `measured_elsewhere` for every merged row elsewhere; `why_empty`; `r9_targets`; clears only its own stale files (`cleared`), never R9's; `short_sentences`, pieces under six words for a hand judgment (G72); `home_measures`, building sentences measured at their home into `A/gaps/home--<topic>.json` (G68), `not measured` with `unmeasured_references` when the home file has no row for the reference; `numbering_differs`, a `marked_here` row whose text is not its reference's sentence `n`, measured as the sentence its text names or not at all (1.4.26); `advisory_failed`, a failed hint that never stops the run (G66); `stale_reference`, each reference row or `marked_here` file older than the current reference format (`reference_format.py`, 1.4.27): rewrite A/reference (step 1.1, then steps 1.2 and 1.3); `--check` exit 1, and a run saves its report and exits 1 (1.4.28); `hints`, whether `--hints` ran; an unmeasured `numbering_differs` row is in `home_unguessed` too (1.4.27); an `--out` that is the area, or holds it, exits 2 (1.4.27), as does one inside the area other than `A/gaps` or below it (1.4.28); a `marked_here` reference rewritten on every run (1.4.27); saves its JSON as `A/run_gaps.json` (G90), inside `DIR` with any other `--out DIR` (1.4.26), and writes a missing reference into `DIR/reference` with any other `--out DIR` (1.4.26); `--check` read-only, comparing every key of that report (`advisory_failed` too, 1.4.26, only when both ran alike on `--hints`, else named in `not_compared`, 1.4.27; `--check --out DIR` compares `DIR/run_gaps.json`, named as `report`) and counting a non-empty `would_clear` as a change (G67); `r9_stale`, R9 files whose recorded reference hash is missing or stale (G94); `markers` and `repeat_of` (G103, G104); `home_shared_words` on a guessed home (G121); every unguessed building sentence in `home_unguessed` (G95); `--check` with neither `--hints` nor `--no-hints` runs as the saved report ran (`hints_from`, G96); `--digest` adds a one-line record of the check (G120); `--keys` prints each key's shape only (1.4.33); `--keys`/`--summary`/`--digest`/`--rows KEY` without `--check` read the saved report, never run (G122, G138); a run with no hints flag keeps the saved `hints` (G122); a building sentence's `mark` (its own marks-file entry) is not a row's `marked_for` (the areas every plan's marks name, never null: `"unmarked"` or `"unknown"`, G124, G147); `held_by_wording`, every cookr hold for the plan to re-judge (G132); `count_only` and `home_recorded` on `home_unguessed` rows (G123, G145); `kind` `piece` when uncertain or a colonless bold line (G125); `review_focus_pair` and `pieces` on `repeat_of` (G146); 1.4.37: `held_by_wording` rows carry `id` and `topic_sentence`, and `verdict` (or `verdict_was`, `verdict_why` once either sentence changed) from `A/held.json` (G159); `home_recorded` also from `A/homes.json` (G156); `opener` is a piece starting Review or Closing or a procedure lead ending in `:`, never a piece ending in "pass" (G161); a `--check` change to a `short_sentences` kind carries `kind_changed` (G180); `--check --out DIR` with no `DIR/run_gaps.json` exits 2 (G172); 1.4.39: `held_by_wording` rows carry `rule_sentence`, `topic_hash`, `modal_piece`, `modal_topic`, `modal_differs`, `home_topic`, `home` (G201, G202), and a verdict resets when either changes (`verdict_unpinned` on an older record); a `not` verdict counts the piece lacking in the figures (`not_held_by_verdict`, G189); `--check` lists `gap_total` (the plan's `This area's gaps: N` against `measured_total`, G189; 1.4.40: one form, every other form and a missing line a row too, G225, G226, G233) and `verdict_changes` (G247) and names `new_keys` on stderr (G218); 1.4.40: `lacking_pieces` (each `{id, speciality, n, topic, text, counted}`), `measured_total`, each held row's `modal_piece_all`, `modal_sentence`, `modal_topic_implied`, `nearest_modal_sentence`, `rule_is_topic_sentence`, `counted` (G223, G224, G227, G250), `short_sentences` rows an `id` and `counted`; `--rows a,b` takes a comma list (G239); `stale_home`, a recorded home naming no topic, also on stderr (G205); a saved-report view says on stderr when a marks file is newer than the report (G207); `--rows` of another script's key names its owner (G220); 1.4.43: the area positionally too (G299); `missing_subjects` beside `measured_total` (G286); `--check` adds `counted_rows_differ` and `figure_change` (G283, G300); `--check-homes` and `--check-verdicts`, read-only over the workspace, `--area` filtering (G273, G280, G282); `home_lacking` rows carry `text` and `pieces` (G302) (stage 1) |
| `reference_format.py` | `REFERENCE_FORMAT`, the reference format `<devteam>/speciality_reference.py` stamps on each `A/reference.json` row (`format`), and `stale_reference(rows)`, the rows written before it, shared by `run_gaps.py`, `unmeasured.py` and `stage_status.py` (1.4.27); each stale row's `reason`, `report_row` (a saved report older than the format) and `is_current`, the one test of a recorded format (1.4.29) |
| `r9_stamp.py` | stamps an R9 file with `reference_hashes`, the `git hash-object` hash of each reference it was measured against, and `folder_hash`, the hash of the survivor folder's `artifact.json` and `*.md` files (1.4.34), right after the R9 measure, with `--repo <repo>` so a repo-relative survivor `folder` is found (1.4.35); never written by hand; a relative path resolves against the area folder and the folders above it up to the workspace's (or `--repo`), never the cwd (G94, 1.4.33) |
| `json_keys.py` | a library with no command line: `keys()`, a JSON value's keys with their shapes only, behind each script's `--keys`/`--summary` (G119, 1.4.33); `ROW_KEYS` (`plan_sections`, `stale_reference`, `r9_stale`, `stale_copy_check`, `other_plans_changed`, `survivor_carries`, `carries_asked`, `held_by_wording`, `new_keys`, `changes`) print their rows whole (G135, G138, 1.4.36; G171, 1.4.37); a string prints whole; any other list as `{"rows": N}` |
| `repo_path.py` | the cookbook repo every script that reads it uses: `--repo`, else the nearest folder at or above the current directory holding `cookbook/guidelines/`, else exit 2 (G76) |
| `team_probe.py` | whether a myteams team can run, without starting one (stages 2 and 3) |
| `apply_second_check.py` | the claims the second check covers (`--list`), and its result applied to `research.json` (stage 2) |
| `owner_list.py` | `owner-list.md` from the research, and a draft checked against it (stage 3) |
| `write_brief.py` | the prompts, the write brief, each review round's brief and review prompt (stages 2–5) |
| `review_findings.py` | review rounds parsed and counted; open findings to the owner (stage 4) |

## Cites

A **cite** is the one form `stage_status.py`'s `stale_pointer` and
`other_plans_changed` read as a plan line pointing at a folder or a plan
(1.4.42, G258): the folder or plan path in a list item, a table cell holding
the path alone (bare or backticked) or a link target `](...)`; for a plan,
also "the <area> plan" with the area's exact name. A prose paragraph, a
heading, a whole-bold heading line, a table cell holding more than the path
and a backticked speciality id are no cites. `cite_moved` reads a cited
question number on a cite line and compares its lead phrase in the cited
plan's snapshot with today's, so a renumbered question is a row.

## The marks file

`A/building-<name>.json`, `<name>` the speciality's basename
(`platform-windows` for `building/platform-windows`), is written by
`quote_building.py` and changed only through `mark.py`:

```
{"speciality": "building/platform-windows",
 "sentences": [{"n": 1, "text": "..."}],
 "marks": {"1": "implementing/ui" | ["implementing/ui", "shipping/deployment"] | null}}
```

`speciality` is a string; `sentences` a list of `{"n": int, "text": str}`,
numbered from 1; `marks` a dict keyed by the sentence number as a string.
A mark is an area path below `cookbook/guidelines/`, a list of them (a
sentence that spans areas: each area gets it in `marked_here`), or null
(unmarked; `--marks` exits 2 on one). Two plans conflict only when their
marks name different areas, order aside (G55, 1.4.24). An area is a folder
of `cookbook/guidelines/`, or a planned new area: one with
`<workspace>/areas/<area>/area-plan.md` (G65, 1.4.25).

Mark many sentences in one call, `--mark <n>=<area>[,<area>]` repeated
(`<n>=` clears it; every mark is checked before any is written, and one bad
mark writes none, G70, 1.4.25):

```
$COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/mark.py --area implementing/ui --workspace <workspace> --repo <repo> --speciality building/platform-windows --mark 1=implementing/ui,shipping/deployment --mark 2=implementing/ui --mark 3=shipping/deployment
```

Give each command as a plain line, never held in a shell variable: zsh does
not split a variable's value into words, so `$cmd` runs as one word and fails.

## Output shapes

The top-level keys each script prints, with their JSON type (G59, 1.4.24);
every key is always present unless marked `?`.

| Script | Top-level keys |
|---|---|
| `stage_status.py` | `area` str, `dir` str, `plan` bool, `approval` str, `cookr` dict, `topics` dict (by topic name), `incoming` list, `incoming_unplanned` list, `conflicts` list, `pending_target` list, `speciality_points_at_copy` list, `stale_gaps` list or dict (`{"refused"}`), `stale_reference` list (each `{speciality, file, format, want, why, reason}`, from `A/reference.json` (`reason` `"old_format"`), the `marked_here` rows `A/run_gaps.json` lists stale (`"no_writer"`), and `A/run_gaps.json` itself when its `reference_format` is missing, lower than the current one or unreadable (`"old_report"`, `speciality` null; a fresh `run_gaps.py` run clears it, 1.4.29), or when it was saved while it listed a stale row (an `"old_format"` row or one with no `reason`, 1.4.30) or its `stale_reference` is not a list (1.4.31), and `A/reference.json` itself when it cannot be read as a list of rows, or is absent beside `area-plan.md` (`"unreadable_reference"`, 1.4.31, absent 1.4.32); holds `next` at `plan`, approved or not, 1.4.28), `approval_why` str or null (`"no_record"`, `"plan_changed"`, `"reference_hash"`: the line naming the plan's hash carries no `reference-hash` equal to `git hash-object A/reference.json`; `"reference_format"`: it records `reference-format`, the 1.4.29 form, which approves nothing since 1.4.30), `reference_hash` str or null (the hash an approval records; null with no readable `A/reference.json`, and null while `stale_reference` lists any row, 1.4.30), `next` str or null, `next_why` str, `r9_stale` list (each `{file, input, reference, recorded, current, reason, why}`: `input` `"reference"` (`reason` `no_hash`, `changed`, `missing_reference`), `"folder"` (`reference` the survivor folder; `folder_no_hash`, `folder_changed`, `missing_folder`, 1.4.34) or null (`unreadable`: invalid JSON, no `folder`, or an empty `references` list), G94, 1.4.33; `next_why` counts files and rows), `plan_sections` list (each a missing, misspelled or out-of-order section, or a Missing subject not carried: `carried nowhere`, `named only under Owner questions`, `carried, no host but not under Owner questions`, or `no bold lead phrase`; matched by its bold lead phrase verbatim in Research questions, G97, G105, 1.4.33, 1.4.34); `old_report` also lists a plan with no `A/run_gaps.json` (G99, 1.4.33), and a `stale_reference` row with a null `file` is a legacy row, counted (G108, 1.4.33); 1.4.36: `plan_sections` also lists `not a list item`, `named but not carried`, a second bold phrase of an item, and per Topics-table topic (else per Proposed-topics `Topic`, else one `Topics` row) a missing research-bar Owner question, a topic merged elsewhere excepted (`found` null, G126–G128); `stale_copy_check` list (each `{recorded, current, why}`, holds `next` at `plan`, G133), `other_plans_changed` list (each `{plan, recorded, current, sections, why}`, advisory, G134, G153), `survivor_carries` list (each `{question, subject, kind, survivors, why}`, advisory, a copy-only plan, G130, G150; `kind` G185, 1.4.38), `carries_asked` list (each `{plan, question, subject, kind, why}`, G151, 1.4.37; a `subject` row a hold since 1.4.39, G214); 1.4.39: `host_check` list (a hold, G188), `shared_no_host` and `stale_pointer` lists (advisory, G190, G216); `other_plans_changed` rows also carry `cited_at` and `question_cites` (G194, G211); `--digest` prints `stage_status.py <area>: next X; plan_sections N; ...; result <sha12>` (G137) |
| `run_gaps.py --area` (saved as `A/run_gaps.json`) | `area` str, `out` str, `note` str, `topics` list, `building` list, `same_text` list, `why_empty` str or null, `cleared` list (a run, `--out` included), `r9_targets` list, `measured_elsewhere` list, `unmeasurable` list, `missing_files` list, `stale_gaps` list or dict, `r9_missing` list, `failed` list, `unplaced` list (a topic folder that cannot be read, with its error; any row exits 2, `--check` too), `short_sentences` list, `home_measures` list, `home_unguessed` list, `numbering_differs` list, `advisory_failed` list, `stale_reference` list (each row with a `reason`: `"old_format"` or `"no_writer"`, 1.4.29), `reference_format` int (the format the report was measured under, 1.4.29; `stage_status.py` lists a report with none or a lower one as stale), `hints` bool, `r9_stale` list (G94, shaped as in `stage_status.py`), `markers` list, `repeat_of` list (1.4.33), `held_by_wording` list (each `{speciality, n, text, topic, marked_for, number_differs, topic_sentence, id}`, with `verdict`? or `verdict_was`? and `verdict_why`?, G132, 1.4.36; G159, 1.4.37); a `short_sentences` row's `fragment` is true for every `kind: "label"` row too, so the fragment and label counts overlap (1.4.34) |
| `run_gaps.py --check` | `area` str, `check` str, `out` str, `report` str (the saved report compared), `would_clear` list, `failed` list, `unplaced` list, `stale_reference` list, `r9_stale` list, `hints` bool, `hints_from` str (`"flag"` or `"report"`, G96), `not_compared` list (only when the two runs differ on `--hints`), `new_keys` list (only when a key the saved report lacks has an empty fresh value: `[]`, `{}`, null or false, at any depth; no change, never sets the exit; a non-empty new key is a change, 1.4.34), `changes` list, `gap_total` list (each `{stated, counted, saved, line, form, why}`, advisory; `--digest` prints `gap_total_rows N; measured_total M`, 1.4.39, G189; 1.4.40), `measured_total` int, `saved_total` int or null, `verdict_changes` list (each `{id, kind, was, now, total_delta}`, G247); `--digest` prints one line instead of the JSON (G120, 1.4.33) |
| `run_gaps.py --area --check` | `area` str, `check` str, `out` str, `would_clear` list, `failed` list, `unplaced` list (a topic folder that cannot be read, new or unchanged; any row exits 2), `changes` list |
| `unmeasured.py` | `area` str, `new_topics` list, `building` list, `unplaced` list, `marked_here` list, `mark_conflicts` list, `against_survivor` list, `survivor_elsewhere` list, `unread_marks` list, `ignored_marks` list (G109, 1.4.33); `--check` prints `{area, check, saved_file, stale_reference, changes}` and `new_keys` as `run_gaps.py --check` does (1.4.34); the area as a positional or `--area`, `--reference` defaulting to `A/reference.json`, `--check --digest` one line (`check`, `changes`, `new_keys`, `stale_reference` counts and the result's hash), `--keys`/`--summary` (G137, G139, 1.4.36) |
| `unmeasured.py --check` | `area` str, `check` str, `saved_file` str (the file compared; nothing is written), `stale_reference` list (1.4.27; a non-empty one is a change), `changes` list |
| `paraphrase_hints.py` | `advisory` str, `gaps` list (nested per file and reference), `sentences` list (flat, one row per lacking sentence: `gaps_file`, `folder`, `file`, `text`, `hints`) |
| `copy_check.py` | `area` str, `twin_differs` list, `copies` list (each with `stamps`, `parts.differ_uncarried` and `kept`, 1.4.33), `moved` list, `unreadable` list; `--digest` prints `copy_check.py <area>: copies N; identical N; moved N; unreadable N; twin_differs N; differ_uncarried <copy:part,...\|none>; result <sha12>` (G133, 1.4.36) |
| `mark.py` | `file` str, `n` int, `text` str, `was` and `now` (a mark); with `--mark`, `file` str and `marks` list (`n`, `text`, `was`, `now`); with `--home`, `file` str or null, `homes_file` str and `homes` list (`n`, `text`, `was`, `now`: the topic, `<area>:<topic>` for another area's, or null when cleared; G145, 1.4.36; G156, 1.4.37); with `--held`, `file` str, `id` str, `was` and `now` (G159, 1.4.37); with `--held-file`, `file` str, `verdicts` int, `changed` list (G199, 1.4.39) |
| `quote_building.py --check` | `file` str, `renumbered` bool, `old_count` int, `new_count` int, `marks` list, `joined` list, `lost` list, `changed` list, `kept` bool (G111, 1.4.33) |
