# Stage 4: Review each topic, in detail

The detail of SKILL.md's *Stage 4*. The commands are in SKILL.md; the steps
here are numbered as there. Which way a topic goes after a round (`next`)
is in SKILL.md, stage 4 step 3.

## Reads and writes

**Reads:** the artifact folder, `<artifact>/research/`, `A/topics/<topic>/owner-list.md`,
`A/topics/<topic>/second-check.md`, `A/topics/<topic>/write-brief.md`, and from
round 2 the saved `review-<N>.md`, `draft-<N>.md` and `disputes.md`.
**Writes:** `A/topics/<topic>/review-prompt.md`, `A/topics/<topic>/review.md`,
from round 2 `A/topics/<topic>/diff-<N>.md`.

## Step 1: The review prompt

1. Write the round's review prompt:

It prints `{"round", "prompt"[, "diff"]}` and writes `review-prompt.md`:
- round 1, `review-full`: the review criteria, every instance of a
  finding's class named in that one finding, `/lint-artifact` run with the
  cookr line;
- round 2 and later, `review-scoped`: the earlier `review-<N>.md` files,
  `disputes.md`, the findings still open, and the diff from the last draft
  (`diff-<N>.md`). The reviewer rules on each open finding (`fixed`,
  `disputed-accepted`, `routed` or `open`, under `## Rulings`; `routed`:
  the finding belongs to a named sibling topic and was recorded in that
  sibling's write-brief.md if it has not passed stage 4, or in its
  integrate.md if it has, and closes it like `fixed`), raises a new finding
  only on text the diff shows changed or for a factual error against a
  cited claim, and never asks to reverse an earlier fix without citing
  the claim that makes it wrong.
Both prompts say that a stale `version`, `modified` or Change History is
never a finding (stage 5's `cookr bump` writes them), that the owner list
exempts only wording, and that a rule's citations are authoritative.

## Step 2: The review

2. Dispatch one fresh Agent that wrote none of the topic and reviewed no
   earlier round of it (`subagent_type: general-purpose`, `model: opus`),
   with the text of `review-prompt.md` exactly. It writes `review.md`:
   `# Review: <topic>`, `## Findings` (findings only, each naming every
   instance of its class), `## Checked` (positive notes), from round 2
   `## Rulings`, `## Lint` (the /lint-artifact result, ending with exactly
   `lint: clean` or `lint: fail <n>`), and last the line `verdict: pass` or
   `verdict: fail`. Lint fails closed: `review_findings.py` reads only that
   lint line, and `lint: fail <n>`, a missing or malformed line, or no
   `## Lint` is a lint error, which makes the round a failure whatever its
   verdict says. The review is done when `review.md` ends with that
   verdict line; a later notification from the same agent changes nothing.

## Step 3: Counting the round

3. Count the round:

`append` saves `review.md` as `review-<N>.md` and `draft.md` as
`draft-<N>.md` (N the round just reviewed), and appends
`## Round <N> findings` to the brief: each finding with its id
(`R<N>.<n>`) and the author's disputes so far. A lint error goes to the
author too: on `lint: fail <n>` the brief carries the review's `## Lint`
section, each error for the author to fix; on a missing or malformed lint
line, the reviewer's fault, the brief tells the author to leave the draft
unchanged on lint grounds, and the next review prompt restates the
lint-line rule. The same review twice is
no new round. It refuses a round past the cap (exit 3); `status` then
says where the topic goes. This is the one place `append` runs.
`status` prints `{"rounds", "max_rounds", "allowed_rounds", "verdict",
"lint_errors", "lossless", "open", "next", "why"}` (`stage_status.py`
reports the same `rounds`, `owner` and `next`):
