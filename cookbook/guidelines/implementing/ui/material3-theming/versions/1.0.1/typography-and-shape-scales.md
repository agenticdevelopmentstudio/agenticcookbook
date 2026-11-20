
- Use the M3 type scale roles (`displayLarge` … `labelSmall`) via `MaterialTheme.typography.<role>`. **MUST NOT** apply ad-hoc `fontSize`/`fontWeight` where a scale role fits.
- Use the shape scale (`extraSmall` … `extraLarge`) via `MaterialTheme.shapes`. Component corner treatment **SHOULD** come from the scale, not per-component magic numbers.

