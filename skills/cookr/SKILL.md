---
name: cookr
version: "0.23.9"
description: "Inventory, coverage, extraction prompts and arrangement for the specs of a library cookbook (a repo's cookbook/ directory with cookbook.json). Wraps the `cookr` CLI at ~/.local/bin/cookr. Use when the user asks which components have specs, what is left to write for a group, to write the spec for a component, to scope a change to the recipes it touches, to check what recipe work a change still owes, to record which code implements a recipe and confirm it, to rename or look up a recipe's id, to upgrade a cookbook to format 2, to relink specs after code moved, to convert artifacts into source folders and compile them back into docs, to compile them into routed skills for skill-router, to install, check or uninstall the compiled skills (the routed set and the always-on principles skill), or to tune them for the host and model you are running as (payload, stamp)."
argument-hint: "[--help] [-p <repo-root>] <inventory|coverage|arrangement|relink|scope|check|status|implements|confirm|id|rename|diff|upgrade|skills sync|convert|compile|roles set|roles check|roles lossless|roles worklist|roles gaps|fold|install|uninstall|payload|stamp|prompt extract <name>|--tier <group>> [...]"
allowed-tools: Bash(cookr *), Bash(command -v cookr)
model: sonnet
---

# cookr v0.23.9

Thin wrapper around the `cookr` CLI at `~/.local/bin/cookr`. All work goes
through the CLI — never duplicate its logic in this skill, including recipe
frontmatter, indexes, validation and lint (`cookr update`, `cookr validate`,
`cookr lint`, `cookr bump`).

## Startup

```bash
command -v cookr
```

If missing, tell the user:

> The `cookr` CLI is not installed. Run `skills/cookr/setup/install` from the agenticcookbook repo, then re-invoke me.

…and stop.

## The library cookbook

A repo's specs live in `<repo>/cookbook/`, grouped by concept, general to
specific (`cookbook/ai/chat/chat-context/`), never by platform. Every spec is a
source folder (below). Its identity is its UUID; its rdid
(`<cookbook-rdid>.<type>.<folder path>`) is a label held in
`cookbook/index.json`, which only cookr writes (`format: 2`, like
`cookbook.json`, `artifact.json` and `.cookr.json`). Specs link to each other
by UUID (`[<rdid>](cookbook:<uuid>)` in text).

The index also holds each spec's **implementations**: repo-relative paths of
the code (a trailing `/` claims a whole directory), each with a platform and a
conformance state (`planned`, `unverified`, `needs-validation`, `confirmed`).
Record them with `cookr implements`, never by hand. `cookbook/cookbook.json`'s
`code` block lists the source roots, so a file no spec claims yet still shows up
in `cookr status` and `cookr inventory`, named inside its root's `recipes`
group. A "tier" or group is any directory of the cookbook
(`--tier ai-plugin-kit/chat`).

A cookbook still on format 1 or the legacy layout is converted only by
`cookr upgrade [--dry-run]`, and only when you choose to run it while working on
that repo. No other command and not the hook ever converts it; they say on
stderr that the upgrade is available and carry on. The upgrade rewrites many
files and needs a clean work tree: look at `--dry-run` first, and commit the
result on its own. A format-2 `.cookr.json` is kept whole (its
`cookbook` dir, roots, dependencies and ignore); one whose `cookbook` names a
directory outside the repo, or one holding no cookbook, is refused (exit 2),
never answered with a new cookbook.

## Routing

| Request | Command |
|---|---|
| what components exist / what groups there are | `cookr inventory [--tier <group>]` |
| what is left to write | `cookr coverage [--tier <group>]` |
| write the recipe for X | `cookr prompt extract X --out-dir <dir>` → dispatch (below) |
| write everything a group still needs | extraction workflow (below) |
| is every spec in its code's concept group | `cookr arrangement [--tier <group>]` |
| code moved (renamed in version control) | `cookr relink [--since <ref>] [--dry-run]` |
| which recipes does this change touch (minimum, siblings) | `cookr scope [paths\|ids] [--since REF] [--json]` |
| what recipe work a change still owes | `cookr check [--staged\|--branch] [--json]` |
| uncovered files and each implementation's conformance | `cookr status [--json]` |
| record the code implementing a recipe | `cookr implements <id> <location> [--platform P] [--planned] [--remove LOC]` |
| implementation matches the recipe's current version | `cookr confirm <id> [--platform P] [--location L]` |
| look up an artifact's uuid, rdid, path | `cookr id <uuid\|rdid> [--json]` |
| rename a recipe's rdid | `cookr rename <uuid\|rdid> <new-rdid>` |
| what changed between two versions of a recipe | `cookr diff <id> <from> [<to>]` |
| upgrade a repo or cookbook to format 2 | `cookr upgrade [--rdid R] [--dry-run]` |
| compile and register this repo's skill sets | `cookr skills sync` |
| turn `.md` artifacts into source folders | `cookr convert [paths] [--dry-run] [--out <dir>] [--remove-source]` |
| fold an edited `.md` back into its folder | `cookr convert --update [--force] <paths>` |
| build the single-file docs from source folders | `cookr compile --target doc [paths] [--out <dir>] [--check] [--force]` |
| compile artifacts into routed skills | `cookr compile --target skill [paths] --out <set-dir> [--library L] [--check]` |
| which hosts / models cookr tunes for | `cookr targets [--host H] [--model M] [--json]` |
| what a skill looks like on a host / model, and does it load | `cookr render <skill-dir> --host H [--model M] [--out <file>] [--check]` |
| is the group written | `cookr prompt extract --tier <group> --out-dir <dir>` lists nothing to write |
| is the phase done | `cookr coverage --tier <group> --require complete` then `cookr validate -p <cookbook_dir>` |
| no args / `--help` | `cookr --help`, present the module table verbatim |

Forward `-p <repo-root>` to every `cookr` call when the user supplies one;
otherwise run from cwd and let the CLI find `cookbook/cookbook.json`. Pass
`cookr` the absolute `cookbook_dir` from the worklist JSON below, never a
cwd-relative path.

## Working in a cookr repo

A repo with `.cookr.json` is recipes-first. The cookr hook (installed by
`skills/cookr/setup/install`) only tells you to pay attention: it reminds you
once per session (and says when the repo is still format 1), and on a commit
runs `cookr check` and hands you any recipe work it finds, by rdid, as advice.
It never blocks, never writes a file and never converts anything. What to
change and whether to commit it is your call while you work on the files.
`CC_ALLOW_COOKR=1` in the commit command quiets the advice.

1. During planning, run `cookr scope` on the planned files and give Mike the
   minimum and the siblings; record his answer in the plan.
2. Write or update the recipes in the worktree **before** the code, as the shared
   design.
3. Keep them updated as the code changes; a missing recipe is written with the
   existing `prompt extract` brief and verify pass (below). Claim the code with
   `cookr implements`.
4. When an implementation matches its recipe, `cookr confirm` it.
5. `cookr bump` each recipe you changed, then `cookr validate` before the work is
   done.

### Building from a recipe: settle its open questions first

A `NEEDS REVIEW` marker is a decision the recipe's writer could not settle from
the code. Building past one means guessing, and the guess spreads to every
platform that copies the code. So whenever you read a recipe in order to build
from it (a new feature, a port to another platform, a change to code it
claims):

1. Search the recipe for `NEEDS REVIEW`, in its source folder's parts or its
   compiled skill and that skill's `references/`. A compiled skill that has
   markers opens with an *Open questions* notice that says so.
2. For each marker that bears on what you are about to make, **stop and ask
   the user to settle it**, one question at a time. Give what the code does
   today, what the marker leaves open, and what each answer would mean for the
   build. Never settle a product decision yourself. A marker you can settle
   with evidence, such as measuring a contrast ratio, you settle yourself and
   report.
3. Write the answer into the recipe's source folder in place of the marker,
   either restated as fact or as a requirement to build. Then run
   `cookr compile --target doc` and `cookr bump`, and build to the settled text.
4. Leave markers that don't touch your work as they are. They wait for whoever
   next builds that part.

The phase gate (`cookr coverage --require complete`) stays red while markers
remain. That is expected: markers are settled as their recipes are used, not
in a review pass of their own.

## Source folders

An artifact source folder is `<name>/artifact.json` plus one `<part>.md` per
section. The spec is `docs/superpowers/specs/2026-10-03-artifact-source-folder.md`
in the agenticcookbook repo. `convert` refuses any file that would not compose
back byte for byte. It reports type-shape problems (missing or out-of-order
sections) without failing. `compile --check` exits 1 when a doc is missing or
stale, and `cookr validate` runs the same check. Once an artifact has a folder,
the folder is the source: edit its parts and run `cookr compile`, or edit the
`.md` and run `cookr convert --update` on it. A plain `convert` skips an
artifact that already has a folder, and a doc with no folder fails `validate`,
`compile` and `install`.

`artifact.json` records `synced`, the digest of the doc cookr last wrote, so
cookr knows which side changed when a doc and its folder disagree:
- **Doc edited:** `compile` refuses to overwrite it. `convert --update` folds the
  edit in; `compile --force` discards it.
- **Folder edited:** `compile` writes the doc. `convert --update` refuses to
  fold over the folder's edit; `convert --update --force` discards it.
- **Both edited** (or no record and they differ): both refuse. Keep one side
  with `convert --update --force` (the doc) or `compile --force` (the folder).

`bump`, `update` and `relink` edit from the newer side, write
through the folder and record the sync; they refuse an artifact edited on both
sides.

A spec with child specs (`telemetry.md` beside `telemetry/sources.md`) shares
its folder with them: `telemetry/` holds the parent's `artifact.json` and parts
next to the children's docs and folders. An artifact owns only its manifest and
its parts, so writing it never removes anything else, and `convert` refuses a
part that would overwrite another file (rename the section or the child).

## Host tuning

Shared text names no host or model. Wording true for one host, family or model
goes in a `hosts/` addition beside the source: `hosts/<target>.add.md` is appended
to the body, and `hosts/<target>.add.yaml` (flat `key: value` lines) is merged into
the frontmatter. A target is `claude`, `claude.opus` or `claude.opus-5-5`; the
host list ships in cookr (`cookr targets`). `cookr render` applies the additions
host → family → version and reports BROKEN, exiting 1, when the result would not
load on that host (Codex accepts only `name`, `description`, `license`,
`allowed-tools` and `metadata` in frontmatter). `cookr validate` fails an
artifact whose shared text names a host unless its `artifact.json` gives the
reason in `names_hosts`, fails an addition it cannot apply, and warns when a
stamped addition was written against an older source.

## Tuning workflow

A model tunes the cookbook for itself. Nobody can tune for a model they are not.

1. **Identity.** State your host and exact model ID from your own context, for
   example the system prompt's "the exact model ID is …". Never infer it from
   tooling or from which CLI is installed. The target is `<host>.<version>`,
   for example `claude.opus-5-5` or `codex.gpt-5-codex`. If your context does
   not show your model ID (Codex's first pass could not see it), your target is
   the bare host, for example `codex`, and you write only `<host>.add.*`
   additions, never a family or version one.
2. **Survey.** Run `cookr payload --target <target> --json`. For each level it
   prints `source_sha256` and the additions it already has along your chain,
   with `stale` set on any written against an older source. Templates come with
   their `text`. A template level is `template:<kind>` (every skill of one type)
   or `always:principles` (the always-on principles skill).
3. **Templates first.** For each template, ask four questions:
   - Is anything here false for me?
   - Is anything true only for me?
   - What can I do that the general version cannot assume?
   - Does the general version already work?

   If it already works, write nothing; an empty pass is a valid result. Otherwise
   write the addition at the **least specific level where it holds**: true for
   every Claude model goes in `<hosts_dir>/claude.add.md`, true for every Opus
   model in `claude.opus.add.md`, true only for you in `claude.opus-5-5.add.md`. A `.md`
   addition is appended to the body; a `.yaml` addition merges frontmatter keys.
   Keep each one short. It is read every time the skill loads.
4. **Exceptions.** Run `cookr payload --target <target> --out-dir <scratch dir>
   --batch-size 25` to write worklists. Each entry holds the skill as you
   receive it today (`text`) and the file to write (`write_to`). Ask the same
   four questions per artifact, and write only where the artifact itself needs
   more than its template's addition. Work the worklists with subagents running
   **your own model**. Pinning them to a cheaper model would tune for the wrong
   model. Run up to 8 at a time.
5. **Stamp.** Run `cookr stamp <addition>...` on every addition you wrote or
   re-checked, then run `cookr validate` (it warns about stale additions and
   fails on ones it cannot apply). Render a sample with `cookr render` or
   `cookr compile --target skill --check` to confirm each host still loads.

## Skills

`compile --target skill --out <set-dir>` makes one skill per artifact.
- **Name:** the path below the type directory, joined with `-` (a one-segment
  path keeps its type: `principle-simplicity`). `--library L` prefixes it. A
  library cookbook grouped by concept rather than type uses the path below its
  root (the directory holding `cookbook.json`): `ui/settings/rows/button-view`
  becomes `adtoolkit-ui-settings-rows-button-view`.
- **Routes:** derived from the type:
  - guidelines: `coding/<phase>[/<category>]`, plus
    `coding/when/<trigger>/...` for each trigger;
  - principles: `principles`;
  - ingredients and recipes: `components/<library>/...`, plus a platform branch.
  `routes` in `artifact.json` overrides them.
- **Text:** the type's template in `cookr/data/templates/skill/` decides which
  sections stay. History is left out. SKILL.md keeps only what doing the task
  needs: the template's `refer` list moves rationale, test vectors, platform
  notes and cross-cutting checks into `<name>/references/<file>.md`, and SKILL.md
  ends with a `## More` list linking each file with a line saying when to read it
  (progressive disclosure, as skill-router 0.7.0 expects). Templates are read from
  `$COOKR_TEMPLATES` when set, else from the cookbook's own repo
  (`skills/cookr/cli/cookr/data/templates/`) when it has one, else from the
  installed cookr.
- **Frontmatter:** `name` and `description` only. Every cookr key goes under
  `metadata:`, so the shared SKILL.md loads on every host.
- **Variants:** a host or model that reads differently gets
  `targets/<target>.SKILL.md`. `targets.json` (the host table) sits at the set's root,
  next to `skills.json` (the receipt).
- **Open questions:** an artifact that still holds `NEEDS REVIEW` markers
  (outside Change History) gets a `## Open questions: settle them before you
  build` notice after its opening. The notice tells the model building from the
  skill to stop and settle the markers its work touches, as in *Building from a
  recipe* above. A settled artifact gets no notice.

In a cookr repo each cookbook (this repo's and its dependencies') has its own set
in `$COOKR_HOME/sets/<cookbook-rdid>`, registered with skill-router under that
cookbook's rdid and scoped to the repos that use it. `cookr skills sync [-p REPO]`
compiles and registers whatever is stale or missing; the hook runs it at the
start of each session, so you rarely run it yourself.

A compiled skill's description is the artifact's summary as plain text (bold
markers dropped), and when the artifact names platforms they go under
`metadata.platforms`, which skill-router's `--platform` filters on.

**Roles.** A guideline or principle whose parts carry roles (`role` in
`artifact.json`) compiles to four skills instead of one, each the intro plus the parts of its
roles, in part order:

| Skill | Roles | Name |
|---|---|---|
| builder | `rules`, `how-to`, `examples` | `<use-case>-<tail>` (the name it has today) |
| build-verifier | `build-bar` | `verifying-build-<tail>` |
| reviewer | `rules`, `review-focus` | `reviewing-<tail>` |
| review-verifier | `review-bar` | `verifying-review-<tail>` |

Each routes under its own use case, with the artifact's own use case below it
(`coding/verifying-build/planning/data`; a principle's `coding/verifying-build/principles`), so
no route node gathers one kind from every use case. Each carries
`metadata.skill: <kind>`; the receipt records its `kind`. The builder keeps the
artifact's description; the other three say what they are for ("Review code
against this guideline: ..."). `rationale` and `references` parts go to each
skill's `references/`. Only the builder shows the Reference Implementations. A
verifier ends its bar with the line it grades by. The templates are
`<type>.<kind>.md`. A roled guideline may live under any use case but
`guidelines/reviewing/` (folded, never roled); a principle `principles/t`
keeps its type segment: `principle-t`, `reviewing-principle-t`,
`verifying-build-principle-t` and `verifying-review-principle-t`. An ingredient or
recipe is never roled. One `cookr validate` faults (a missing role, an unnamed
rule, a `hosts/` directory, its own `routes`, a skill name another artifact
also derives) is refused. Its skills
get no variants, and `payload` does not offer it for tuning. An artifact with
no role compiles as before.

**Research.** An artifact's research lives in its folder's `research/`
(`research.json`, the research-results document, and `research.md`, under the
four question headings `## Best practices`, `## Known solutions`,
`## Platform guidelines` and `## The expert's view`, in that order). Nothing
compiles, walks or reads `research/` as a spec. `cookr validate`'s Research
section makes a cookbook with a `research-exempt.json` research-first: every
artifact in it needs `research/`, except the topics that file lists as owed
research. A cookbook without the file checks every roled artifact and every
artifact that has a `research/` folder, and leaves the rest alone. It refuses
an artifact that needs research and has no `research/`, a claim missing a field of
its record, a rule that cites no claim or an unknown one, a citation that
does not end its rule, and a cited claim no verdict names. A rule cites claims
once, at the end of its named bullet, as `(claim: <id>)` or
`(claims: <id>, <id>)`; the skill compile leaves the citation out, and
`roles lossless` reads a rule without it. `research` is a reserved spec name,
like `hosts` and `versions`. `research-exempt.json` (`{"why", "topics": [paths below the cookbook
dir]}`) is emptied as research lands. A listed topic that has its
`research/`, that is no artifact, or that is listed twice, is refused by name. Every verdict names a claim. A rule the research cannot support is recorded as a claim itself, its source the cookbook's own text at the topic's base commit, with an `unsupported` verdict (`contradicted` when the research finds against it) naming that claim; a rule kept for the owner cites it, and `cookr validate` passes it with an `owner-decides` warning naming the rule and the claim. Only a rule citing such a prior-cookbook-text claim is warned of; a rule citing a research claim that shares the verdict is not the owner's.
`cookr validate --research <folder>` checks that folder's research alone,
without its rules' citations, as research ends; a path that is no artifact
source folder (a typo) exits 2 naming it, never `no-research`.
`/grow-cookbook` in the agenticcookbook repo is the procedure that writes the
research.

**Converting a topic to roles.** Six commands, each printing JSON (`roles gaps` with `--json`):

- `cookr roles set <folder> --part <name>=<role>... [--twin-differs TEXT]` gives the
  named parts roles (`<name>=none` clears one) and prints the parts with the
  census findings left. A part the folder lacks, a role not in the list, or a
  role on the intro or history is refused and nothing is written.
- `cookr roles check <folder>` runs the census (name collisions judged against
  the whole cookbook) and, when it is clean, composes the four skills: their
  names, sizes and the rule count. Exit 1 on any finding.
- `cookr roles lossless <folder> --base <rev> [--copy <folder>]... [--draft]`
  lists every sentence the folder (and each copy folded into it, at its
  `--base` path) had at `<rev>` that is no whole sentence of its parts now
  (`~~struck~~` text and `<!-- comments -->` removed, across lines). A
  sentence is a line split after `.`, `!` or `?` before a capital, a backtick
  or `*`, list markers and whitespace normalized; one moved between parts still
  counts, and so does one that now follows a rule's or a rationale bullet's
  label. A markdown-only line of the base — a thematic break (`---`) or a
  heading that only restates the title — is not read. Every other one is
  accounted for in the folder's `lossless.json`,
  `{"base": "<rev>", "copies": ["<copy folded in, its path at rev>"], "moved":
  [{"sentence": "<base text verbatim>", "to": "<target>" | [targets],
  "judged": {"by", "verdict": "pass" | "fail", "note", "pin"},
  "retargeted": {"from", "to", "judged", "seal"}}], "obsolete":
  [{"sentence", "reason", "judged"}], "retargets": ["<sentence>"]}` (named
  copies are read as `--copy`; `judged`, `retargeted` and `retargets` are
  optional, the last two written only by `--retarget`; a sentence named twice
  is refused). A topic moved since the base (`git mv`, then `cookr rename` for
  its rdid) names its old path in `"renamed_from": "<its path at rev>"`, which
  is read as its own base; that path must be gone and carry the topic's
  artifact id, and a same-named folder renamed away, not folded, is no twin to
  list. The gate does not
  prove meaning: it is an accounting, tripwires, and a judge's recorded,
  pinned verdict.
  A target is a rule, or a non-rule part judged by its one item or line
  (code lines included) that holds most of the sentence. A moved sentence
  passes when its targets (at most 3) exist, together hold at least 80% of its
  content words (function words dropped, light suffixes stemmed), each holds at
  least one, and the tripwires hold: the targets are split into clauses (lines,
  sentences, `;`, `:`, an em dash or a spaced en dash, a parenthesis, a comma,
  ` or `, ` while `; struck-through text dropped; a clause of only RFC
  keywords and negations, such as "Never", joined to its neighbour), and each
  clause of the
  sentence is matched to the one target clause that holds most of it, which
  must keep its negations (as many; `without` never stands in for `never`),
  every RFC 2119 level it states (`required` counts as MUST; MAY and OPTIONAL
  only in capitals), every number (number words such as "three", "twice",
  "half" count; unit spellings are unified) and every meaning word (avoid,
  only, at least, at most, before, after, until, unless, except, without,
  instead, prefer, minimum, maximum, more than, less than, fewer than). A
  parenthetical gloss holding no meaning word of its own is read with the
  before, after or until that opens the clause it glosses ("After applying
  server records (step 5 of the sync cycle)" keeps "after step 5"), and
  nothing else. A rule's name lends a moved sentence nothing (a
  bare lead-in aside): it is judged on its text. A bare lead-in (ends in `:`, at most 8 content words, no
  RFC keyword, no negation) maps to the rules it introduced, marked
  `"lead_in": true`, when those rules, their names (split at the hyphens:
  "Access methods:" is held by `platform-access-methods`) and their rationale
  bullets hold its own words (generic ones such as "rules", "following",
  "three" left out) and its numbers. A framing lead-in (ends in `:`, an RFC level, a word such as
  "follow", "rules" or "these") maps to rules that all carry that level,
  marked `"framing": true`, when they hold every one of its other words
  ("migration", say), one rule holding them all, and its numbers. A lead-in
  may name every rule it introduced.
  A moved sentence is verbatim, marked `"verbatim": true` and needing no
  judge, only when it equals one whole sentence of a target once both are
  normalised (list markers, paired emphasis markers around words and code
  span backticks dropped, whitespace collapsed outside code, `~~struck~~` text
  and comments removed; the text of a code span, and a `_` or `*` inside a
  word, is kept as written); one inside a longer sentence, or only in struck
  text, is reworded. Every reworded entry (lead-ins included) and every
  `obsolete` entry needs a judged pass whose `pin` matches; a `judged` fail
  always fails. A moved entry whose judged fail named content carried by a
  rule or part outside its `to` may be retargeted once, by `--retarget`
  (below), and a fresh judge rules on the new targets. A second retarget fails
  the entry by name, "a second retarget is refused": a `retargeted` record
  whose `seal` does not match (one written by hand), a `to` other than the
  record's `to`, or a sentence in `retargets` with no record. Otherwise a
  retargeted entry is judged like any other: a fail whose pin matches fails it,
  marked "after its one retarget"; once the targets' text is rewritten that
  fail is stale and the entry is re-judged; a pass clears it. A retargeted
  entry prints `"retargeted": true`; an obsolete entry never has a record. The pin is the sha256 of the JSON `[sentence, sorted to-list,
  the normalised full text of each target]` for a moved entry and `[sentence,
  the copy it came from, reason, the normalised full text of the topic]` for
  an obsolete one, so a verdict whose sentence, targets, target text, topic
  text or reason has changed, or that has no pin, is `stale`: it counts as
  unjudged, and stderr names it. The judge writes the pin with its verdict;
  nothing stamps one. `--draft` passes unjudged and stale
  entries (the JSON says `"draft": true` and stderr says DRAFT);
  `--require-judged`, the default, is accepted and ignored.
  An `obsolete` entry, printed on stderr, is for a folded copy's sentence that
  only pointed at the topic; a sentence of the topic's own base, or one stating
  an RFC keyword, a negation or a meaning word, is refused. Every copy folded
  since `--base` is read: a "Fold <path> into this topic" Change History row
  added since `--base`, and an artifact folder at `--base` with the topic's
  folder name that is gone now, must each be in `copies` or `--copy`, and a
  listed copy that still exists fails. Prints `{checked, draft, missing,
  failures, obsolete, moved, unused, counts}`, `counts` being `verbatim`,
  `reworded_judged`, `reworded_unjudged`, `judged_fail`, `stale`,
  `obsolete_judged` and `obsolete_unjudged` (also on stderr); exit 1 on any
  missing sentence, failed account or unused entry (each printed on stderr),
  or when the file's base is another commit than `--base`. The file never
  reaches a compiled doc or skill.
- `cookr roles lossless --pin-for <folder> --entry <n>` prints `{folder, entry,
  kind, sentence, pin}` for entry `n` (from 1: `moved` in order, then
  `obsolete`) of the folder's `lossless.json`, the pin its judge writes beside
  the verdict. It writes nothing; an entry that does not exist, or whose target
  or copy is gone, is refused.
- `cookr roles lossless --retarget <folder> --entry <n> --to <name>
  [--to <name>]...` retargets moved entry `n` once: its `to` and its judged
  fail move into `"retargeted": {"from", "to", "judged", "seal"}` (`seal` the
  sha256 of the sentence, `from`, `to` and the fail), `to` becomes the new
  targets, `judged` goes, and the sentence joins the file's `retargets`
  ledger. Prints `{folder, entry, sentence, from, to}`. It refuses, writing
  nothing, an obsolete or missing entry, an entry already retargeted or in the
  ledger (a second retarget), one with no judged fail whose pin matches its
  targets now, and new targets that do not exist, number more than 3, equal
  the old ones, or fail the 80% bar or a tripwire (the check `--draft` runs),
  so a bad target never spends the one retarget. The seal is taken over
  canonical JSON (sorted keys, fixed separators): re-serialising the file
  keeps it. `from` is therefore the targets the fail was pinned on.
- `cookr fold <copy> --into <topic> [--author A] [--date D]` appends each part of
  the unroled copy holding a sentence the topic lacks as a new unroled part (the
  census then names it until it gets a role), records the fold in the topic's
  Change History as `cookr bump` would, redirects every link to it across the
  cookbook to the topic (the topic's own links to it become plain text), then
  deletes the copy. A cookbook folder that cannot be read stops it before
  anything is written. Prints
  `{"redirected": [paths], "parts_added": [names], "identical": bool}`. A roled
  copy is refused. Approve the topic afterwards with `/approve-artifact`.
- `cookr roles worklist --map <file> --batches <file> --new-rows <file>
  [--cookbook <dir>] [--json] [--out <file>]` lists every guideline topic (a
  distinct folder name) to convert: its survivor (`implementing/`, then
  `planning/`, `testing/`, `shipping/`, the other use cases, `reviewing/` last;
  a topic held only under `reviewing/<area>/` gets `new_home`
  `implementing/<area>/`), its copies to fold, each flagged `identical` when its
  line similarity to the survivor's twin text is at least 0.9 (`exact` when
  byte-equal) and `fold_check` when below 0.2 or listed in `--batches`, the
  specialities standing on it with their case, or `authored` when none does,
  and `roled`. cookr inventories the cookbook; the rest is the caller's, in
  three JSON files. `--map`: `{"specialities": [all], "assignments":
  [{"speciality", "case", "specialists", "topic"}], "covers": [{"speciality",
  "specialist", "via"}]}` (a cover makes a building row: the speciality builds
  whatever `via` stands on). `--batches`: `{"labels": {key: name}, "areas":
  {area: key}, "default": key, "overrides": {path: {"batch", "new_home"}},
  "fold_check": [copy]}`. `--new-rows`: `{"rows": [{"path", "kind",
  "specialities", "owner_decision", "note"}]}`, topics still to write; a
  speciality a new row claims is listed there alone. Every declared speciality
  must stand on a topic or a new row and every topic named must exist; a
  missing or malformed file, or any offender, is an error that names them.
  Without `--json` it prints the counts.
- `cookr roles gaps <folder> --against <file> [--against <file>]... [--json]`
  measures each reference file against the topic's own text (every `*.md`
  in `<folder>`, never `research/`). A reference file is plain text the
  caller extracts; cookr knows no team. Each sentence of 6 words or more
  (fenced code dropped; split after `. ! ? ; :`, at a blank line, before a
  list item and around a heading or a table row; a wrapped line within a paragraph joins
  the next, never ending a sentence) is held when
  its normalised form (lowercase, every run of non `[a-z0-9]` one space) is a
  substring of the topic's, or 80% of its words are among the topic's words;
  otherwise the topic lacks it. Prints, per file, its sentence, held and
  lacking counts and each lacking sentence in its original wording; `--json`
  prints `{"folder", "references": [{"file", "sentences", "held", "lacking",
  "lacking_sentences"}]}`. Exit 0; 2 when `<folder>` is no artifact source
  folder or a file cannot be read.

A recompile prunes only what the receipt lists. `--check` exits 1 when anything
is stale or missing. The set fails on a duplicate name, a rendering a host would
refuse, or a route level over 50 entries.

skill-router (0.4.0 or later) registers one skill at a time:
`skill-router register <set-dir>/<skill> --new-keyword`, for each skill of the set.
`cookr install` does this for you, and unregisters the set's skills that are no
longer in it. It passes `--new-keyword` because a set's
keywords are its library's directory names, so a near-duplicate such as
`service` beside `services` is accepted and listed in the `routed:` detail
rather than refused.

## Install

`cookr install [paths] [--target T]... [--library L] [--adopt] [--force] [--replace] [--dry-run] [--check] [--json]`
puts a compiled cookbook where agents reach it. There are three items:
- **`set:<library>`**: the routed skills, compiled into `$COOKR_HOME/sets/<library>`
  (`$COOKR_HOME` defaults to `~/.cookr`).
- **`routed:<library>`**: that set's skills, each registered with skill-router through
  `skill-router`, or the command in `$COOKR_SKILL_ROUTER`. The set is the registered
  skills whose origin is a dir of `$COOKR_HOME/sets/<library>`.
- **`always-on:<host>:<name>`**: the principles skill, rendered for one target into
  the host's skills dir. It is `general-principles` for this cookbook and
  `<library>-principles` for a library. It lists every principle with its gist
  and routed skill, then the pipeline concerns from `workflows/pipeline-concerns.json`
  (`--concerns` overrides that path).

`--target` is `routed`, or a host target: `claude` (its default model), a
family such as `claude.opus`, or a model such as `claude.opus-5-5`. You may give
one target per host. With no `--target`, cookr installs the routed set and the
always-on skill for every host whose home directory exists.

Each item is OK, MISSING, DRIFT or BROKEN. `--check` changes nothing and exits 1
unless everything is OK. Install is idempotent.

A skill dir that cookr did not install is BROKEN and is left alone. `--adopt`
moves it to `$COOKR_HOME/backup/`, and uninstall puts it back. If you edit the
always-on file after install, it is DRIFT, and install will not overwrite it
unless you pass `--force`. A library already installed from other paths is
refused; `--replace` installs it over them, replacing every skill it installed.

`$COOKR_HOME/install.json` is the receipt. `cookr uninstall [--target T]
[--library L | --every-library] [--force] [--dry-run]` removes only what the
receipt lists, for `--library`'s library (default `cookbook`) or, with
`--every-library`, every library it lists. It unregisters the routed set,
deletes the set, removes the always-on skill (restoring any adopted original)
and removes any dirs install created. An edited always-on file stays unless you
pass `--force`.

Never adopt or replace the user's live `general-principles` without their OK.

## Extraction workflow

1. `cookr prompt extract --tier <group> --out-dir <scratch dir> --json` — the
   worklist. It writes one brief per spec that still needs a writer and prints
   `repo_root`, `cookbook_dir`, `write` (one entry per brief: `name`,
   `recipe_file`, `reference_implementations`, `existing`, `brief`)
   and `awaiting_review`. Use a scratch directory outside the repo, e.g.
   `$TMPDIR/cookr-briefs/<group>`.
2. For each `write` entry, dispatch a subagent pinned to `claude-sonnet-4-6`
   whose whole prompt is: ``Read `<brief>` in full and do exactly what it says.``
   Never paste the brief into the prompt. For a composite, first rebuild its
   brief with `cookr prompt extract <name> --type recipe --out-dir <scratch dir>`.
   Run up to 8 subagents at a time.
3. `cookr update -p <cookbook_dir> --author "<user>"` — fills empty
   frontmatter. A writer that rewrote an existing recipe (`existing: true`)
   has already recorded it with `cookr bump`, as its brief says; never bump
   it again, and never hand-edit `version`, `modified` or Change History.
4. `cookr validate -p <cookbook_dir>` and `cookr coverage --tier <group>`.
   Run `cookr implements` for the recipe's code, then `cookr status`.
5. Rerun step 1. Every recipe still in `write` goes back to step 2; its brief
   now includes the existing recipe, so the subagent completes rather than
   restarts. Stop when `write` is empty.
6. Verify pass (below) on every recipe written in the batch.
7. `cookr lint -p <cookbook_dir> --since main` before committing.

`awaiting_review` lists recipes whose only problem is a `NEEDS REVIEW`
marker: finished work waiting on a reviewer's decision, never a rewrite target.
Report how many there are; don't walk the user through them. Each one is
settled when its recipe is next used to build something (*Building from a
recipe*, above). The phase is done when `write` is empty and validate passes.
`cookr coverage --require complete` stays red until the last marker is
settled.

## Verify pass

Writers assert behavior the source does not have — a MUST claiming validation
the code never does, "may be null" where the type forbids it, a branch that
does not exist, a helper called "not in source" when it is imported from a real
path — and Platform Notes repeat the same errors. After each batch, dispatch one
subagent per new recipe, pinned to `claude-sonnet-4-6`, with this brief:

- Read every source file in full, and every imported helper the recipe
  describes (search the repo for it).
- Check each Behavioral Requirement, test vector, edge case, configuration row,
  Platform Notes claim and Design Decision against source; fix inaccuracies in
  place with minimal edits. Keep the section order and the `- **name**:` form.
- Re-read every kept `NEEDS REVIEW` marker against the marker rules in
  `<brief>` (the writer's brief from the worklist: its preamble's
  `NEEDS REVIEW` bullets and, for a non-UI component, its
  `## non-UI component` section). Restate as fact every marker those rules do
  not allow; keep every one they call a genuine gap.
- Do not commit and do not touch any other file. Reply
  `<name> fixed N claims, markers M`.

Then check the kept markers yourself against those same rules in the brief
before accepting them: a verify agent is still a writer. The brief is the only
statement of the marker rules; never judge markers by a shorter list of your
own.

## Interpreting coverage

Rows are keyed by spec name. The `problems` column names exactly what keeps a
spec at `partial`. Quote it to the subagent; do not re-derive it. Every graded
rule (the Compliance checks every component cites, the minimum test vectors,
the Design Decision lines, frontmatter `platforms`, the
implementations in the index) is stated once, in the writer rules of
`modules/prompt/prompts/extract/module.md`, which every brief carries as its
preamble; point at the brief, never restate the rules.

A spec listed under "specs with no source file" is not an error: it is a
vocabulary or composite spec with no source of its own.

Implementation problems:

- An implementation naming a missing path: the code moved or was deleted. After
  a move, run `cookr relink`; otherwise `cookr implements <id> --remove <location>`.
- A path claimed by another spec too: two specs record the same path. Keep it
  in one (`cookr implements --remove` on the other).
- An unclaimed file shows up as its own row, named by where it sits. To fold
  it into an existing spec, `cookr implements <id> <path>` (or its directory,
  with a trailing `/`); a file row beats a directory row, and the deepest
  directory wins.
- A name collision across roots: two unclaimed files from different roots
  land on one name. Claim each in a spec, or ignore one.

## Arrangement

`cookr arrangement` reports each spec as `aligned` (it sits in, or anywhere
below, the `recipes` group of the root its code is under), `drifted`,
`unplaced` (no implementations) or `outside` (a row under no root). A drifted spec either
moves into its group in the cookbook (move the spec's folder, `cookr relink`
and `cookr rename` it to match, then `cookr bump` it), or its root's `recipes` changes. Rearranging the code is the user's call: propose it,
never do it unasked.

## Non-UI code

Shared code with no visual surface — models, clients, engines — goes under a
root marked `"kind": "logic"` in `cookbook.json`'s `code.roots`. It uses the same `ingredient`
template; `prompt extract` adds the non-UI guidance (contract, errors,
concurrency, persistence; Appearance, States and Accessibility as one
`Not applicable` line each). Python sources use `"platform": "python"`. A directory that mixes view and
model files takes a root-scoped `"ignore"` list (`["**/*ViewController.swift"]`)
so the top-level `ignore` never drops files a UI root needs.

## Behavior notes

- Never edit files in `~/.local/bin/_cookr_pkg/`. Edit `skills/cookr/cli/` in agenticcookbook and re-run `skills/cookr/setup/install`.
- Never `pip install` from this skill.
- `cookbook/cookbook.json` holds the roots and ignores; `cookbook/index.json` holds what each spec implements. Never put either in the other, and never edit `index.json` by hand.
