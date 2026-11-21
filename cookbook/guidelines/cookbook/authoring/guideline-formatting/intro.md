
# Guideline Formatting

A cookbook guideline carries complete frontmatter with `type: guideline`, opens with a summary statement under an H1 that matches its title, states each requirement as a named rule with an RFC 2119 keyword that ends by citing the research claims it stands on, and ends with a change history. A roled guideline gives every part but the intro and the history a role, and a guideline not listed in `cookbook/research-exempt.json` keeps the research it was written from in its folder.

Following this guideline means keeping every absolute rule in `## Rules`, and keeping every recommended rule there or saying why not; the keywords mean what [adc.guideline.cookbook.authoring.requirement-keywords](cookbook:456f23bd-4523-47e8-9541-073ac046f2ad) says they mean. Only `## Rules` is normative. The reviewer and build parts restate its rules as checks, and every other part is informative.

This guideline covers the structure of a guideline artifact in this cookbook: its frontmatter, headings, summary, parts and their roles, named rules and their research citations, and its change history. The trigger vocabulary belongs to [adc.guideline.cookbook.authoring.activity-triggers](cookbook:1b7b83f9-3b8a-46f7-81b7-9a55291a23a2), and the shape of the research document to [adc.guideline.researching.evidence.research-results-document](cookbook:2795e06d-b081-43ac-97d9-20ff3d0a93b1).

