
- `should-score-claims-by-evidence`: a claim's score that follows its tone (assertive, certain wording) rather than the evidence cited for it
- `should-lower-trust-for-uncited-certainty`: words like "proven" or "scientists confirm" with no supporting citation, scored as raising trust rather than lowering it
- `may-surface-unsupported-claims-scored-low`: a popular-but-unsupported claim that is surfaced carries a low score, not a silent drop or a high one
- `should-not-present-unsupported-claims-as-true`: a popular-but-unsupported claim stated as fact in the output
- `should-match-confidence-to-sources`: stated confidence stronger than the strength and independence of the sources behind it
- `should-scrutinize-urgency-and-emotion`: urgent or emotionally framed sources taken at face value instead of checked harder
