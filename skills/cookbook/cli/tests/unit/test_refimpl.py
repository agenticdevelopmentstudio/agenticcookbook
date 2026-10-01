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


# --- with_section ----------------------------------------------------------------------------

_ROWS = [Implementation("apple", "A/B.swift"), Implementation("web", "c/d/")]
_TABLE = "| Platform | Path |\n|----------|------|\n| apple | `A/B.swift` |\n| web | `c/d/` |"


def test_with_section_replaces_an_existing_sections_rows_leaving_the_rest_verbatim():
    text = (
        "---\ntype: ingredient\n---\n\n"
        "## Overview\n\nx\n\n"
        "## Reference Implementations\n\n"
        "| Platform | Path |\n|----------|------|\n| web | `old/Path.tsx` |\n\n"
        "## Design Decisions\n\ny\n"
    )
    out = refimpl.with_section(text, _ROWS)
    assert out == (
        "---\ntype: ingredient\n---\n\n"
        "## Overview\n\nx\n\n"
        f"## Reference Implementations\n\n{_TABLE}\n\n"
        "## Design Decisions\n\ny\n"
    )
    assert refimpl.implementations(out) == _ROWS


def test_with_section_inserts_before_design_decisions_when_absent():
    text = "## Overview\n\nx\n\n## Design Decisions\n\ny\n"
    out = refimpl.with_section(text, _ROWS)
    assert out == f"## Overview\n\nx\n\n## Reference Implementations\n\n{_TABLE}\n\n## Design Decisions\n\ny\n"


def test_with_section_inserts_before_compliance_when_no_design_decisions():
    text = "## Overview\n\nx\n\n## Compliance\n\ny\n"
    out = refimpl.with_section(text, _ROWS)
    assert out == f"## Overview\n\nx\n\n## Reference Implementations\n\n{_TABLE}\n\n## Compliance\n\ny\n"


def test_with_section_inserts_before_change_history_when_no_other_anchor():
    text = "## Overview\n\nx\n\n## Change History\n\ny\n"
    out = refimpl.with_section(text, _ROWS)
    assert out == f"## Overview\n\nx\n\n## Reference Implementations\n\n{_TABLE}\n\n## Change History\n\ny\n"


def test_with_section_prefers_design_decisions_over_compliance_and_change_history():
    text = "## Design Decisions\n\na\n\n## Compliance\n\nb\n\n## Change History\n\nc\n"
    out = refimpl.with_section(text, _ROWS)
    at = out.index("## Reference Implementations")
    assert at < out.index("## Design Decisions") < out.index("## Compliance") < out.index("## Change History")


def test_with_section_appends_at_the_end_when_none_of_the_anchors_exist():
    text = "## Overview\n\nx\n"
    out = refimpl.with_section(text, _ROWS)
    assert out == f"## Overview\n\nx\n\n## Reference Implementations\n\n{_TABLE}\n"


def test_with_section_appends_a_missing_trailing_newline_before_the_new_section():
    text = "## Overview\n\nx"  # no trailing newline at all
    out = refimpl.with_section(text, _ROWS)
    assert out == f"## Overview\n\nx\n\n## Reference Implementations\n\n{_TABLE}\n"


def test_with_section_writes_an_empty_table_for_no_rows():
    text = "## Overview\n\nx\n\n## Design Decisions\n\ny\n"
    out = refimpl.with_section(text, [])
    assert "## Reference Implementations\n\n| Platform | Path |\n|----------|------|\n\n" in out
    assert refimpl.implementations(out) == []


def test_with_section_ignores_a_reference_implementations_heading_inside_a_fence():
    text = (
        "## Overview\n\nx\n\n"
        "## Notes\n\n```\n## Reference Implementations\n| apple | `fenced/Example.swift` |\n```\n\n"
        "## Design Decisions\n\ny\n"
    )
    out = refimpl.with_section(text, _ROWS)
    # the real section lands before Design Decisions, not inside the fence in Notes
    assert out.index("```") < out.index("## Reference Implementations") < out.index("## Design Decisions")
    assert "fenced/Example.swift" in out  # the fenced example is untouched
