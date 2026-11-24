# Integrate: decision-records

## For the owner

No `cookr validate` owner-decides rows for this topic.

Open questions from the owner list:

- Whether naming the decider is a MUST or a SHOULD: MADR marks decision-makers optional and Nygard's template has no decider field, while PEP-Delegate, DACI and GOV.UK always name one; the owner sets the strength.
- Whether alternatives are required on every record, or only where two or more options were real: Nygard and GOV.UK omit the section, Google Cloud ties ADRs to 'two or more engineering options', MADR's minimal template keeps it.
- Whether a clarification may edit an accepted record in place (GDS Way allows it before implementation; Henderson's collection prefers dated amendments) or every change must be a new superseding record (Microsoft, AWS, Fowler).
- Where records live: in the code repository (Nygard, Fowler, GDS, Thoughtworks, log4brains) or a wiki readable by non-developers (Google Cloud notes both; Atlassian's decision log); or the repository with a mirrored wiki.
- Which template to standardise on: Nygard's, MADR, or Y-statements; Zimmermann advises choosing one and sticking to it.
- Whether 'deprecated' is a status distinct from 'superseded' (Nygard and MADR list both) and whether superseded records may ever be deleted (Zimmermann mentions deleting; Nygard and Microsoft keep them).
- Whether sequential numbering is required (Nygard, Fowler, adr-tools) or avoided to dodge merge conflicts (log4brains).

## Lossless

New topic, no base text (`cookr roles lossless`: not in the base commit).

## Validate

`cookr validate` passed. Bumped 1.0.0 → 1.0.1; /add-artifact approved it (no lint failures; warnings: the names `capture-rationale-alternatives-and-decider`, `decision-has-rationale-and-decider` and `decisions-findable-and-linked` say more than their rules, and `record-consequences-good-and-bad` holds two obligations; names left as they are because rule names stay stable).

integrated: 2026-11-24
