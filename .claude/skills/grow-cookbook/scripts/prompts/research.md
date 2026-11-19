You are researching one cookbook topic. Your research is the only source
the topic's guideline will be written from, so every claim must rest on
a source you fetched and quoted.

Today is {{today}}: use it for every citation's `accessed` and for the
research's dates.
{{privacy}}

Read, in this order, and follow them:
1. {{repo}}/cookbook/guidelines/researching/process/research-methodology-and-sources/
   (artifact.json and its .md parts): your method. Use its source
   catalogue for this topic's domain. Primary sources (specifications,
   standards, the platform owners' and vendors' own documentation) come
   before secondary ones; use a secondary source only for what no
   primary source covers, and say so in the claim's trust basis.
2. {{repo}}/cookbook/guidelines/researching/evidence/verification-and-trust-scoring/:
   how to score each claim 0-100, applying cite-the-claim-not-the-document,
   independence-before-corroboration, domain-stratified-trust,
   suppress-unsupported-confidence and provenance-at-generation-time.
3. {{repo}}/cookbook/guidelines/researching/evidence/research-results-document/:
   the shape of research.json.
4. {{repo}}/guide/introduction/conventions.md, section "Research": every
   field `cookr validate` checks.
5. {{topic_dir}}/research-brief.md: the topic, its research questions, and
   the rules to verify, each quoted word for word and named. Those rules are
   claims to check, never sources.

Answer these four questions, verbatim, each as its own section:
1. Best practices: what is current best practice for this topic?
2. Known solutions: what solutions, patterns, libraries and tools already
   exist, and how do they compare?
3. Platform guidelines: what do the platform owners' own guidelines say,
   for each platform the topic touches (Apple, Android, Windows, web, the
   databases and runtimes concerned)?
4. The expert's view: if we hired an expert consultant in this topic,
   what would they tell us: what to do, what to avoid, and what people
   usually get wrong?

Use WebSearch to find sources and WebFetch to read every source you
cite. Never cite a page you did not fetch, and never quote from memory.
A citation holds the claim's quote: cite a page only if the quoted words
are on it, and count a claim `multi-independent` only when two or more
independent publishers each hold them.

Write exactly two files and edit nothing else; write no scripts or other
files of your own:
- {{repo}}/{{artifact}}/research/research.json: the research-results-document
  container fields (topic and scope, the questions, methodology, agents
  and sources, dates, summary, open questions, limitations, license), a
  `claims` list and a `verdicts` list.
  - Each claim has every one of these fields, each a non-blank value
    (`cookr validate` refuses a claim lacking any):
    - `id`: kebab-case (lowercase letters and digits joined by single
      hyphens, e.g. `fk-index-postgres`), unique in the file.
    - `question`: exactly one of `best-practices`, `known-solutions`,
      `platform-guidelines`, `experts-view`.
    - `claim`, `source_type`, `generated_by` (who found it: `grow-cookbook
      research agent`), `query` (the search that found it): non-blank
      strings.
    - `quote`: the source's own words, verbatim, non-blank.
    - `citations`: a non-empty list; each citation has `title`, `author`,
      `publisher`, `date`, `url` and `accessed`, every one a non-blank
      string. An author that is not named: the organization that
      publishes the source (e.g. `PostgreSQL Global Development Group`).
      A date that is not given: `n.d.`. `accessed`: {{today}}.
    - `trust`: `{"score": <an integer 0-100, never a decimal or a
      string>, "basis": "<why that score, non-blank>"}`.
    - `independence`: exactly one of `multi-independent`, `single`,
      `uncorroborated`.
  - A verdict for every rule the brief lists, keyed on the name the brief
    gives it (prior rule names are fixed):
    {"rule": "<name>", "verdict": "supported"|"contradicted"|"unsupported", "claims": [<ids>]}.
    `supported` means supported at the rule's stated strength: a MUST
    needs a source that requires it, not one that recommends it. A rule
    whose strength the sources do not support is `unsupported`, with a
    note in research.md saying which strength they do support.
    Add a `new` verdict, naming a kebab-case rule, for each practice
    the research finds that no listed rule covers, stating the strength
    its sources support. Every verdict names at least one claim.
  - A rule the research cannot support (`unsupported`), or finds
    against (`contradicted`), is itself recorded as one claim, so the
    rule can be kept and cite it while the owner decides:
    - `id`: `<rule-name>-prior`; `question`: the question the rule
      falls under; `claim`: the rule's text; `quote`: the rule's text
      verbatim from the brief;
    - `source_type`: `prior cookbook text`; one citation: `title`
      `<topic> (<part file>)`, `author` `Agentic Developer Cookbook`,
      `publisher` `agenticcookbook`, `date` `n.d.`, `url`
      `git:<base commit>:<artifact>/<part file>`, `accessed` {{today}};
    - `trust`: `{"score": 0, "basis": "no research source supports it"}`
      (or, for a contradicted rule, the claims against it, by id);
      `independence`: `uncorroborated`;
    - the rule's verdict names this claim, and, for `contradicted`, the
      claims that contradict it too.
  - Every claim a rule will cite appears in some verdict's `claims`.
  - What you could not establish goes under limitations; every question or
    policy choice the owner must decide goes under `open_questions`, one
    entry each, never into a claim.
- {{repo}}/{{artifact}}/research/research.md: the same findings, readable,
  under exactly these headings in this order: `## Best practices`,
  `## Known solutions`, `## Platform guidelines`, `## The expert's view`;
  each finding names its claim id. Do not repeat trust scores or
  independence here: research.json holds them, once.

Check your two files with this checkout's cookr, exactly this line:
  {{cookr}} validate --research {{artifact}}
(`--research` takes the artifact folder, not its `research/` folder.) It must
print `Research passed.`; correct what it names until it does.

Then reply with: the two file paths, the number of claims per question,
and one line per verdict (rule, verdict, claim ids).
