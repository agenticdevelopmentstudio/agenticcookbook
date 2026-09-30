<!-- leaf: compliance/user-safety · source: compliance/user-safety.md -->

**Rules** (cite as `compliance/user-safety#<slug>`):

- `user-generated-content-moderated-before-public-display` MUST — User-generated content MUST be moderated before public display.
- `content-classified-gated-per-platform` MUST — Content MUST be classified and gated per platform age-rating requirements.
- `facing-input-surfaces-implement-rate-limiting-abuse` MUST — User-facing input surfaces MUST implement rate limiting and abuse prevention measures.
- `content-pipelines-filter-harmful-illegal-policy` MUST — Content pipelines MUST filter harmful, illegal, or policy-violating material.
- `user-generated-content-provide-mechanism-report-problematic` SHOULD — Features with user-generated content SHOULD provide a mechanism to report problematic content.
- `features-default-safest-configuration-riskier` MUST — Features MUST default to the safest configuration; riskier options require explicit opt-in.

# User Safety Compliance

User safety compliance ensures that features protect users from harmful content, abuse, and unsafe defaults. These checks apply to any recipe that displays, generates, or accepts user-contributed content, as well as features whose configuration choices can affect user wellbeing.

## Applicability

This category applies to recipes and guidelines that involve user-generated content, content display or generation, social features, configurable behavior with safety implications, or content targeting specific age groups.

## Checks

### content-moderation

User-generated content MUST be moderated before public display.

**Applies when:** recipe accepts and displays content submitted by users.

**Guidelines:**
- Input Validation

---

### age-appropriate-content

Content MUST be classified and gated per platform age-rating requirements.

**Applies when:** recipe displays or generates content that may not be suitable for all ages.

---

### abuse-prevention

User-facing input surfaces MUST implement rate limiting and abuse prevention measures.

**Applies when:** recipe exposes input fields, forms, or APIs to end users.

**Guidelines:**
- Rate Limiting
- Input Validation

---

### harmful-content-filtering

Content pipelines MUST filter harmful, illegal, or policy-violating material.

**Applies when:** recipe processes, transforms, or displays content from external or user sources.

**Guidelines:**
- Input Validation

---

### reporting-mechanism

Features with user-generated content SHOULD provide a mechanism to report problematic content.

**Applies when:** recipe includes UGC or social features.

---

### safe-defaults

Features MUST default to the safest configuration; riskier options require explicit opt-in.

**Applies when:** recipe has configurable behavior affecting user safety.
