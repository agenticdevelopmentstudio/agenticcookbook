---
id: 0bfc8dc6-94ac-4bf4-8601-621ee9086487
title: "Grounded Synthesis"
domain: agenticdevelopercookbook://guidelines/storytelling/grounded-synthesis
type: guideline
version: 1.0.1
status: draft
language: en
created: 2026-06-29
modified: 2026-10-03
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Tell a project's story by synthesizing a high-signal dossier and grounding every claim in it — invent nothing; improve quality by enriching the dossier, not by loosening the grounding rule."
platforms: []
tags:
  - storytelling
  - grounding
  - narrative
related:
  - agenticdevelopercookbook://guidelines/storytelling/narrative-arc
  - agenticdevelopercookbook://guidelines/storytelling/ecosystem
  - agenticdevelopercookbook://guidelines/storytelling/positioning
triggers: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-03"
depends-on: []
references: []
---

# Grounded Synthesis

The narrator turns gathered material (commit history, docs, Claude memories, cross-references) into a told story. The whole discipline rests on grounding: the LLM writes only what the evidence supports.

## Ground Every Claim
- **gs-ground-every-claim**: Every assertion in a story MUST be traceable to the gathered dossier; the narrator MUST invent no facts.
- **gs-refuse-ungrounded**: When the evidence does not support a claim, the narrator MUST refuse to assert it rather than fabricate a bridge. Refusing an ungrounded link is correct behavior, not a failure.

## The Dossier Is The Lever
- **gs-dossier-is-the-lever**: Story quality MUST be improved by enriching the dossier (better gather, less truncation), NOT by loosening the grounding rule or embellishing the prompt.
- **gs-high-signal**: The dossier SHOULD be compact and high-signal; low-signal padding dilutes grounding and crowds out the material that matters.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-29 | Mike Fullerton | Initial creation |
| 1.0.1 | 2026-10-03 | Mike Fullerton | Add the missing Change History section |
