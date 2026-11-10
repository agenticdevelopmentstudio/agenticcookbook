from cookr.core import refimpl
from cookr.core.refimpl import Implementation

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


# --- render / part: index implementations as the derived section ---------------------------

def _rows():
    from cookr.core.index import Conformance, Implementation as Row
    return [Row("macos", "Sources/Kit/Label.swift", Conformance("confirmed", "1.2.0")),
            Row("web", "packages/kit/label/", Conformance("unverified")),
            Row("ios", None, Conformance("planned"))]


def test_render_draws_location_and_conformance():
    assert refimpl.render(_rows()) == (
        "| Platform | Location | Conformance |\n"
        "|----------|----------|-------------|\n"
        "| macos | `Sources/Kit/Label.swift` | confirmed (1.2.0) |\n"
        "| web | `packages/kit/label/` | unverified |\n"
        "| ios | (planned) | planned |")


def test_part_is_the_derived_section():
    part = refimpl.part(_rows())
    assert part.heading == refimpl.SECTION and part.name == "reference-implementations"
    assert part.text == f"\n{refimpl.render(_rows())}\n\n"


def test_no_rows_is_no_part():
    assert refimpl.part([]) is None
