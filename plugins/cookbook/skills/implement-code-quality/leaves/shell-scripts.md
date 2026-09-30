<!-- leaf: implement-code-quality/shell-scripts · source: guidelines/implementing/code-quality/shell-scripts.md -->

**Rules** (cite as `implement-code-quality/shell-scripts#<slug>`):

- `script-main-functions-only-call-other-functions` MUST — Shell script main() functions MUST only call other functions — no inline logic. Scripts MUST be kept composable and …

# Shell scripts

Shell script `main()` functions MUST only call other functions — no inline logic. Scripts MUST be kept composable and testable.
