<!-- leaf: ship-general/incident-response · source: guidelines/shipping/incident-response.md -->

**Rules** (cite as `ship-general/incident-response#<slug>`):

- `incident-commander` MUST
- `communications-lead` SHOULD
- `operations-lead` SHOULD
- `incidents-one-person-hold-roles-severity-rises` MUST — For small incidents one person MAY hold all roles; as severity rises, roles MUST be split across people.
- `ic-role-explicitly-handed-off-implicitly` MUST — The IC role MUST be explicitly handed off (not implicitly dropped) at shift boundaries or when the holder steps away.
- `declaration-scale-response-re-evaluate-understanding-changes` MUST — Classify severity at declaration to scale the response, and MUST re-evaluate as understanding changes. Use a small …
- `severity-map-concrete-actions-who` MUST — Severity MUST map to concrete actions (who is paged, who is notified, update cadence) — a label with no behavior …
- `impact-data-loss-get-written-postmortem-org` MUST — A significant incident (e.g., SEV1/SEV2, or any with customer impact or data loss) SHOULD get a written postmortem; an …
- `postmortems-blameless-focus-contributing-systemic` MUST — Postmortems MUST be blameless: focus on contributing systemic and process factors, not on naming individuals at fault. …
- `postmortem-record-timeline-detection-method` MUST — Each postmortem MUST record: timeline, detection method, user impact, root/contributing causes, and what went well and …
- `remediation-items-concrete-owned-tracked-normal` MUST — Remediation items MUST be concrete, owned, and tracked in the normal work backlog (issues/tickets) — MUST NOT live only …
- `action-items-tracked-closure-same-rigor` SHOULD — Action items SHOULD be tracked to closure with the same rigor as feature work; a postmortem whose items never close has …
- `postmortem-shared-widely-circulating-real` MAY — A postmortem MAY be shared widely; circulating real ones builds the reflex and removes stigma.
- `call-load-bounded-so-single-shift` SHOULD — On-call load SHOULD be bounded so a single shift is not flooded; an established cap is no more than ~2 significant …
- `call-compensated-time-off-pay` MUST — On-call MUST be compensated (time off or pay) and SHOULD rotate across a team large enough to avoid burnout.
- `toil-drove-paging-feed-back-into-postmortem` SHOULD — Toil that drove paging SHOULD feed back into postmortem action items rather than being silently absorbed.

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
