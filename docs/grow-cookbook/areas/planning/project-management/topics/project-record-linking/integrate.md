# Integrate: project-record-linking

## For the owner

No `cookr validate` owner-decides rows for this topic.

Open questions from the owner list:

- Whether a two-way link is written in both records' files or written once and its reverse computed by the checker; the trackers compute the reverse, file-based records must choose.
- What identifier scheme project records use: one prefix per record type (R-1, D-1, I-1) or one global sequence; the sources require only uniqueness and no reuse.
- Whether a link to an unknown identifier fails the check (as Doorstop's error does) or only warns (as Sphinx-Needs does by default).
- Whether a link whose target is closed or superseded is reported at all, and if so at what level; Linear keeps it as Related, Doorstop warns when a child links to an inactive parent.
- Whether every record must be linked to at least one other record (an orphan check), or only the record types whose host topics require a link.
- Whether accepted decision records are immutable (Microsoft Learn, Nygard) or may take dated amendments (Henderson's teams found mutability worked better).
- Whether a realised risk keeps its record and links forward to the new issue (the 'realised, see I-01' convention) or is moved to the issue register as PRINCE2 summaries describe.

## Lossless

New topic, no base text (`cookr roles lossless`: not in the base commit).

## Validate

`cookr validate` passed. Bumped 1.0.0 → 1.0.1; /add-artifact approved it (no lint failures, no warnings).

integrated: 2026-11-24
