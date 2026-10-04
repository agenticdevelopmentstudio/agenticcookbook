---
id: 2041fbd9-d210-485e-9a3a-b2d8295ed924
title: "Incident response and blameless postmortems"
domain: agenticdevelopercookbook://guidelines/shipping/incident-response
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Run production incidents with defined command roles and severity tiers, then close them with blameless, tracked-to-completion postmortems."
platforms: []
tags:
  - operations
  - sre
  - reliability
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/observability/service-level-objectives
references:
  - https://sre.google/sre-book/managing-incidents/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - pre-pr
---

# Incident response and blameless postmortems

In-code error recovery stops at the process boundary; production incidents need an operational response on top of it. This guideline covers the durable practices: command roles, severity classification, blameless postmortems, and sustainable on-call.

## Incident command roles

Separate *coordinating* the response from *doing* the work so neither starves the other. The roles below follow the established Incident Management At Google (IMAG) model; adapt names to your org but keep the separation.

- **incident-commander**: One person **MUST** hold overall coordination of a declared incident. The IC decides, delegates, and owns the response — they do not also debug.
- **communications-lead**: For higher-severity incidents a CL **SHOULD** own stakeholder and customer updates so the IC and responders are not interrupted.
- **operations-lead**: One or more responders **SHOULD** own mitigation and investigation, reporting to the IC.
- For small incidents one person **MAY** hold all roles; as severity rises, roles **MUST** be split across people.
- The IC role **MUST** be explicitly handed off (not implicitly dropped) at shift boundaries or when the holder steps away.

## Severity classification

Classify severity at declaration to scale the response, and **MUST** re-evaluate as understanding changes. Use a small fixed ladder; exact thresholds are org-specific.

| Severity | Rough meaning | Typical response |
|----------|---------------|------------------|
| SEV1 | Major outage / data loss / broad customer impact | Full roles, immediate page, exec/comms notified |
| SEV2 | Significant degradation or partial outage | IC + ops lead, page on-call |
| SEV3 | Minor / contained impact, workaround exists | On-call handles, no full mobilization |

- Severity **MUST** map to concrete actions (who is paged, who is notified, update cadence) — a label with no behavior attached is noise.
- Tie thresholds to SLO error budgets where they exist (see related) rather than to gut feel.

## Blameless postmortems

- A significant incident (e.g., SEV1/SEV2, or any with customer impact or data loss) **SHOULD** get a written postmortem; an org **MUST** have a clear threshold defining "significant."
- Postmortems **MUST** be blameless: focus on contributing systemic and process factors, not on naming individuals at fault. Blame suppresses the honest reporting that prevents recurrence.
- Each postmortem **MUST** record: timeline, detection method, user impact, root/contributing causes, and what went well and poorly.
- Remediation items **MUST** be concrete, owned, and tracked in the normal work backlog (issues/tickets) — **MUST NOT** live only inside the postmortem document.
- Action items **SHOULD** be tracked to closure with the same rigor as feature work; a postmortem whose items never close has no value.
- A postmortem **MAY** be shared widely; circulating real ones builds the reflex and removes stigma.

## Sustainable on-call

- On-call load **SHOULD** be bounded so a single shift is not flooded; an established cap is no more than ~2 significant incidents per 12-hour on-call shift, which preserves time for careful response.
- On-call **MUST** be compensated (time off or pay) and **SHOULD** rotate across a team large enough to avoid burnout.
- Toil that drove paging **SHOULD** feed back into postmortem action items rather than being silently absorbed.

## Forecast and caveats

- Specific tooling (paging vendors, ChatOps incident bots, AI-assisted triage and summarization) evolves quickly — treat any named product as an example, not a requirement. The role/severity/postmortem structure is the durable part.
- AI-assisted incident summarization and correlation are increasingly common as of 2026; treat their output as a draft for a human responder, not as the authority — keep a human IC accountable.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
