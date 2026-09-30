<!-- leaf: story-general/grounded-synthesis · source: guidelines/storytelling/grounded-synthesis.md -->

**Rules** (cite as `story-general/grounded-synthesis#<slug>`):

- `gs-ground-every-claim` MUST
- `gs-refuse-ungrounded` MUST
- `gs-dossier-is-the-lever` MUST
- `gs-high-signal` SHOULD

# Grounded Synthesis

The narrator turns gathered material (commit history, docs, Claude memories, cross-references) into a told story. The whole discipline rests on grounding: the LLM writes only what the evidence supports.

## Ground Every Claim
- **gs-ground-every-claim**: Every assertion in a story MUST be traceable to the gathered dossier; the narrator MUST invent no facts.
- **gs-refuse-ungrounded**: When the evidence does not support a claim, the narrator MUST refuse to assert it rather than fabricate a bridge. Refusing an ungrounded link is correct behavior, not a failure.

## The Dossier Is The Lever
- **gs-dossier-is-the-lever**: Story quality MUST be improved by enriching the dossier (better gather, less truncation), NOT by loosening the grounding rule or embellishing the prompt.
- **gs-high-signal**: The dossier SHOULD be compact and high-signal; low-signal padding dilutes grounding and crowds out the material that matters.
