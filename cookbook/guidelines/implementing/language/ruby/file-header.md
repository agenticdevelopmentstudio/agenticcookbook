
- Begin every file with `# frozen_string_literal: true`. The comment applies to that file only and must be in the first comment section.
- Mutate a string only after `+""` or `String.new`, or `dup` a frozen one.

