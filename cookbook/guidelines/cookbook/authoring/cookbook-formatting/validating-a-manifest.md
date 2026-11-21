
Check a manifest in this order; each step assumes the one before it passed.

1. **Read the bytes.** Refuse a file that begins with the UTF-8 byte order mark (`EF BB BF`), then decode it as UTF-8 (`manifest-is-utf8-without-bom`).
2. **Parse the JSON.** Refuse text that is not JSON (`cf-valid-json`) and an object that repeats a member name (`no-duplicate-member-names`): a parser that keeps the last duplicate hides the first from the schema.
3. **Validate against the schema.** Collect every error, each with the path to the member it is about (`cf-schema-valid`, `report-every-error`). Either turn format assertion on or give each `format` field a `pattern` as well (`enable-format-assertion`).
4. **Run the semantic checks in code** (`semantic-checks-in-code`): each `spec` resolves to an existing markdown file inside the cookbook directory (`cf-spec-paths-valid`, `relative-paths-stay-inside-the-cookbook`); each `source.id` resolves in its cookbook's `index.json` (`cf-source-domains`); `depends-on` has no cycle (`cf-no-circular-deps`).

In Python, with python-jsonschema and the standard library's `graphlib`:

```python
import json
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from jsonschema import Draft202012Validator


def _unique_members(pairs):
    names = [name for name, _ in pairs]
    repeated = sorted({name for name in names if names.count(name) > 1})
    if repeated:
        raise ValueError(f"duplicate member names: {', '.join(repeated)}")
    return dict(pairs)


def schema_errors(manifest: Path, schema: dict) -> list[str]:
    raw = manifest.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return [f"{manifest}: begins with a byte order mark"]
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_members)
    # One way to keep enable-format-assertion; a `pattern` beside each `format` is the other.
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    return [
        f"{manifest}: /{'/'.join(str(p) for p in error.absolute_path)}: {error.message}"
        for error in validator.iter_errors(data)
    ]


def depends_on_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """graph maps each element's dot-path to its depends-on list."""
    try:
        tuple(TopologicalSorter(graph).static_order())
    except CycleError as error:
        return error.args[1]  # the cycle's nodes, the first and the last the same
    return None
```

Check the schema itself the same way before any manifest: compile it strictly (`validate-the-schema-strictly`; in Ajv, strict mode is the default) and run it against its positive and negative test manifests (`schema-has-positive-and-negative-tests`).

