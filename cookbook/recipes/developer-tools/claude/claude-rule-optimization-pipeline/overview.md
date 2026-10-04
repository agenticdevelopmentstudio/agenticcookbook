
Claude Code rule files in `.claude/rules/` are injected into the system prompt on every turn — not just at session start. A 200-line rule costs 200 lines × N turns per session. The agenticdevelopercookbook's own rules went from 381 lines / 17,689 bytes per turn to 10 lines / 358 bytes — a 97% reduction — by applying a systematic optimization pipeline.

This recipe codifies that pipeline into four repeatable phases:

1. **Audit** — inventory rules, measure per-turn cost, detect waste
2. **Optimize** — propose and apply context-reduction strategies
3. **Validate** — verify behavioral preservation and run lint checks
4. **Report** — produce before/after metrics

The pipeline is sequential: each phase gates the next. Phase 2 (Optimize) requires explicit user confirmation before modifying any files — rule files are behavioral guardrails and MUST NOT be changed autonomously.

