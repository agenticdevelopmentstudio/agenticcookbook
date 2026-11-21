# Research brief: principle-formatting

- **Topic:** principle-formatting, area `cookbook/authoring`.
- **Artifact:** `cookbook/guidelines/cookbook/authoring/principle-formatting` (new: no rules of its own yet; its folder holds only `research/` until stage 3).
- **Base commit:** `071e52f9572bf4b7c534cfcf95fb111282abc423` (from `base.txt`).
- **Research type:** How-to / troubleshooting (intent Do; domain technical writing; method practitioner and standards sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner ruling, Owner question 1: "no escalation for any topic. Each keeps its proposed bar.").

What the topic rules: the structure of a cookbook **principle** artifact, a short, always-loaded statement of an engineering principle: its meta (frontmatter), its title heading, its one-paragraph statement, its actionable guidance, its change history, its length, and the parts of the cookbook's standard (`guide/introduction/conventions.md`, *The Standard* and *Roles*) that govern a principle.

**Not this topic's:** RFC 2119 keyword case (RFC 8174's uppercase-only meaning) and the severity a rule's keyword gives a lint finding belong to the sibling topic `requirement-keywords` (`cookbook/guidelines/cookbook/authoring/requirement-keywords`, owner ruling Q10 + Q11). This topic cites it and never restates it: research neither keyword case nor a keyword-to-severity mapping here. Where a question below asks which checks a tool can decide, answer tool-decidable versus reviewer-judged only; the severity of each follows requirement-keywords.

## The four questions

Answer each as its own section, verbatim:

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

## Research questions (from the area plan)

1. Best practice: what structure do style guides and docs-as-code practice give a short, always-loaded statement of principle (frontmatter, title, one-sentence statement, actionable guidance, change history), and how short should it be?
2. Known solutions: how do markdownlint, Vale and front-matter schema checks (JSON Schema over YAML) verify the required fields, heading and length of a short document, and which of the draft's 7 checks can a tool decide and which need a reviewer (the severity of each follows requirement-keywords)?
3. Platform guidelines: what do the Diátaxis framework, the Google developer documentation style guide and the Microsoft Writing Style Guide say about a principle-like "explanation" page, and what do Anthropic's and other agent hosts' guidance say about the length of always-loaded context?
4. The expert's view: what do documentation and agent-context practitioners say about the cost of long always-loaded instructions, and where does a length cap help or hurt?
5. **Principle brevity evidence**: find the evidence for a line or token cap on an always-loaded principle (agent instruction-following studies, host guidance on memory files), state the cap the evidence supports, or record that the about-50-lines cap is unsupported.
6. Where this research finds against `guide/introduction/conventions.md` (*The Standard*, *Roles*), record each finding with its claims: `conventions.md` changes to match the research (owner ruling Q12).

## Method

- Research to `guidelines/researching/process/research-methodology-and-sources`, using its source catalogue for the domain (technical writing; agent context). Primary sources (specifications, standards, vendor documentation: markdownlint's rule docs, Vale's docs, JSON Schema, Diátaxis, the Google and Microsoft style guides, Anthropic's and other agent hosts' own documentation on memory/instruction files) come before secondary ones.
- Verify every rule listed below. Each is quoted **verbatim**, with the file it is in and the base commit, as a claim to check, never as a source.
- Score each claim 0–100 per `guidelines/researching/evidence/verification-and-trust-scoring`, applying the principles `cite-the-claim-not-the-document`, `independence-before-corroboration`, `domain-stratified-trust`, `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- `supported` means supported **at the rule's stated strength**: a MUST whose sources say "should" is `unsupported`, with the claim saying so. A rule marked *no RFC keyword* is judged on whether the research supports the practice it states; record the strength the sources support.
- Rules that state the cookbook's own internal design (what `cookr` compiles, which roles exist) cannot be confirmed by an outside source as such; judge whether outside practice supports the design choice they make (e.g. role-separated content, one rule per bullet, rules citing evidence), and record what it supports or finds against. Where it finds against `conventions.md`, say so plainly: the owner ruled `conventions.md` changes to match (Q12), in stage 5.
- Find what the topic is missing: practice the research finds that no rule covers, each as a `new` verdict naming a kebab-case rule.

## The rules to verify

All quoted verbatim at base commit `071e52f9572bf4b7c534cfcf95fb111282abc423`.

### From `tbd/compliance/artifact-formatting/principle-formatting.md` (the draft; all 7 checks)

The draft's preamble, context only (not a rule): "Principles are concise, philosophical statements that guide engineering decisions. They are the most lightweight artifact type — a clear statement, practical guidance, and nothing more." Its *Applicability*: "This category applies to any file with `type: principle` in its frontmatter. All files in `principles/` MUST have this type."

1. **pf-frontmatter-complete** (section `### pf-frontmatter-complete`):
   > All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field.
   >
   > The artifact's `id` is its identity: every link to it stores that UUID. Its rdid and folder path are held in the cookbook's `index.json`, never in the artifact; `cookr validate` fails when the index and the folders disagree.
   >
   > **Applies when:** always.
   >
   > **Required fields:** id, title, type, version, status, language, created, modified, author, copyright, license, summary, platforms, tags, depends-on, related, references.

2. **pf-type-field** (section `### pf-type-field`):
   > The `type` field MUST be `principle`.
   >
   > **Applies when:** always.

3. **pf-title-heading** (section `### pf-title-heading`):
   > The first H1 heading MUST match the frontmatter `title` field exactly.
   >
   > **Applies when:** always.

4. **pf-statement** (section `### pf-statement`):
   > A concise statement paragraph MUST appear immediately after the H1 heading. This is the principle's core idea — typically 1-3 sentences.
   >
   > **Applies when:** always.

5. **pf-actionable-guidance** (section `### pf-actionable-guidance`):
   > The principle SHOULD include bullet points with practical applications of the idea. These translate the philosophical statement into concrete actions.
   >
   > **Applies when:** the statement alone is not self-evident in practice.

6. **pf-change-history** (section `### pf-change-history`):
   > The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary.
   >
   > **Applies when:** always.

7. **pf-brevity** (section `### pf-brevity`):
   > Principles SHOULD be concise. The body (excluding frontmatter and Change History) SHOULD NOT exceed ~50 lines. Principles are philosophical anchors, not exhaustive guides — detailed guidance belongs in guidelines.
   >
   > **Applies when:** always.

### From `guide/introduction/conventions.md`, *The Standard* (the parts that govern a principle)

8. **standard-roled-parts** (no RFC keyword):
   > **Roled parts.** A guideline or a principle gives each part a role (below), so it compiles to a builder, a reviewer and their two verifiers.

9. **standard-named-rules** (no RFC keyword):
   > **Named rules.** Each rule is a bullet of a `rules` part, `- **kebab-name**: … MUST|SHOULD|MAY …`, one rule to a bullet (see *Named Requirements*).

10. **standard-one-source-per-topic** (no RFC keyword):
    > **One source per topic.** A topic is written once, in one folder (see *One Source Per Topic*).

11. **standard-research-cited** (no RFC keyword):
    > **Research.** The topic is written from research kept in its `research/` folder, and each named rule cites the claims it stands on (see *Research*).

### From `guide/introduction/conventions.md`, *Roles* (the parts that govern a principle)

12. **roles-vocabulary** (no RFC keyword):
    > A part may carry a `role` in `artifact.json`: `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`.

13. **roles-intro-history-unroled** (no RFC keyword):
    > The intro and the history never carry one.

14. **roles-principle-may-be-roled** (no RFC keyword):
    > a principle may carry roles too, an ingredient or a recipe never.

15. **roles-every-part-roled** (no RFC keyword):
    > A roled artifact gives every other part a role, names each rule in its `rules` parts (`- **kebab-name**: … MUST|SHOULD|MAY …`), and sets no `routes` and no `hosts/`.

16. **roles-four-skills** (no RFC keyword):
    > It compiles to four skills, each the intro plus the parts of its roles:
    >
    > | Skill | Roles | Name |
    > |---|---|---|
    > | builder | `rules`, `how-to`, `examples` | `<use-case>-<tail>` |
    > | build-verifier | `build-bar` | `verifying-build-<tail>` |
    > | reviewer | `rules`, `review-focus` | `reviewing-<tail>` |
    > | review-verifier | `review-bar` | `verifying-review-<tail>` |

17. **roles-principle-skill-names** (no RFC keyword):
    > `principles/t`, which has no use case, keeps its type: `principle-t` and `reviewing-principle-t`.

18. **roles-rationale-references-linked** (no RFC keyword):
    > `rationale` and `references` go to each skill's linked reference files, never its SKILL.md.

19. **roles-principle-routing** (no RFC keyword):
    > Each skill has its own description and routes under its own use case, with the artifact's own use case below it (`coding/reviewing/planning/data`; a principle's `coding/reviewing/principles`).

## The devteam's text

None: the area has no speciality (`run_gaps.py` `why_empty` "area has no speciality"; `reference.json` is `[]`). No devteam sentence is quoted under this topic.

## Missing subject this topic hosts

- **Principle brevity evidence** (area plan, Missing subjects 1): "the principle draft caps a principle at about 50 lines (pf-brevity) and cites nothing for the number; a practitioner expects the cap to rest on evidence about how long an always-loaded principle can be before agents or readers skip it." Research question 5 above.

## Overlaps to respect

- `guide/introduction/conventions.md` is no artifact and no survivor; this topic must agree with it, and where the research finds against it, `conventions.md` changes (Q12).
- `skills/cookr/SKILL.md` (*Source folders*) and `cookr validate` already enforce the source-folder form; the topic cites the tool's checks rather than restating them.
- `requirement-keywords` owns keyword case and lint severity (Q10 + Q11).
