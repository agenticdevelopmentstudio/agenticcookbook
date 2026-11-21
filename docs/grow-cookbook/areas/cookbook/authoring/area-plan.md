# cookbook/authoring: area plan

The cookbook's own rules for writing its artifacts: the structural checks
`/lint-artifact` and `/approve-artifact` evaluate each artifact type against,
the requirement keywords those checks rest on, and the `triggers` field that
selects guidelines by activity. Every topic but recipe-formatting is new to
`cookbook/guidelines/cookbook/authoring/`. The unpublished drafts named below
are inputs to check against research, never a source of rules. The owner has
ruled on every Owner question; each ruling is recorded where it applies and
quoted under **Owner questions**.

## Topics

| Topic | Path | Survivor | Copies | Specialities | Research type |
|---|---|---|---|---|---|
| requirement-keywords | `cookbook/guidelines/cookbook/authoring/requirement-keywords` (new, owner ruling Q10 + Q11; draft inputs: the RFC 2119 parts of `tbd/compliance/artifact-formatting/guideline-formatting.md` and the MUST/SHOULD levels of every formatting draft) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain technical writing; method practitioner and standards sources) |
| principle-formatting | `cookbook/guidelines/cookbook/authoring/principle-formatting` (new; draft input `tbd/compliance/artifact-formatting/principle-formatting.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain technical writing; method practitioner and standards sources) |
| guideline-formatting | `cookbook/guidelines/cookbook/authoring/guideline-formatting` (new; draft input `tbd/compliance/artifact-formatting/guideline-formatting.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain technical writing; method practitioner and standards sources) |
| ingredient-formatting | `cookbook/guidelines/cookbook/authoring/ingredient-formatting` (new; draft input `tbd/compliance/artifact-formatting/ingredient-formatting.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain technical writing; method practitioner and standards sources) |
| recipe-formatting | `cookbook/guidelines/cookbook/recipe-quality/template-conformance` (merged, owner ruling Q7; draft input `tbd/compliance/artifact-formatting/recipe-formatting.md`) | `cookbook/guidelines/cookbook/recipe-quality/template-conformance` | none | none | How-to / troubleshooting (intent Do; domain technical writing; method practitioner and standards sources) |
| cookbook-formatting | `cookbook/guidelines/cookbook/authoring/cookbook-formatting` (new; draft input `tbd/compliance/artifact-formatting/cookbook-formatting.md`) | itself (new) | none | none | Technology / software (intent Do; domain data-format validation; method specification and tool documentation) |
| activity-triggers | `cookbook/guidelines/cookbook/authoring/activity-triggers` (new; draft input `guide/introduction/trigger-guide.md`) | itself (new) | none | none | Technology / software (intent Decide; domain retrieval and agent context selection; method specification, tool documentation and published evaluations) |

No topic has a copy, so nothing folds in this area. `recipe-formatting` is
merged into an existing survivor in another area (owner ruling Q7); the
worklist row's survivor is now
`guidelines/cookbook/recipe-quality/template-conformance`, and the topic runs
under the `cookbook/recipe-quality` area plan, which does not exist yet.

`requirement-keywords` is new by owner ruling (Q10 + Q11): it joins the
RFC 2119 keyword case and the lint severity mapping into one topic, added to
the worklist as `new: true`, `kind: "new"`, `devteam: "authored"`. The
formatting topics cite it and never restate it.

`activity-triggers` keeps its name. The research questions below ask how
retrieval systems select context by the task in hand, and "activity" names
that selector (the 28 canonical triggers are activities such as writing tests
or editing UI); no clearer name came out of them, so its worklist row is
unchanged.

## Gaps

The area has no speciality: `run_gaps.py` reports `why_empty` "area has no
speciality", and `reference.json` is `[]`. No speciality text is measured, no
new topic claims a speciality, and the worklist's `building` list is empty, so
"Building specialities not yet measured" has nothing to list. The gaps of this
area are the **Missing subjects** below, judged by hand.

No R9 measure is owed or possible: every topic is `kind: new` and the area has
no reference. Candidate survivors were chosen from a whole-cookbook search
(G87): every artifact folder under `cookbook/` whose path names trigger,
context, routing, loading, format, template, lint, frontmatter, schema,
keyword, style, writing or document, plus the `cookbook/guidelines/cookbook/`
subfolders and every guideline part mentioning "trigger". The ones that cover
part of a proposed topic are listed under **Overlaps**.

The recipe section names across templates (the component list
`template-conformance` states against the recipe draft's composition list) are
left out of this area by owner ruling (Q9): they are settled in
`template-conformance` when the `cookbook/recipe-quality` area is planned.

## Missing subjects

1. **Principle brevity evidence**: the principle draft caps a principle at about 50 lines (pf-brevity) and cites nothing for the number; a practitioner expects the cap to rest on evidence about how long an always-loaded principle can be before agents or readers skip it.
2. **Ingredient section order rationale**: the ingredient draft fixes 21 sections in order, some MAY-omit, with no stated reason for the order or for which sections may be omitted.
3. **Trigger vocabulary governance**: the trigger guide fixes 28 canonical triggers but says nothing on how a trigger is added, renamed or retired, or how artifacts are migrated when the vocabulary changes.
4. **Trigger selection evaluation**: nothing measures whether trigger-filtered loading picks the guidelines a task needs, or what it misses.
5. **RFC 2119 keyword case**: the drafts require RFC 2119 keywords but not RFC 8174's clarification that only the uppercase forms carry the defined meaning.
6. **Keyword lint severity mapping**: the drafts mark checks MUST or SHOULD but never say how a rule's keyword sets a lint finding's severity (error, warning or suggestion), or which severities block `/approve-artifact`.

## Overlaps

`copy_check.py` finds no copy to fold in this area and one move: `moved` lists
recipe-formatting (`cookbook/guidelines/cookbook/authoring/recipe-formatting`, which
does not exist yet) with survivor
`cookbook/guidelines/cookbook/recipe-quality/template-conformance`, the merge the
owner approved (Q7). Nothing is folded and no link is retargeted, since no
`recipe-formatting` folder exists. The overlaps below are existing topics whose
rules cover part of a proposed topic, from the whole-cookbook search (see
**Gaps**). Under "one source per topic", a proposed topic whose ground is
already held by an artifact is `merged`, never `new`.

- **recipe-formatting** and `cookbook/guidelines/cookbook/recipe-quality/template-conformance`: the survivor already rules recipe frontmatter and structure: "The frontmatter MUST include all required fields: `id`, `title`, `type`, `version`, `status`, `language`, `created`, `modified`, `author`, and `summary`" (must-include-required-frontmatter-fields), "The recipe MUST contain all sections defined in the standard template, in the prescribed order" (must-contain-template-sections-in-order) and "The recipe MUST include a `## Change History` section as the final section" (must-end-with-change-history). The draft's rf-frontmatter, rf-* section and rf-change-history checks rule the same ground, and its section list differs from the survivor's. Ruled (Q7): `merged` into `template-conformance`, which is extended with the draft's checks the research supports; the section-list difference is settled there when the `cookbook/recipe-quality` area is planned (Q9).
- **recipe-formatting** and `cookbook/guidelines/cookbook/recipe-quality/cookbook-compliance`: the survivor rules what a recipe must cite and not contradict ("A recipe's behavioral requirements MUST NOT contradict any applicable cookbook guideline", must-not-contradict-applicable-guidelines; "the recipe SHOULD cite the guideline in the `depends-on` or `references` frontmatter field", should-cite-applicable-guidelines-in-frontmatter). The draft's rf-compliance check (a `## Compliance` section) touches the same ground from the structural side. Partial overlap: content compliance stays in `cookbook-compliance`; only the section's presence belongs to the merged `template-conformance`.
- **ingredient-formatting** and `cookbook/guidelines/cookbook/recipe-quality/template-conformance`: the survivor's component-recipe section list (Overview, Behavioral Requirements, Appearance, States, Accessibility, Conformance Test Vectors, Edge Cases) is an earlier form of the ingredient template's opening sections, and its frontmatter rules apply to every artifact type. Ruled (Q8): the component-recipe section list moves from `template-conformance` to ingredient-formatting, which researches and rules it with the ingredient template's other sections; `template-conformance` keeps the recipe's own list.
- **principle-formatting** and **guideline-formatting** and `guide/introduction/conventions.md` (*The Standard*, *Roles*, *Research*, *Named Requirements*, *RFC 2119 Keywords*): the guide states "A guideline or a principle gives each part a role", "Each rule is a bullet of a `rules` part, `- **kebab-name**: … MUST|SHOULD|MAY …`" and the `research/` shape the guideline draft's gf-roled-parts, gf-named-rules, gf-research-folder and gf-rule-cites-research checks restate. The guide is not an artifact, so it is no survivor; the new topics must agree with it. Ruled (Q12): where research on principle-formatting or guideline-formatting finds against `conventions.md`, `conventions.md` changes to match the research.
- **requirement-keywords** and `guide/introduction/conventions.md` (*RFC 2119 Keywords*) and `.claude/rules/artifact-formatting.md` ("Use RFC 2119 keywords for requirements — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY"): both state the keywords and neither states their case or a lint severity. No artifact survivor; requirement-keywords is new (Q10 + Q11), and every formatting topic cites it rather than restating it.
- **guideline-formatting** and **principle-formatting** and `skills/cookr/SKILL.md` (*Source folders*) with `cookr validate`: cookr already enforces the source-folder form ("`convert` ... reports type-shape problems (missing or out-of-order sections)", "`cookr validate` lists what is wrong" for roles). The formatting topics state the rules; the tool enforces part of them. No artifact survivor; the topics cite the tool's checks rather than restate them.
- **guideline-formatting** and `cookbook/guidelines/cookbook/skills-and-agents/skill-checklist` and `.../agent-checklist`: "The description SHOULD use natural trigger keywords" (should-use-natural-trigger-keywords) rules a skill's description, not an artifact's `triggers` field. No shared ground beyond the word; listed so the owner sees it was checked.
- **activity-triggers** and `cookbook/guidelines/implementing/skills-and-agents/context-and-memory-management`: the survivor rules context loading in general ("should-retrieve-context-just-in-time", "must-not-front-load-context"). `activity-triggers` rules the cookbook's own selector for which guidelines load for an activity. Partial overlap: kept `new`, citing the survivor for the general rule.
- **cookbook-formatting** and `references/cookbook.schema.json`: the draft's cf-schema-valid check defers to this schema. The schema is a reference file, not an artifact; no survivor.
- `cookbook/guidelines/implementing/code-quality/linting` and `.../yaml-frontmatter` were checked: they rule project linting and a parser choice, not the cookbook's artifact structure. No overlap.

copy_check.py cookbook/authoring: copies 0; identical 0; moved 1; unreadable 0; twin_differs 0; differ_uncarried none; result b4fcb364e515

## Proposed topics

| Topic | Action | Artifact | Why |
|---|---|---|---|
| requirement-keywords | new | `cookbook/guidelines/cookbook/authoring/requirement-keywords` | Owner ruling Q10 + Q11: keyword case and the keyword-to-severity mapping in one topic the formatting topics cite; run first so they can. |
| principle-formatting | new | `cookbook/guidelines/cookbook/authoring/principle-formatting` | No artifact rules a principle's structure; the draft's 7 checks are input to research. |
| guideline-formatting | new | `cookbook/guidelines/cookbook/authoring/guideline-formatting` | No artifact rules a guideline's structure; `conventions.md` states the standard but is no artifact. |
| ingredient-formatting | new | `cookbook/guidelines/cookbook/authoring/ingredient-formatting` | No artifact rules the ingredient template's 21 sections; `template-conformance`'s component list moves here (owner ruling Q8). |
| recipe-formatting | merged | `cookbook/guidelines/cookbook/recipe-quality/template-conformance` | `template-conformance` already rules recipe frontmatter, section order and Change History; one source per topic (owner ruling Q7). |
| cookbook-formatting | new | `cookbook/guidelines/cookbook/authoring/cookbook-formatting` | No artifact rules the `cookbook.json` manifest; the schema is a reference file. |
| activity-triggers | new | `cookbook/guidelines/cookbook/authoring/activity-triggers` | No artifact rules the `triggers` field or its vocabulary; `context-and-memory-management` covers loading in general only. |

## Research questions

Every formatting topic (principle-, guideline-, ingredient-, cookbook- and the
merged recipe-formatting) cites requirement-keywords for keyword case and for
the severity a rule's keyword gives a lint finding, and never restates either
(owner ruling Q10 + Q11).

### requirement-keywords (new)

1. Best practice: how do standards bodies and style guides use normative keywords: which words, in which case, one keyword per requirement, and how is a requirement with no keyword read?
2. Known solutions: how do Vale (its error, warning and suggestion levels), markdownlint, ESLint and other linters derive a finding's severity, and how does a spec linter tie a rule's MUST, SHOULD or MAY to that severity and to blocking a merge or an approval?
3. Platform guidelines: what do RFC 2119 and RFC 8174 (BCP 14) say about keyword case and the boilerplate that invokes them, and what do the IETF's and W3C's conformance conventions add on how conformance is reported?
4. The expert's view: what do standards editors and linter maintainers say about lowercase keywords in normative text, and about mapping requirement levels to lint severities?
5. **RFC 2119 keyword case**: find what RFC 8174 and standards practice say about uppercase-only meaning, and state whether only the uppercase keywords carry normative meaning in a cookbook rule and whether a lowercase "must" in rule text is flagged.
6. **Keyword lint severity mapping**: find how linters and spec checkers set a finding's severity from a requirement level, and state the severity each keyword gives a failed check (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) and which severities block `/approve-artifact`.

### principle-formatting (new)

1. Best practice: what structure do style guides and docs-as-code practice give a short, always-loaded statement of principle (frontmatter, title, one-sentence statement, actionable guidance, change history), and how short should it be?
2. Known solutions: how do markdownlint, Vale and front-matter schema checks (JSON Schema over YAML) verify the required fields, heading and length of a short document, and which of the draft's 7 checks can a tool decide and which need a reviewer (the severity of each follows requirement-keywords)?
3. Platform guidelines: what do the Diátaxis framework, the Google developer documentation style guide and the Microsoft Writing Style Guide say about a principle-like "explanation" page, and what do Anthropic's and other agent hosts' guidance say about the length of always-loaded context?
4. The expert's view: what do documentation and agent-context practitioners say about the cost of long always-loaded instructions, and where does a length cap help or hurt?
5. **Principle brevity evidence**: find the evidence for a line or token cap on an always-loaded principle (agent instruction-following studies, host guidance on memory files), state the cap the evidence supports, or record that the about-50-lines cap is unsupported.
6. Where this research finds against `guide/introduction/conventions.md` (*The Standard*, *Roles*), record each finding with its claims: `conventions.md` changes to match the research (owner ruling Q12).

### guideline-formatting (new)

1. Best practice: how do style guides and docs-as-code practice structure a rule-bearing document: named rules, roled sections (rules, how-to, examples, review focus, bars, rationale, references) and a compliance section?
2. Known solutions: how do Vale, markdownlint and schema-validated docs check a guideline's frontmatter, heading, named-rule bullets and research folder shape, and which of the draft's 13 checks can a tool decide (the keyword and severity checks are cited from requirement-keywords)?
3. Platform guidelines: what do the IETF's and W3C's conventions for writing a specification, and Diátaxis's split of reference, how-to and explanation, say about structuring a document of normative rules?
4. The expert's view: what do standards editors and docs-as-code practitioners say about one rule per bullet, citing evidence per rule, and the failure modes of normative prose?
5. Where this research finds against `guide/introduction/conventions.md` (*The Standard*, *Roles*, *Research*, *Named Requirements*), record each finding with its claims: `conventions.md` changes to match the research (owner ruling Q12).

### ingredient-formatting (new)

1. Best practice: how do component specification templates (design-system component pages, interface specs) order their sections, and which sections may be omitted for a component without UI?
2. Known solutions: how do JSON Schema, markdownlint's required-headings rule and Vale check a long fixed section order with optional sections, and which of the draft's 17 checks can a tool decide?
3. Platform guidelines: what do published design-system documentation guides (Material, Apple Human Interface Guidelines, Fluent) and W3C's specification conventions require of a component specification's sections?
4. The expert's view: what do specification authors say about long mandatory templates, empty sections and "not applicable" markers?
5. **Ingredient section order rationale**: for each of the 21 sections, find the reason its place and its MAY-omit status rest on, and state the order and the optional set the research supports.
6. `template-conformance`'s component-recipe section list (Overview, Behavioral Requirements, Appearance, States, Accessibility, Conformance Test Vectors, Edge Cases) moves here (owner ruling Q8): research it with the ingredient template's sections, state how the two lists reconcile, and record that `template-conformance` drops the list when it is next written.

### recipe-formatting (merged into template-conformance)

The topic is a record here: it is researched, written and reviewed under the
plan of `cookbook/guidelines/cookbook/recipe-quality`, where these questions
are carried into `template-conformance`'s.

1. Best practice: how do integration or composition specifications (feature specs that assemble components) structure ingredients, integration requirements, layout, shared state and integration test vectors?
2. Known solutions: how do schema-validated docs and markdownlint check a recipe's `ingredients` frontmatter, its fixed section order and its Change History, and which of the draft's rf-* checks does `template-conformance` already decide?
3. Platform guidelines: what do docs-as-code and specification-template conventions (Diátaxis how-to and reference) say about a composition document's sections?
4. The expert's view: what do specification authors say about a second template for compositions beside the component template?

### cookbook-formatting (new)

1. Best practice: how should a manifest that assembles components into an application be validated: required fields, identifiers, semantic versions, relative paths, dependency graphs without cycles?
2. Known solutions: how do JSON Schema validators (draft 2020-12, ajv, python-jsonschema) and manifest linters (package.json, Cargo.toml, npm and Cargo's own checks) validate a manifest's schema, UUIDs, semver fields, paths and cycles, and which of the draft's 13 checks belong in `references/cookbook.schema.json` rather than in prose?
3. Platform guidelines: what do the JSON Schema specification, RFC 9562 (UUIDs), Semantic Versioning 2.0.0 and RFC 3986 (URI references) require of the fields the manifest holds?
4. The expert's view: what do schema authors say about keeping a manifest's rules in its schema versus in a written guideline, and how the two stay in step?

### activity-triggers (new)

1. Best practice: how should a set of rules be selected for the task in hand: tag-based filtering, a controlled vocabulary of activities, and checkpoint loading (always, on activity, pre-commit, pre-PR)?
2. Known solutions: how do retrieval and agent systems select context by task (Claude Code skills' descriptions and path rules, Cursor rules' globs and descriptions, retrieval-augmented generation with metadata filters), and how does each compare with the trigger guide's 28 canonical triggers and its 1–5 triggers per guideline?
3. Platform guidelines: what do Anthropic's, OpenAI's and other agent hosts' published guidance say about loading instructions conditionally, and what do controlled-vocabulary standards (ISO 25964, SKOS) say about a small fixed vocabulary?
4. The expert's view: what do retrieval and agent-context practitioners say about the precision and recall of tag-filtered loading, and about missing a rule because its tag did not match?
5. **Trigger vocabulary governance**: find how controlled vocabularies are extended, renamed and retired (ISO 25964, SKOS, taxonomy governance practice), and state the procedure for adding, renaming or retiring a trigger and migrating the artifacts that carry it.
6. **Trigger selection evaluation**: find how retrieval systems measure context selection (precision, recall, labelled task sets), and state how the cookbook checks that trigger-filtered loading picks the guidelines a task needs; each metric claim takes the *Statistical* bar.

## Owner questions

Every question is answered; each ruling is quoted as the owner gave it.

1. Research bar for principle-formatting. Answered: "no escalation for any topic. Each keeps its proposed bar." It stays at the *How-to / troubleshooting* bar.
2. Research bar for guideline-formatting. Answered: "no escalation for any topic. Each keeps its proposed bar." It stays at the *How-to / troubleshooting* bar.
3. Research bar for ingredient-formatting. Answered: "no escalation for any topic. Each keeps its proposed bar." It stays at the *How-to / troubleshooting* bar.
4. Research bar for recipe-formatting. Answered: "no escalation for any topic. Each keeps its proposed bar." With the merge standing (Q7), the survivor `template-conformance`'s bar governs; none is owed here.
5. Research bar for cookbook-formatting. Answered: "no escalation for any topic. Each keeps its proposed bar." It stays at the *Technology / software* bar.
6. Research bar for activity-triggers. Answered: "no escalation for any topic. Each keeps its proposed bar. Any metric claim in activity-triggers takes the Statistical bar, as the plan already says." It stays at the *Technology / software* bar (activity-triggers question 6).
7. Merge of recipe-formatting into `cookbook/guidelines/cookbook/recipe-quality/template-conformance`. Answered: "the merge into `cookbook/guidelines/cookbook/recipe-quality/template-conformance` stands. Move the worklist row's survivor to `guidelines/cookbook/recipe-quality/template-conformance`." Done in the worklist, **Topics**, **Overlaps** and **Proposed topics**.
8. Whether `template-conformance`'s component-recipe section list moves to ingredient-formatting. Answered: "`template-conformance`'s component-recipe section list moves to ingredient-formatting. Record that in Overlaps and in ingredient-formatting's research questions." Recorded in **Overlaps** (third row) and ingredient-formatting question 6.
9. Recipe section names across templates. Answered: "recipe section names across templates are settled in `template-conformance` when the recipe-quality area is planned. Record that and leave the subject out of this area." Recorded under **Gaps** and **Overlaps** (first row); the subject is no longer a Missing subject of this area.
10. RFC 2119 keyword case and the lint severity mapping. Answered: "RFC 2119 keyword case and the lint severity mapping become ONE new topic, `requirement-keywords`." Its artifact is `cookbook/guidelines/cookbook/authoring/requirement-keywords`, added to the worklist as `new: true`, `kind: "new"`, `devteam: "authored"`, with its own research questions; "The formatting topics cite it, never restate it." Both subjects left *No host* and are hosted by requirement-keywords (questions 5 and 6); the *No host* list is now empty and removed.
11. Lint severity mapping. Answered with question 10: it is the Keyword lint severity mapping subject of requirement-keywords (question 6).
12. Where research on principle-formatting or guideline-formatting finds against `guide/introduction/conventions.md`, which one changes. Answered: "if research on principle-formatting or guideline-formatting finds against `guide/introduction/conventions.md`, `conventions.md` changes to match the research." Recorded in **Overlaps** (fourth row), principle-formatting question 6 and guideline-formatting question 5.
13. Research bar for requirement-keywords. Answered: "Its bar is How-to / troubleshooting with no escalation. The owner kept every bar where proposed, so record that as the ruling." It stays at the *How-to / troubleshooting* bar.

## Step-4 re-check

### On 1.4.46

Short path: the area has no speciality (`why_empty` "area has no
speciality"), so re-run checklist items 4 to 6 are skipped and item 5 owes no
R9. `held_by_wording`, `modal_differs`, `stale_verdicts` and
`non_home_lacking` are each `[]`.

First check (`stage_status.py --first-check`, `A/first-check.txt`), run on the
saved reports after the plan was first written:

- unmeasured.py cookbook/authoring: check unchanged; changes 0; new_keys 0; stale_reference 0; result a7c23a7e7fca
- run_gaps.py --check cookbook/authoring: changed, exit 1; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 2; gap_total_rows 0; measured_total 0; missing_subjects 7; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report 7205fa20e7858928b27393cbde8e9b043d10ba30
- stage_status.py cookbook/authoring: next approve; plan_sections 0; stale_reference 0; r9_stale 0; stale_copy_check 0; host_check 0; cite_moved 0; stale_verdicts 0; result 0785eeb62840

First check's `new_keys` 0, `changes` 2, `cleared` 0. The two changes are
this plan's own: `measured_elsewhere` gained recipe-formatting (merged into
`cookbook/guidelines/cookbook/recipe-quality/template-conformance`, plan
`cookbook/recipe-quality`, which does not exist yet; Owner questions 7), and
`missing_subjects` went from 0 to 7 (the seven **Missing subjects**). Step 1.3
was re-run (`run_gaps.py --hints`), which saved the report again.

Earlier, `stale_copy_check` held the area: the proposed merge made
`copy_check.py` list one `moved` row (recipe-formatting), so **Overlaps** was
rewritten from the fresh run and its line re-recorded.

Hand-off check, after the plan's final edit:

- unmeasured.py cookbook/authoring: check unchanged; changes 0; new_keys 0; stale_reference 0; result a7c23a7e7fca
- run_gaps.py --check cookbook/authoring: unchanged, exit 0; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 0; gap_total_rows 0; measured_total 0; missing_subjects 7; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report 67248934e3579d9e8faa39b3034bab3b1dcc767a
- run_gaps.py --check-homes cookbook/authoring: `check_homes` [], exit 0
- run_gaps.py --check-verdicts cookbook/authoring: `check_verdicts` [], exit 0
- copy_check.py cookbook/authoring: copies 0; identical 0; moved 1; unreadable 0; twin_differs 0; differ_uncarried none; result b4fcb364e515
- stage_status.py cookbook/authoring: next approve; plan_sections 0; stale_reference 0; r9_stale 0; stale_copy_check 0; host_check 0; cite_moved 0; stale_verdicts 0; result 0785eeb62840

This plan cites no other area plan, so no plan hash is recorded.

### On 1.4.46, after the owner's rulings

The owner ruled on every Owner question. The worklist changed: the
recipe-formatting row's survivor moved to
`guidelines/cookbook/recipe-quality/template-conformance` (Q7), and a
`requirement-keywords` row was added (`new: true`, `kind: "new"`, `devteam:
"authored"`, Q10 + Q11). The plan was rewritten for every ruling: Topics and
Proposed topics gained requirement-keywords; Missing subjects dropped the
recipe section names (Q9) and renamed the lint severity subject to
**Keyword lint severity mapping**, so both keyword subjects are hosted by
requirement-keywords and *No host* is gone; Overlaps and the research
questions record Q7, Q8 and Q12; Owner questions quote every ruling.

First check, on the saved reports before they were rewritten:

- unmeasured.py cookbook/authoring: check changed; changes 1; new_keys 0; stale_reference 0; result a1fa10121c17
- run_gaps.py --check cookbook/authoring: unchanged, exit 0; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 0; gap_total_rows 0; measured_total 0; missing_subjects 7; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report 67248934e3579d9e8faa39b3034bab3b1dcc767a
- copy_check.py cookbook/authoring: copies 0; identical 0; moved 1; unreadable 0; twin_differs 0; differ_uncarried none; result b4fcb364e515

First check's `new_keys` 0, `changes` 1, `cleared` 0. The one change is
`unmeasured.py`'s `new_topics`: requirement-keywords added and
recipe-formatting removed (its survivor is no longer in this area), both from
the worklist rulings. `unmeasured.py` was re-run through `write_on_success.py`
and step 1.3 (`run_gaps.py --hints`) was re-run after the plan was rewritten,
which moved `missing_subjects` from 7 to 6 (the recipe subject left the area,
Q9). The copy_check line is unchanged, so **Overlaps** keeps it.

Hand-off check, after the plan's final edit:

- unmeasured.py cookbook/authoring: check unchanged; changes 0; new_keys 0; stale_reference 0; result a7c23a7e7fca
- run_gaps.py --check cookbook/authoring: unchanged, exit 0; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 0; gap_total_rows 0; measured_total 0; missing_subjects 6; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report 4b933dc102f33e5f3f2c5eeaeb29fadb23cd90da
- run_gaps.py --check-homes cookbook/authoring: `check_homes` [], exit 0
- run_gaps.py --check-verdicts cookbook/authoring: `check_verdicts` [], exit 0
- copy_check.py cookbook/authoring: copies 0; identical 0; moved 1; unreadable 0; twin_differs 0; differ_uncarried none; result b4fcb364e515
- stage_status.py cookbook/authoring: next approve; plan_sections 0; stale_reference 0; r9_stale 0; stale_copy_check 0; host_check 0; cite_moved 0; stale_verdicts 0; result 0785eeb62840

This plan cites no other area plan, so no plan hash is recorded.
