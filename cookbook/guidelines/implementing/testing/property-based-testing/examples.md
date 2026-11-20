
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

