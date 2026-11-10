---
description: "Write or complete the recipe for one component from its source files."
params:
  name:
    description: "The spec's path in the cookbook, without `.md`."
  recipe_path:
    description: "Path of the finished recipe from the repo root."
  recipe_file:
    description: "Absolute path the finished recipe is written to."
  rdid:
    description: "The recipe's rdid in the cookbook index, when it has one."
  type:
    description: "ingredient or recipe."
    default: "ingredient"
  platforms:
    description: "Comma-separated source platforms present in the sources."
  reference_implementations:
    description: "The implementation rows to record in the cookbook index."
---
Write the **{{type}}** recipe for the component `{{name}}`.

Save the result to `{{recipe_file}}` (`{{recipe_path}}` from the repo root;
overwrite it if it exists). Its rdid is `{{rdid}}`.
Source platforms present: {{platforms}}.

Its code is recorded in the cookbook index, not in the recipe: once the recipe
is saved, record each of these rows with `cookr implements` and write no
`## Reference Implementations` section:

{{reference_implementations}}

Use the `{{type}}` template under `## reference: templates/{{type}}.md` above as
the exact section list and order, and the guidelines under the
`## reference: guidelines/` headings above as the acceptance bar. The sources
and any existing recipe follow the task.
