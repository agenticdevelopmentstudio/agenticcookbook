---
id: 09b063bd-74e7-4636-baa6-23ee82ec224b
title: "Privacy by design"
domain: agenticdevelopercookbook://guidelines/planning/security/privacy-by-design
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Map personal-data flows, minimize collection, default to the most private setting, and run a DPIA before building high-risk processing."
platforms: []
tags:
  - privacy
  - design
  - compliance
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/planning/security/threat-modeling
  - agenticdevelopercookbook://guidelines/planning/security/data-privacy-regulations
references:
  - https://gdpr-info.eu/art-25-gdpr/
  - https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42019-article-25-data-protection-design-and_en
  - https://gdpr-info.eu/art-35-gdpr/
  - https://www.nist.gov/privacy-framework
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - security-review
  - data-modeling
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add EDPB Art.25 guidelines, GDPR Art.35, NIST Privacy Framework |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
