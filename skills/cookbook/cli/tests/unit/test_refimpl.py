from cookbook.core import refimpl
from cookbook.core.refimpl import Implementation

BODY = """\
# Label

## Platform Notes

None.

## Reference Implementations

| Platform | Path |
|----------|------|
| Apple | `/Sources/Kit/Label.swift` |
| web | `packages/kit/label/` (the whole package) |
| python | no code span here |

## Design Decisions

```
## Reference Implementations
| apple | `fenced/Example.swift` |
```
"""


def test_rows_are_read_in_order_with_normalized_platform_and_path():
    assert refimpl.implementations(BODY) == [
        Implementation("apple", "Sources/Kit/Label.swift"),
        Implementation("web", "packages/kit/label/"),
    ]


def test_directory_rows_end_in_a_slash():
    rows = refimpl.implementations(BODY)
    assert [r.is_dir for r in rows] == [False, True]


def test_no_section_and_not_applicable_read_as_no_rows():
    assert refimpl.implementations("# T\n\n## Overview\n\nx\n") == []
    assert refimpl.implementations(
        "## Reference Implementations\n\nNot applicable: this cookbook carries no implementations.\n") == []


def test_render_round_trips():
    rows = [Implementation("apple", "A/B.swift"), Implementation("web", "c/d/")]
    assert refimpl.parse(refimpl.render(rows)) == rows
