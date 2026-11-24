## accepted-records-immutable
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: The quote has three segments joined by "|", and each citation holds its own segment word for word: AWS the first, Microsoft the second, Fowler the third. All three say an accepted record is not edited and a changed decision is a new, superseding record.

## adr-tools-supersede-command
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote does not mention numbering or the -s flag, so on its own it does not back those parts of the claim. The README does say both in the text next to it: "This will create a new, numbered ADR file" and "use the -s option. adr new -s 9 ...". Adding those lines to the quote would make it support the claim.
- correction: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST

## clarifications-may-amend
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- citation 2: holds-quote
- result: refuted
- note: GDS allows updating for "clarifications" found during the implementation phase, and requires a new ADR once implementation has occurred. That is not quite "before it is implemented". Henderson's quoted line only says "mutability has worked better". The "dated notes" part is in the next, unquoted sentence: "We insert the new info the existing ADR, with a date stamp, and a note that the info arrived after the decision."
- correction: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST

## supersede-and-link
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Microsoft, Nygard and GDS each hold their own segment. Together they say write a new record, mark the old one superseded and link the two (GDS uses "must").

## supersession-header-fields
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- citation 2: holds-quote
- result: refuted
- note: PEP 1 does carry header fields in both directions (Superseded-By on the old PEP, Replaces on the new one). RFC 7322 §4.1.4 only puts "Updates:" and "Obsoletes:" in the newer RFC's header, which is one direction. So "in both directions" is wrong for RFCs.
- correction: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST

## gds-way-supersede-must
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: GDS says the old ADR "must be clearly marked as 'superseded'", but only says the status line "should appear directly under the heading". The claim says the heading placement is required, which is stronger than the source (MUST where it says SHOULD).
- correction: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

## status-lifecycle
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Microsoft ("Status, such as Proposed, Accepted, or Superseded", italics aside), Fowler and MADR (which adds rejected and deprecated) each hold their segment.

## record-decision-date
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Google Cloud ("might include a timestamp"), MADR's date field and AWS's approval timestamp each hold their segment. The claim states no MUST, so Google's "might" does not undercut it.

## record-consequences-good-and-bad
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Nygard ("All consequences should be listed here, not just the 'positive' ones") and Microsoft ("Avoid hiding consequences") each hold their segment.

## zimmermann-anti-patterns
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both the Fairy Tale and Free Lunch Coupon definitions are on the page word for word. The only difference is a space before each colon.

## one-decision-short-record
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Nygard (a single decision), Fowler ("short, just a couple of pages") and Henderson ("Each ADR should be about one AD") each hold their segment.

## zimmermann-mega-adr
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Mega-ADR definition is on the page word for word, apart from a space before the colon and a footnote marker "4". The page offers "move to a separate document" as the remedy.

## record-significant-decisions
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Microsoft ("Only include choices that affect the system's structure..."), Spotify and AWS each hold their segment.

## record-rejected-decisions
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: AWS (add a rejection reason "to prevent future discussions") and PEP 1 ("still important to have a record of this fact") each hold their segment.

## record-confidence-level
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Both pages have "Record the confidence level of the decision". Fowler's page also has the line about changes that should trigger a re-evaluation. Fowler calls it "handy", but the claim states no strength.

## backfill-undocumented
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- citation 2: holds-quote
- result: refuted
- note: Microsoft makes this conditional: records "should be retroactively generated" only "if the data is available", and only for brownfield workloads. Spotify lists backfilling as one case for writing an ADR. The claim drops the condition and states backfilling as unconditional practice.
- correction: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST

## zimmermann-dummy-alternative-and-sprint
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page has all three segments: the Dummy Alternative definition, Sprint ("Only one option is considered") and "consider at least two options per issue" (from its good-practices list). The only difference is spacing before the colons.
