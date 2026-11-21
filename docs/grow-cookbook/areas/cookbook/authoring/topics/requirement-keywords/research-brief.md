# Research brief: requirement-keywords

- **Area:** `cookbook/authoring`
- **Topic:** `requirement-keywords` (new, owner ruling Q10 + Q11)
- **Artifact:** `cookbook/guidelines/cookbook/authoring/requirement-keywords`
- **Base commit:** `071e52f9572bf4b7c534cfcf95fb111282abc423` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain technical
  writing; method practitioner and standards sources). Bar: How-to /
  troubleshooting, no escalation (owner ruling Q13).

## The topic

The cookbook's rules for requirement keywords in its own artifacts: which
normative keywords a rule uses (RFC 2119 / RFC 8174, BCP 14), in which case
they carry their defined meaning, and how a rule's keyword sets the severity
of a lint finding when an artifact fails the check that rule states, and which
severities block `/approve-artifact`. The formatting topics of this area
(principle-, guideline-, ingredient-, cookbook- and the merged
recipe-formatting) cite this topic for keyword case and severity and never
restate either. The topic is new: it has no rules of its own yet, and no
speciality's text is quoted under it (the area has no speciality).

## Research questions (from the area plan, verbatim)

1. Best practice: how do standards bodies and style guides use normative keywords: which words, in which case, one keyword per requirement, and how is a requirement with no keyword read?
2. Known solutions: how do Vale (its error, warning and suggestion levels), markdownlint, ESLint and other linters derive a finding's severity, and how does a spec linter tie a rule's MUST, SHOULD or MAY to that severity and to blocking a merge or an approval?
3. Platform guidelines: what do RFC 2119 and RFC 8174 (BCP 14) say about keyword case and the boilerplate that invokes them, and what do the IETF's and W3C's conformance conventions add on how conformance is reported?
4. The expert's view: what do standards editors and linter maintainers say about lowercase keywords in normative text, and about mapping requirement levels to lint severities?
5. **RFC 2119 keyword case**: find what RFC 8174 and standards practice say about uppercase-only meaning, and state whether only the uppercase keywords carry normative meaning in a cookbook rule and whether a lowercase "must" in rule text is flagged.
6. **Keyword lint severity mapping**: find how linters and spec checkers set a finding's severity from a requirement level, and state the severity each keyword gives a failed check (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) and which severities block `/approve-artifact`.

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

For this topic the "platforms" are the standards bodies whose conventions
define normative keywords and conformance (IETF: RFC 2119, RFC 8174, RFC 7322
and the RFC Style Guide; W3C: the Manual of Style and the conformance
section conventions, e.g. the QA Framework: Specification Guidelines; and
where useful ISO/IEC Directives Part 2's verbal forms and OASIS), plus the
linters named in question 2 (Vale, markdownlint, ESLint) and spec checkers
(e.g. W3C's specberus / pubrules, IETF idnits, Bikeshed or ReSpec) as the
tools' own documentation states them.

## Method

- Research to `cookbook/guidelines/researching/process/research-methodology-and-sources`,
  using its source catalogue for the domain. Primary sources (specifications,
  standards, vendor documentation) come before secondary ones.
- Score each claim 0–100 per `cookbook/guidelines/researching/evidence/verification-and-trust-scoring`,
  applying the principles `cite-the-claim-not-the-document`,
  `independence-before-corroboration`, `domain-stratified-trust`,
  `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- Verify every rule listed below. Each is quoted **verbatim**, with the file it
  is in at the base commit, as a claim to check, never as a source. Never
  restate or summarize a rule.
- `supported` means supported at the rule's stated strength. A rule marked
  *no RFC keyword* states its obligation in plain words; judge it at the
  strength its words carry, and say in research.md what strength the sources
  support.
- A rule the research cannot support or finds against is recorded as its own
  `<rule-name>-prior` claim, `source_type` `prior cookbook text`, its one
  citation `title` `requirement-keywords (<file>)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`,
  `url` `git:071e52f9572bf4b7c534cfcf95fb111282abc423:<file>`, where `<file>`
  is the repo-relative file named with the rule below (the topic has no part
  files yet: its rules are quoted from these drafts).
- Find what the topic is missing: practice the research finds that no rule
  covers. Give each a `new` verdict naming the kebab-case rule stage 3 will
  write and the strength its sources support. Questions 5 and 6 above each
  owe at least one `new` verdict (keyword case; the severity each keyword gives
  a failed check, and which severities block approval), unless a listed rule
  already covers it.
- If the research finds against `guide/introduction/conventions.md`, record
  it as a finding (a `contradicted` or `unsupported` verdict and a note in
  research.md). `conventions.md` is not changed in this stage.
- What the research leaves to a policy choice goes in `open_questions`, one
  entry per question.

## The rules to verify

Each rule is quoted verbatim from its file at the base commit. The names are
fixed from here on.

### From `tbd/compliance/artifact-formatting/guideline-formatting.md` (check `gf-rfc-keywords`)

1. **gf-rfc-keywords**: "Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels."
2. **gf-rfc-keywords-bold-or-uppercase**: "Keywords MUST be bold or uppercase when used normatively."

### From `guide/introduction/conventions.md` (section *RFC 2119 Keywords*)

3. **use-rfc-2119-keywords-for-behavioral-requirements** (no RFC keyword): "Use RFC 2119 keywords for all behavioral requirements:"
4. **must-is-absolute-requirement** (no RFC keyword; a definition): "**MUST** / **MUST NOT**: Absolute requirements."
5. **should-is-recommendation** (no RFC keyword; a definition): "**SHOULD** / **SHOULD NOT**: Recommendations."
6. **may-is-optional-behavior** (no RFC keyword; a definition): "**MAY**: Optional behavior."

### From `.claude/rules/artifact-formatting.md` (named in the plan's Overlaps)

7. **rule-uses-rfc-2119-keywords** (no RFC keyword): "**Use RFC 2119 keywords** for requirements — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY."
8. **follow-must-address-should-checks** (no RFC keyword): "Follow every MUST check. Address every SHOULD check unless there is a documented reason to skip it."

### From `.claude/skills/approve-artifact/SKILL.md` (the approval's current blocking behaviour, for question 6)

9. **approve-on-zero-fail** (no RFC keyword): "Run `/lint-artifact` on a cookbook artifact. If it passes (zero FAIL), stamp the frontmatter with approval metadata. If it fails, report the issues and do not approve."

### Not this topic's rules

- `guide/introduction/trigger-guide.md` states no requirement keyword and no
  severity: it has no rule for this topic.
- The rest of each formatting draft's checks (`principle-`, `guideline-`,
  `ingredient-`, `recipe-` and `cookbook-formatting.md`) are the formatting
  topics' own rules, researched there; this topic does not verify them. Their
  levels are the inputs question 6 maps to severities. These lines, quoted
  verbatim, show the levels the drafts use, for the research to classify
  (each a level example, no verdict owed):
  - `principle-formatting.md`: "Principles SHOULD be concise. The body (excluding frontmatter and Change History) SHOULD NOT exceed ~50 lines."
  - `guideline-formatting.md`: "The guideline MAY include a `## Compliance` section listing evaluated compliance checks and their status. This is recommended when the guideline is referenced by compliance checks in other categories."
  - `guideline-formatting.md`: "The `triggers` field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the canonical taxonomy defined in `introduction/trigger-guide.md`."
  - `ingredient-formatting.md`: "Ingredients MUST follow this section order. Optional sections (marked MAY) can be omitted entirely but MUST NOT appear out of order."
  - `.claude/skills/lint-artifact/SKILL.md` (its guideline table, the current mapping of a check to a result): "| GF-03 | RFC 2119 keywords in requirements | Requirements use MUST, SHOULD, MAY | WARN if missing |"
- The named-rule form (`- **kebab-name**: … MUST|SHOULD|MAY …`, in
  `conventions.md` *The Standard*, *Roles* and `guideline-formatting.md`
  `gf-named-rules`) is guideline-formatting's rule. This topic says which
  keywords and in which case; it does not verify the bullet form.
