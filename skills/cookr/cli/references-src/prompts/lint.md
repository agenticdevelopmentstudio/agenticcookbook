You are reviewing a single cookbook artifact for adherence to the project's
principles, conventions, and recipe-quality guidance below. Your goal is to
identify actionable issues a maintainer should fix — not to summarize the file.

# Principles (file names, read the bundled originals for full text)
{{principles}}

# Conventions
{{conventions}}

# Glossary
{{glossary}}

# Artifact under review

**Path:** {{file_path}}

**Contents:**
```
{{file_contents}}
```

# Output

Respond in concise Markdown. If everything is fine, output a single line:

    OK: no actionable issues.

Otherwise, group findings under three headings — omit any heading with no
findings. Each finding is a single bullet starting with a short rule slug and
ending with a one-sentence suggestion.

## Principle violations
- `<principle-slug>`: <what's wrong> → <suggestion>

## Convention drift
- `<convention>`: <what's off> → <suggestion>

## Recipe quality
- `<aspect>`: <what would improve agent execution> → <suggestion>

Be terse. Skip anything that is already fine. Do not restate the file.
