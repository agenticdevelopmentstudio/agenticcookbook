# Research brief: dependency-tracking

- **Area:** `planning/project-management`
- **Topic:** `dependency-tracking` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/planning/project-management/dependency-tracking`
- **Base commit:** `f0dd450e1188364e9e221d912d49657944ae46ad` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain cross-team delivery dependencies; method standards bodies and practitioner sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner approval 2026-11-24, Owner questions 1 and 4).
  Any metric claim (a review cadence, a task size or a schedule accuracy backed by a study or survey) takes the
  *Statistical* bar of `guidelines/researching/process/research-methodology-and-sources`: name the study, its
  sample, its measure and its result, and score it on that bar.

## The topic

How a delivery team maps and tracks the delivery dependencies it waits on (other teams, vendors, tasks, decisions; internal and external): each dependency's type, owner, status and need-by date, how one at risk or blocked is flagged and escalated before it delays a milestone.

The cookbook states general practice for any delivery team, not projectteam's: projectteam's `.dev-team-project/`
paths, its file formats and its specialist names stay in projectteam and are not researched.

**Not this topic's:**

- Software dependencies (libraries, OS frameworks) are `planning/code-quality/system-dependencies` and `implementing/security/dependency-security`'s, not this topic's: this topic is about delivery dependencies between teams, vendors, tasks, decisions and milestones.
- Milestone dependency chains, cycle detection and the critical path are `milestone-scheduling`'s; the general linking convention between records is `project-record-linking`'s.

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

1. Best practice: how should a delivery team map and track its dependencies on other teams, vendors, tasks and decisions: internal versus external, each with a type, an owner, a status and a need-by date?
2. Known solutions: how do dependency boards, SAFe's program board, RAID logs and the dependency links of Jira, Linear and GitHub Projects compare for tracking delivery dependencies?
3. Platform guidelines: what do the PMBOK Guide's schedule and stakeholder guidance, PRINCE2 and the scaled-agile frameworks (SAFe, LeSS) say about recording and managing dependencies between teams?
4. The expert's view: what do delivery leads say teams get wrong with dependencies (found late, no owner on the other side, status never updated), and what to do instead?
5. **Blocked dependency flagging**: find how teams mark a dependency at risk or blocked and escalate it before it delays a milestone, and state the status values a dependency carries and when a blocked one is escalated.

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
  `source_type` `prior cookbook text`, its one citation `title` `dependency-tracking (teams/projectteam/specialities/project/dependencies.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:736232c055d56077e7e1bc03e7e1accf7173a87f:teams/projectteam/specialities/project/dependencies.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/projectteam/specialities/project/dependencies.md` in the teams repo at commit `736232c055d56077e7e1bc03e7e1accf7173a87f` (projectteam's
compiled speciality; the cookbook base commit is `f0dd450e1188364e9e221d912d49657944ae46ad`), as a claim to check, never as a source.
The file's two sections, whole, for context:

> **Worker Focus:** Internal and external dependency mapping; track availability and status of each dependency; flag at-risk or blocked dependencies that could affect milestones

> **Verify:** Every dependency has a type and status; blocked or at-risk dependencies are linked to affected milestones or todos

The rules, one per clause, named here; the names are fixed from here on:

1. **map-internal-and-external-dependencies** (no RFC keyword; section *Worker Focus*): "Internal and external dependency mapping"
2. **track-dependency-availability-and-status** (no RFC keyword; section *Worker Focus*): "track availability and status of each dependency"
3. **flag-at-risk-or-blocked-dependencies** (no RFC keyword; section *Worker Focus*): "flag at-risk or blocked dependencies that could affect milestones"
4. **dependency-has-type-and-status** (no RFC keyword; section *Verify*): "Every dependency has a type and status"
5. **blocked-dependency-linked-to-affected-work** (no RFC keyword; section *Verify*): "blocked or at-risk dependencies are linked to affected milestones or todos"
