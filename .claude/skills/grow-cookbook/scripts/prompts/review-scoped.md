You are re-reviewing a cookbook guideline you did not write. Today is
{{today}}. Do not edit any file except the one you are told to write, and run
no background work: reply only once review.md is complete.

The guideline: {{repo}}/{{artifact}}/ (artifact.json and one .md per part).
Its research: {{repo}}/{{artifact}}/research/research.json and research.md.
The second check: {{topic_dir}}/second-check.md.
The owner list: {{topic_dir}}/owner-list.md.
The earlier reviews: {{reviews}}
The author's disputes: {{topic_dir}}/disputes.md (absent when there are none).
What changed this round: {{diff}} (the diff from the previous draft).

Run cookr, this checkout's own, as `{{cookr}} <command>`: for example
`{{cookr}} roles check {{artifact}}`.

This is round {{round}} of at most {{max_rounds}}: a scoped re-review, not a
fresh one.

{{criteria}}

The findings still open, to rule on:
{{open}}

1. Rule on every open finding above, in `## Rulings`, one line each:
   `- <id>: fixed|disputed-accepted|routed|open — <reason>`.
   - `fixed`: the change resolves it.
   - `disputed-accepted`: the author disputed it in disputes.md and is
     right. A dispute you reject is `open`, with why.
   - `routed`: the finding belongs to a named sibling topic and was recorded
     in that sibling's write-brief.md if it has not passed stage 4, or in its
     integrate.md if it has. Name the sibling in the reason.
   - `open`: it still stands.
2. Raise a new finding only on text the diff shows changed this round, or for
   a factual error against a cited claim (name the claim). Nothing else is
   reviewed again.
3. Never ask to reverse a fix an earlier round asked for unless you cite the
   claim that makes that fix wrong.
A new finding names every instance of its class in the changed text.

Then run the /lint-artifact skill on {{repo}}/{{artifact}}, telling it to run cookr as
above, and include its result. A lint WARN is not an error.
{{lint_rule}}
Write {{topic_dir}}/review.md:
- `# Review: {{topic}}`
- `## Findings`: new findings only, one top-level `- ` bullet each: the file,
  the rule or line, what is wrong (every instance), and the fix. Write `none`
  if there are none.
- `## Checked`: what you checked and found right, one bullet each.
- `## Rulings`: one line per open finding, as above.
- `## Lint`: the /lint-artifact result, then, as the section's last line,
  exactly `lint: clean` (no lint error) or `lint: fail <n>` (n lint errors).
  A script reads only that line; without it the round counts as a lint
  failure.
- last, a line of its own, exactly `verdict: pass` or `verdict: fail`.
  `fail` when a new finding, a ruling of `open`, or a lint error stands.
Reply with the verdict line only.
