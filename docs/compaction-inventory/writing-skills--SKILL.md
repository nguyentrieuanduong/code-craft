# Inventory: skills/writing-skills/SKILL.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "**Writing skills uses tiered evidence for process documentation.**" | merged into R146 | |
| R2 | "**Personal skills live in your runtime's skills directory**" | cut: non-normative (rule 6) | |
| R3 | "Every change gets deterministic validation. New skills and behavior-shaping edits also use one focused before/after scenario. Larger repeated campaigns are optional release evidence." | merged into R146 | |
| R4 | "**Core principle:** Match evidence cost to risk and test behavioral claims with the smallest scenario that can disprove them." | "**Core principle:** Match evidence cost to risk and test behavioral claims with the smallest scenario that can disprove them." | |
| R5 | "**REQUIRED BACKGROUND:** You MUST understand test-driven-development before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation." | "**REQUIRED BACKGROUND:** You MUST understand test-driven-development before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation." | |
| R6 | "**Official guidance:** For Anthropic's official skill authoring best practices, see anthropic-best-practices.md. This document provides additional patterns and guidelines that complement the TDD-focused approach in this skill." | "**Official guidance:** see anthropic-best-practices.md for Anthropic's skill authoring best practices; this skill complements them with a TDD-focused approach." | |
| R7 | "A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future agents find and apply effective approaches." | cut: non-normative (rule 6) | |
| R8 | "**Skills are:** Reusable techniques, patterns, tools, reference guides" | cut: non-normative (rule 6) | |
| R9 | "**Skills are NOT:** Narratives about how you solved a problem once" | merged into R287 | |
| R10 | "&#124; **Test case** &#124; Deterministic fixture or focused behavior scenario &#124;" | "&#124; **Test case** &#124; Deterministic fixture or focused behavior scenario &#124;" | |
| R11 | "&#124; **Production code** &#124; Skill document (SKILL.md) &#124;" | "&#124; **Production code** &#124; Skill document (SKILL.md) &#124;" | |
| R12 | "&#124; **Test fails (RED)** &#124; Agent violates rule without skill (baseline) &#124;" | "&#124; **Test fails (RED)** &#124; Agent violates rule without skill (baseline) &#124;" | |
| R13 | "&#124; **Test passes (GREEN)** &#124; Agent complies with skill present &#124;" | "&#124; **Test passes (GREEN)** &#124; Agent complies with skill present &#124;" | |
| R14 | "&#124; **Refactor** &#124; Close loopholes while maintaining compliance &#124;" | "&#124; **Refactor** &#124; Close loopholes while maintaining compliance &#124;" | |
| R15 | "&#124; **Write test first** &#124; Run baseline scenario BEFORE writing skill &#124;" | "&#124; **Write test first** &#124; Run baseline scenario BEFORE writing skill &#124;" | |
| R16 | "&#124; **Watch it fail** &#124; Document exact rationalizations agent uses &#124;" | "&#124; **Watch it fail** &#124; Document exact rationalizations agent uses &#124;" | |
| R17 | "&#124; **Minimal code** &#124; Write skill addressing those specific violations &#124;" | "&#124; **Minimal code** &#124; Write skill addressing those specific violations &#124;" | |
| R18 | "&#124; **Watch it pass** &#124; Verify agent now complies &#124;" | "&#124; **Watch it pass** &#124; Verify agent now complies &#124;" | |
| R19 | "&#124; **Refactor cycle** &#124; Find new rationalizations → plug → re-verify &#124;" | "&#124; **Refactor cycle** &#124; Find new rationalizations → plug → re-verify &#124;" | |
| R20 | "New skills and behavior-shaping edits follow RED-GREEN-REFACTOR. Mechanical metadata, description, link, typo, and routing-fixture changes use the deterministic tier." | merged into R155 | |
| R21 | "**Create when:**" | "**Create when:**" | |
| R22 | "- Technique wasn't intuitively obvious to you" | "- Technique wasn't intuitively obvious to you" | |
| R23 | "- You'd reference this again across projects" | "- You'd reference this again across projects" | |
| R24 | "- Pattern applies broadly (not project-specific)" | "- Pattern applies broadly (not project-specific)" | |
| R25 | "- Others would benefit" | "- Others would benefit" | |
| R26 | "**Don't create for:**" | "**Don't create for:**" | |
| R27 | "- One-off solutions" | "- One-off solutions" | |
| R28 | "- Standard practices well-documented elsewhere" | "- Standard practices well-documented elsewhere" | |
| R29 | "- Project-specific conventions (put in your instructions file)" | "- Project-specific conventions (put in your instructions file)" | |
| R30 | "- Mechanical constraints (if it's enforceable with regex/validation, automate it—save documentation for judgment calls)" | "- Mechanical constraints (if it's enforceable with regex/validation, automate it—save documentation for judgment calls)" | |
| R31 | "Concrete method with steps to follow (condition-based-waiting, root-cause-tracing)" | cut: non-normative (rule 6) | |
| R32 | "Way of thinking about problems (flatten-with-flags, test-invariants)" | cut: non-normative (rule 6) | |
| R33 | "API docs, syntax guides, tool documentation (office docs)" | cut: non-normative (rule 6) | |
| R34 | Fenced block starting `skills/` | "(same fenced block, byte for byte)" | |
| R35 | "**Flat namespace** - all skills in one searchable namespace" | "**Flat namespace** - all skills in one searchable namespace" | |
| R36 | "**Separate files for:**" | "**Separate files for:**" | |
| R37 | "1. **Heavy reference** (100+ lines) - API docs, comprehensive syntax" | "1. **Heavy reference** (100+ lines) - API docs, comprehensive syntax" | |
| R38 | "2. **Reusable tools** - Scripts, utilities, templates" | "2. **Reusable tools** - Scripts, utilities, templates" | |
| R39 | "**Keep inline:**" | "**Keep inline:**" | |
| R40 | "- Principles and concepts" | "- Principles and concepts" | |
| R41 | "- Code patterns (< 50 lines)" | "- Code patterns (< 50 lines)" | |
| R42 | "- Everything else" | "- Everything else" | |
| R43 | "**Frontmatter (YAML):**" | "**Frontmatter (YAML):**" | |
| R44 | "- Two required fields: `name` and `description` (see [agentskills.io/specification](https://agentskills.io/specification) for all supported fields)" | "- Two required fields: `name` and `description` (see [agentskills.io/specification](https://agentskills.io/specification) for all supported fields)" | |
| R45 | "- Max 1024 characters total" | "- Max 1024 characters total" | |
| R46 | "- `name`: Use letters, numbers, and hyphens only (no parentheses, special chars)" | "- `name`: Use letters, numbers, and hyphens only (no parentheses, special chars)" | |
| R47 | "- `description`: Third-person, describes ONLY when to use (NOT what it does)" | "- `description`: Third-person, describes ONLY when to use (NOT what it does)" | |
| R48 | "- Start with \"Use when...\" to focus on triggering conditions" | "- Start with \"Use when...\" to focus on triggering conditions" | |
| R49 | "- Include specific symptoms, situations, and contexts" | "- Include specific symptoms, situations, and contexts" | |
| R50 | "- **NEVER summarize the skill's process or workflow** (see SDO section for why)" | "- **NEVER summarize the skill's process or workflow** (see SDO section for why)" | |
| R51 | "- Keep under 500 characters if possible" | "- Keep under 500 characters if possible" | |
| R52 | Fenced block starting `---` | "(same fenced block, byte for byte)" | |
| R53 | "**Critical for discovery:** Future agents need to FIND your skill" | cut: non-normative (rule 6) | |
| R54 | "**Purpose:** Your agent reads the description to decide which skills to load for a given task. Make it answer: \"Should I read this skill right now?\"" | "**Purpose:** Your agent reads the description to decide which skills to load for a given task. Make it answer: \"Should I read this skill right now?\"" | |
| R55 | "**Format:** Start with \"Use when...\" to focus on triggering conditions" | merged into R48 | |
| R56 | "**CRITICAL: Description = When to Use, NOT What the Skill Does**" | merged into R47 | |
| R57 | "The description should ONLY describe triggering conditions. Do NOT summarize the skill's process or workflow in the description." | merged into R50 | |
| R58 | "**Why this matters:** Testing revealed that when a description summarizes the skill's workflow, an agent may follow the description instead of reading the full skill content. A description saying \"code review between tasks\" caused an agent to do ONE review, even though the skill's flowchart clearly showed TWO reviews (spec compliance then code quality)." | "**Why the description must not summarize the workflow:** when it does, an agent may follow the description instead of reading the full skill. A description saying \"code review between tasks\" caused an agent to do ONE review, even though the skill's flowchart clearly showed TWO reviews (spec compliance then code quality). Descriptions that summarize workflow create a shortcut agents will take; the skill body becomes documentation agents skip." | |
| R59 | "When the description was changed to just \"Use when executing implementation plans with independent tasks\" (no workflow summary), the agent correctly read the flowchart and followed the two-stage review process." | cut: non-normative (rule 7) | quote:Use when executing implementation plans with independent tasks |
| R60 | "**The trap:** Descriptions that summarize workflow create a shortcut agents will take. The skill body becomes documentation agents skip." | merged into R58 | |
| R61 | Fenced block starting `# ❌ BAD: Summarizes workflow - agents may follow this instead of reading skill` | cut: non-normative (rule 7) — the kept pair is the first BAD and first GOOD line of this block, now its own block after R58 | block:# ❌ BAD: Summarizes workflow - agents may follow this instead of reading skill |
| R62 | "**Content:**" | "**Content:**" | |
| R63 | "- Use concrete triggers, symptoms, and situations that signal this skill applies" | "- Use concrete triggers, symptoms, and situations that signal this skill applies" | |
| R64 | "- Describe the *problem* (race conditions, inconsistent behavior) not *language-specific symptoms* (setTimeout, sleep)" | "- Describe the *problem* (race conditions, inconsistent behavior) not *language-specific symptoms* (setTimeout, sleep)" | |
| R65 | "- Keep triggers technology-agnostic unless the skill itself is technology-specific" | "- Keep triggers technology-agnostic unless the skill itself is technology-specific" | |
| R66 | "- If skill is technology-specific, make that explicit in the trigger" | "- If skill is technology-specific, make that explicit in the trigger" | |
| R67 | "- Write in third person (injected into system prompt)" | "- Write in third person (injected into system prompt)" | |
| R68 | "- **NEVER summarize the skill's process or workflow**" | merged into R50 | |
| R69 | Fenced block starting `# ❌ BAD: Too abstract, vague, doesn't include when to use` | cut: non-normative (rule 7) | block:# ❌ BAD: Too abstract, vague, doesn't include when to use |
| R70 | "Use words an agent would search for:" | "Use words an agent would search for, early and often:" | |
| R71 | "- Error messages: \"Hook timed out\", \"ENOTEMPTY\", \"race condition\"" | "- Error messages: \"Hook timed out\", \"ENOTEMPTY\", \"race condition\"" | |
| R72 | "- Symptoms: \"flaky\", \"hanging\", \"zombie\", \"pollution\"" | "- Symptoms: \"flaky\", \"hanging\", \"zombie\", \"pollution\"" | |
| R73 | "- Synonyms: \"timeout/hang/freeze\", \"cleanup/teardown/afterEach\"" | "- Synonyms: \"timeout/hang/freeze\", \"cleanup/teardown/afterEach\"" | |
| R74 | "- Tools: Actual commands, library names, file types" | "- Tools: Actual commands, library names, file types" | |
| R75 | "**Use active voice, verb-first:**" | "**Name by what you DO or the core insight, in active voice, verb-first; gerunds (-ing) work well for processes:**" | |
| R76 | "- ✅ `creating-skills` not `skill-creation`" | "- ✅ `creating-skills` not `skill-creation`" | |
| R77 | "- ✅ `condition-based-waiting` not `async-test-helpers`" | "- ✅ `condition-based-waiting` not `async-test-helpers`" | |
| R78 | "**Problem:** getting-started and frequently-referenced skills load into EVERY conversation. Every token counts." | "**Problem:** getting-started and frequently-referenced skills load into EVERY conversation. Every token counts." | |
| R79 | "**Target word counts:**" | "**Target word counts:**" | |
| R80 | "- getting-started workflows: <150 words each" | "- getting-started workflows: <150 words each" | |
| R81 | "- Frequently-loaded skills: <200 words total" | "- Frequently-loaded skills: <200 words total" | |
| R82 | "- Other skills: <500 words (still be concise)" | "- Other skills: <500 words (still be concise)" | |
| R83 | "**Techniques:**" | "**Techniques:**" | |
| R84 | "**Move details to tool help:**" | "**Move details to tool help:**" | |
| R85 | Fenced block starting `# ❌ BAD: Document all flags in SKILL.md` | "(same fenced block, byte for byte)" | |
| R86 | "**Use cross-references:**" | "**Use cross-references:**" | |
| R87 | Fenced block starting `# ❌ BAD: Repeat workflow details` | "(same fenced block, byte for byte)" | |
| R88 | "**Compress examples:**" | "**Compress examples:**" | |
| R89 | Fenced block starting `# ❌ BAD: Verbose example (42 words)` | "(same fenced block, byte for byte)" | |
| R90 | "**Eliminate redundancy:**" | "**Eliminate redundancy:**" | |
| R91 | "- Don't repeat what's in cross-referenced skills" | "- Don't repeat what's in cross-referenced skills" | |
| R92 | "- Don't explain what's obvious from command" | "- Don't explain what's obvious from command" | |
| R93 | "- Don't include multiple examples of same pattern" | "- Don't include multiple examples of same pattern" | |
| R94 | "**Verification:**" | "**Verification:**" | |
| R95 | Fenced block starting `wc -w skills/path/SKILL.md` | "(same fenced block, byte for byte)" | |
| R96 | "**Name by what you DO or core insight:**" | merged into R75 | |
| R97 | "- ✅ `condition-based-waiting` > `async-test-helpers`" | merged into R77 | |
| R98 | "- ✅ `using-skills` not `skill-usage`" | cut: non-normative (rule 7) | code:using-skills; code:skill-usage |
| R99 | "- ✅ `flatten-with-flags` > `data-structure-refactoring`" | "- ✅ `flatten-with-flags` not `data-structure-refactoring`" (moved under R75) | |
| R100 | "- ✅ `root-cause-tracing` > `debugging-techniques`" | cut: non-normative (rule 7) | code:root-cause-tracing; code:debugging-techniques |
| R101 | "**Gerunds (-ing) work well for processes:**" | merged into R75 | |
| R102 | "- `creating-skills`, `testing-skills`, `debugging-with-logs`" | cut: non-normative (rule 7) | code:testing-skills; code:debugging-with-logs |
| R103 | "- Active, describes the action you're taking" | merged into R75 | |
| R104 | "**When writing documentation that references other skills:**" | "**When writing documentation that references other skills:**" | |
| R105 | "Use skill name only, with explicit requirement markers:" | "Use skill name only, with explicit requirement markers:" | |
| R106 | "- ✅ Good: `**REQUIRED SUB-SKILL:** Use test-driven-development`" | "- ✅ Good: `**REQUIRED SUB-SKILL:** Use test-driven-development`" | |
| R107 | "- ✅ Good: `**REQUIRED BACKGROUND:** You MUST understand systematic-debugging`" | "- ✅ Good: `**REQUIRED BACKGROUND:** You MUST understand systematic-debugging`" | |
| R108 | "- ❌ Bad: `See skills/testing/test-driven-development` (unclear if required)" | "- ❌ Bad: `See skills/testing/test-driven-development` (unclear if required)" | |
| R109 | "- ❌ Bad: `@skills/testing/test-driven-development/SKILL.md` (force-loads, burns context)" | "- ❌ Bad: `@skills/testing/test-driven-development/SKILL.md` (force-loads, burns context)" | |
| R110 | "**Why no @ links:** `@` syntax force-loads files immediately, consuming 200k+ context before you need them." | "**Why no @ links:** `@` syntax force-loads files immediately, consuming 200k+ context before you need them." | |
| R111 | Fenced block starting `digraph when_flowchart {` | "(same fenced block, byte for byte)" | |
| R112 | "**Use flowcharts ONLY for:**" | "**Use flowcharts ONLY for:**" | |
| R113 | "- Non-obvious decision points" | "- Non-obvious decision points" | |
| R114 | "- Process loops where you might stop too early" | "- Process loops where you might stop too early" | |
| R115 | "- \"When to use A vs B\" decisions" | "- \"When to use A vs B\" decisions" | |
| R116 | "**Never use flowcharts for:**" | "**Never use flowcharts for:**" | |
| R117 | "- Reference material → Tables, lists" | "- Reference material → Tables, lists" | |
| R118 | "- Code examples → Markdown blocks" | "- Code examples → Markdown blocks" | |
| R119 | "- Linear instructions → Numbered lists" | "- Linear instructions → Numbered lists" | |
| R120 | "- Labels without semantic meaning (step1, helper2)" | "- Labels without semantic meaning (step1, helper2)" | |
| R121 | "See `graphviz-conventions.dot` in this directory for graphviz style rules." | "See `graphviz-conventions.dot` in this directory for graphviz style rules." | |
| R122 | "**Visualizing a skill's flowcharts:** Use `render-graphs.js` in this directory to render a skill's flowcharts to SVG:" | "**Visualizing a skill's flowcharts:** Use `render-graphs.js` in this directory to render a skill's flowcharts to SVG:" | |
| R123 | Fenced block starting `./render-graphs.js ../some-skill           # Each diagram separately` | "(same fenced block, byte for byte)" | |
| R124 | "**One excellent example beats many mediocre ones**" | "**One excellent example beats many mediocre ones**" | |
| R125 | "Choose most relevant language:" | "Choose most relevant language:" | |
| R126 | "- Testing techniques → TypeScript/JavaScript" | "- Testing techniques → TypeScript/JavaScript" | |
| R127 | "- System debugging → Shell/Python" | "- System debugging → Shell/Python" | |
| R128 | "- Data processing → Python" | "- Data processing → Python" | |
| R129 | "**Good example:**" | "**Good example:**" | |
| R130 | "- Complete and runnable" | "- Complete and runnable" | |
| R131 | "- Well-commented explaining WHY" | "- Well-commented explaining WHY" | |
| R132 | "- From real scenario" | "- From real scenario" | |
| R133 | "- Shows pattern clearly" | "- Shows pattern clearly" | |
| R134 | "- Ready to adapt (not generic template)" | "- Ready to adapt (not generic template)" | |
| R135 | "**Don't:**" | "**Don't:**" | |
| R136 | "- Implement in 5+ languages" | "- Implement in 5+ languages" | |
| R137 | "- Create fill-in-the-blank templates" | "- Create fill-in-the-blank templates" | |
| R138 | "- Write contrived examples" | "- Write contrived examples" | |
| R139 | "You're good at porting - one great example is enough." | merged into R124 | |
| R140 | Fenced block starting `defense-in-depth/` | cut: non-normative (rule 7) | block:defense-in-depth/ |
| R141 | "When: All content fits, no heavy reference needed" | merged into R42 | |
| R142 | Fenced block starting `condition-based-waiting/` | cut: non-normative (rule 7) | block:condition-based-waiting/ |
| R143 | "When: Tool is reusable code, not just narrative" | merged into R38 | |
| R144 | Fenced block starting `pptx/` | cut: non-normative (rule 7) | block:pptx/ |
| R145 | "When: Reference material too large for inline" | merged into R37 | |
| R146 | "Match evidence cost to the change; do not fan out agents by default." | "Match evidence cost to the change; do not fan out agents by default." | |
| R147 | "&#124; Deterministic &#124; Every skill change &#124; `python3 -m tools.check` &#124; 0 &#124;" | "&#124; Deterministic &#124; Every skill change &#124; `python3 -m tools.check` &#124; 0 &#124;" | |
| R148 | "&#124; Focused behavioral &#124; New skill or behavior-shaping rule change &#124; One scenario, one before and one after run &#124; 2 maximum &#124;" | "&#124; Focused behavioral &#124; New skill or behavior-shaping rule change &#124; One scenario, one before and one after run &#124; 2 maximum &#124;" | |
| R149 | "&#124; Full campaign &#124; Explicit release decision, unresolved variance, or user request &#124; `--all --allow-many N`, chosen models and reps &#124; Numeric budget required &#124;" | "&#124; Full campaign &#124; Explicit release decision, unresolved variance, or user request &#124; `--all --allow-many N`, chosen models and reps &#124; Numeric budget required &#124;" | |
| R150 | "Description, metadata, link, typo, and routing-fixture changes stop after the deterministic tier when structural, positive, and negative checks pass and collision warnings are reviewed. Do not spend model tokens merely to reconfirm a mechanical property." | "Description, metadata, link, typo, and routing-fixture changes stop after the deterministic tier when structural, positive, and negative checks pass and collision warnings are reviewed. Do not spend model tokens merely to reconfirm a mechanical property." | |
| R151 | "When an intended skill or description change alters routing, update the affected routing case with a rationale in the commit describing the intended shift. This is the only sanctioned exception to the rule against editing fixtures merely to recover a score." | "When an intended skill or description change alters routing, update the affected routing case with a rationale in the commit describing the intended shift. This is the only sanctioned exception to the rule against editing fixtures merely to recover a score." | |
| R152 | "For a behavior-shaping edit, choose the smallest scenario that reproduces the failure. Run the current wording once, make the minimal edit, then run the same scenario once with the edited wording. Runs are sequential; do not dispatch a subagent fleet. Read both transcripts. A single sample is focused evidence, not a statistical claim." | "For a behavior-shaping edit, choose the smallest scenario that reproduces the failure. Run the current wording once, make the minimal edit, then run the same scenario once with the edited wording. Runs are sequential; do not dispatch a subagent fleet. Read both transcripts. A single sample is focused evidence, not a statistical claim." | |
| R153 | "A full campaign is optional and never runs in CI. Use it only when the release decision needs cross-model or repeated evidence. Calculate the planned calls first, then pass that number as `--allow-many N`." | "A full campaign is optional and never runs in CI. Use it only when the release decision needs cross-model or repeated evidence. Calculate the planned calls first, then pass that number as `--allow-many N`." | |
| R154 | Fenced block starting `NO BEHAVIOR-SHAPING SKILL CHANGE WITHOUT A FAILING FOCUSED TEST FIRST` | "(same fenced block, byte for byte)" | |
| R155 | "This applies to new skills and edits that change what a skill teaches. Mechanical changes use deterministic RED/GREEN checks instead." | "This applies to new skills and edits that change what a skill teaches. Mechanical changes use deterministic RED/GREEN checks instead." | |
| R156 | "Write skill before testing? Delete it. Start over. Edit skill without testing? Same violation." | "Write skill before testing? Delete it. Start over. Edit skill without testing? Same violation." | |
| R157 | "**No exceptions for behavior-shaping edits:**" | "**No exceptions for behavior-shaping edits:**" | |
| R158 | "- Don't keep untested changes as \"reference\"" | "- Don't keep untested changes as \"reference\"" | |
| R159 | "- Don't \"adapt\" while running the focused test" | "- Don't \"adapt\" while running the focused test" | |
| R160 | "- Delete means delete" | "- Delete means delete" | |
| R161 | "**REQUIRED BACKGROUND:** The test-driven-development skill explains why this matters. Same principles apply to documentation." | merged into R5 | |
| R162 | "Different skill types need different test approaches:" | "Different skill types need different test approaches:" | |
| R163 | "**Examples:** TDD, verification-before-completion, designing-before-coding" | cut: non-normative (rule 7) | |
| R164 | "**Test with:**" | "**Test with:**" | |
| R165 | "- Academic questions: Do they understand the rules?" | "- Academic questions: Do they understand the rules?" | |
| R166 | "- Pressure scenarios: Do they comply under stress?" | "- Pressure scenarios: Do they comply under stress?" | |
| R167 | "- Multiple pressures combined: time + sunk cost + exhaustion" | "- Multiple pressures combined: time + sunk cost + exhaustion" | |
| R168 | "- Identify rationalizations and add explicit counters" | "- Identify rationalizations and add explicit counters" | |
| R169 | "**Success criteria:** Agent follows rule under maximum pressure" | "**Success criteria:** Agent follows rule under maximum pressure" | |
| R170 | "**Examples:** condition-based-waiting, root-cause-tracing, defensive-programming" | cut: non-normative (rule 7) | |
| R171 | "**Test with:**" | "**Test with:**" | |
| R172 | "- Application scenarios: Can they apply the technique correctly?" | "- Application scenarios: Can they apply the technique correctly?" | |
| R173 | "- Variation scenarios: Do they handle edge cases?" | "- Variation scenarios: Do they handle edge cases?" | |
| R174 | "- Missing information tests: Do instructions have gaps?" | "- Missing information tests: Do instructions have gaps?" | |
| R175 | "**Success criteria:** Agent successfully applies technique to new scenario" | "**Success criteria:** Agent successfully applies technique to new scenario" | |
| R176 | "**Examples:** reducing-complexity, information-hiding concepts" | cut: non-normative (rule 7) | |
| R177 | "**Test with:**" | "**Test with:**" | |
| R178 | "- Recognition scenarios: Do they recognize when pattern applies?" | "- Recognition scenarios: Do they recognize when pattern applies?" | |
| R179 | "- Application scenarios: Can they use the mental model?" | "- Application scenarios: Can they use the mental model?" | |
| R180 | "- Counter-examples: Do they know when NOT to apply?" | "- Counter-examples: Do they know when NOT to apply?" | |
| R181 | "**Success criteria:** Agent correctly identifies when/how to apply pattern" | "**Success criteria:** Agent correctly identifies when/how to apply pattern" | |
| R182 | "**Examples:** API documentation, command references, library guides" | cut: non-normative (rule 7) | |
| R183 | "**Test with:**" | "**Test with:**" | |
| R184 | "- Retrieval scenarios: Can they find the right information?" | "- Retrieval scenarios: Can they find the right information?" | |
| R185 | "- Application scenarios: Can they use what they found correctly?" | "- Application scenarios: Can they use what they found correctly?" | |
| R186 | "- Gap testing: Are common use cases covered?" | "- Gap testing: Are common use cases covered?" | |
| R187 | "**Success criteria:** Agent finds and correctly applies reference information" | "**Success criteria:** Agent finds and correctly applies reference information" | |
| R188 | "&#124; \"Skill is obviously clear\" &#124; Clear to you ≠ clear to other agents. Run the applicable tier. &#124;" | "&#124; \"Skill is obviously clear\" / \"I'm confident it's good\" &#124; Clear to you ≠ clear to other agents, and confidence is not evidence. Run the applicable tier. &#124;" | |
| R189 | "&#124; \"It's just a reference\" &#124; References can have gaps; deterministic checks still apply. &#124;" | "&#124; \"It's just a reference\" &#124; References can have gaps; deterministic checks still apply. &#124;" | |
| R190 | "&#124; \"Testing is overkill\" &#124; Use deterministic checks for mechanical changes and focused evidence for behavior. &#124;" | "&#124; \"Testing is overkill\" &#124; Use deterministic checks for mechanical changes and focused evidence for behavior. &#124;" | |
| R191 | "&#124; \"I'll test if problems emerge\" &#124; Problems = agents can't use skill. Test BEFORE deploying. &#124;" | "&#124; \"I'll test if problems emerge\" / \"Too tedious to test\" / \"No time to test\" &#124; Problems = agents can't use skill, and fixing a bad skill in production costs more than testing it. Test BEFORE deploying. &#124;" | |
| R192 | "&#124; \"Too tedious to test\" &#124; Testing is less tedious than debugging bad skill in production. &#124;" | merged into R191 | |
| R193 | "&#124; \"I'm confident it's good\" &#124; Overconfidence guarantees issues. Test anyway. &#124;" | merged into R188 | |
| R194 | "&#124; \"Academic review is enough\" &#124; Reading ≠ using. Test application scenarios. &#124;" | "&#124; \"Academic review is enough\" &#124; Reading ≠ using. Test application scenarios. &#124;" | |
| R195 | "&#124; \"No time to test\" &#124; Deploying untested skill wastes more time fixing it later. &#124;" | merged into R191 | |
| R196 | "**All of these mean: Complete the applicable tier before deploying.**" | "**All of these mean: Complete the applicable tier before deploying.**" | |
| R197 | "Before writing guidance, classify the baseline failure. The form that bulletproofs one failure type measurably backfires on another." | "Before writing guidance, classify the baseline failure. The form that bulletproofs one failure type measurably backfires on another." | |
| R198 | "&#124; Skips/violates a rule under pressure (knows better, does it anyway) &#124; Prohibition + rationalization table + red flags (see Bulletproofing below) &#124; Soft guidance (\"prefer...\", \"consider...\") &#124;" | "&#124; Skips/violates a rule under pressure (knows better, does it anyway) &#124; Prohibition + rationalization table + red flags (see Bulletproofing below) &#124; Soft guidance (\"prefer...\", \"consider...\") &#124;" | |
| R199 | "&#124; Complies, but output has the wrong shape (bloated prompt, buried verdict, restated spec) &#124; Positive recipe or contract: state what the output IS — its parts, in order &#124; Prohibition list (\"don't restate\", \"never narrate\") &#124;" | "&#124; Complies, but output has the wrong shape (bloated prompt, buried verdict, restated spec) &#124; Positive recipe or contract: state what the output IS — its parts, in order &#124; Prohibition list (\"don't restate\", \"never narrate\") &#124;" | |
| R200 | "&#124; Omits a required element from something they already produce &#124; Structural: REQUIRED field or slot in the template they fill in &#124; Prose reminders near the template &#124;" | "&#124; Omits a required element from something they already produce &#124; Structural: REQUIRED field or slot in the template they fill in &#124; Prose reminders near the template &#124;" | |
| R201 | "&#124; Behavior should depend on a condition &#124; Conditional keyed to an observable predicate (\"if the brief exists, reference it\") &#124; Unconditional rule + exemption clauses &#124;" | "&#124; Behavior should depend on a condition &#124; Conditional keyed to an observable predicate (\"if the brief exists, reference it\") &#124; Unconditional rule + exemption clauses &#124;" | |
| R202 | "**Why prohibitions backfire on shaping problems:** under a competing incentive (\"make the prompt self-contained\"), agents negotiate with \"don't X\". In head-to-head wording tests on dispatch-prompt guidance, the prohibition arm produced clearly more of the unwanted content than the recipe arm (fully separated distributions), and trended worse than even the no-guidance control — micro-test your own case rather than assuming, but never reach for the prohibition by default. A recipe leaves nothing to negotiate: the output matches the stated shape or it doesn't." | "**Why prohibitions backfire on shaping problems:** under a competing incentive (\"make the prompt self-contained\"), agents negotiate with \"don't X\". In head-to-head wording tests on dispatch-prompt guidance, the prohibition arm produced clearly more of the unwanted content than the recipe arm (fully separated distributions), and trended worse than even the no-guidance control — micro-test your own case rather than assuming, but never reach for the prohibition by default. A recipe leaves nothing to negotiate: the output matches the stated shape or it doesn't." | |
| R203 | "**Rules for whichever form you pick:**" | "**Rules for whichever form you pick:**" | |
| R204 | "- **No nuance clauses.** \"Don't X unless it matters\" reopens the negotiation — appending a single nuance clause to a winning recipe degraded it from consistent to noisy in the same wording tests. Express a real exception as its own conditional on an observable predicate." | "- **No nuance clauses.** \"Don't X unless it matters\" reopens the negotiation — appending a single nuance clause to a winning recipe degraded it from consistent to noisy in the same wording tests. Express a real exception as its own conditional on an observable predicate." | |
| R205 | "- **Exemption clauses don't scope.** \"This limit doesn't apply to code blocks\" still suppresses code blocks. If part of the output must be exempt, restructure so the rule can't reach it." | "- **Exemption clauses don't scope.** \"This limit doesn't apply to code blocks\" still suppresses code blocks. If part of the output must be exempt, restructure so the rule can't reach it." | |
| R206 | "Skills that enforce discipline (like TDD) need to resist rationalization. Agents are smart and will find loopholes when under pressure." | cut: non-normative (rule 6) | |
| R207 | "**Scope:** this toolkit is for discipline failures — an agent that knows the rule and skips it under pressure. For wrong-shaped output or omitted elements, prohibition-based bulletproofing backfires; use the forms in Match the Form to the Failure instead." | "**Scope:** this toolkit is for discipline failures — an agent that knows the rule and skips it under pressure. For wrong-shaped output or omitted elements, prohibition-based bulletproofing backfires; use the forms in Match the Form to the Failure instead." | |
| R208 | "**Psychology note:** Understanding WHY persuasion techniques work helps you apply them systematically. See persuasion-principles.md for research foundation (Cialdini, 2021; Meincke et al., 2025) on authority, commitment, scarcity, social proof, and unity principles." | "**Psychology note:** to apply persuasion techniques systematically, see persuasion-principles.md for why they work — research foundation (Cialdini, 2021; Meincke et al., 2025) on authority, commitment, scarcity, social proof, and unity principles." | |
| R209 | "Don't just state the rule - forbid specific workarounds:" | "Don't just state the rule - forbid specific workarounds:" | |
| R210 | "<Bad>" | "<Bad>" | |
| R211 | Fenced block starting `Write code before test? Delete it.` | "(same fenced block, byte for byte)" | |
| R212 | "</Bad>" | "</Bad>" | |
| R213 | "<Good>" | "<Good>" | |
| R214 | Fenced block starting `Write code before test? Delete it. Start over.` | "(same fenced block, byte for byte)" | |
| R215 | "</Good>" | "</Good>" | |
| R216 | "Add foundational principle early:" | "Add foundational principle early:" | |
| R217 | Fenced block starting `**Violating the letter of the rules is violating the spirit of the rules.**` | "(same fenced block, byte for byte)" | |
| R218 | "This cuts off entire class of \"I'm following the spirit\" rationalizations." | "This cuts off entire class of \"I'm following the spirit\" rationalizations." | |
| R219 | "Capture rationalizations from baseline testing (see Testing section below). Every excuse agents make goes in the table:" | "Capture rationalizations from baseline testing (see Testing section below). Every excuse agents make goes in the table:" | |
| R220 | Fenced block starting `&#124; Excuse &#124; Reality &#124;` | "(same fenced block, byte for byte)" | |
| R221 | "Make it easy for agents to self-check when rationalizing:" | "Make it easy for agents to self-check when rationalizing:" | |
| R222 | Fenced block starting `## Red Flags - STOP and Start Over` | "(same fenced block, byte for byte)" | |
| R223 | "Add to description: symptoms of when you're ABOUT to violate the rule:" | "Add to description: symptoms of when you're ABOUT to violate the rule:" | |
| R224 | Fenced block starting `description: use when implementing any feature or bugfix, before writing implementation code` | "(same fenced block, byte for byte)" | |
| R225 | "Follow the TDD cycle:" | "Follow the TDD cycle:" | |
| R226 | "For new skills and behavior changes, run one focused scenario against the current wording. Document exact behavior:" | "For new skills and behavior changes, run one focused scenario against the current wording. Document exact behavior:" | |
| R227 | "- What choices did they make?" | "- What choices did they make?" | |
| R228 | "- What rationalizations did they use (verbatim)?" | "- What rationalizations did they use (verbatim)?" | |
| R229 | "- Which pressures triggered violations?" | "- Which pressures triggered violations?" | |
| R230 | "This is \"watch the test fail\" - you must see what agents naturally do before writing the skill." | "This is \"watch the test fail\" - you must see what agents naturally do before writing the skill." | |
| R231 | "Trigger-only and other mechanical changes use failing deterministic routing or structure cases instead." | "Trigger-only and other mechanical changes use failing deterministic routing or structure cases instead." | |
| R232 | "Write skill that addresses those specific rationalizations. Don't add extra content for hypothetical cases." | "Write skill that addresses those specific rationalizations. Don't add extra content for hypothetical cases." | |
| R233 | "Run the same focused scenario once with the edited skill. The agent should now comply. For a mechanical edit, rerun the deterministic check." | "Run the same focused scenario once with the edited skill. The agent should now comply. For a mechanical edit, rerun the deterministic check." | |
| R234 | "Agent found new rationalization? Add explicit counter. Re-test until bulletproof." | "Agent found new rationalization? Add explicit counter. Re-test until bulletproof." | |
| R235 | "Focused before/after evidence is the default behavioral gate. When a release decision needs statistical or cross-model evidence, run an explicit full campaign:" | "Focused before/after evidence is the default behavioral gate. When a release decision needs statistical or cross-model evidence, run an explicit full campaign:" | |
| R236 | "1. Calculate calls across scenarios, arms, models, and repetitions." | "1. Calculate calls across scenarios, arms, models, and repetitions." | |
| R237 | "2. Pass the total with `--all --allow-many N`." | "2. Pass the total with `--all --allow-many N`." | |
| R238 | "3. Include a no-guidance control when attribution matters." | "3. Include a no-guidance control when attribution matters." | |
| R239 | "4. Manually read every flagged match; template echoes and quoted counter-examples can masquerade as hits." | "4. Manually read every flagged match; template echoes and quoted counter-examples can masquerade as hits." | |
| R240 | "5. Treat variance as a metric, not proof from any single sample." | "5. Treat variance as a metric, not proof from any single sample." | |
| R241 | "Full campaigns strengthen focused evidence when a release decision needs it; they are not a routine merge requirement." | merged into R153 | |
| R242 | "**Optional campaign methodology:** See [testing-skills-with-subagents.md](testing-skills-with-subagents.md) for:" | "**Optional campaign methodology:** See [testing-skills-with-subagents.md](testing-skills-with-subagents.md) for:" | |
| R243 | "- How to write pressure scenarios" | "- How to write pressure scenarios" | |
| R244 | "- Pressure types (time, sunk cost, authority, exhaustion)" | "- Pressure types (time, sunk cost, authority, exhaustion)" | |
| R245 | "- Plugging holes systematically" | "- Plugging holes systematically" | |
| R246 | "- Meta-testing techniques" | "- Meta-testing techniques" | |
| R247 | "\"In session 2025-10-03, we found empty projectDir caused...\" **Why bad:** Too specific, not reusable" | merged into R287 | quote:In session 2025-10-03, we found empty projectDir caused...; number:03; number:10 |
| R248 | "example-js.js, example-py.py, example-go.go **Why bad:** Mediocre quality, maintenance burden" | merged into R136 | |
| R249 | Fenced block starting `step1 [label=\"import fs\"];` | "(same fenced block, byte for byte)" (moved under R120) | |
| R250 | "**Why bad:** Can't copy-paste, hard to read" | "Code in a flowchart can't be copy-pasted and is hard to read:" | |
| R251 | "helper1, helper2, step3, pattern4 **Why bad:** Labels should have semantic meaning" | merged into R120 | |
| R252 | "**After writing any skill, stop and complete its applicable evaluation tier.**" | "**STOP after writing any skill: complete its applicable evaluation tier before moving to the next one.** Do NOT create multiple skills in batch without testing each, or skip testing because \"batching is more efficient\". Deploying without the applicable evidence is a quality failure." | |
| R253 | "**Do NOT:**" | merged into R252 | |
| R254 | "- Create multiple skills in batch without testing each" | merged into R252 | |
| R255 | "- Move to next skill before current one is verified" | merged into R252 | |
| R256 | "- Skip testing because \"batching is more efficient\"" | merged into R252 | |
| R257 | "**The deployment checklist below is MANDATORY for EACH skill.**" | merged into R259 | |
| R258 | "Deploying without the applicable evidence is a quality failure." | merged into R252 | |
| R259 | "**IMPORTANT: Create a todo for EACH checklist item below.**" | "**IMPORTANT: This checklist is MANDATORY for EACH skill. Create a todo for EACH checklist item below.**" | |
| R260 | "**RED Phase - Establish Evidence:**" | "**RED Phase - Establish Evidence:**" | |
| R261 | "- [ ] Add deterministic positive/negative routing or structure coverage" | "- [ ] Add deterministic positive/negative routing or structure coverage" | |
| R262 | "- [ ] For a new skill or behavior change, add one focused scenario" | "- [ ] For a new skill or behavior change, add one focused scenario" | |
| R263 | "- [ ] Run the focused scenario once with current wording and record the failure" | "- [ ] Run the focused scenario once with current wording and record the failure" | |
| R264 | "**GREEN Phase - Write Minimal Skill:**" | "**GREEN Phase - Write Minimal Skill:**" | |
| R265 | "- [ ] Name uses only letters, numbers, hyphens (no parentheses/special chars)" | "- [ ] Name uses only letters, numbers, hyphens (no parentheses/special chars)" | |
| R266 | "- [ ] YAML frontmatter with required `name` and `description` fields (max 1024 chars; see [spec](https://agentskills.io/specification))" | "- [ ] YAML frontmatter with required `name` and `description` fields (max 1024 chars; see [spec](https://agentskills.io/specification))" | |
| R267 | "- [ ] Description starts with \"Use when...\" and includes specific triggers/symptoms" | "- [ ] Description starts with \"Use when...\" and includes specific triggers/symptoms" | |
| R268 | "- [ ] Description written in third person" | "- [ ] Description written in third person" | |
| R269 | "- [ ] Keywords throughout for search (errors, symptoms, tools)" | "- [ ] Keywords throughout for search (errors, symptoms, tools)" | |
| R270 | "- [ ] Clear overview with core principle" | "- [ ] Clear overview with core principle" | |
| R271 | "- [ ] Address specific baseline failures identified in RED" | "- [ ] Address specific baseline failures identified in RED" | |
| R272 | "- [ ] Guidance form matches the failure type (see Match the Form to the Failure)" | "- [ ] Guidance form matches the failure type (see Match the Form to the Failure)" | |
| R273 | "- [ ] For behavior-shaping guidance, run the same focused scenario once after the edit and read both transcripts" | "- [ ] For behavior-shaping guidance, run the same focused scenario once after the edit and read both transcripts" | |
| R274 | "- [ ] Code inline OR link to separate file" | "- [ ] Code inline OR link to separate file" | |
| R275 | "- [ ] One excellent example (not multi-language)" | "- [ ] One excellent example (not multi-language)" | |
| R276 | "- [ ] Run `python3 -m tools.check`" | "- [ ] Run `python3 -m tools.check`" | |
| R277 | "**REFACTOR Phase - Close Loopholes:**" | "**REFACTOR Phase - Close Loopholes:**" | |
| R278 | "- [ ] Identify NEW rationalizations from testing" | "- [ ] Identify NEW rationalizations from testing" | |
| R279 | "- [ ] Add explicit counters (if discipline skill)" | "- [ ] Add explicit counters (if discipline skill)" | |
| R280 | "- [ ] Build rationalization table from all test iterations" | "- [ ] Build rationalization table from all test iterations" | |
| R281 | "- [ ] Create red flags list" | "- [ ] Create red flags list" | |
| R282 | "- [ ] Re-run the focused scenario only when closing an observed behavioral loophole" | "- [ ] Re-run the focused scenario only when closing an observed behavioral loophole" | |
| R283 | "**Quality Checks:**" | "**Quality Checks:**" | |
| R284 | "- [ ] Small flowchart only if decision non-obvious" | "- [ ] Small flowchart only if decision non-obvious" | |
| R285 | "- [ ] Quick reference table" | "- [ ] Quick reference table" | |
| R286 | "- [ ] Common mistakes section" | "- [ ] Common mistakes section" | |
| R287 | "- [ ] No narrative storytelling" | "- [ ] No narrative storytelling" | |
| R288 | "- [ ] Supporting files only for tools or heavy reference" | "- [ ] Supporting files only for tools or heavy reference" | |
| R289 | "**Deployment:**" | "**Deployment:**" | |
| R290 | "- [ ] Commit skill to git and push to your fork (if configured)" | "- [ ] Commit skill to git and push to your fork (if configured)" | |
| R291 | "- [ ] Consider contributing back via PR (if broadly useful)" | "- [ ] Consider contributing back via PR (if broadly useful)" | |
| R292 | "How future agents find your skill:" | cut: non-normative (rule 6) | |
| R293 | "1. **Encounters problem** (\"tests are flaky\")" | cut: non-normative (rule 6) | quote:tests are flaky |
| R294 | "2. **Searches skills** (greps descriptions, browses categories)" | cut: non-normative (rule 6) | |
| R295 | "3. **Finds SKILL** (description matches)" | cut: non-normative (rule 6) | |
| R296 | "4. **Scans overview** (is this relevant?)" | cut: non-normative (rule 6) | |
| R297 | "5. **Reads patterns** (quick reference table)" | cut: non-normative (rule 6) | |
| R298 | "6. **Loads example** (only when implementing)" | cut: non-normative (rule 6) | |
| R299 | "**Optimize for this flow** - put searchable terms early and often." | merged into R70 | |
| R300 | "**Creating skills uses TDD where behavior changes and deterministic checks where it does not.**" | merged into R155 | |
| R301 | "Same Iron Law for behavior: no behavior-shaping edit without a focused RED. Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes). Same benefits: Better quality, fewer surprises, bulletproof results." | merged into R154 | |
| R302 | "If you follow TDD for code, follow it for skills. It's the same discipline applied to documentation." | cut: non-normative (rule 6) | |

Counts (checker): 4040 -> 3284 words (18% cut), 532 -> 428 nonblank lines.
Note: the "Code in Flowcharts" anti-example block (R249) is kept and moved under R120 because the checker splits Items on ";" and that block's first line ends in ";", so it cannot be listed as an exemption.
