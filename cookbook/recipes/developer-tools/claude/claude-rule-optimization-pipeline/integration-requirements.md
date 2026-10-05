
- **sequential-gating**: Phases MUST execute in order: 1 → 2 → 3 → 4. A phase MUST NOT start until the previous phase completes successfully.
- **human-gate-before-writes**: The pipeline MUST NOT modify any rule file without explicit user confirmation. Phases 1 and 4 are read-only. Phase 2 requires confirmation. Phase 3 re-validates after writes.
- **audit-findings-drive-proposals**: The rule optimizer MUST build its proposals only from the rule audit's findings (duplication, ungated rules, mandatory reads), and every proposal MUST cite the finding that motivated it.
- **same-measurement-method**: The validation phase MUST measure per-turn cost with the same method as the audit so the before and after numbers in the report are comparable.
- **baseline-carried-to-report**: The audit's before metrics MUST be carried unchanged to the report, even when the user declines every optimization.
- **validation-failure-halts**: A behavioral-preservation failure or a lint FAIL in the validation phase MUST halt the pipeline before the report phase writes an "optimized" outcome, and the pipeline outcome MUST be recorded as Validation Failed.

