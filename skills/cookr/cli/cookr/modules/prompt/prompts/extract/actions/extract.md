---
description: "Write or complete the recipe for one component from its source files."
params:
  name:
    description: "Component name (kebab-case)."
  recipe_path:
    description: "Repo-relative path the finished recipe is written to."
  type:
    description: "ingredient or recipe."
    default: "ingredient"
  platforms:
    description: "Comma-separated source platforms present in the sources."
---
Write the **{{type}}** recipe for the component `{{name}}`.

Save the result to `{{recipe_path}}` (overwrite if it exists). Source platforms
present: {{platforms}}.

Use the `{{type}}` template under `## reference: templates/` above as the exact
section list and order. Use the guidelines under `## reference: guidelines/` as
the acceptance bar. The sources and any existing recipe follow.
