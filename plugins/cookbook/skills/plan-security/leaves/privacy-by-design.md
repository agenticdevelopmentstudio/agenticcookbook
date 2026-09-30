<!-- leaf: plan-security/privacy-by-design · source: guidelines/planning/security/privacy-by-design.md -->

**Rules** (cite as `plan-security/privacy-by-design#<slug>`):

- `writing-code-you-produce-personal-data-flow` MUST — Before writing code, you MUST produce a personal-data flow map and treat it as a maintained artifact, not a throwaway …
- `map-updated-fields-processors-destinations` MUST — The map MUST be updated when fields, processors, or destinations change.
- `you-flag-data-stated-purpose` SHOULD — You SHOULD flag any data with no stated purpose as a candidate for removal.
- `you-run-data-protection-impact` SHOULD — You SHOULD run a Data Protection Impact Assessment (DPIA) before building any high-risk processing — large-scale …
- `dpia-identify-risks-individuals-mitigations` MUST — The DPIA MUST identify risks to individuals and the mitigations applied, and SHOULD be revisited when the processing …
- `cannot-mitigate-you-escalate-rather-than-ship` MUST — If a DPIA surfaces a residual high risk you cannot mitigate, you MUST escalate rather than ship silently.
- `stated-purpose-you-not-collect-data-just-case` MUST — Collect the minimum data necessary for the stated purpose — you MUST NOT collect data "just in case."
- `you-pseudonymize-anonymize-wherever-use` SHOULD — You SHOULD pseudonymize or anonymize wherever the use case allows; prefer true anonymization (irreversible) when no …
- `you-keep-raw-identifiers-out` SHOULD — You SHOULD keep raw identifiers out of logs, analytics, and AI prompts; hash, tokenize, or redact before they leave the …
- `retention-up-front-delete-de-identify-data` MUST — Define retention up front and MUST delete or de-identify data when its purpose ends.
- `out-box-configuration-most-privacy-protective` MUST — Per GDPR Article 25 (privacy by *default*), the out-of-the-box configuration MUST be the most privacy-protective:
- `visibility-broad-processing-opt-opt-out` MUST — Sharing, public visibility, and broad processing MUST be opt-in, not opt-out.
- `optional-telemetry-tracking-default-off` MUST — Optional telemetry and tracking MUST default to off.
- `access-follow-least-privilege-only` SHOULD — Access SHOULD follow least privilege: only the roles that need a data category can read it.

# Privacy by design

Build privacy into the system from the first design decision, not as a later bolt-on. This is the privacy lens of threat modeling: enumerate how personal data flows, minimize what you touch, and default to the most protective option. This guidance is engineering practice, **NOT** legal advice — consult counsel for jurisdiction-specific obligations.

## Make the data-flow map a first-class artifact

Before writing code, you **MUST** produce a personal-data flow map and treat it as a maintained artifact, not a throwaway sketch. For each category of personal data, record:

| Dimension | Question to answer |
|-----------|-------------------|
| What | Which personal data is collected (including derived/inferred data)? |
| Why | What specific, documented purpose justifies it? |
| Where | Where does it travel, rest, and replicate (services, regions, third parties)? |
| How long | What is the retention period and deletion mechanism? |

- The map **MUST** be updated when fields, processors, or destinations change.
- You **SHOULD** flag any data with no stated purpose as a candidate for removal.

## Assess high-risk processing

- You **SHOULD** run a Data Protection Impact Assessment (DPIA) before building any high-risk processing — large-scale sensitive data, systematic monitoring, profiling, or automated decisions with legal/significant effects.
- The DPIA **MUST** identify risks to individuals and the mitigations applied, and **SHOULD** be revisited when the processing materially changes.
- If a DPIA surfaces a residual high risk you cannot mitigate, you **MUST** escalate rather than ship silently.

## Minimize and de-identify

- Collect the **minimum** data necessary for the stated purpose — you **MUST NOT** collect data "just in case."
- You **SHOULD** pseudonymize or anonymize wherever the use case allows; prefer true anonymization (irreversible) when no re-identification is needed, and pseudonymization (keyed, reversible) otherwise.
- You **SHOULD** keep raw identifiers out of logs, analytics, and AI prompts; hash, tokenize, or redact before they leave the trusted boundary.
- Define retention up front and **MUST** delete or de-identify data when its purpose ends.

## Default to the most private option

Per GDPR Article 25 (privacy by *default*), the out-of-the-box configuration **MUST** be the most privacy-protective:

- Sharing, public visibility, and broad processing **MUST** be opt-in, not opt-out.
- Optional telemetry and tracking **MUST** default to off.
- Access **SHOULD** follow least privilege: only the roles that need a data category can read it.

## Adopt heavier controls only when justified

Privacy-enhancing infrastructure (dedicated tokenization vaults, differential-privacy pipelines, confidential-compute enclaves, per-tenant key management) adds real cost and operational drag. Per YAGNI, adopt these **only when a measured need justifies them** — driven by data sensitivity, regulatory scope, or DPIA findings — not as a reflexive default. Start with minimization and de-identification; escalate to specialized tooling when the risk profile demands it.
