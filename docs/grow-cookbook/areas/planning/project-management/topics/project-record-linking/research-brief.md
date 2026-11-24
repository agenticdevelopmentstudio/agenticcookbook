# Research brief: project-record-linking

- **Area:** `planning/project-management`
- **Topic:** `project-record-linking` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/planning/project-management/project-record-linking`
- **Base commit:** `f0dd450e1188364e9e221d912d49657944ae46ad` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain traceability between project records; method standards bodies, tool documentation and practitioner sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner approval 2026-11-24, Owner questions 1 and 4).
  Any metric claim (a review cadence, a task size or a schedule accuracy backed by a study or survey) takes the
  *Statistical* bar of `guidelines/researching/process/research-methodology-and-sources`: name the study, its
  sample, its measure and its result, and score it on that bar.

## The topic

How a delivery team's project records (risks, decisions, dependencies, issues, milestones, tasks) reference each other and the findings that raised them: which record carries each link, which links are two-way, how a link names its target so it stays valid when the target moves or closes, and how links are checked for dangling targets.

The cookbook states general practice for any delivery team, not projectteam's: projectteam's `.dev-team-project/`
paths, its file formats and its specialist names stay in projectteam and are not researched.

**Not this topic's:**

- The record-specific fields stay with their host topics, researched there: decision supersession (`decision-records`), issue resolution traceability (`issue-tracking`), blocked milestone accounting (`milestone-scheduling`) and task blocker naming (`task-breakdown`), and the risk and dependency records' own fields (`risk-tracking`, `dependency-tracking`). This topic researches the linking convention those records share: identifiers, link direction, link types, and checking for dangling links.
- Requirements traceability in safety or regulated engineering (DO-178C, ISO 26262) is context only: research it only for what it says about link direction and dangling-link checking that applies to project records.

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

For this topic the "platforms" are the method owners and standards bodies (PMI's PMBOK Guide and its
practice standards, ISO 21502, ISO 31000 where risk is concerned, AXELOS PRINCE2, the Scrum Guide, the
Kanban Guide, and the scaled frameworks SAFe and LeSS where they speak to it) and the published guidance of
the issue trackers teams use (GitHub Issues and Projects, Jira, Linear). Apple, Android and Windows have no
bearing on this topic; say so in one line rather than researching them. Where a standard is paywalled, use
its owner's own public summary or excerpt and say so in the claim's trust basis.

## Research questions (from the area plan, verbatim)

1. Best practice: how should a delivery team link its project records (risks, decisions, dependencies, issues, milestones, tasks) to each other and to the findings that raised them: which record carries each link, which links are two-way, and how a record is identified so a link stays valid when the record moves or closes?
2. Known solutions: how do RAID logs, traceability matrices, ADR links, and the linked-issue, sub-issue, relation and dependency fields of GitHub Issues and Projects, Jira and Linear compare for keeping links between records findable?
3. Platform guidelines: what do the PMBOK Guide, ISO 21502, PRINCE2's registers and logs, and the trackers' own documentation say about cross-referencing risks, issues, decisions and the plan?
4. The expert's view: what do delivery leads and traceability practitioners say teams get wrong with links between records (one-way links, links to closed or deleted records, records findable from none of the others), and what to do instead?
5. **Cross-artifact linking**: find how practitioners and trackers keep each project record findable from the records it touches, and state which links each record type carries (a blocked milestone to its issue or risk, a task to its milestone and blocker, a superseding decision to the one it supersedes, a resolved issue to its resolution), how a link names its target, and how links are checked for dangling targets. The record-specific fields stay at their hosts (**Decision supersession**, **Issue resolution traceability**, **Blocked milestone accounting**, **Task blocker naming**); this topic rules the linking convention they share.

## Method

- Research to `cookbook/guidelines/researching/process/research-methodology-and-sources`, using its source
  catalogue for the domain. Primary sources (standards, method owners' guides, the trackers' own documentation)
  come before secondary ones (practitioner articles, books); use a secondary source only for what no primary
  source covers, and say so in the claim's trust basis.
- Score each claim 0–100 per `cookbook/guidelines/researching/evidence/verification-and-trust-scoring`,
  applying the principles `cite-the-claim-not-the-document`, `independence-before-corroboration`,
  `domain-stratified-trust`, `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- Verify every rule listed below. Each is quoted **verbatim**, with the file it is in, as a claim to check,
  never as a source. Never restate or summarize a rule.
- `supported` means supported at the rule's stated strength. Every rule below is marked *no RFC keyword*: it
  states its obligation in plain words (a Verify clause reads as a check that must hold; a Worker Focus
  clause as what the worker attends to). Judge each at the strength its words carry, and say in research.md
  what strength (MUST, SHOULD or MAY) the sources support.
- A rule the research cannot support or finds against is recorded as its own `<rule-name>-prior` claim,
  `source_type` `prior cookbook text`, its one citation `title` `project-record-linking (teams/projectteam/specialities/project/<file>)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:736232c055d56077e7e1bc03e7e1accf7173a87f:teams/projectteam/specialities/project/<file>` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

This topic has no rules of its own to verify, so every verdict it owes is `new`. Each of projectteam's
six specialities requires links between records; the sentences below, quoted verbatim from their files
in the teams repo at commit `736232c055d56077e7e1bc03e7e1accf7173a87f` (the cookbook base commit is `f0dd450e1188364e9e221d912d49657944ae46ad`), are the links the record
topics require. They are context, never a source, and **no verdict is owed on them here**: each is
verified, under the name shown, in its host topic's research. Use them to find which links the shared
convention must serve (which record carries each link, its direction, how it names its target, how a
dangling target is found), and give each convention rule the research supports a `new` verdict.

- `teams/projectteam/specialities/project/concerns.md`, section *Worker Focus* (verified in its host topic as **link-concerns-to-related-elements**): "link concerns to related project elements"
- `teams/projectteam/specialities/project/decisions.md`, section *Worker Focus* (verified in its host topic as **decisions-findable-and-linked**): "ensure decisions are findable and linked to the work they affect"
- `teams/projectteam/specialities/project/decisions.md`, section *Verify* (verified in its host topic as **acknowledge-contradicted-decisions**): "no decision contradicts a previous decision without acknowledging the change"
- `teams/projectteam/specialities/project/dependencies.md`, section *Verify* (verified in its host topic as **blocked-dependency-linked-to-affected-work**): "blocked or at-risk dependencies are linked to affected milestones or todos"
- `teams/projectteam/specialities/project/issues.md`, section *Worker Focus* (verified in its host topic as **link-issues-to-findings**): "link issues to specialist findings when applicable"
- `teams/projectteam/specialities/project/issues.md`, section *Verify* (verified in its host topic as **resolved-issue-references-resolution**): "resolved issues reference what resolved them"
- `teams/projectteam/specialities/project/schedule.md`, section *Verify* (verified in its host topic as **blocked-milestone-has-issue-or-concern**): "no milestone is blocked without a corresponding issue or concern"
- `teams/projectteam/specialities/project/todos.md`, section *Worker Focus* (verified in its host topic as **link-tasks-to-milestones**): "link tasks to milestones"
- `teams/projectteam/specialities/project/todos.md`, section *Verify* (verified in its host topic as **blocked-task-references-blocker**): "blocked todos reference a specific blocker"
- `teams/projectteam/specialities/project/todos.md`, section *Verify* (verified in its host topic as **task-milestone-must-exist**): "no todo is assigned to a nonexistent milestone"
