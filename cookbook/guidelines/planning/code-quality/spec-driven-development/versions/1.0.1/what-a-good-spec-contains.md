
A spec **MUST** be self-contained — readable and executable in a fresh session with no prior context. It **MUST** include:

| Section | Requirement |
|---------|-------------|
| Goal | One or two sentences stating the "what" and "why" — not the "how". |
| Files & interfaces | Name the concrete files, functions, and interfaces to add or change. |
| Out of scope | An explicit list of what this change will **NOT** touch. This is the highest-signal section for keeping an agent on task. |
| Verification | An end-to-end check that proves the feature works (test command, build, script, or screenshot diff). |

- The spec **SHOULD** reference existing patterns to follow ("model X on the existing Y") rather than inviting a from-scratch design.
- The spec **MUST NOT** be discarded once coding starts; it is the artifact the implementation is reviewed against.

