# Stage 2: Research each topic, in detail

The detail of SKILL.md's *Stage 2*. The commands are in SKILL.md; the steps
here are numbered as there.

## Reads and writes

**Reads:** `A/area-plan.md`, `A/approval.md` (stop unless the status
script's `approval` is `current`), the topic's current folder if it has one.
**Writes:** per topic, `A/topics/<topic>/base.txt`, `A/topics/<topic>/research-brief.md`,
`A/topics/<topic>/team-run.md` (the team ran) or
`A/topics/<topic>/agent-run.md` (the fallback ran),
`A/topics/<topic>/second-check.md`, in the
artifact's own folder `<artifact>/research/research.json` and
`<artifact>/research/research.md`, and the topic's removal from
`cookbook/research-exempt.json` when it is listed there. A new topic's
folder holds only `research/` until stage 3.

## Step 0: The base commit

0. Record the topic's base commit, before anything is written. Unless
   `base.txt` exists already (a re-run keeps the first one):

The research cites the topic's current rules at this commit, and stage
5's lossless check compares against it.

## Step 1: The research brief

1. Write `research-brief.md`: the topic, its research type, its research
   questions from the plan, the four questions (SKILL.md, *The four questions*) verbatim, and the method:
   - Research to `guidelines/researching/process/research-methodology-and-sources`,
     using its source catalogue for the domain. Primary sources
     (specifications, standards, vendor documentation) come before secondary ones.
   - Verify every existing rule of the topic and every rule the devteam's text
     adds. Quote each one **verbatim**, with the file it is in and the base
     commit from `base.txt`, as a claim to check, never as a source. Never
     restate or summarize a rule: a paraphrase carries your own facts (a
     guideline number, a version) into the research as if the rule said them.
     The devteam's text is the area's sentences of each speciality the plan
     quotes under this topic; a building speciality's sentences marked
     another area's (stage 1, `quote_building.py`) are not this topic's.
   - **Name every rule.** A rule with no `**name**:` (a prose sentence or a
     bullet list) gets a kebab-case name in the brief, one name per rule, the
     same name for the same text repeated in several parts. These names are
     fixed from here on: research verdicts key on them, and stage 3 keeps
     them. Mark each rule whose text has no MUST, SHOULD or MAY as having no
     RFC keyword.
   - Score each claim 0–100 per `guidelines/researching/evidence/verification-and-trust-scoring`,
     applying the principles `cite-the-claim-not-the-document`,
     `independence-before-corroboration`, `domain-stratified-trust`,
     `suppress-unsupported-confidence` and `provenance-at-generation-time`.
   - Find what the topic is missing: practice the research finds that no rule covers.

## Step 2: Run the research

2. Run the research. First check whether the research team can run, with the
   probe that never starts a run (`myteams … --help` is no probe: myteams
   routes it into dispatch):

- **If `ok` is true**, run the team on the brief in the foreground:

  Follow each `__MYTEAMS_NEXT__` line until `__MYTEAMS_DONE__`. Save the
  final report to `team-run.md`, then go on to step 3, which turns the
  team's output into `research.json`. If the team fails once it has
  started, stop and report its error verbatim.
- **If `ok` is false**, say its `why` once (never install into the team's
  environment), and dispatch the research as one fresh Agent instead
  (`subagent_type: general-purpose`, `model: opus`; it uses WebSearch and
  WebFetch), with the `research` prompt:

The prompt holds everything the research needs: the method files, the
four questions, the shape of every claim and verdict, the
`<rule-name>-prior` claim for a rule the research cannot support, the
open questions for the owner, and the `cookr validate --research` line
it checks its files with. `supported` there means supported **at the
rule's stated strength**: a MUST whose sources say "should" is
`unsupported`, with the claim saying so. Save the reply to
`agent-run.md`. Steps 3 and 4 then check the two files the agent wrote
against what they require and correct them, rather than writing them anew.

## Step 3: research.json

3. Write `<artifact>/research/research.json` in the shape of
   `guidelines/researching/evidence/research-results-document`: its container
   fields (topic and scope, the questions, methodology, agents and sources,
   dates, summary, open questions, limitations, license), a `claims` list and
   a `verdicts` list. Each claim carries every field `cookr validate` checks
   (see `guide/introduction/conventions.md`, *Research*), with the values the
   `research` prompt lists. A team claim with no quoted source is fetched and
   quoted, or dropped and listed under limitations. Each existing or devteam
   rule, under the name the brief gave it, gets a verdict,
   `{"rule": "<name>", "verdict": "supported"|"contradicted"|"unsupported"|"new", "claims": [<ids>]}`,
   with `supported` meaning supported at the rule's stated strength; a rule
   the research cannot support or finds against is recorded as its own
   `<rule-name>-prior` claim. Each practice no rule covers gets a `new`
   verdict naming the rule stage 3 will write. Every verdict names at least
   one claim. What the research leaves to a policy choice goes in
   `open_questions`, one entry per question: the owner list carries them.
   (When the fallback Agent ran, it wrote this file: check it holds all of
   this.)

## Step 4: research.md

4. Write `<artifact>/research/research.md`: the same, readable, under exactly
   these headings in this order: `## Best practices`, `## Known solutions`,
   `## Platform guidelines`, `## The expert's view`. Each finding names its
   claim id. It never repeats a trust score or an independence value:
   research.json holds those, once, so a later correction cannot leave
   research.md stale.

## Step 5: The exemption list

5. If `cookbook/research-exempt.json` lists the topic (its `topics` list
   holds `<artifact>` without the leading `cookbook/`), remove that entry now,
   in the same change that adds `research/`. A listed topic that has its
   `research/` is refused by `cookr validate` (`stale-exemption`). Never add
   an entry: the list only shrinks.

## Step 6: The second check

6. Second check, the independent check of every `contradicted` and `new`
   claim. List the claims it covers (every claim a `contradicted` or `new`
   verdict names, except the `prior cookbook text` claims):

Whether the team or the fallback did the research, dispatch one fresh
Agent (`subagent_type: general-purpose`, `model: opus`; it uses WebFetch)
that did not run the research, with the `second-check` prompt, its
`claims` that list, one `- <id>` per line:

The prompt carries the rule (a claim is refuted unless `quote-found` and
`supports-claim` are both `yes`; `partly` is not `yes`) and asks, per
citation, whether that source holds the quote. Write the reply to
`second-check.md`, then apply it by script, never by hand:

It applies the rule whatever each block's `result` line says (and names
the blocks it overrode in `result_disagrees`): a refuted claim's trust is
lowered, with the reason in `trust.basis`; a citation that lacks the
quote is dropped when another holds it, and the claim's independence is
recomputed from the citations left. Each change gets a `- correction:`
line in `second-check.md`, which stage 3's write brief carries. Run again,
it changes nothing. On exit 2 (a block names a claim research.json lacks),
stop and report its output.

## Step 7: Check the research alone

7. Check the research alone, before any rule cites it:

`--research` takes the artifact folder, never its `research/` folder
(that gives "not an artifact source folder"). It must print
`Research passed.` It checks research.json and research.md (every claim
field and value, every verdict, the four headings) and the exemption
list, and leaves out the rules' citations, which stage 3 writes. On a
finding, correct the file it names and run it again. Its
`owner-decides` warnings are expected here only if the topic's rules
already cite claims; they are stage 5's to list.

## After stage 2

After stage 2, a topic's research is fixed. A rule's citations, written in
stage 3, are authoritative: a verdict's `claims` list is stage 2's record of
the old rule, and neither `cookr validate` nor the reviewer compares the two.
The author never edits research; a review finding that asks for it is
answered in the draft or disputed.
