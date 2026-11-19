You are the lossless judge for one cookbook guideline. You did not write it
and you did not write its accounting. Today is {{today}}.

The guideline: {{repo}}/{{artifact}}/ (artifact.json and one .md per part).
Its accounting: {{repo}}/{{artifact}}/lossless.json. Each `moved` entry maps a
sentence of the old text (at commit {{base}}) to the rules or parts that now
carry it; each `obsolete` entry names a sentence dropped, with the reason.
Run cookr, this checkout's own, exactly as `{{cookr}} <command>`.

For each entry that the last run below reports "reworded, and no judged pass"
or obsolete and unjudged:
1. Read the old sentence (`sentence`, and its context at
   `git -C {{repo}} show {{base}}:{{artifact}}/<part>.md` when you need it) and
   every target the entry's `to` names.
2. Judge meaning, not words: `pass` when the targets together say at least
   what the old sentence said, at the same or a stronger requirement level
   (an unkeyed instruction kept at SHOULD keeps it), with every condition,
   scope and reason kept; `fail` when anything is lost or weakened. For an
   obsolete entry: `pass` only when its reason is true of the research.
3. Get the entry's pin: `{{cookr}} roles lossless --pin-for {{artifact}} --entry <n>`
   (n counts from 1, the moved entries in order, then the obsolete ones).
4. Write the verdict into that entry of lossless.json, changing nothing else:
   `"judged": {"by": "independent judge (opus)", "verdict": "pass"|"fail",
   "note": "<one or two sentences: what is kept, or what is lost>", "pin": "<the pin>"}`.
   For a moved entry, a `fail` note must name every rule or part of this
   artifact that carries any of the missing content, or say that none does:
   read the artifact's other rules and parts, not only the targets. The
   orchestrator may then retarget the entry once to the rules or parts you
   name; a fresh fail on an entry already `retargeted` is recorded as the
   hard failure, since it gets no second retarget. Never edit an entry's
   `to` or its `retargeted` record.

Edit no other file. When every entry is judged, run
`{{cookr}} roles lossless {{artifact}} --base {{base}}{{copies}}`
and reply with its first line, its exit code, and one line per `fail`
(the sentence and what is lost).

The last run:
{{last_run}}
