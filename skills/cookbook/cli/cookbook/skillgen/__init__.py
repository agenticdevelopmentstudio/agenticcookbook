"""Compile a cookbook-schema tree into a Claude Code plugin of routed skills.

`cookbook skills build` drives it. The stages, each its own module:

    source   load the docs (frontmatter + body) and the source's layout
    groups   assign each doc to a router skill, and dedup identical bodies
    leaves   clean a body and split it into leaves under the size cap
    rules    extract MUST/SHOULD/MAY rules and test-vector ids from a leaf
    emit     render router SKILL.md, index.md, leaf files and manifest.json
    gates    depth, names, links, description budget, leaf size
    build    orchestrate, prove byte-stability, write or --check

Everything is built in memory as {relative path: text}, so a check and a
write see the same bytes.
"""
