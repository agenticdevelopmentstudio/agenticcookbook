# Devteam-text batch 0 report

## cookbook/principles/make-it-work-make-it-right-make-it-fast (95ec9111)

34 sentences placed, 7 rules added.

**new rules** (all from `behavioral/feature-behavior`; every keyword chosen by the brief's rule: "never"/"no" is MUST NOT, "every"/"each" is MUST, a plain check is SHOULD):
- `must-walk-each-claimed-behavior-to-its-effect` (MUST): from "(1) State the claim in one sentence ..." and "(2) Walk the primary path entry-to-effect ..."
- `must-not-silently-remove-old-behavior` (MUST NOT): from "a behavior the change silently removed or broke is a finding even when every new line is individually correct."
- `must-order-every-step-on-a-path-correctly` (MUST): from "(a) What else runs on this path, and in what order? ... a step that runs when it should not, runs twice, or runs before the thing it depends on is a finding."
- `must-treat-paired-operations-alike` (MUST): from "(b) Do paired operations treat the same input the same way? ..."
- `must-close-every-route-to-a-fixed-failure` (MUST): from "(c) Does a fix close every route to the failure it targets? ..."
- `should-ask-no-more-than-the-use-needs` (SHOULD NOT): from "(d) Does each low-level call ask for more than it needs? ..."
- `must-not-ship-a-path-that-cannot-work` (MUST NOT): from "(5) File every real defect ... A condition tested twice, a check that can never be true, a wrong index or off-by-one are bugs and are yours."

The three `code-quality/make-it-work` bar sentences were added as new bullets under the existing rules `should-first-make-it-work`, `must-not-skip-make-it-right` and `should-optimize-only-measured-slowness`.

**reader-specific**:
- "when `read_base_file` is among your tools, use it to read what the code did BEFORE the change;" and "when it is not (some providers and degraded runs cannot open the base commit), read the before-code from the diff's removed and context lines instead, and say in your summary that the comparison reached only as far as the hunks show." (tool name, "your summary")
- "using the repo tools to read past the diff, including into submodule and vendored paths;" (devteam tools)
- "leave it to the specialists that own it." (other specialities)
- "the before-behavior was compared ... via the base commit when `read_base_file` was available, otherwise via the diff's removed and context lines with that limit stated" (review-bar)
- "File every real defect you find on the way ... whether or not the changeset made a claim about it." and "every real defect seen on the way is filed, claimed behavior or not." (reviewer procedure phrased as a rule)

**contradictions**: none.

**not placed**: none.

## cookbook/guidelines/implementing/concurrency/concurrency (dfb61dcf)

5 sentences placed, 2 rules added.

**new rules** (from `architecture/concurrency`):
- `must-hold-one-lock-across-check-and-act` (MUST): from "when a change adds or moves a lock ... a check outside the lock with its act or mark after it (check-then-act, Has-then-Set, Stat-then-Open) is still a race;" and "every check-then-act on shared state holds one lock across both the check and the act;"
- `must-revalidate-state-after-waiting-on-a-lock` (MUST): from "then ask what a caller that now WAITS on the lock finds when it gets in ..." and "a caller that waits on a newly added lock re-validates state it read before waiting"

**reader-specific**: none. The lead-in "shared state across threads/goroutines/tasks:" is joined to its bullet.
**contradictions**: none.
**not placed**: none.

## cookbook/guidelines/implementing/ui/design-time-data (0ab0c346)

3 sentences placed, 2 rules added.

**new rules** (from `platform-native/design-time-data`):
- `should-keep-design-time-data-lightweight-and-separate` (SHOULD): from "keep design-time data classes lightweight and separate from production code"
- `must-not-put-production-logic-in-design-time-data` (MUST NOT): from "no production logic in design-time data classes"

"XAML views have `d:DataContext` or `d:DesignInstance` set;" was added as a review-bar bullet under the existing `should-use-design-time-data-context`.

**reader-specific**: none.
**contradictions**: none.
**not placed**: none.
