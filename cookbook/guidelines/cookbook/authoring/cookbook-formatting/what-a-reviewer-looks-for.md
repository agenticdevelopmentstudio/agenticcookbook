
- The manifest is read as bytes: a byte order mark is refused, the text decoded as UTF-8, and a repeated member name caught before the schema sees the parsed object.
- The schema declares draft 2020-12 with `$schema`, carries an absolute-URI `$id`, requires `format`, `id` and `rdid`, and pins `format` with `const`.
- Every `pattern` is anchored with `^` and `$`; the UUID patterns match the 8-4-4-4-12 hex-and-dash form; the rdid pattern admits only lowercase letters, digits and hyphens after a leading letter.
- No field relies on `format` alone while the validator runs without format assertion, and no format's checker package is silently missing.
- `version` checks: a semver claim that the `^\d+\.\d+\.\d+$` pattern does not keep (it accepts leading zeroes); a released version whose contents changed without a new `version`.
- Objects closed with `"additionalProperties": false` are closed for typo detection by choice; an object meant to be extended through `allOf`, if closed, is closed with `unevaluatedProperties` rather than `additionalProperties`, or the change says why.
- Checks the schema cannot make (path existence, paths climbing out with `..`, cycles, cross-file `source.id` resolution, one field compared with another) live in cookr's code and report every failure, not the first.
- The project rules hold: `type` is `"cookbook"`, the project fields are present, `structure` has a `description`, `structure.kind` is one of the four values, a library's tree is its arrangement, and code roots and dependencies live in `.cookr.json`, not `cookbook.json`.
- The schema ships with test manifests, run with a real validator, and is compiled strictly.

