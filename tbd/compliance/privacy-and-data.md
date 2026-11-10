---
id: 8A9E6D0E-CC26-497C-867B-3171A0213F5A
title: "Privacy and Data"
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for data privacy, personal data handling, and secure storage."
platforms: []
tags: [compliance, privacy, data]
depends-on: []
related:
  - tbd/compliance/security.md
  - tbd/compliance/platform-compliance.md
  - tbd/compliance/user-safety.md
references: []
---

# Privacy and Data

Compliance checks that govern how components collect, store, transmit, and process personal and sensitive data. These checks ensure respect for user privacy, compliance with data protection principles, and responsible data stewardship.

## Applicability

Any recipe or guideline that collects, stores, transmits, or processes personal or sensitive data.

## Checks

### data-minimization

Components MUST collect only the minimum data necessary for their functionality.

**Applies when:** a component requests, collects, or stores user data.

**Guidelines:**
- [adc.guideline.implementing.security.privacy](cookbook:29057cf0-a38b-4c35-8b8b-52e12bf54784)

---

### consent-before-collection

Personal data collection MUST be preceded by informed user consent.

**Applies when:** a component collects personal or identifiable information from the user.

**Guidelines:**
- [adc.guideline.implementing.security.privacy](cookbook:29057cf0-a38b-4c35-8b8b-52e12bf54784)

---

### secure-data-storage

Personal and sensitive data MUST be stored using platform-specific secure storage.

**Applies when:** a component persists personal or sensitive data locally or remotely.

**Guidelines:**
- [adc.guideline.implementing.security.secure-storage](cookbook:926dff1a-dc12-46a4-b8c1-bdedbc142afd)
- [adc.guideline.implementing.security.sensitive-data](cookbook:22f1ca04-2d1d-4faf-8bf0-c6abcd60802c)

---

### no-pii-in-logs

Personally identifiable information MUST NOT appear in log output at any level.

**Applies when:** a component writes log output and has access to personal data.

**Guidelines:**
- [adc.guideline.implementing.security.sensitive-data](cookbook:22f1ca04-2d1d-4faf-8bf0-c6abcd60802c)
- [adc.guideline.implementing.observability.logging](cookbook:0f0c1da3-1c53-417b-890d-0259d7513c65)

---

### data-retention-policy

Components handling personal data MUST define retention duration and deletion behavior.

**Applies when:** a component stores personal data beyond the current session.

**Guidelines:**
- [adc.guideline.implementing.security.privacy](cookbook:29057cf0-a38b-4c35-8b8b-52e12bf54784)

---

### data-portability

Users SHOULD be able to export their personal data in a standard format.

**Applies when:** a component stores significant amounts of user-generated or personal data.

**Guidelines:**
- [adc.guideline.implementing.security.privacy](cookbook:29057cf0-a38b-4c35-8b8b-52e12bf54784)

---

### third-party-disclosure

Data sharing with third parties MUST be disclosed and require user consent.

**Applies when:** a component transmits user data to external services or analytics providers.

**Guidelines:**
- [adc.guideline.implementing.security.privacy](cookbook:29057cf0-a38b-4c35-8b8b-52e12bf54784)

---

### encryption-at-rest

Sensitive data stored locally MUST be encrypted at rest.

**Applies when:** a component persists sensitive data to the local filesystem or database.

**Guidelines:**
- [adc.guideline.implementing.security.sensitive-data](cookbook:22f1ca04-2d1d-4faf-8bf0-c6abcd60802c)
- [adc.guideline.implementing.security.secure-storage](cookbook:926dff1a-dc12-46a4-b8c1-bdedbc142afd)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
