# Example

A run of SKILL.md's five stages on one topic.

```
/grow-cookbook plan implementing/feature-management --workspace .superpowers/sdd/2026-11-16-finish-the-cookbook-roles
# owner approves A/area-plan.md, recorded in A/approval.md
/grow-cookbook research implementing/feature-management --topic feature-flags
/grow-cookbook write implementing/feature-management --topic feature-flags
/grow-cookbook review implementing/feature-management --topic feature-flags
/grow-cookbook integrate implementing/feature-management --topic feature-flags
```

After stage 5, `A/topics/feature-flags/integrate.md` records `/add-artifact`
passing and ends with `integrated: <date>`, and the Research section of `cookr validate` counts
`guidelines/implementing/feature-management/feature-flags` among the
researched artifacts with no finding.
