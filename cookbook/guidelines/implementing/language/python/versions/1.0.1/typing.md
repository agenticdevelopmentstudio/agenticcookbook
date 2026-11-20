
- Annotate every function signature and every public attribute. Run a type checker in strict mode in CI (for mypy, `--strict`, which includes `--disallow-untyped-defs`).
- Do not silence a checker with a blanket `# type: ignore`; ignore one error code and say why.

