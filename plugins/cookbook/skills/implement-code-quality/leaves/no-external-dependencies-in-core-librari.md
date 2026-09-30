<!-- leaf: implement-code-quality/no-external-dependencies-in-core-librari · source: guidelines/implementing/code-quality/no-external-dependencies-in-core-librari.md -->

**Rules** (cite as `implement-code-quality/no-external-dependencies-in-core-librari#<slug>`):

- `pyyaml-requests-etc-not-added-core-library-code` MUST — roadmap_lib uses the standard library only. Third-party packages (PyYAML, requests, etc.) MUST NOT be added to core …

# No external dependencies in core libraries

`roadmap_lib` uses the standard library only. Third-party packages (PyYAML, requests, etc.) MUST NOT be added to core library code. This keeps the library portable and installable without dependency management.
