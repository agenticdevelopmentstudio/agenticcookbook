# Research brief: milestone-scheduling

- **Area:** `planning/project-management`
- **Topic:** `milestone-scheduling` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/planning/project-management/milestone-scheduling`
- **Base commit:** `f0dd450e1188364e9e221d912d49657944ae46ad` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain project scheduling; method standards bodies and practitioner sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner approval 2026-11-24, Owner questions 1 and 4).
  Any metric claim (a review cadence, a task size or a schedule accuracy backed by a study or survey) takes the
  *Statistical* bar of `guidelines/researching/process/research-methodology-and-sources`: name the study, its
  sample, its measure and its result, and score it on that bar.

## The topic

How a team defines milestones, sequences the work between them, sets target dates, keeps the schedule current, checks its dependency chains for cycles and finds the critical path, and accounts for every at-risk or blocked milestone.

The cookbook states general practice for any delivery team, not projectteam's: projectteam's `.dev-team-project/`
paths, its file formats and its specialist names stay in projectteam and are not researched.

**Not this topic's:**

- Delivery dependencies on other teams and vendors are `dependency-tracking`'s; tasks and their blockers are `task-breakdown`'s; the general linking convention between records is `project-record-linking`'s.
- `cookbook/guidelines/implementing/code-quality/use-roadmaplib` rules a library's use for roadmap files, not scheduling; no bearing.

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

1. Best practice: how should a team set milestones, sequence the work between them, set target dates and keep the schedule current?
2. Known solutions: how do milestone plans, roadmaps, Gantt charts, critical path method and rolling-wave planning compare for a software team, and which do GitHub milestones, Jira and Linear cycles support?
3. Platform guidelines: what do the PMBOK Guide's schedule guidance, ISO 21502 and the Scrum and Kanban Guides say about milestones, dates and forecasting?
4. The expert's view: what do delivery leads say teams get wrong with schedules (dates without dependencies, no buffer, milestones blocked with no reason recorded), and what to do instead?
5. **Milestone cycle detection**: find how scheduling practice and tools detect cycles in a dependency chain and find the critical path, and state how a milestone plan is checked so its chains hold no cycle.
6. **Blocked milestone accounting**: find how practitioners tie a milestone's status to the risks and issues that explain it, and state the rule that every blocked or at-risk milestone names the issue or risk that blocks it.

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
  `source_type` `prior cookbook text`, its one citation `title` `milestone-scheduling (teams/projectteam/specialities/project/schedule.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:736232c055d56077e7e1bc03e7e1accf7173a87f:teams/projectteam/specialities/project/schedule.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/projectteam/specialities/project/schedule.md` in the teams repo at commit `736232c055d56077e7e1bc03e7e1accf7173a87f` (projectteam's
compiled speciality; the cookbook base commit is `f0dd450e1188364e9e221d912d49657944ae46ad`), as a claim to check, never as a source.
The file's two sections, whole, for context:

> **Worker Focus:** Milestone definition, sequencing, target dates, dependency chains between milestones, status tracking; identify milestones that are at risk or blocked

> **Verify:** Every milestone has a status and target date; dependency chains have no cycles; no milestone is blocked without a corresponding issue or concern

The rules, one per clause, named here; the names are fixed from here on:

1. **define-and-sequence-milestones** (no RFC keyword; section *Worker Focus*): "Milestone definition, sequencing, target dates, dependency chains between milestones, status tracking"
2. **identify-at-risk-or-blocked-milestones** (no RFC keyword; section *Worker Focus*): "identify milestones that are at risk or blocked"
3. **milestone-has-status-and-target-date** (no RFC keyword; section *Verify*): "Every milestone has a status and target date"
4. **milestone-chains-have-no-cycles** (no RFC keyword; section *Verify*): "dependency chains have no cycles"
5. **blocked-milestone-has-issue-or-concern** (no RFC keyword; section *Verify*): "no milestone is blocked without a corresponding issue or concern"
