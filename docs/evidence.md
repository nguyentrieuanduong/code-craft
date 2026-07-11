# Why process, not capability — the evidence

The suite's premise is that output quality comes from process, not raw
capability. That premise is measurable. Sources verified 2026-07-11;
full citations in [anti-patterns.md](anti-patterns.md) Appendix B and the
source list in `recommend.md`.

## The documented AI-assisted failure mode

| Finding | Source |
|---|---|
| +25% AI adoption → delivery throughput −1.5%, delivery **stability −7.2%**. Named mechanism: AI inflates change batch size | DORA, *State of DevOps 2024* |
| "AI is an amplifier" — it magnifies strong systems and dysfunctional ones alike; ~30% of respondents report little or no trust in AI-generated code, yet ship it | DORA, *State of AI-assisted Software Development 2025* |
| Experienced OSS maintainers *felt* ~20% faster with AI assistance; measured **19% slower** (RCT, 246 real tasks, early-2025 tools) | METR 2025 |
| Duplicated code blocks up ~8x in 2024; copy/paste exceeded refactor-moves for the first time on record | GitClear (vendor dataset, 211M changed lines) |
| 19.7% of LLM package suggestions name nonexistent packages; 43% of fake names recur across runs — pre-registerable by attackers ("slopsquatting") | Spracklen et al., USENIX Security 2025 |

Honesty notes: METR's 2026 follow-up suggests parity-or-better with newer
tools but is confounded by selection effects, and METR labels the original
result historical. The durable lesson is the **perception gap**: "feels
done / feels faster / works" is untrustworthy, so verification must be
mechanical. GitClear is vendor research — treat direction, not magnitude.

## What the suite does about it, mechanism by mechanism

| Existing mechanism | Supporting evidence |
|---|---|
| TDD iron law (`test-driven-development`) | 4 industrial IBM/Microsoft teams: pre-release defect density −40–90% for +15–35% initial time (Nagappan 2008) |
| Evidence over adjectives (`verification-before-completion`) | The METR perception gap above: self-assessment of speed and doneness is measurably wrong, so only command output counts |
| Small commits, one feature per commit (`coding-standards`, `executing-plans`) | Batch-size inflation is DORA 2024's named mechanism for the −7.2% stability cost; Google's median reviewed change is ~24 LOC with <4h review latency (Sadowski 2018) |
| Review physics (`code-review`) | Defect-finding collapses past ~400 changed LOC and ~500 LOC/hour (SmartBear/Cisco study of 2,500 reviews) |
| Checklists + hard gates as the *form* of every skill | WHO 19-item surgical checklist: deaths 1.5%→0.8%, complications 11%→7% across 8 hospitals (Haynes 2009, NEJM) — checklists beat expertise-on-the-fly even in high-skill work |
| Worst-case coverage + boundary error handling (`test-driven-development`, `coding-standards`) | 92% of catastrophic distributed-system failures stem from mishandled non-fatal errors; 58% preventable by trivial error-path tests (Yuan et al., OSDI 2014); OWASP added *Mishandling of Exceptional Conditions* in 2025 |
| REFACTOR step on green (`test-driven-development`) | GitClear's duplication trend above: AI-generated code trends anti-refactor unless a step forces it |
| Design-doc gate before code (`brainstorming` → `docs/specs/`) | Decision records with context survive session loss (Nygard 2011) — matches the resume-from-git-log model |
| Reproduction-first debugging (`systematic-debugging`) | 77% of the OSDI-2014 production failures were reproducible by a unit test — reproduction is the highest-yield move |
| Supply-chain gate (SEC-09 + `guard-installs.py`) | The slopsquatting numbers above; OWASP promoted Software Supply Chain Failures to A03 in 2025 |
| Hooks over instructions | DORA 2025's amplifier thesis: value comes from the surrounding system, not the model — so the system, not the prompt, carries the rules |

## DORA 2025 capabilities → code-craft

Of the seven capabilities DORA identifies as turning AI adoption into
positive outcomes, the suite mechanically implements four (the others are
organizational: data ecosystems, AI-accessible internal data, user focus):

| DORA capability | Where in the suite |
|---|---|
| Clear, communicated AI stance | `AGENTS.md` non-negotiables + dispatch table — the agent's working agreement |
| Strong version control practices | Commit-per-step recovery model; `guard-bash.py` blocks `--no-verify` and force-pushes |
| Working in small batches | One-feature-per-commit; plan steps sized to single commits |
| Quality internal platform | The plugin itself: hooks enforce what instructions merely request |

Skill pressure-tests should target exactly the failure modes on this page:
code before test, done without verification, batch inflation, invented
dependencies, copy-paste instead of refactoring.
