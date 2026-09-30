<!-- leaf: compliance/performance · source: compliance/performance.md -->

**Rules** (cite as `compliance/performance#<slug>`):

- `ui-updates-rendering-not-block-main-thread` MUST — UI updates and rendering MUST NOT block the main thread.
- `animations-target-60fps-frames-exceed` MUST — Animations MUST target 60fps; frames MUST NOT exceed 16ms.
- `sets-heavy-resources-use-lazy-loading-pagination` MUST — Large data sets and heavy resources MUST use lazy loading or pagination.
- `components-minimize-memory-allocations-cpu` MUST — Components MUST minimize memory allocations and CPU usage during idle states.
- `components-not-add-measurable-delay-app` MUST — Components MUST NOT add measurable delay to app startup.
- `images-appropriately-sized-compressed-use` MUST — Images MUST be appropriately sized, compressed, and use platform-preferred formats.
- `accessed-remote-data-use-caching-strategy-defined` SHOULD — Frequently accessed remote data SHOULD use a caching strategy with defined invalidation.
- `operations-exceeding-200ms-show-progress-indication` MUST — Operations exceeding 200ms MUST show progress indication.

# Performance Compliance

Performance compliance ensures that implementations remain responsive, efficient, and resource-conscious across all platforms. These checks cover main-thread discipline, animation smoothness, data loading strategies, memory and CPU usage, startup impact, image handling, caching, and user-perceived latency.

## Applicability

This category applies to any recipe or guideline that renders UI, loads data, displays images, manages long-lived components, or performs work during app startup. If a recipe affects what the user sees or how quickly they see it, these checks apply.

## Checks

### main-thread-freedom

UI updates and rendering MUST NOT block the main thread.

**Applies when:** recipe performs computation, I/O, or network calls alongside UI rendering.

**Guidelines:**
- Concurrency

---

### animation-frame-rate

Animations MUST target 60fps; frames MUST NOT exceed 16ms.

**Applies when:** recipe includes animations, transitions, or motion effects.

**Guidelines:**
- Animation and Motion

---

### lazy-loading

Large data sets and heavy resources MUST use lazy loading or pagination.

**Applies when:** recipe displays lists, grids, or collections of unbounded size.

**Guidelines:**
- Data Display
- Pagination

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
- Caching

---

### progress-indication

Operations exceeding 200ms MUST show progress indication.

**Applies when:** recipe performs operations that may take a noticeable amount of time.

**Guidelines:**
- Always Show Progress
