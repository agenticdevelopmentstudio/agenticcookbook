
### Non-Contradiction

- **must-not-contradict-applicable-guidelines**: A recipe's behavioral requirements MUST NOT contradict any applicable cookbook guideline.
- **must-be-at-least-as-strict-as-guideline-musts**: Where a cookbook guideline establishes a MUST, the recipe's requirements MUST be at least as strict. A recipe MUST NOT relax a cross-cutting MUST to a SHOULD or MAY without an explicit documented exception approved by the cookbook maintainers.
- **must-satisfy-all-applicable-guidelines-together**: Where a recipe's domain intersects with multiple guidelines, all applicable guidelines MUST be satisfied simultaneously. Compliance with one guideline MUST NOT be used to justify non-compliance with another.

### Referencing Applicable Guidelines

- **should-cite-applicable-guidelines-in-frontmatter**: When a cookbook guideline directly applies to the recipe's domain, the recipe SHOULD cite the guideline in the `depends-on` or `references` frontmatter field.
- **should-reference-guideline-inline**: When a requirement in the recipe is derived from or constrained by a guideline, the requirement SHOULD include an inline reference (e.g., `per [adc.guideline.implementing.ui.touch-click-targets](cookbook:73b254b4-c611-434a-a9f4-67c8a7155576)`).
- **must-not-copy-guideline-content-without-attribution**: Authors MUST NOT silently incorporate guideline content without attribution. Duplicating guideline text verbatim into a recipe without reference creates maintenance drift when the guideline changes.

### Security-Relevant Recipes

- **must-include-security-section-when-security-relevant**: Any recipe whose subject matter involves authentication, authorization, session management, token handling, credential storage, or transmission of sensitive data MUST include a dedicated section or sub-section addressing the relevant security concerns.
- **must-address-minimum-security-concerns**: Security requirements MUST address at minimum: what data is considered sensitive in this context, how that data MUST be stored or transmitted, and what MUST happen when a security violation is detected.
- **must-specify-token-lifetimes-storage-revocation**: A security-relevant recipe MUST NOT leave token lifetimes, storage mechanisms, or revocation behavior unspecified.
- **must-not-defer-security-to-best-practices**: Security requirements MUST NOT defer entirely to "follow platform best practices" without citing specific practices.

### UI and Accessibility

- **must-address-accessibility-in-ui-recipes**: Any recipe whose subject matter involves a visible user interface element or user interaction flow MUST address accessibility.
- **must-cover-core-accessibility-requirements**: UI recipes MUST include requirements covering: keyboard and assistive technology navigation, minimum contrast ratios, touch/click target sizes, and meaningful labels for interactive controls.
- **must-not-make-required-accessibility-optional**: UI recipes MUST NOT treat accessibility as optional (MAY) when the relevant platform requires it by law or platform policy (e.g., WCAG 2.1 AA for web, Apple Human Interface Guidelines for iOS).
- **should-reference-accessibility-guideline**: UI recipes SHOULD reference the applicable accessibility guideline in the `depends-on` field.

### Networking and Error Handling

- **must-specify-network-failure-retry-and-errors**: Any recipe whose subject matter involves network requests, API calls, or external service communication MUST include requirements for: failure modes (timeout, unreachable host, unexpected status codes), retry behavior (including backoff strategy), and user-facing error communication.
- **must-not-make-routine-error-handling-should**: Networking recipes MUST NOT treat error handling as a SHOULD when failure is a routine operating condition (e.g., mobile networking).

### Data Persistence

- **must-specify-durability-guarantees**: Any recipe that writes to local storage, a database, or a file system MUST specify durability guarantees: what data survives an app restart, what is ephemeral, and under what conditions data may be lost.
- **must-specify-backup-and-conflict-resolution**: Recipes that handle user-generated content MUST specify whether and how data is backed up and how conflicts are resolved.

