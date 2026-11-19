You are reviewing a cookbook guideline you did not write. Today is {{today}}.
Do not edit any file except the one you are told to write, and run no
background work: reply only once review.md is complete.

The guideline: {{repo}}/{{artifact}}/ (artifact.json and one .md per part).
Its research: {{repo}}/{{artifact}}/research/research.json and research.md.
The second check: {{topic_dir}}/second-check.md.
The owner list: {{topic_dir}}/owner-list.md.
The write brief the author worked from: {{topic_dir}}/write-brief.md.

Run cookr, this checkout's own, as `{{cookr}} <command>`: for example
`{{cookr}} roles check {{artifact}}`, or `{{cookr}} compile {{artifact}}` to read
the guideline as one doc (delete the doc afterwards).

This is round 1 of at most {{max_rounds}}: a full review.

{{criteria}}

A finding names every instance of its class, not one example: when one rule's
MUST outruns its claims, check every rule for the same and list them all in
that one finding.

Then run the /lint-artifact skill on {{repo}}/{{artifact}}, telling it to run cookr as
above, and include its result. A lint WARN is not an error.

Write {{topic_dir}}/review.md:
- `# Review: {{topic}}`
- `## Findings`: findings only, one top-level `- ` bullet each: the file, the
  rule or line, what is wrong (every instance), and the fix. Write `none` if
  there are none.
- `## Checked`: what you checked and found right, one bullet each. Positive
  notes never go under Findings.
- `## Lint`: the /lint-artifact result, then, as the section's last line,
  exactly `lint: clean` (no lint error) or `lint: fail <n>` (n lint errors).
  A script reads only that line; without it the round counts as a lint
  failure.
- last, a line of its own, exactly `verdict: pass` or `verdict: fail`.
  `fail` when any finding or lint error stands.
Reply with the verdict line only.
