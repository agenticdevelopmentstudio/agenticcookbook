"""markdown.uncited: research citations leave prose; code keeps its text (review f5)."""

from cookr.core.markdown import uncited


def test_a_citation_in_prose_is_removed():
    assert uncited("Pin every version (claims: a1, a2).\n") == "Pin every version.\n"


def test_an_inline_code_span_keeps_its_text():
    text = "Call `cite(claims: x)` or ``a`(claim: y)`` once (claims: z).\n"
    assert uncited(text) == "Call `cite(claims: x)` or ``a`(claim: y)`` once.\n"


def test_a_fenced_block_keeps_its_text():
    text = "Before (claim: a).\n```py\nf(claims: b)\n```\n~~~\ng (claims: c)\n~~~\nAfter (claims: d)\n"
    assert uncited(text) == "Before.\n```py\nf(claims: b)\n```\n~~~\ng (claims: c)\n~~~\nAfter\n"


def test_text_without_code_or_citations_is_unchanged():
    text = "No citations here.\nSecond line"
    assert uncited(text) == text
