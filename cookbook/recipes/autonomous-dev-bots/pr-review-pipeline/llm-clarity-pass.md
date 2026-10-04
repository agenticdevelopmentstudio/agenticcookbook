
Beyond Vale's deterministic rules, the LLM clarity pass checks for:

- **Ambiguous antecedents**: pronouns whose referent requires re-reading prior context
- **Implicit assumptions**: statements that assume knowledge not present in the document
- **Terminology drift**: a concept called X in one section and Y in another
- **Section isolation**: can each section be understood without reading the others?
- **Unresolved references**: mentions of concepts not defined or linked
- **Vague quantification in requirements**: "handle multiple items" (how many?) vs "handle 1-1000 items"

