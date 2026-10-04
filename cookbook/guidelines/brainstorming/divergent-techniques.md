---
id: 17d2fa7e-0a8e-4ce7-96a0-de417db82220
title: "Divergent Techniques"
domain: agenticdevelopercookbook://guidelines/brainstorming/divergent-techniques
type: guideline
version: 1.0.1
status: draft
language: en
created: 2026-06-27
modified: 2026-10-03
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Concrete generation techniques for the Diverge phase. Goal is volume, variety, and surprise — not quality or feasibility. Feasibility assessment belongs in the Critique phase."
platforms: []
tags:
  - brainstorming
  - divergence
  - ideation
depends-on:
  - agenticdevelopercookbook://principles/defer-judgment-go-for-quantity
  - agenticdevelopercookbook://principles/counteract-homogenization-with-diversity
  - agenticdevelopercookbook://principles/bridge-distant-domains
  - agenticdevelopercookbook://principles/constraints-as-creative-fuel
  - agenticdevelopercookbook://principles/break-fixation-deliberately
related:
  - agenticdevelopercookbook://guidelines/brainstorming/framing-techniques
  - agenticdevelopercookbook://guidelines/brainstorming/facilitation-without-anchoring
references:
  - Osborn, Applied Imagination, 1953
  - IDEO, 7 Simple Rules of Brainstorming
  - "Eberle, SCAMPER: Games for Imagination Development, 1971"
  - van Gundy, Techniques of Structured Problem Solving, 1988
  - "de Bono, Lateral Thinking: Creativity Step by Step, 1970"
  - Fauconnier & Turner, The Way We Think, 2002
  - Mednick, Psychological Review, 1962
triggers: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-03"
---

# Divergent Techniques

Concrete generation techniques for the Diverge phase. Goal is volume, variety, and surprise —
not quality or feasibility. Feasibility assessment belongs in the Critique phase.

## Wild Ideation

Quantity-over-quality generation without constraint.

- **wild-ideation-human-first**: The user MUST contribute at least one idea before the AI
  contributes any.
- **wild-ideation-volume-target**: Facilitator SHOULD aim for ≥10 distinct ideas before signaling
  readiness to evaluate.

## Distant Analogy

Structural pattern import from far domains.

- **distant-analogy-domain-gap**: Analogy source domain MUST be different in industry, domain, or
  scale from the user's domain.
- **distant-analogy-mapping**: After surfacing the analogy, facilitator MUST identify the
  structural match ("In X, Y solves Z because... In your problem, the equivalent of Y would be...").

## Conceptual Blending

Merging two input spaces to produce emergent properties.

- **blend-emergent-property**: Facilitator MUST describe at least one emergent property the blend
  produces that neither input space possesses alone.
- **blend-invite-user**: Facilitator SHOULD invite the user to name the emergent property before
  supplying it.

## Surprising Inversion

Reversing an assumption to surface novel directions.

- **inversion-identify-assumption**: Facilitator MUST state the assumption being inverted before
  inverting it.
- **inversion-explore**: After inversion, facilitator MUST ask "What would actually be valuable
  about this reversed version?" before discarding it.

## Constraint Injection

Strategic constraint introduction to redirect stuck thinking.

- **constraint-framed-as-question**: Constraint injection MUST be framed as a question ("What if
  you could only...?"), not a directive.
- **constraint-user-choice**: The user MUST be offered the choice to accept, modify, or reject the
  injected constraint.

## Reverse Brainstorm

"How to guarantee failure."

- **reverse-inversion-required**: The inversion step ("what does this failure mode tell us about
  how to succeed?") MUST follow the failure-generation step; stopping at failure generation without
  inverting is incomplete.
- **reverse-distinct-mechanisms**: Failure generation SHOULD produce at least 5 distinct failure
  mechanisms before inverting.

## SCAMPER

Substitute, Combine, Adapt, Modify/Magnify, Put-to-another-use, Eliminate, Reverse.

- **scamper-axis-limit**: Facilitator MUST NOT apply more than 2 SCAMPER axes in a single turn to
  avoid overwhelm.
- **scamper-one-idea**: Each SCAMPER axis MUST be applied to one specific idea, not to the problem
  in general.

## Random Stimulus

Lateral-thinking random entry.

- **random-stimulus-forced-connection**: After introducing the random word or object, facilitator
  MUST prompt "What does this make you think of, applied to your problem?" before suggesting
  connections.
- **random-stimulus-novel**: The random stimulus MUST be unrelated to the user's domain.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Mike Fullerton | Initial creation |
| 1.0.1 | 2026-10-03 | Mike Fullerton | Quote two references whose colons made YAML read them as mappings |
