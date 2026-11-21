# Research brief: guideline-formatting

- **Area:** `cookbook/authoring`
- **Topic:** `guideline-formatting` (new)
- **Artifact:** `cookbook/guidelines/cookbook/authoring/guideline-formatting`. The topic is new: it has no rules of its own yet, and its folder holds only `research/` until stage 3.
- **Base commit:** `071e52f9572bf4b7c534cfcf95fb111282abc423` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain technical writing; method practitioner and standards sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner ruling, Owner question 2: "no escalation for any topic. Each keeps its proposed bar.").

## Scope

The structure of a cookbook guideline: its meta (frontmatter), title, summary
statement, structured guidance, roled parts, named rules, the research each
rule cites, its compliance section, its `triggers` field and its change
history.

**Not this topic's:** keyword case (whether only uppercase MUST/SHOULD/MAY
carry normative meaning, RFC 8174) and the severity a rule's keyword gives a
lint finding belong to the sibling topic
`cookbook/guidelines/cookbook/authoring/requirement-keywords` (owner ruling
Q10 + Q11). This topic cites that sibling for both and never restates them:
research neither. Where a rule below rests on keyword case or severity (part
of `gf-rfc-keywords`), say so in its verdict's note and in limitations, and
judge only the structural part (whether a guideline's requirements carry a
normative keyword at all, one obligation per rule). The `triggers` field's
vocabulary belongs to the sibling topic `activity-triggers`; this topic judges
only whether a guideline carries the field and its shape.

**The owner's ruling on `conventions.md` (Q12):** "if research on
principle-formatting or guideline-formatting finds against
`guide/introduction/conventions.md`, `conventions.md` changes to match the
research." Where the research finds against a `conv-*` rule below, record it
as a finding (a `contradicted` or `unsupported` verdict with its claims, and a
line in research.md); `conventions.md` is changed in stage 5, never now.

## Research questions (from the area plan, verbatim)

1. Best practice: how do style guides and docs-as-code practice structure a rule-bearing document: named rules, roled sections (rules, how-to, examples, review focus, bars, rationale, references) and a compliance section?
2. Known solutions: how do Vale, markdownlint and schema-validated docs check a guideline's frontmatter, heading, named-rule bullets and research folder shape, and which of the draft's 13 checks can a tool decide (the keyword and severity checks are cited from requirement-keywords)?
3. Platform guidelines: what do the IETF's and W3C's conventions for writing a specification, and Diátaxis's split of reference, how-to and explanation, say about structuring a document of normative rules?
4. The expert's view: what do standards editors and docs-as-code practitioners say about one rule per bullet, citing evidence per rule, and the failure modes of normative prose?
5. Where this research finds against `guide/introduction/conventions.md` (*The Standard*, *Roles*, *Research*, *Named Requirements*), record each finding with its claims: `conventions.md` changes to match the research (owner ruling Q12).

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

For this topic the "platforms" are the owners of the standards and tools a
rule-bearing document is written and checked with: the IETF (RFC 7322 style,
RFC 7991 xml2rfc, the RFC Editor's style guide), the W3C (Manual of Style,
specification conformance conventions), Diátaxis, the Google developer
documentation style guide and the Microsoft Writing Style Guide, and the
tools' own documentation (Vale, markdownlint, JSON Schema).

## Method

- Research to `guidelines/researching/process/research-methodology-and-sources`, using its source catalogue for the domain (technical writing; standards). Primary sources (specifications, standards, the tool vendors' own documentation) come before secondary ones; a secondary source only for what no primary source covers, said so in the claim's trust basis.
- Verify every rule below. Each is quoted **verbatim**, with the file it is in and the base commit, as a claim to check, never as a source. Never restate or summarize a rule.
- Score each claim 0–100 per `guidelines/researching/evidence/verification-and-trust-scoring`, applying `cite-the-claim-not-the-document`, `independence-before-corroboration`, `domain-stratified-trust`, `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- Find what the topic is missing: practice the research finds that no rule covers, each a `new` verdict naming the rule stage 3 will write, at the strength its sources support.
- A rule's `-prior` claim cites the file the rule is quoted from at the base commit: `url` `git:071e52f9572bf4b7c534cfcf95fb111282abc423:<file>` (the file below, e.g. `tbd/compliance/artifact-formatting/guideline-formatting.md` or `guide/introduction/conventions.md`), `title` `guideline-formatting (<file>)`.
- A rule that is a tool's behaviour (what `cookr` compiles or validates) rather than a writing practice: judge whether the research supports the practice it encodes; where no outside source can speak to it, it is `unsupported` with its `-prior` claim, and the reason goes in research.md.

## Rules to verify

Each rule below is named; the names are fixed from here on. Rules marked
**no RFC keyword** have no MUST, SHOULD or MAY in their text.

### From `tbd/compliance/artifact-formatting/guideline-formatting.md` at `071e52f9572bf4b7c534cfcf95fb111282abc423` (the draft's 13 checks)

1. **gf-frontmatter-complete**:
   > All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.
   >
   > The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.
   >
   > **Applies when:** always.
   >
   > **Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

2. **gf-type-field**:
   > The `type` field MUST be `guideline`.
   >
   > **Applies when:** always.

3. **gf-title-heading**:
   > The first H1 heading MUST match the frontmatter `title` field exactly.
   >
   > **Applies when:** always.

4. **gf-summary-statement**:
   > A summary statement MUST appear immediately after the H1 heading. This is the guideline's core message — typically 1-3 sentences that a reader can act on without reading further.
   >
   > **Applies when:** always.

5. **gf-structured-guidance**:
   > The guideline MUST include structured guidance in the form of bullet points, tables, subsections, or a combination. Unstructured prose without actionable items is not sufficient.
   >
   > **Applies when:** always.

6. **gf-rfc-keywords** (keyword case and severity: cite `requirement-keywords`, never research them here; see *Scope*):
   > Requirements within the guideline MUST use RFC 2119 keywords (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) to indicate obligation levels. Keywords MUST be bold or uppercase when used normatively.
   >
   > **Applies when:** the guideline contains requirements or rules (not purely informational content).

7. **gf-change-history**:
   > The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.
   >
   > **Applies when:** always.

8. **gf-compliance-section**:
   > The guideline MAY include a `## Compliance` section listing evaluated compliance checks and their status. This is recommended when the guideline is referenced by compliance checks in other categories.
   >
   > **Applies when:** the guideline is referenced by one or more compliance check definitions.

9. **gf-triggers-field** (the vocabulary itself is `activity-triggers`'s; see *Scope*):
   > The `triggers` field SHOULD be present in guideline frontmatter. It MUST be a YAML list of trigger names from the canonical taxonomy defined in `introduction/trigger-guide.md`. Empty list `[]` is acceptable for guidelines not yet classified.
   >
   > **Applies when:** always.

10. **gf-roled-parts**:
    > A roled guideline MUST give every part but the intro and the history a `role` in `artifact.json`, one of `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`, and MUST have at least one part of each of `rules`, `review-focus`, `review-bar` and `build-bar`. It sets no `routes` and no `hosts/`, and does not live under `guidelines/reviewing/`.
    >
    > What each role holds (`guidelines/implementing/data/indexing` is a worked example; its parts are `rules`, `look-for`, `a-complete-review-must-establish` and `a-build-must-establish`, among others):
    >
    > | Role | Holds | Goes to |
    > |---|---|---|
    > | none (`intro`) | the summary statement | every skill |
    > | `rules` | the named rules | builder, reviewer |
    > | `how-to`, `examples` | how to keep the rules | builder |
    > | `review-focus` | what a reviewer looks for | reviewer |
    > | `review-bar` | what a complete review must establish | review-verifier |
    > | `build-bar` | what a complete build must establish: exactly one line per named rule, `` - `rule-name`: … ``, and no line naming anything else | build-verifier |
    > | `rationale`, `references` | why, and the sources | each skill's references |
    > | none (`history`) | the change history | none |
    >
    > **Applies when:** any part of the guideline carries a `role`.

11. **gf-named-rules**:
    > Every bullet in a `rules` part MUST be a named rule: `- **kebab-name**: … MUST|SHOULD|MAY …`, its name unique in the guideline and its obligation an RFC 2119 keyword.
    >
    > **Applies when:** the guideline is roled.

12. **gf-research-folder**:
    > The guideline MUST keep the research it was written from in `research/` in its folder: `research/research.json`, in the shape of the research-results document (`guidelines/researching/evidence/research-results-document`), and `research/research.md`, the same, readable, under the four question headings in this order: `## Best practices`, `## Known solutions`, `## Platform guidelines`, `## The expert's view`.
    >
    > Each claim in `research.json`'s `claims` list is the per-claim record: `id` (kebab-case, unique), `question` (`best-practices`, `known-solutions`, `platform-guidelines` or `experts-view`), `claim`, `citations` (each with `title`, `author`, `publisher`, `date`, `url`, `accessed`), `source_type`, `quote`, `generated_by`, `query`, `trust` (`{"score": 0-100, "basis"}`) and `independence` (`multi-independent`, `single` or `uncorroborated`). The `verdicts` list gives each rule checked a verdict, `supported`, `contradicted`, `unsupported` or `new`, and the claims it rests on, at least one; every claim a rule cites MUST be named by a verdict. A rule the research cannot support is recorded as a claim itself, its source the cookbook's own text at the topic's base commit, with an `unsupported` verdict (`contradicted` when the research finds against it) naming that claim; a rule kept for the owner cites it, and `cookr validate` passes it with an `owner-decides` warning naming the rule and the claim.
    >
    > **Applies when:** always, unless the guideline is listed in `cookbook/research-exempt.json` as a topic written before research-first whose research is still to come.

13. **gf-rule-cites-research**:
    > Each named rule MUST cite the claims of its research it stands on, once, at the end of its bullet: `(claim: <id>)`, or `(claims: <id>, <id>)` for several. Nothing follows the citation. Every id cited MUST be a claim in `research/research.json`. The citation names the claim, never the document (`cite-the-claim-not-the-document`), so a reader can follow a rule to the quote and source behind it.
    >
    > ```markdown
    > - **index-foreign-keys**: Every foreign-key column MUST have an index. (claims: fk-index-postgres, fk-index-sqlite)
    > ```
    >
    > **Applies when:** the guideline has a `research/` folder. In a roled guideline the named rules are its `rules` parts' bullets; in an unroled one, every named bullet that states MUST, SHOULD or MAY outside the intro and the history.

### From `guide/introduction/conventions.md` at `071e52f9572bf4b7c534cfcf95fb111282abc423` (*The Standard*, *Roles*)

14. **conv-roled-parts** (*The Standard*; **no RFC keyword**):
    > **Roled parts.** A guideline or a principle gives each part a role (below), so it compiles to a builder, a reviewer and their two verifiers.

15. **conv-named-rules** (*The Standard*; **no RFC keyword**):
    > **Named rules.** Each rule is a bullet of a `rules` part, `- **kebab-name**: … MUST|SHOULD|MAY …`, one rule to a bullet (see *Named Requirements*).

16. **conv-one-source-per-topic** (*The Standard*; **no RFC keyword**):
    > **One source per topic.** A topic is written once, in one folder (see *One Source Per Topic*).

17. **conv-research-cited** (*The Standard*; **no RFC keyword**):
    > **Research.** The topic is written from research kept in its `research/` folder, and each named rule cites the claims it stands on (see *Research*).

18. **conv-legacy-keeps-working** (*The Standard*; **no RFC keyword**):
    > An artifact written before this design keeps working as it is: an unroled artifact compiles as it always did, and one with no research is listed in `cookbook/research-exempt.json` until its research is written.

19. **conv-role-values** (*Roles*; **no RFC keyword**):
    > A part may carry a `role` in `artifact.json`: `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`. The intro and the history never carry one. An artifact with no role is compiled as it always was.

20. **conv-no-roles-under-reviewing** (*Roles*; **no RFC keyword**):
    > A guideline with roles may live under any use-case folder but `guidelines/reviewing/`, which is folded into each topic and never roled; a principle may carry roles too, an ingredient or a recipe never.

21. **conv-roled-artifact-complete** (*Roles*; **no RFC keyword**):
    > A roled artifact gives every other part a role, names each rule in its `rules` parts (`- **kebab-name**: … MUST|SHOULD|MAY …`), and sets no `routes` and no `hosts/`. `cookr validate` lists what is wrong.

22. **conv-four-skills** (*Roles*; **no RFC keyword**):
    > It compiles to four skills, each the intro plus the parts of its roles:
    >
    > | Skill | Roles | Name |
    > |---|---|---|
    > | builder | `rules`, `how-to`, `examples` | `<use-case>-<tail>` |
    > | build-verifier | `build-bar` | `verifying-build-<tail>` |
    > | reviewer | `rules`, `review-focus` | `reviewing-<tail>` |
    > | review-verifier | `review-bar` | `verifying-review-<tail>` |

23. **conv-skill-names** (*Roles*; **no RFC keyword**):
    > The builder keeps the name the artifact would have unroled; the other three replace only its use case: `guidelines/planning/data/t` gives `planning-data-t` and `reviewing-data-t`, and `principles/t`, which has no use case, keeps its type: `principle-t` and `reviewing-principle-t`. Two artifacts whose skills would share a name, after a long name is cut to the hosts' limit, are refused, each naming the other.

24. **conv-rationale-to-references** (*Roles*; **no RFC keyword**):
    > `rationale` and `references` go to each skill's linked reference files, never its SKILL.md. Each skill has its own description and routes under its own use case, with the artifact's own use case below it (`coding/reviewing/planning/data`; a principle's `coding/reviewing/principles`). A builder writes the code, a reviewer reviews it, and each verifier grades the other's work against its bar.

The devteam's text adds no rule: the area has no speciality (`reference.json`
is `[]`), so no speciality sentence is quoted under this topic.

## What to look for that no rule covers

For example (each only if the research finds it): a rule-bearing document's
conformance or applicability statement; rule identifiers that stay stable
across versions; one testable requirement per rule; rationale kept apart from
the normative text; normative versus informative sections marked as such; a
maximum length or count of rules; examples marked non-normative.
