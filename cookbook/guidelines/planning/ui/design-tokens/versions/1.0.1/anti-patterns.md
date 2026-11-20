
- Do **NOT** hardcode hex/spacing/font literals in components — that defeats single-source propagation.
- Do **NOT** reference primitive tokens from components; an intent change then requires editing many call sites.
- Do **NOT** fork per-platform token copies; divergence is inevitable.

> Privacy/compliance note: this is engineering guidance, not legal advice.

