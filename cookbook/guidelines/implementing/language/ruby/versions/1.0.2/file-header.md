
- Every file MUST begin with `# frozen_string_literal: true`. The comment applies to that file only and MUST be in the first comment section.
- Code MUST mutate a string only after `+""` or `String.new`, or `dup` a frozen one.

