<!-- leaf: compliance/privacy-and-data · source: compliance/privacy-and-data.md -->

**Rules** (cite as `compliance/privacy-and-data#<slug>`):

- `components-collect-only-minimum-data` MUST — Components MUST collect only the minimum data necessary for their functionality.
- `personal-data-collection-preceded-informed-user-consent` MUST — Personal data collection MUST be preceded by informed user consent.
- `personal-sensitive-data-stored-using-platform-specific` MUST — Personal and sensitive data MUST be stored using platform-specific secure storage.
- `personally-identifiable-information-not-appear-log-output-level` MUST — Personally identifiable information MUST NOT appear in log output at any level.
- `handling-personal-data-define-retention-duration-deletion` MUST — Components handling personal data MUST define retention duration and deletion behavior.
- `users-able-export-their-personal` SHOULD — Users SHOULD be able to export their personal data in a standard format.
- `sharing-third-parties-disclosed-require-user-consent` MUST — Data sharing with third parties MUST be disclosed and require user consent.
- `data-stored-locally-encrypted-rest` MUST — Sensitive data stored locally MUST be encrypted at rest.

# Privacy and Data

Compliance checks that govern how components collect, store, transmit, and process personal and sensitive data. These checks ensure respect for user privacy, compliance with data protection principles, and responsible data stewardship.

## Applicability

Any recipe or guideline that collects, stores, transmits, or processes personal or sensitive data.

## Checks

### data-minimization

Components MUST collect only the minimum data necessary for their functionality.

**Applies when:** a component requests, collects, or stores user data.

**Guidelines:**
- Privacy

---

### consent-before-collection

Personal data collection MUST be preceded by informed user consent.

**Applies when:** a component collects personal or identifiable information from the user.

**Guidelines:**
- Privacy

---

### secure-data-storage

Personal and sensitive data MUST be stored using platform-specific secure storage.

**Applies when:** a component persists personal or sensitive data locally or remotely.

**Guidelines:**
- Secure Storage
- Sensitive Data

---

### no-pii-in-logs

Personally identifiable information MUST NOT appear in log output at any level.

**Applies when:** a component writes log output and has access to personal data.

**Guidelines:**
- Sensitive Data
- Logging

---

### data-retention-policy

Components handling personal data MUST define retention duration and deletion behavior.

**Applies when:** a component stores personal data beyond the current session.

**Guidelines:**
- Privacy

---

### data-portability

Users SHOULD be able to export their personal data in a standard format.

**Applies when:** a component stores significant amounts of user-generated or personal data.

**Guidelines:**
- Privacy

---

### third-party-disclosure

Data sharing with third parties MUST be disclosed and require user consent.

**Applies when:** a component transmits user data to external services or analytics providers.

**Guidelines:**
- Privacy

---

### encryption-at-rest

Sensitive data stored locally MUST be encrypted at rest.

**Applies when:** a component persists sensitive data to the local filesystem or database.

**Guidelines:**
- Sensitive Data
- Secure Storage
