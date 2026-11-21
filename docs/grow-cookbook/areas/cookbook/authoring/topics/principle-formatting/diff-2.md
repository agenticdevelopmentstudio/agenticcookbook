--- draft-1.md
+++ draft.md
@@ -10,7 +10,7 @@
 author: Mike Fullerton
 copyright: 2026 Mike Fullerton
 license: MIT
-summary: "How a cookbook principle is shaped: required frontmatter, one title, its main point first, actionable bullets that say why, a dated history, and roled parts."
+summary: "How a cookbook principle is shaped: required frontmatter, one title, its main point and why first, actionable bullets, a dated history, and roled parts."
 platforms: []
 tags:
   - principle
@@ -65,29 +65,41 @@
 
 # Principle Formatting
 
-A cookbook principle is a short Markdown artifact that agents load. Give it its required frontmatter with `type: principle`, one title, its core idea first, specific bullets that say why, and a dated Change History, newest first. Keep it to what the agent cannot work out for itself, size it against the always-loaded budget, and leave every check a script can decide to a tool.
+A cookbook principle is a short Markdown artifact that agents load. Give it its required frontmatter with `type: principle`, one title, its core idea first with the reason it holds, then specific bullets, and a dated Change History, newest first. Keep it to what the agent cannot work out for itself, size it against the always-loaded budget when it loads on every task, and leave every check a script can decide to a tool.
 
 ## Rules
 
-- **pf-frontmatter-complete**: All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. There is no `domain` field. (claims: pep-preamble-required, skill-frontmatter-required, json-schema-required, astro-frontmatter-schema)
+- **pf-frontmatter-complete**: All required meta fields (the frontmatter of the compiled doc) MUST be present per `guide/introduction/conventions.md`. (claims: pep-preamble-required, skill-frontmatter-required, json-schema-required, astro-frontmatter-schema)
+- **pf-no-domain-field**: The frontmatter MUST NOT have a `domain` field. (claims: pep-preamble-required, astro-frontmatter-schema)
 - **pf-type-field**: The `type` field MUST be `principle`. (claims: json-schema-const, pep-preamble-required, astro-frontmatter-schema)
 - **pf-summary-what-and-when**: The frontmatter `summary` SHOULD say both what the principle is about and when it applies, because a compiled skill's name and description are the only part of it loaded at startup. (claims: skill-description-what-and-when, agentskills-metadata-always-loaded)
 - **pf-title-heading**: The first H1 heading MUST match the frontmatter `title` field exactly. (claim: pf-title-heading-prior)
 - **pf-single-title**: A principle SHOULD have exactly one level-1 heading, the first heading of the document, serving as its title. (claims: google-single-h1, md025-single-title, md041-title-heading)
 - **pf-statement**: A concise statement paragraph MUST appear immediately after the H1 heading. This is the principle's core idea — typically 1-3 sentences. (claim: pf-statement-prior)
-- **pf-key-guidance-first**: A principle SHOULD put its most important guidance first: the statement before the bullets, and the bullets that matter most before the rest, since readers read the first screen and the opening sentence most and models use the start of their context best and favour earlier instructions. (claims: lost-in-the-middle, ifscale-earlier-instructions, ms-first-screen, google-opening-sentence)
-- **pf-actionable-guidance**: When the statement alone is not self-evident in practice, the principle SHOULD include bullet points with practical applications of the idea. These translate the philosophical statement into concrete actions: each bullet SHOULD be specific enough to guide a decision yet flexible enough to work as a heuristic, and written as a full sentence, not a fragment; the list SHOULD hold two to seven short items of one structure. (claims: right-altitude, claude-md-specific-concise, claude-md-headers-and-bullets, cursor-focused-actionable, ms-lists-short, nygard-bullets-not-fragments)
+- **pf-statement-before-bullets**: A principle SHOULD put its statement before its bullets, since readers read the first screen and the opening sentence most and models use the start of their context best. (claims: lost-in-the-middle, ms-first-screen, google-opening-sentence)
+- **pf-key-guidance-first**: A principle SHOULD put the bullets that matter most before the rest, since the first screen is the most read, models use the start of their context best and they favour earlier instructions. (claims: lost-in-the-middle, ifscale-earlier-instructions, ms-first-screen)
+- **pf-actionable-guidance**: When the statement alone is not self-evident in practice, the principle SHOULD include bullet points with practical applications of the idea, translating the statement into focused, actionable guidance. (claims: cursor-focused-actionable, claude-md-headers-and-bullets)
+- **pf-bullet-right-altitude**: Each bullet SHOULD be specific enough to guide a decision yet flexible enough to work as a heuristic. (claims: right-altitude, claude-md-specific-concise)
+- **pf-bullet-full-sentence**: Each bullet SHOULD be written as a full sentence, not a fragment. (claim: nygard-bullets-not-fragments)
+- **pf-bullet-list-shape**: The list of bullets SHOULD hold two to seven short items of one structure. (claim: ms-lists-short)
 - **pf-state-why**: A principle SHOULD say why it holds (the motivation, the constraints or the design decision behind it), not only what to do, so the agent can target its behaviour and a later reader need not blindly accept or blindly change it. (claims: prompting-explain-why, diataxis-explain-why, adr-motivation-lost)
-- **pf-only-what-the-agent-lacks**: A principle SHOULD hold only what the agent could not work out for itself, the smallest set of high-signal guidance that produces the behaviour wanted; it SHOULD NOT copy in common style conventions the agent already knows or a linter can check, and a bullet SHOULD be added only when agents repeat the same mistake without it. (claims: skill-only-new-context, claude-md-only-what-agent-lacks, cursor-use-a-linter, smallest-high-signal-set, cursor-start-simple)
+- **pf-only-what-the-agent-lacks**: A principle SHOULD hold only what the agent could not work out for itself, the smallest set of high-signal guidance that produces the behaviour wanted. (claims: skill-only-new-context, claude-md-only-what-agent-lacks, smallest-high-signal-set)
+- **pf-no-copied-conventions**: A principle SHOULD NOT copy in common style conventions the agent already knows or a linter can check. (claim: cursor-use-a-linter)
+- **pf-bullet-for-a-repeated-mistake**: A bullet SHOULD be added only when agents repeat the same mistake without it. (claim: cursor-start-simple)
 - **pf-brevity**: Principles SHOULD be concise. The body (excluding frontmatter and Change History) SHOULD NOT exceed ~50 lines. Principles are philosophical anchors, not exhaustive guides — detailed guidance belongs in guidelines. (claim: pf-brevity-prior)
 - **pf-always-loaded-budget**: Principles that load on every task SHOULD be sized against the budget for everything an agent always loads, not one file alone, because every always-loaded line takes some of the agent's attention on every task and instruction-following accuracy falls as instruction density grows; the hosts set that budget (Claude Code targets under 200 lines per always-loaded file, and Codex stops adding instruction files once their combined size reaches 32 KiB by default), and of a principle compiled to skills only each skill's name and description load at startup. (claims: claude-md-200-lines, codex-32kib-combined, claude-md-every-line-costs, ifscale-density-degrades, agentskills-metadata-always-loaded)
 - **pf-change-history**: The file MUST end with a `## Change History` section containing a table with columns: Version, Date, Author, Summary. (claim: pf-change-history-prior)
-- **pf-history-newest-first**: The Change History SHOULD have a row for every version, each showing its date, with the latest version first. (claims: changelog-latest-first, changelog-entry-per-version, changelog-dated)
-- **pf-format-checks-tool-enforced**: Each format check a script can decide (the required fields and the `type` value by schema, the required headings, the H1 against the front-matter title, sentence, word or line counts, how often a token appears, and structural checks such as paragraphs per section) SHOULD be enforced by a tool run the way code checks are run (a schema, a linter or CI), not left to the agent's prose or to a reviewer; the agent reads the text whatever its headings, so a required structure serves authors and tools, and the principle's text SHOULD hold only the guidance no tool can check. (claims: docs-as-code, codex-lint-in-ci, cursor-use-a-linter, claude-md-hooks-for-absolutes, md043-required-headings, json-schema-required, markdownlint-custom-rules-frontmatter, vale-metric-formulas, vale-occurrence, vale-script, agentsmd-any-headings)
+- **pf-history-row-per-version**: The Change History SHOULD have a row for every version. (claim: changelog-entry-per-version)
+- **pf-history-dated**: Each Change History row SHOULD show its version's date. (claim: changelog-dated)
+- **pf-history-newest-first**: The Change History SHOULD list the latest version first. (claim: changelog-latest-first)
+- **pf-format-checks-tool-enforced**: Each format check a script can decide (the required fields and the `type` value by schema, the required headings, the H1 against the front-matter title, sentence, word or line counts, how often a token appears, and structural checks such as paragraphs per section) SHOULD be enforced by a tool run the way code checks are run (a schema, a linter or CI), not left to the agent's prose or to a reviewer. (claims: docs-as-code, codex-lint-in-ci, cursor-use-a-linter, claude-md-hooks-for-absolutes, md043-required-headings, json-schema-required, markdownlint-custom-rules-frontmatter, vale-metric-formulas, vale-occurrence, vale-script)
+- **pf-text-holds-untooled-guidance**: A principle's text SHOULD hold only the guidance no tool can check, since the agent reads the text whatever its headings, so a required structure serves authors and tools, and formatting and lint checks belong to CI and enforcement rather than to the agent. (claims: agentsmd-any-headings, codex-lint-in-ci, claude-md-hooks-for-absolutes)
 - **standard-roled-parts**: A principle the cookbook adds or rewrites SHOULD give each part a role, so it compiles to a builder, a reviewer and their two verifiers, each skill loading only the parts its task needs. (claims: evaluator-optimizer, skills-lighter-than-always-loaded, agentskills-progressive-disclosure)
 - **standard-named-rules**: Each rule of a roled principle SHOULD be its own bullet of a `rules` part, `- **kebab-name**: … MUST|SHOULD|MAY …`, one rule to a bullet, grouped under the part's heading rather than written as dense paragraphs. (claims: claude-md-headers-and-bullets, cursor-rules-500-lines, ms-lists-short)
-- **standard-one-source-per-topic**: A principle's topic SHOULD be written once, in one folder, and detailed guidance SHOULD live in the artifact that owns it and be linked from the principle, not copied in, so the same guidance is never stated twice in diverging forms. (claims: claude-md-conflicts, cursor-reference-not-copy, diataxis-keep-bounded)
-- **standard-research-cited**: A principle SHOULD be written from research kept in its folder's `research/`, and each named rule SHOULD cite the claims it stands on, so the motivation behind each rule stays recoverable. (claims: adr-motivation-lost, prompting-explain-why, diataxis-explain-why)
+- **standard-one-source-per-topic**: A principle's topic SHOULD be written once, in one folder, so the same guidance is never stated twice in diverging forms. (claim: claude-md-conflicts)
+- **standard-link-detail-not-copy**: Detailed guidance SHOULD live in the artifact that owns it and be linked from the principle, not copied in. (claims: cursor-reference-not-copy, diataxis-keep-bounded)
+- **standard-research-kept**: A principle SHOULD be written from research kept in its folder's `research/`, so the motivation and design decisions behind it stay recoverable. (claims: adr-motivation-lost, diataxis-explain-why)
+- **standard-research-cited**: Each named rule of a principle SHOULD cite the claims it stands on, so the motivation behind each rule stays recoverable. (claims: adr-motivation-lost, prompting-explain-why)
 - **roles-principle-may-be-roled**: A principle MAY carry roles, as a guideline does, and is then compiled to skills whose bodies load only when a task calls for them. (claims: evaluator-optimizer, skills-lighter-than-always-loaded, agentskills-progressive-disclosure)
 - **roles-vocabulary**: In a principle, a role MAY be given this way: A part may carry a `role` in `artifact.json`: `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`. (claim: roles-vocabulary-prior)
 - **roles-intro-history-unroled**: The intro and the history SHOULD NOT carry a role: the intro holds the main point, which every compiled skill gets, and the history is written for people, so none of the skills an agent loads gets it. (claims: changelog-for-humans, claude-md-every-line-costs, claude-md-only-what-agent-lacks, lead-with-main-point)
@@ -101,10 +113,10 @@
 
 - Start from the frontmatter block in `guide/introduction/conventions.md`, set `type: principle`, and write a `summary` that names the idea and the decisions it applies to.
 - Write the H1 as the frontmatter `title`, word for word, and use no other level-1 heading anywhere in the body.
-- Write the statement first, in one to three sentences, as the paragraph a reader who stops there still acts on. Put the reason the principle holds in it or in the bullet it explains.
+- Write the statement first, typically in one to three sentences, as the paragraph a reader who stops there still acts on. Put the reason the principle holds in it or in the bullet it explains.
 - Write each bullet as a full sentence naming a concrete action, most important first. When a bullet needs a procedure, a table or a worked case, link the guideline that holds it instead of copying it in.
 - Before adding a bullet, ask whether the agent already gets this right without it. Leave out common conventions the agent knows and anything a linter already checks.
-- Count the principle with the others that load on every task, not alone, and measure that total against the hosts' own limits.
+- When the principle loads on every task, count it with the others that do, not alone, and measure that total against the hosts' own limits.
 - Let tools decide what they can: run `cookr validate` for the frontmatter, the type, the roles and the citations, and a markdownlint or Vale rule for headings and counts. Keep the reviewer for whether the statement holds the core idea and whether the bullets are actionable.
 - For a roled principle, give every part but the intro and the history one role with `cookr roles set`, then run `cookr roles check` to confirm the census and the four skills.
 - Record each new version with `cookr bump <folder> --summary "<what changed>"`, which adds the dated row to the Change History.
@@ -144,14 +156,17 @@
 - A missing required frontmatter field, a `domain` field, or a `type` other than `principle`
 - A `summary` that names the topic but not when the principle applies
 - An H1 that differs from the frontmatter `title`, a second level-1 heading, or a heading before the title
-- A body that does not open with the statement, or a statement that is not the core idea or runs past three sentences
-- Bullets that are fragments, vague platitudes, or a long list of mixed shapes; the most important guidance buried below the rest
+- A body that does not open with the statement, or a statement that is not the core idea or runs well past the typical one to three sentences
+- Bullets placed before the statement, or the most important bullets buried below the rest
+- A statement that is not self-evident in practice with no bullets applying it
+- Bullets that are vague platitudes or brittle hard-coded steps, bullets that are fragments, or a list outside two to seven short items of one structure
 - Guidance with no reason given for it
 - Text the agent already knows: copied style conventions, lint rules, or bullets added for no mistake agents make
 - A body past ~50 lines, or principles whose always-loaded total is not weighed against the hosts' limits
 - Detailed guidance copied in from a guideline instead of linked, or the same guidance stated in two artifacts in different forms
 - A Change History that is not last, lacks the Version, Date, Author and Summary columns, skips a version, lacks a date, or lists the oldest first
-- A check a script can decide left to prose or to the reviewer
+- A check a script can decide left to prose or to the reviewer, or principle text spent on what a tool already checks
+- Research missing from the principle's `research/` folder, or a named rule that cites no claim
 - In a roled principle: a part with no role or an unknown role, an intro or history that carries one, a rule bullet that is not `- **kebab-name**: …` with an RFC 2119 keyword, a rule with no claim cited, `routes` or `hosts/` set, `rationale` or `references` placed in a SKILL.md, or skill names and routes that differ from the ones the rules give
 
 ## A complete review must establish
@@ -159,38 +174,52 @@
 - Every required frontmatter field was checked against `guide/introduction/conventions.md`, along with the absence of `domain` and a `type` of `principle`
 - The `summary` was read for both what the principle is about and when it applies
 - The first H1 was compared with the frontmatter `title`, and the body was checked for any other level-1 heading
-- The statement was confirmed to follow the H1 directly, to hold the core idea in one to three sentences, and to come before the bullets
-- Each bullet was read for a concrete, full-sentence action, the list for its length and shape, and the order for the most important guidance first
+- The statement was confirmed to follow the H1 directly, to hold the core idea in typically one to three sentences, and to come before the bullets
+- The statement was weighed for whether it is self-evident in practice, and if not, for bullets that apply it
+- Each bullet was read for being specific yet usable as a heuristic and for being a full sentence, the list for its length and shape, and the order for the most important bullets first
 - The principle was checked for the reason it holds
-- Each bullet was weighed for whether the agent could work it out alone or a linter already checks it
-- The body's length was counted, and the principle's share of the always-loaded total was weighed against the hosts' limits
-- Detailed guidance was checked for being linked, not copied, and for agreeing with the artifact that owns it
-- The Change History was checked for being last, for its four columns, for a dated row per version and for newest-first order
-- Each format check was checked for a tool that decides it, and any left to prose or review was reported
+- Each bullet was weighed for whether the agent could work it out alone, whether it copies a convention or a lint rule, and whether it answers a mistake agents repeat
+- The body's length was counted, and, for a principle that loads on every task, its share of the always-loaded total was weighed against the hosts' limits
+- The topic was checked for a single folder, and detailed guidance for being linked, not copied, and for agreeing with the artifact that owns it
+- The Change History was checked for being last, for its four columns, for a row per version, for a date on each row and for newest-first order
+- Each format check was checked for a tool that decides it, any left to prose or review was reported, and the text was checked for guidance a tool already checks
+- The principle's `research/` folder was checked for being present, and each named rule for citing its claims
 - For a roled principle: the role of every part, the unroled intro and history, every rule's name, keyword and citation, the absence of `routes` and `hosts/`, the placement of `rationale` and `references`, and the four skills' names and routes were checked
 - Each finding names the rule it breaks
 
 ## A build must establish
 
-- `pf-frontmatter-complete`: every meta field `guide/introduction/conventions.md` requires is present, and there is no `domain` field
+- `pf-frontmatter-complete`: every meta field `guide/introduction/conventions.md` requires is present
+- `pf-no-domain-field`: the frontmatter has no `domain` field
 - `pf-type-field`: `type` is `principle`
 - `pf-summary-what-and-when`: the `summary` says what the principle is about and when it applies
 - `pf-title-heading`: the first H1 matches the frontmatter `title` exactly
 - `pf-single-title`: the document has one level-1 heading, its first heading, which is the title
 - `pf-statement`: a concise statement paragraph of the principle's core idea, typically one to three sentences, follows the H1 directly
-- `pf-key-guidance-first`: the statement comes before the bullets, and the most important bullets come first
-- `pf-actionable-guidance`: unless the statement is self-evident in practice, bullets give its practical applications, each a specific full sentence, two to seven short items of one structure
+- `pf-statement-before-bullets`: the statement comes before the bullets
+- `pf-key-guidance-first`: the most important bullets come first
+- `pf-actionable-guidance`: unless the statement is self-evident in practice, bullets give its practical applications
+- `pf-bullet-right-altitude`: each bullet is specific enough to guide a decision yet flexible enough to work as a heuristic
+- `pf-bullet-full-sentence`: each bullet is a full sentence, not a fragment
+- `pf-bullet-list-shape`: the list holds two to seven short items of one structure
 - `pf-state-why`: the principle says why it holds
-- `pf-only-what-the-agent-lacks`: no bullet holds what the agent already knows, a copied style convention or a lint rule, and each answers a mistake agents make
+- `pf-only-what-the-agent-lacks`: the principle holds only what the agent could not work out for itself
+- `pf-no-copied-conventions`: no bullet copies a common style convention the agent knows or a rule a linter checks
+- `pf-bullet-for-a-repeated-mistake`: each bullet answers a mistake agents repeat without it
 - `pf-brevity`: the body, without frontmatter and Change History, is concise and within ~50 lines, and detailed guidance is in guidelines
-- `pf-always-loaded-budget`: the principle was sized with everything else always loaded, against the hosts' limits
+- `pf-always-loaded-budget`: a principle that loads on every task was sized with everything else always loaded, against the hosts' limits
 - `pf-change-history`: the file ends with a `## Change History` table whose columns are Version, Date, Author and Summary
-- `pf-history-newest-first`: the history has a dated row for every version, the latest first
-- `pf-format-checks-tool-enforced`: every check a script can decide is run by a schema, linter or CI, and the text holds only what no tool checks
+- `pf-history-row-per-version`: the history has a row for every version
+- `pf-history-dated`: each history row shows its version's date
+- `pf-history-newest-first`: the history lists the latest version first
+- `pf-format-checks-tool-enforced`: every check a script can decide is run by a schema, linter or CI
+- `pf-text-holds-untooled-guidance`: the principle's text holds only guidance no tool checks
 - `standard-roled-parts`: a principle added or rewritten gives each part a role
 - `standard-named-rules`: each rule of a roled principle is its own `- **kebab-name**: …` bullet of a `rules` part, with an RFC 2119 keyword
-- `standard-one-source-per-topic`: the topic has one folder, and its detailed guidance is linked from the artifact that owns it, not copied
-- `standard-research-cited`: the principle's research is in its `research/` folder and each named rule cites its claims
+- `standard-one-source-per-topic`: the topic is written once, in one folder
+- `standard-link-detail-not-copy`: detailed guidance lives in the artifact that owns it and is linked, not copied
+- `standard-research-kept`: the principle's research is in its folder's `research/`
+- `standard-research-cited`: each named rule cites the claims it stands on
 - `roles-principle-may-be-roled`: a roled principle compiles to skills like a roled guideline
 - `roles-vocabulary`: every role given is one of `rules`, `how-to`, `examples`, `review-focus`, `review-bar`, `build-bar`, `rationale` or `references`
 - `roles-intro-history-unroled`: neither the intro nor the history carries a role
@@ -202,21 +231,21 @@
 
 ## Rationale
 
-- `pf-frontmatter-complete`, `pf-type-field`: Standards-process documents such as PEPs require a fixed preamble, agent skill files require validated frontmatter, and JSON Schema's `required` and `const` and Astro's collection schemas make required fields and a fixed type checkable by a tool, so both rules stay MUST.
+- `pf-frontmatter-complete`, `pf-no-domain-field`, `pf-type-field`: Standards-process documents such as PEPs require a fixed preamble, agent skill files require validated frontmatter, and JSON Schema's `required` and `const` and Astro's collection schemas, which error on a violation, make required fields, a fixed field set and a fixed type checkable by a tool, so the three rules stay MUST.
 - `pf-summary-what-and-when`: The Agent Skills specification loads only a skill's name and description at startup, and Anthropic's skill guidance asks that the description say what the skill does and when to use it. The sources state this as advice, so the rule is a SHOULD.
 - `pf-title-heading`: Kept as written for the owner to decide. No outside source requires the H1 to equal the frontmatter title. With default settings MD041 accepts a front-matter title in place of an H1 without comparing the two, and MD025 counts a front-matter title as the H1 and flags a later `# Title`; a markdownlint custom rule, which receives the front-matter lines apart from the body, can make the comparison.
 - `pf-single-title`: Google's style guide uses one level-1 heading per page, MD025 asks for a single H1 that is the title, and MD041 treats the first top-level heading as the title; a style guide and a linter's rationale are advice, so the rule is a SHOULD.
 - `pf-statement`: Kept as written for the owner to decide. NN/g's inverted pyramid, Microsoft's "lead with what's most important" and Google's weight on the opening sentence all support the statement first, PEP 1's ~200-word abstract supports a short opening, and readers welcome paragraphs of three to five sentences; each is a recommendation, not a requirement, so the outside evidence holds the rule at SHOULD.
-- `pf-key-guidance-first`: Models use information at the start or end of a long context best (Lost in the Middle) and, at high instruction density, show a bias toward earlier instructions (IFScale), and Microsoft finds the first screen the most read. The IFScale claim was only partly confirmed by the second check, so the rule is a SHOULD.
-- `pf-actionable-guidance`: Anthropic's context-engineering guidance sets instructions at the altitude between brittle logic and vague guidance; its Claude Code guidance finds specific, concise instructions in headed bullets followed more consistently; Cursor asks for focused, actionable rules; Microsoft keeps lists to two to seven short items of one structure; Nygard allows bullets only for visual style, never for fragments.
-- `pf-state-why`, `standard-research-cited`: Anthropic finds that the motivation behind an instruction yields better-targeted behaviour, Diátaxis's explanation pages give the why, and Nygard notes that a decision's motivation is the hardest thing to recover later. The second check confirmed the Nygard claim only in part, so neither rule is a MUST.
-- `pf-only-what-the-agent-lacks`: Anthropic's guidance keeps an always-loaded file to what the agent could not work out itself and asks for the smallest high-signal set of tokens; Cursor says to use a linter rather than copy style guides and to add a rule only when the agent repeats a mistake. The skill-authoring claim was only partly confirmed, so the rule is a SHOULD.
+- `pf-statement-before-bullets`, `pf-key-guidance-first`: Models use information at the start or end of a long context best (Lost in the Middle) and show a bias toward earlier instructions (IFScale), Microsoft finds the first screen the most read, and Google treats the opening sentence as the most important. The IFScale claim was only partly confirmed by the second check, and the others are advice, so both rules are SHOULD.
+- `pf-actionable-guidance`, `pf-bullet-right-altitude`, `pf-bullet-full-sentence`, `pf-bullet-list-shape`: Anthropic's context-engineering guidance sets instructions at the altitude between brittle logic and vague guidance; its Claude Code guidance finds specific, concise instructions in headed bullets followed more consistently; Cursor asks for focused, actionable rules; Microsoft keeps lists to two to seven short items of one structure; Nygard allows bullets only for visual style, never for fragments.
+- `pf-state-why`, `standard-research-kept`, `standard-research-cited`: Anthropic finds that the motivation behind an instruction yields better-targeted behaviour, Diátaxis's explanation pages give the why, and Nygard notes that a decision's motivation is one of the hardest things to track. The second check confirmed the Nygard claim only in part, so none of these rules is a MUST.
+- `pf-only-what-the-agent-lacks`, `pf-no-copied-conventions`, `pf-bullet-for-a-repeated-mistake`: Anthropic's guidance keeps an always-loaded file to what the agent could not work out itself and asks for the smallest high-signal set of tokens; Cursor says to use a linter rather than copy style guides and to add a rule only when the agent repeats a mistake. The skill-authoring claim was only partly confirmed, and the rest is advice, so the rules are SHOULD.
 - `pf-brevity`, `pf-always-loaded-budget`: `pf-brevity` is kept as written for the owner to decide: no source supports a ~50-line cap. The length evidence sets budgets, not a per-principle number: Claude Code targets under 200 lines per always-loaded file, Codex caps the combined instruction files at 32 KiB by default, every always-loaded line costs attention on every task, and instruction-following accuracy falls with density. Which figure a principle's own cap should name depends on whether principles load always or as skills, which is the owner's question.
-- `pf-change-history`, `pf-history-newest-first`: `pf-change-history` is kept as written for the owner to decide; Keep a Changelog recommends an entry for every version, each dated, the latest first, and MD043 can require a final `## Change History` heading. These are recommendations, so the outside evidence holds them at SHOULD.
-- `pf-format-checks-tool-enforced`: Docs-as-code writes documentation with the same tools as code; OpenAI reserves formatting and lint checks for CI; Anthropic puts what must happen every time into enforcement rather than prose; AGENTS.md shows that an agent reads the text whatever its headings. markdownlint (MD043, custom rules), Vale (`metric`, `occurrence`, `script`) and JSON Schema can decide the structural checks. Several of these claims were only partly confirmed, so the rule is a SHOULD.
+- `pf-change-history`, `pf-history-row-per-version`, `pf-history-dated`, `pf-history-newest-first`: `pf-change-history` is kept as written for the owner to decide; Keep a Changelog recommends an entry for every version, each dated, the latest first, and MD043 can require a final `## Change History` heading. These are recommendations, so the outside evidence holds them at SHOULD.
+- `pf-format-checks-tool-enforced`, `pf-text-holds-untooled-guidance`: Docs-as-code writes documentation with the same tools as code; OpenAI reserves formatting and lint checks for CI; Anthropic puts what must happen every time into enforcement rather than prose; AGENTS.md shows that an agent reads the text whatever its headings. markdownlint (MD043, custom rules), Vale (`metric`, `occurrence`, `script`) and JSON Schema can decide the structural checks. Several of these claims were only partly confirmed, so the rule is a SHOULD.
 - `standard-roled-parts`, `roles-principle-may-be-roled`, `roles-four-skills`, `roles-rationale-references-linked`: Anthropic's evaluator-optimizer pattern pairs a generator with an evaluator working against clear criteria, the pattern behind each builder or reviewer and its verifier; a skill's body loads only when a task calls for it; and the Agent Skills specification and Anthropic's skill guidance move detailed reference material into separate files to keep the activated body short.
 - `standard-named-rules`: Headed bullets are easier for an agent to follow than dense paragraphs, Cursor splits large rules into composable ones, and Microsoft keeps list items short and of one structure.
-- `standard-one-source-per-topic`: When two instructions contradict, Claude may pick either; Cursor references a canonical file instead of copying it; Diátaxis keeps instruction out of explanation because it belongs in its own place.
+- `standard-one-source-per-topic`, `standard-link-detail-not-copy`: When two instructions contradict, Claude may pick either; Cursor references a canonical file instead of copying it; Diátaxis keeps instruction out of explanation because it belongs in its own place.
 - `roles-intro-history-unroled`: The main point comes first and reaches every reader; a change history is written for people, not machines, and every line an agent always loads costs attention, so the history stays out of the skills.
 - `roles-vocabulary`, `roles-every-part-roled`, `roles-principle-skill-names`, `roles-principle-routing`: Kept as written for the owner to decide. They are the cookbook's own role mechanics, and no outside source bears on them.
 
