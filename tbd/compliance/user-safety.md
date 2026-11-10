---
id: B8ABAA15-35E6-4C51-9735-9A405CC7336C
title: "User Safety Compliance"
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for content moderation, age gating, abuse prevention, and safe defaults."
platforms: []
tags: [compliance, user-safety]
depends-on: []
related:
  - tbd/compliance/security.md
  - tbd/compliance/privacy-and-data.md
  - tbd/compliance/platform-compliance.md
references: []
---

# User Safety Compliance

User safety compliance ensures that features protect users from harmful content, abuse, and unsafe defaults. These checks apply to any recipe that displays, generates, or accepts user-contributed content, as well as features whose configuration choices can affect user wellbeing.

## Applicability

This category applies to recipes and guidelines that involve user-generated content, content display or generation, social features, configurable behavior with safety implications, or content targeting specific age groups.

## Checks

### content-moderation

User-generated content MUST be moderated before public display.

**Applies when:** recipe accepts and displays content submitted by users.

**Guidelines:**
- [adc.guideline.implementing.security.input-validation](cookbook:4ca8a3d5-cdcc-4f74-a2ec-3a198608b419)

---

### age-appropriate-content

Content MUST be classified and gated per platform age-rating requirements.

**Applies when:** recipe displays or generates content that may not be suitable for all ages.

---

### abuse-prevention

User-facing input surfaces MUST implement rate limiting and abuse prevention measures.

**Applies when:** recipe exposes input fields, forms, or APIs to end users.

**Guidelines:**
- [adc.guideline.implementing.networking.rate-limiting](cookbook:c84400d9-83b3-4c4c-83d4-325dfa989202)
- [adc.guideline.implementing.security.input-validation](cookbook:4ca8a3d5-cdcc-4f74-a2ec-3a198608b419)

---

### harmful-content-filtering

Content pipelines MUST filter harmful, illegal, or policy-violating material.

**Applies when:** recipe processes, transforms, or displays content from external or user sources.

**Guidelines:**
- [adc.guideline.implementing.security.input-validation](cookbook:4ca8a3d5-cdcc-4f74-a2ec-3a198608b419)

---

### reporting-mechanism

Features with user-generated content SHOULD provide a mechanism to report problematic content.

**Applies when:** recipe includes UGC or social features.

---

### safe-defaults

Features MUST default to the safest configuration; riskier options require explicit opt-in.

**Applies when:** recipe has configurable behavior affecting user safety.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
