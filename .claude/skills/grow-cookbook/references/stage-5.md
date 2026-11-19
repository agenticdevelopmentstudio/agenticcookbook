# Stage 5: Integrate each topic, in detail

The detail of SKILL.md's *Stage 5*. The commands are in SKILL.md; the steps
here are numbered as there.

## Reads and writes

**Reads:** `A/topics/<topic>/review.md` (stop unless `review_findings.py
status` says `next: integrate`, or `next: owner` and its open findings are in
`integrate.md`), `A/topics/<topic>/base.txt`.
**Writes:** `<artifact>/lossless.json`, `A/topics/<topic>/lossless-<N>.md`
(on a hard failure), `A/topics/<topic>/integrate.md`, a log of each command
and its result.

## Step 1: Nothing the topic held is lost

1. Nothing the topic held is lost. The orchestrator writes the accounting;
   one fresh judge rules on it.
   1. Run the check, with `--copy <folder>` for each folder in the topic's
      `fold` (from `stage_status.py`: every merged copy, the worklist copies
      whatever their `fold_check` and the existing topics other plans merge into
      this one; only a copy a plan keeps (Action `kept`) and no plan merges
      is not folded):

Exit 0: on to step 2. A new topic has no base text: log that and go
on. A `---` line or a heading that only repeats the title is no
sentence and is never reported.

### Step 1.2: lossless.json

2. On exit 1 with `missing` sentences, write `<repo>/<artifact>/lossless.json`
   yourself, as the orchestrator: `{"base": "<base>", "copies": [<the
   folded copies>], "moved": [...], "obsolete": [...]}`, one `moved` entry
   per missing sentence, `{"sentence", "to": [<rule names or parts>]}`,
   naming the rules or
   parts that now carry it, or one `obsolete` entry, `{"sentence",
   "reason"}`, for a sentence the research made obsolete. Tune the
   targets with `cookr roles lossless <artifact> --base <base>
   [--copy <folder>]... --draft` until no tripwire fails (a sentence's
   words mostly found in its targets). Never judge an entry yourself.

### Step 1.3: the lossless judge

3. When entries report `reworded, and no judged pass`, or a stale verdict
   (`stale`: the text it judged has changed), or obsolete and unjudged,
   dispatch one fresh Agent (`subagent_type: general-purpose`,
   `model: opus`) that wrote none of the topic, as the lossless judge,
   with the `lossless-judge` prompt:

The judge judges meaning, pins each verdict with
`cookr roles lossless --pin-for <artifact> --entry <n>`, writes it into
the entry's `judged`, and re-runs the check. A `fail` note names every
rule or part of the artifact that carries any of the missing content,
or says that none does.

### Step 1.4: one retarget

4. One retarget. When a judged `fail`'s note names a rule or non-rule
   part outside the entry's `to` that carries missing content, the
   orchestrator may retarget the entry once, before recording anything,
   by cookr, never by hand, with `cookr roles lossless --retarget <artifact>
   --entry <n> --to <name>...`, naming the targets that carry the sentence (still at most 3). `--retarget` refuses targets that fail the 80% bar or a tripwire, the
check `--draft` runs in step 2, and writes nothing then: a bad pick
spends nothing, so try others. On targets that pass, cookr moves the
old `to` and that fail into the entry's sealed `retargeted` record,
adds the sentence to the file's `retargets` ledger, and drops the
fail. Then dispatch a fresh judge as in step 3. A
second retarget is refused: `--retarget` exits non-zero on an entry
already retargeted, and `roles lossless` fails the entry by name when
its `to` differs from the record's, its record was written or changed
by hand, or the ledger names it with no record. A second judged fail
on the same entry is recorded as the hard failure (step 5); so is a
first fail whose note names nothing outside `to`. A sentence whose
content spans more than 3 rules or parts still takes a lossless round:
no retarget can name them all. The retarget allowance stays spent
through that round: a stale fail on a retargeted entry is re-judged
(step 3) after the author's rewrite, a pass clears it, and a fresh
fail is the round's failure.

### Step 1.5: a hard failure

5. A hard failure (a `fail` verdict that step 4 does not retarget, or a
   tripwire no target can meet, such as a lead-in whose items are lost): save the last run's JSON
   output to `A/topics/<topic>/lossless-run.json` and record it by script,
   never by hand:

Each missing sentence and failed entry becomes an open finding
`L<N>.<n>` in `lossless-<N>.md` and in the brief under
`## Lossless failure after round <N>`, with the author's rule for
carrying a lost sentence into a rule: every word added to the rule must
be covered by a claim the rule cites (the claim added to its citations,
at the strength the claims allow); a lost sentence no cited claim can
cover is disputed in disputes.md instead of added uncovered. The
`author` prompt says the same. The failure opens one round
past the 3-round cap, and exactly one round, even when the topic has
rounds left under the cap: stage 3's next round, then stage 4 as a scoped
round that rules on each `L` finding, then step 1 again. Then
`review_findings.py status` decides: `next: integrate` (that round
passed) runs step 1 again; `next: stop` (that round failed, or a
second lossless failure) stops the topic. A lossless failure never
goes to the owner.

## Step 2: cookr validate

2. `cookr validate` must pass, its Research section included. The topic left
   `research-exempt.json` in stage 2. Copy every `owner-decides` warning it
   prints for this topic (each names a rule and the prior claim it cites,
   whose verdict the research rules `unsupported` or `contradicted`) into
   `integrate.md` under `## For the owner`, with the owner list's open
   questions, and give the owner that list, with every `## From <topic>'s
   review` section in `integrate.md` (findings siblings routed there), when
   the stage ends: those rules
   stand as they were until the owner decides each. They are warnings:
   validate still passes. They match `owner-list.md`'s prior rules; a rule
   in one and not the other is a stage 3 error.
   - If it fails on this topic (its folder is named in the finding), fix the
     cause in the stage that owns it: a research finding (`missing-question`,
     `incomplete-claim`, `bad-verdict`, `unverdicted-claim`,
     `stale-exemption`, …) in stage 2, then stage 3 again with
     `write_brief.py write ... --restart` (the brief and owner list are
     rebuilt from the new research and the topic starts again at round 1),
     then stage 4; a rule or part finding
     (`rule-cites-nothing`, `citation-not-at-end`, `unknown-claim`, a roles
     finding) in
     stage 3, then stage 4 again. Re-run this stage from step 1.
   - If it fails on something this topic did not touch, run
     `/repair-cookbook`, then this step again.
   - If it still fails, stop and report the output verbatim.
