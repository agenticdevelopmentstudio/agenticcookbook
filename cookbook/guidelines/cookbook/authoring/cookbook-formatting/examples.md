
The smallest manifest, a source cookbook's identity and nothing else:

```json
{
  "format": 2,
  "id": "8f14e45f-ceea-4e7a-9e3b-2c1d0a7b6f55",
  "rdid": "adc"
}
```

Versions against `version-is-semver`:

| `version` | Semantic Versioning 2.0.0 |
|---|---|
| `1.2.3` | a normal version |
| `01.2.3` | not a version: a leading zero, which `^\d+\.\d+\.\d+$` still accepts |
| `1.2` | not a version: two numeric parts |

A `depends-on` cycle, reported by its nodes (`report-every-error`): an element `app.ui` that depends on `app.store`, which depends on `app.ui`, gives `['app.ui', 'app.store', 'app.ui']`.

