<!-- leaf: test-general/property-based-testing · source: guidelines/testing/property-based-testing.md -->

**Rules** (cite as `test-general/property-based-testing#<slug>`):

- `at-least-one-property-test-must-be-written-per-data-transformation-function` MUST — Examples:

# Property-Based Testing

When to use: parsers, serializers, data transformers, encoders/decoders, validators — anything
where "for all valid inputs X, property Y holds."

**The principle:** Instead of testing specific examples, describe properties of the output
and let the framework generate hundreds of random inputs to try to falsify them.

**Platform tools:**

| Platform | Library | Install |
|----------|---------|---------|
| Python | [Hypothesis](https://github.com/HypothesisWorks/hypothesis) | `pip install hypothesis` |
| TypeScript/JS | [fast-check](https://github.com/dubzzz/fast-check) | `npm install fast-check` |
| Swift | `@Test(arguments:)` (parameterized) | Built into swift-testing |
| .NET | [FsCheck](https://fscheck.github.io/FsCheck/) | `dotnet add package FsCheck` |
| Kotlin/JVM | [jqwik](https://jqwik.net/) | Gradle/Maven dependency |

**At least one property test MUST be written per data transformation function.** Examples:

- `encode(decode(x)) == x` (round-trip)
- `sort(xs).length == xs.length` (preservation)
- `parse(serialize(obj)).fields == obj.fields` (fidelity)

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.text())
def test_encode_decode_roundtrip(s):
    assert decode(encode(s)) == s
```
