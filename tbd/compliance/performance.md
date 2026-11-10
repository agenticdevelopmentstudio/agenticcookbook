---
id: 4325D8FF-ECB5-460B-836E-4F55309F2DC0
title: "Performance Compliance"
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for main-thread responsiveness, frame rates, lazy loading, and resource efficiency."
platforms: []
tags: [compliance, performance]
depends-on: []
related:
  - tbd/compliance/reliability.md
  - tbd/compliance/accessibility.md
  - tbd/compliance/access-patterns.md
references: []
---

# Performance Compliance

Performance compliance ensures that implementations remain responsive, efficient, and resource-conscious across all platforms. These checks cover main-thread discipline, animation smoothness, data loading strategies, memory and CPU usage, startup impact, image handling, caching, and user-perceived latency.

## Applicability

This category applies to any recipe or guideline that renders UI, loads data, displays images, manages long-lived components, or performs work during app startup. If a recipe affects what the user sees or how quickly they see it, these checks apply.

## Checks

### main-thread-freedom

UI updates and rendering MUST NOT block the main thread.

**Applies when:** recipe performs computation, I/O, or network calls alongside UI rendering.

**Guidelines:**
- [adc.guideline.implementing.concurrency.concurrency](cookbook:6302654b-8200-4e03-862d-4734d4960d19)

---

### animation-frame-rate

Animations MUST target 60fps; frames MUST NOT exceed 16ms.

**Applies when:** recipe includes animations, transitions, or motion effects.

**Guidelines:**
- [adc.guideline.implementing.ui.animation-motion](cookbook:9f13dbec-cecb-482b-824b-f7d3e341878a)

---

### lazy-loading

Large data sets and heavy resources MUST use lazy loading or pagination.

**Applies when:** recipe displays lists, grids, or collections of unbounded size.

**Guidelines:**
- [adc.guideline.implementing.ui.data-display](cookbook:704fef7e-0e8d-480c-8019-cf84b5fd851b)
- [adc.guideline.implementing.networking.pagination](cookbook:49acdf9f-e4cb-4492-a620-809438eefb37)

---

### resource-efficiency

Components MUST minimize memory allocations and CPU usage during idle states.

**Applies when:** recipe defines a long-lived component.

---

### startup-impact

Components MUST NOT add measurable delay to app startup.

**Applies when:** recipe is loaded at launch.

---

### image-optimization

Images MUST be appropriately sized, compressed, and use platform-preferred formats.

**Applies when:** recipe displays images.

---

### caching-strategy

Frequently accessed remote data SHOULD use a caching strategy with defined invalidation.

**Applies when:** recipe fetches data from a remote source that is accessed repeatedly.

**Guidelines:**
- [adc.guideline.implementing.networking.caching](cookbook:3416a359-e01c-40b2-8876-4a8634d4395e)

---

### progress-indication

Operations exceeding 200ms MUST show progress indication.

**Applies when:** recipe performs operations that may take a noticeable amount of time.

**Guidelines:**
- [adc.guideline.implementing.ui.always-show-progress](cookbook:8d52028b-d358-4965-93a1-030fc8405068)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
