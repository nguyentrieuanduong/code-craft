# code-craft: what to add — evidence-backed recommendations

Verdict: the suite's core loop (design gate → exact plans → TDD → verification
→ two-verdict review → finishing gate) is not just internally consistent — it
is the empirically supported response to how AI-assisted development fails.
The highest-value additions are, in order: an eval harness (it gates all other
skill work), supply-chain vetting (the one live security hole), a diff-size
gate (the mechanism behind AI's instability cost), and an evidence doc (the
adoption pitch). Deployment-stage skills are worthwhile but second tier.

Evidence basis: full skill/hook/test inventory re-read 2026-07-11 (14 skills,
5 hooks, ~40 hook regression tests, ~61 encoded rules/gates); web-verified
practice evidence gathered 2026-07-11 (sources at end); incident evidence in
`docs/anti-patterns.md` appendices. Vendor-research caveats are marked.

## 1. What the suite already gets right — now with numbers

Do not churn these; the evidence says keep them. Attach these numbers to the
README pitch (see R4).

| Existing mechanism | Supporting evidence |
|---|---|
| TDD iron law (`test-driven-development`) | 4 industrial IBM/Microsoft teams: pre-release defect density −40–90% for +15–35% initial time (Nagappan 2008) |
| Verification gate — evidence over adjectives (`verification-before-completion`) | METR RCT: devs *felt* 20% faster with AI, measured 19% *slower* (early-2025 tools); self-perception is untrustworthy, so mechanical verification is the only honest signal (METR 2025) |
| Small commits, one-feature-per-commit (`coding-standards`, `executing-plans`) | DORA 2024: +25% AI adoption → delivery stability −7.2%, throughput −1.5%; DORA's stated mechanism is AI inflating batch size. Google's median reviewed change is ~24 LOC (Sadowski 2018) |
| Checklists + hard gates as the *form* of every skill | WHO 19-item surgical checklist: deaths 1.5%→0.8% (−47% rel.), complications 11%→7% across 8 hospitals (Haynes 2009, NEJM) — checklists beat expertise-on-the-fly in high-skill work |
| Worst-case test coverage + boundary error handling (`test-driven-development`, `coding-standards`) | 92% of catastrophic distributed-system failures stem from mishandled non-fatal errors; 58% preventable by trivial error-path tests (Yuan 2014); OWASP added Mishandling of Exceptional Conditions in 2025 |
| REFACTOR step on green (`test-driven-development`) | GitClear (vendor data, 211M lines): 2024 duplicated blocks up ~8x, copy/paste exceeded moved lines for the first time; AI code trends anti-refactor unless forced |
| Design-doc gate before code (`brainstorming` → `docs/specs/`) | Functions as ADR practice (Nygard 2011): decisions with context survive session/context loss — matches this repo's resume-from-git-log model |
| Systematic debugging with 3-failure circuit breaker | Matches Yuan 2014: 77% of production failures reproducible by unit test — reproduction-first is the highest-yield move |
| Hook enforcement over instructions | DORA 2025 AI Capabilities Model: value comes from the surrounding system, not the model — "AI is an amplifier" |

## 2. Ranked additions

Rank = mission impact (junior devs + lower-capability models shipping
disciplined work) per unit effort, respecting the standing caution that
skill-wording changes require before/after evals (§4).

### R1. Skill eval harness — `tests/scenarios/` (L, no eval needed — it IS the eval)

**What:** Pressure-test scenario corpus + runner: per skill, 3–5 scenarios
(baseline agent without skill vs with skill), recorded rationalizations,
pass/fail assertions on behavior (e.g. "wrote code before test?", "claimed
done without running suite?"). `writing-skills` already prescribes exactly
this (RED→GREEN→REFACTOR for docs, subagent testing) — the corpus and runner
just don't exist; `tests/` covers hooks only.
**Why first:** every other skill-touching item below is gated on evals; the
README's own next step ("pressure-test on a real Sonnet/Haiku session") is
this; and new skills (R6) are barred by writing-skills' iron law until a
failing test exists.
**Shape:** `tests/scenarios/<skill>/*.md` + a runner script dispatching
subagents; start with the 3 skills whose wording gets edited most.

### R2. Supply-chain vetting — SEC-09 + install-guard hook (M, hook needs no eval; SEC-09 is additive)

**What:** `security-baseline` currently stops at "no dependency added without
stated reason." Add SEC-09: lockfile committed, versions pinned, new packages
verified to exist on the registry with plausible age/adoption before install,
provenance preferred. Pair with a `PreToolUse` Bash hook matching
`npm|pnpm|yarn add`, `pip install`, `uv add`, `cargo add`, `go get` that
returns permission-decision *ask* with the vetting checklist.
**Why:** the one live hole, and it is AI-specific: ~19.7% of LLM package
suggestions name nonexistent packages, 43% of hallucinated names recur every
run — pre-registerable by attackers ("slopsquatting", Spracklen 2025, USENIX
Security). OWASP promoted Software Supply Chain Failures to A03 in 2025; xz
(2024) and left-pad (2016) show both ends of the failure class. Fits the
repo's own rule: mechanical constraint → automate it.

### R3. Diff-size gate — finishing-work + code-review (S, needs eval: edits two skills)

**What:** `finishing-work` step 1.5: `git diff --stat main...HEAD`; if changed
LOC > ~400, propose a split before offering merge options. `code-review`
review-request package adds the LOC count so the reviewer knows what physics
apply. Optional later: advisory hook.
**Why:** defect-finding collapses past ~400 changed lines and ~500 LOC/hour
(SmartBear/Cisco, 2,500 reviews); Google's median change is ~24 LOC with <4h
median review latency (Sadowski 2018); DORA 2024 names batch-size inflation
as the mechanism by which AI degrades stability (−7.2%). This is the single
cheapest countermeasure to the documented AI failure mode.

### R4. Evidence doc — `docs/evidence.md` + README pitch line (S, no eval)

**What:** One page: the table from §1, the DORA arc (2024: stability −7.2% →
2025: throughput positive but instability persists; amplifier thesis; the
seven AI capabilities and which ones this suite implements — clear policy,
strong version control, small batches, quality platform), the METR
perception-gap story with its caveats stated honestly (early-2025 tools;
METR's 2026 follow-up suggests improvement but is confounded by selection
effects), GitClear trends with vendor caveat.
**Why:** the suite's premise ("output quality comes from process, not raw
capability") is now empirically defensible; adoption and marketplace pitch
need the numbers in one place; eval design (R1) should target exactly these
failure modes.

### R5. Pre-mortem step in writing-plans (S, needs eval: wording change)

**What:** One checklist line in the pre-submission review: "Assume this plan
failed. Check the matching `docs/anti-patterns.md` sections (§1–3) for the
failure you'd predict; add the missing guard or state why not."
**Why:** prospective hindsight measurably improves failure identification
(Klein 2007, HBR); the planning fallacy is the documented default (Kahneman &
Tversky 1979); the catalog exists precisely to be this checklist — currently
nothing wires it into the workflow.

### R6. `releasing-safely` skill — optional stage after finishing-work (L, new skill → requires R1-style RED test first)

**What:** Staged rollout (canary → rings → fleet), config/flag/data changes
get code-grade rigor, rehearsed rollback + expand–contract migrations, flag
lifecycle (owner + expiry), post-deploy smoke verification.
**Why:** catalog §10 is the only stage with heavyweight incident evidence
(Knight: $460M pre-tax, 45 min; CrowdStrike: ~8.5M machines, no staged
rollout for content; Cloudflare 2019: global-instant config) and zero skill
coverage. Second tier only because the suite's audience mostly stops at
PR/merge — but agents increasingly deploy.
**Constraint:** writing-skills iron law — no skill without a failing
(baseline) test first; sequence after R1.

### R7. Fuzz/property row in TDD + duplication check in review (S, needs eval: wording changes)

**What:** TDD coverage prescription gains one line: "for parsers, codecs, and
input boundaries, add a property-based/fuzz test." Code-review checklist
gains: "search the diff for cloned blocks" (or wire `jscpd`/`pylint
--enable=duplicate-code` into the verification loop).
**Why:** OSS-Fuzz: 13,000+ vulnerabilities and 50,000+ bugs across ~1,000
projects (May 2025) — created in response to Heartbleed; CrowdStrike's RCA
adopted fuzzing as a remediation. Duplication: GitClear's 4–8x cloning trend
is the measured AI signature the REFACTOR step needs backup against.

### R8. CONTRIBUTING.md agent gate (S, no eval; pre-marketplace blocker)

**What:** Contributor gate stating: PRs must include eval evidence for skill
changes, no drive-by wording edits, agents must read writing-skills first.
**Why:** upstream (superpowers) reports ~94% rejection rate of low-quality
AI-generated PRs and added agent-directed gates; publishing without one
invites the same flood. Carried over from the prior review pass — still open.

### R9. Housekeeping (S, no eval)

`.gitignore` for `.DS_Store` (one is already sitting untracked in `skills/`);
decide whether `recommend.md` is tracked or stays a local scratchpad; drop
GEMINI.md if still present (harness EOL'd 2026-06-18 — prior review pass).

## 3. Coverage map — practice corpus vs suite

| Practice (evidence) | Suite status |
|---|---|
| TDD (Nagappan 2008: −40–90% defects) | ✅ `test-driven-development` iron law |
| Verify before claiming done (METR 2025 perception gap) | ✅ `verification-before-completion` |
| Small batches / trunk-like flow (DORA 2024/2025; Accelerate) | ✅ commits · ⚠️ no PR/diff-size rule → R3 |
| Review physics ≤400 LOC (SmartBear 2006; Google 24-LOC median) | ❌ → R3 |
| Error-path testing (Yuan 2014: 92%/58%; OWASP 2025 new category) | ✅ TDD worst-case coverage + boundary error handling |
| Parse/validate at boundary (King 2019) | ✅ SEC-05 + coding-standards eager validation |
| Structured logging, no debug prints (SRE) | ✅ SEC-03 + audit hook |
| Secrets hygiene | ✅ SEC-02 + scan-secrets hook |
| Least privilege / deny-by-default | ✅ SEC-06/07/08 |
| Supply-chain vetting (OWASP A03:2025; Spracklen 2025; xz) | ❌ → R2 |
| Fuzz/property testing (OSS-Fuzz 13k+ vulns) | ❌ → R7 |
| Anti-duplication refactoring (GitClear 4–8x cloning) | ⚠️ REFACTOR step exists; no review check → R7 |
| Reproduction-first debugging (Yuan: 77% unit-reproducible) | ✅ `systematic-debugging` phases + circuit breaker |
| Decision records (Nygard 2011) | ✅ `docs/specs/` design docs |
| Pre-mortem (Klein 2007) | ❌ → R5 |
| Checklist form itself (Haynes 2009: −36–47%) | ✅ every skill — cite it → R4 |
| Staged rollout / config-as-code / rollback (Knight, CrowdStrike, Cloudflare) | ❌ post-merge scope → R6 |
| Skill self-testing (writing-skills TDD-for-docs) | ⚠️ process defined, corpus/runner missing → R1 |
| Blameless postmortems, error budgets, golden signals (SRE) | ❌ consciously out of scope for a dev-loop suite; reference material lives in `docs/anti-patterns.md` §11 |
| Estimation discipline (McConnell 2006) | ❌ consciously out of scope: agents execute plans, they don't commit calendar dates |

## 4. Standing cautions (carried from the prior review pass)

- **No skill-wording rewrites without before/after evals** — upstream wording
  (Red Flags tables, rationalization lists) is deliberately tuned. R3, R5, R7
  are flagged accordingly; R1 exists to make them cheap.
- **Guard the bootstrap token budget** — always-on dispatch injection is a
  known tax (~37 lines today); none of R1–R9 touches it.
- **Contributor gate before marketplace publication** → promoted to R8.

## Sources added in this pass (verified 2026-07-11)

- Nagappan, Maximilien, Bhat, Williams, *Realizing quality improvement through
  test driven development*, Empirical Software Engineering 13(3), 2008
- Sadowski et al., *Modern Code Review: A Case Study at Google*, ICSE-SEIP 2018
- Haynes et al., *A Surgical Safety Checklist to Reduce Morbidity and
  Mortality in a Global Population*, NEJM 360:491–9, 2009
- METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source
  Developer Productivity* (2025-07-10) and *We are Changing our Developer
  Productivity Experiment Design* (2026-02-24) — original result now labeled
  historical; follow-up confounded by selection effects. metr.org
- GitClear, *AI Copilot Code Quality* 2025/2026 research — vendor dataset
  (211M changed lines); directionally corroborated by DORA 2024. gitclear.com
- DORA, *Accelerate State of DevOps 2024* (−1.5% throughput, −7.2% stability
  per +25% AI adoption) and *State of AI-assisted Software Development 2025*
  (amplifier thesis, seven AI capabilities). dora.dev
- Google, OSS-Fuzz — 13,000+ vulnerabilities / 50,000+ bugs across ~1,000
  projects as of May 2025. google.github.io/oss-fuzz
- Spracklen et al., *We Have a Package for You!*, USENIX Security 2025 —
  19.7% hallucinated packages, 43% recurrence
- Klein, *Performing a Project Premortem*, HBR 2007
- Cohen/SmartBear Cisco study (2006), Yuan et al. OSDI 2014, OWASP Top
  10:2025 — previously verified; full citations in `docs/anti-patterns.md`
  Appendix B
