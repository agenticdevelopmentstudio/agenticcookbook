
- Non-trivial HTTP APIs **SHOULD** be defined contract-first: write the OpenAPI document, agree on it, then implement.
- The OpenAPI document **MUST** be the source of truth. When code and spec disagree, the spec wins and the code is the defect.
- New or changed APIs **MUST** ship the spec change in the same change set as the implementation, never after the fact.
- The spec **MUST** be linted in CI, and the lint step **MUST** fail the build on errors.

