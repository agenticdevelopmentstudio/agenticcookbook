You are checking research you did not do. Do not edit any file. Today is
{{today}}.
{{privacy}}

Research file: {{repo}}/{{artifact}}/research/research.json

For each claim id listed below, read the claim's record in that file, then:
1. Fetch every URL in its `citations` with WebFetch, and re-read the
   source yourself; do not rely on the quote as recorded.
2. For each citation, in order, decide whether that source holds the
   claim's `quote`, word for word or with only formatting differences:
   `holds-quote`, `lacks-quote`, or `unreachable`.
3. Decide whether the quote is found at all (some citation holds it), and
   whether the quote supports the `claim` as written: its scope, its
   strength (MUST against SHOULD), and the platforms it names.
Use only the claim's own citations. If you know a better source, name it in
the note; do not use it to confirm the claim.

The rule for `result`: a claim is `refuted` unless both `quote-found` and
`supports-claim` are `yes`. `partly` is not `yes`: a claim the quote only
partly supports is refuted. A script applies this rule to your blocks
whatever your `result` line says, so write the line by the rule.

Claims to check (every claim a `contradicted` or `new` verdict names,
except the `prior cookbook text` claims, which are the rules themselves):
{{claims}}

Reply with one block per claim, in the order given, and nothing else:

## <claim id>
- quote-found: yes | no | source-unreachable
- supports-claim: yes | partly | no
- citation 1: holds-quote | lacks-quote | unreachable
- citation 2: holds-quote | lacks-quote | unreachable   (one line per citation)
- result: confirmed | refuted
- note: <one or two sentences; for refuted, what the source actually says>
