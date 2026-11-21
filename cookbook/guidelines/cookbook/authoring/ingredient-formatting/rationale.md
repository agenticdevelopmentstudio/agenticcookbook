
- `if-section-order`, `short-required-core-labelled-optional-rest`: specification style guides and design-system templates fix an order of named sections so readers and tools can navigate them, but RFC 7322 only strongly recommends its order inside the body, the RFC series and the ACT Rules Format require only a short core, and an experienced design-doc author warns that a template serves clarity, not the other way round.
- `inapplicable-section-stated-not-omitted`: IANA asks that a section with nothing to say be kept and say so, so that a later reader can tell a deliberate "none" from a section that was simply left out; Apple and Google Play do the same for platforms and data collection.
- `per-platform-target-sizes`, `tmpl-accessibility-min-tap-target`: the platforms disagree on the minimum target (Apple by platform, Android 48dp, Windows 40px, WCAG 24px at AA), so one value is wrong for most of them.
- `deep-links-use-verified-https-links`: Apple strongly recommends universal links over custom URL schemes, which are a potential attack vector; Android recommends App Links.
- `analytics-event-names-fit-platform-limits`: Firebase Analytics accepts only letters, digits and underscores in an event name, so a dotted name is invalid there.
- `test-vectors-cover-pass-fail-inapplicable`, `compliance-status-includes-inapplicable`: W3C's ACT and EARL outcome vocabularies include "inapplicable", so a check that cannot apply is not reported as a pass.
- `section-structure-machine-checked`: a structural check a tool can decide (headings, required fields, order) need not be left to a reader, though MD043 alone cannot name an optional heading.
- `released-version-immutable`: Semantic Versioning forbids changing a released version, so every reader of a version sees the same text.

