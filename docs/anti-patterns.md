# Anti-patterns: what to avoid across the software lifecycle

A field catalog of mistakes, anti-designs, and bad practices, organized by
lifecycle stage. Use it three ways:

1. **Pre-mortem checklist** during brainstorming/planning — scan the relevant
   section before committing to a design or plan.
2. **Review lens** — code-review and verification stages check against the
   implementation/testing/security sections.
3. **Skill-authoring evidence** — when patching this suite's rationalization
   tables, cite rows here instead of re-arguing from scratch.

Evidence policy: rows with a `(Author Year)` marker are backed by the source
listed in [Appendix B](#appendix-b-sources). Rows without a citation are
practitioner consensus. Appendix B separates sources re-verified on
2026-07-11 from canonical sources cited from the literature. Named incidents
resolve in [Appendix A](#appendix-a-incidents--the-anti-patterns-that-caused-them).

Sections: [1 Framing](#1-framing--brainstorming) ·
[2 Planning](#2-planning--estimation) · [3 Design](#3-design--architecture) ·
[4 Implementation](#4-implementation) · [5 Testing](#5-testing) ·
[6 Debugging](#6-debugging) · [7 Review](#7-code-review--collaboration) ·
[8 Version control](#8-version-control--integration) · [9 Security](#9-security) ·
[10 Deployment](#10-deployment--release) · [11 Operations](#11-operations-observability--incident-response) ·
[12 Maintenance](#12-maintenance--evolution) · [13 AI-assisted](#13-ai-assisted-development) ·
[14 Laws](#14-cross-cutting-laws-why-these-mistakes-recur)

---

## 1. Framing & brainstorming

*Suite mapping: `brainstorming`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Solutioneering | A favorite solution is chosen before the problem is stated; you optimize the wrong thing | Write the problem statement first; keep problem and solution space separate |
| XY problem | You ask for help with your attempted fix X, hiding the real goal Y; everyone debugs the wrong layer (Raymond 2001) | State the underlying goal whenever asking or investigating |
| Anchoring on the first idea | The first proposal frames all later discussion (Kahneman 2011) | Generate 2–3 genuinely different options before comparing any |
| Building without validating demand | "Build it and they will come" — months of work on an unwanted thing | Validate with the cheapest artifact: a doc, mock, or spike |
| Not-Invented-Here | Rebuilding solved problems, worse, with your bugs | Search existing libraries/systems first; a custom build must justify itself |
| Ignoring non-functional requirements | Perf, security, compliance, and ops surface late, where they are most expensive | Ask about scale, data sensitivity, and availability up front |
| Unbounded scope ("while we're at it") | Scope creep destroys estimates and review quality | Write down what is *out* of scope; park extras as new items |
| Design by committee / HiPPO | Decisions by hierarchy or consensus-averaging, not evidence | One accountable decider plus written options with trade-offs |
| Bikeshedding | Energy flows to trivial, easily-understood details while hard questions go unexamined (Parkinson 1957) | Timebox trivia; force discussion onto the risky parts |
| Analysis paralysis | Endless evaluation, no contact with reality | Timebox the decision; prototype the riskiest assumption |
| Unrecorded assumptions | Silent assumptions become invisible constraints, then "bugs" | Write assumptions into the design doc; mark unvalidated ones |
| Tearing out what you don't understand | Existing guards usually encode a forgotten incident (Chesterton 1929); Therac-25 removed hardware interlocks its software "replaced" | Find out why it exists (`git log`, ask) before removing it |

## 2. Planning & estimation

*Suite mapping: `writing-plans`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Planning fallacy | Best-case estimates become commitments; insiders systematically underestimate their own tasks (Kahneman & Tversky 1979) | Estimate from past actuals (reference class), not intentions |
| 90% syndrome | "Almost done" for half the project; effort spent is mistaken for progress | Measure progress only in completed, verified slices |
| Horizontal slicing | Plan by layer (all models → all APIs → all UI): nothing works until everything works | Vertical slices: thinnest end-to-end path first (walking skeleton; Hunt & Thomas 1999) |
| Big-bang integration | Deferred integration compounds failures and localizes nothing | Integrate continuously in small batches (DORA/Accelerate 2018) |
| Riskiest part deferred | The scary unknown lands in week 8 and invalidates weeks 1–7 | Do the highest-risk, highest-information task first (spike) |
| Staffing a late project | Ramp-up plus communication overhead makes it later (Brooks 1975) | Re-scope or re-sequence instead of adding people late |
| Rewrite-from-scratch as default | Old code's ugliness is encoded knowledge; rewrites rediscover every fixed bug (Spolsky 2000) | Incremental replacement behind a stable interface (Strangler Fig; Fowler 2004) |
| No rollback/kill criteria | Plans that only describe success can't be safely abandoned | Define abort conditions and the back-out path before starting |
| Steps without verification | "Implement X" with no "prove X works" invites 90% syndrome | Every plan step ends in an observable check (test passes, demo runs) |
| Parkinson's law + student syndrome | Work expands to fill the time; work starts at the deadline | Short milestones, each ending in a demo |
| Estimate = target = commitment | A hope silently becomes a promise (McConnell 2006) | Label every number as estimate, target, or commitment |
| Dependency blindness | External approvals, access, and third parties discovered mid-plan | List external dependencies and their lead times in the plan |

## 3. Design & architecture

*Suite mapping: `brainstorming`, `writing-plans`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Big ball of mud | No enforced structure; every part talks to every part (Foote & Yoder 1997) | Draw module boundaries by information hiding: hide the decisions most likely to change (Parnas 1972) |
| Distributed monolith | Microservice deployment with monolith coupling: sync call chains, shared DBs, lockstep releases | Keep the monolith, or split along real seams with async contracts |
| Second-system effect | The successor design carries every idea deferred from v1 (Brooks 1975) | Same discipline as v1; give v2 a feature budget |
| Complex system designed from scratch | It won't work and can't be patched into working (Gall 1975) | Grow complex systems from working simple ones |
| Speculative generality | Frameworks, plugin systems, and config for imagined future needs (Fowler 1999; YAGNI) | Build for today's requirements; add extension points only at proven variation points |
| The wrong abstraction | Shared code forced over divergent cases; conditionals metastasize | Prefer duplication over the wrong abstraction; inline it back, re-abstract when proven (Metz 2016) |
| Shallow modules | Many small units whose interfaces are as complex as their implementations; glue everywhere (Ousterhout 2018) | Deep modules: simple interface, powerful implementation |
| Unacknowledged leaky abstraction | The abstraction hides a cost or failure mode users eventually hit (Spolsky 2002) | Document what leaks; never pretend remote calls are local (Nygard 2007) |
| Designing for imaginary scale | Planet-scale architecture for a 100-user tool: ops burden now, benefit never | Boring tech and vertical scaling first; measure before sharding (McKinley 2015) |
| Golden hammer / resume-driven choices | Tech chosen by familiarity or fashion, not fit | Novel tech must buy its complexity; spend "innovation tokens" deliberately (McKinley 2015) |
| No failure design | Integration points assumed reliable; one slow dependency stalls the fleet (Nygard 2007) | Timeouts, retries with backoff+jitter, circuit breakers, bulkheads; design the degraded mode |
| God object | One component knows everything, so every change touches it | Split along reasons-to-change (Parnas 1972) |
| Validation scattered everywhere | Every layer re-checks strings; illegal states remain representable | Parse, don't validate: convert at the boundary into types that make illegal states unrepresentable (King 2019) |
| Flag/config combinatorics | Behavior determined by 2^n flag combinations nobody tests; a repurposed flag detonated Knight Capital | Few flags, short-lived, owned, with expiry dates |
| Robustness principle over-applied | "Liberal in what you accept" ossifies bugs into de-facto protocol (RFC 9413; Hyrum's law) | Strict parsing plus explicit versioning and deprecation |

## 4. Implementation

*Suite mapping: `coding-standards`, `test-driven-development`, `security-baseline`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Swallowed errors | Empty catch blocks and ignored return codes; 92% of catastrophic failures in a 198-failure study traced to mishandled non-fatal errors (Yuan 2014); now its own OWASP category, Mishandling of Exceptional Conditions (OWASP 2025) | Handle at the boundary or propagate; never silently continue |
| Placeholder error handlers | `TODO` / log-and-continue handlers; roughly a third of the catastrophic failures above were *trivial* handler mistakes (Yuan 2014) | Test error paths like features |
| Shared mutable state | Hidden coupling, race conditions, untestable units | Immutable data, pure functions, state pushed to the edges |
| Check-then-act races (TOCTOU) | `if exists: use` breaks under concurrency | Atomic operations, locks, or design out the shared resource |
| Null-happy interfaces | Hoare's "billion-dollar mistake": every caller must remember the check (Hoare 2009) | Option types, non-null defaults, empty collections instead of null |
| Primitive obsession | IDs, money, and time as bare strings/floats invite unit and precision bugs; a lbf·s-vs-N·s mismatch lost Mars Climate Orbiter | Domain types; decimals for money; UTC plus tz-aware libraries for time |
| Clever code | Code at the limit of your ingenuity is past the limit of your debugging (Kernighan 1974) | Optimize for the reader |
| Premature optimization | Micro-tuning cold paths costs clarity for nothing, ~97% of the time (Knuth 1974) | Correct and clear first; profile before touching hot paths — but do design for the critical 3% |
| Copy-paste divergence | Cloned logic drifts; the bug gets fixed in one of five copies | Extract when genuinely identical and stable (rule of three) — balanced against wrong-abstraction risk |
| Dead code kept "just in case" | Dormant paths can reactivate: Knight's Power Peg lay dead for ~8 years, then fired (SEC 2013) | Delete it; git remembers |
| Magic literals, lying names | Unexplained numbers and stale names misdirect every future reader | Named constants; rename when behavior changes |
| Deep nesting | The arrow shape hides the happy path and multiplies branch states | Guard clauses, early returns |
| Debug prints left in | Unstructured, unlevelled, leaks data — suite-enforced rule #4 | Structured logging with levels and context |
| Hand-rolled crypto/auth/date math | Subtle, catastrophic, already-solved failure modes | Vetted libraries and platform primitives only |
| Catch-everything blocks | Broad catches convert programming errors into silent runtime noise | Catch the narrowest type you can handle meaningfully |
| Eager init at import time | Imports doing I/O cause slow starts, test pain, hidden ordering | Lazy initialization; explicit lifecycle |
| Hidden side effects | "Getters" that write, constructors that do I/O | Command–query separation (Meyer 1988) |

## 5. Testing

*Suite mapping: `test-driven-development`, `verification-before-completion`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Tests written to confirm the code | Test-after mirrors the implementation, tautologically passing | TDD red-green-refactor; watch each test fail first, for the right reason (Beck 2003) |
| Happy-path-only suites | Error paths are where catastrophes live: 58% of catastrophic failures were preventable by trivial error-path tests (Yuan 2014) | Test failures, timeouts, malformed input, partial writes |
| Coverage as a target | Goodhart's law: coverage is gamed with assertion-free tests; 100% proves execution, not correctness | Use coverage to find gaps; review what assertions actually claim |
| Over-mocking | Mocks of things you don't own drift from reality; CI passes, prod fails | Real implementations or contract-tested fakes; mock only true externals at the boundary |
| Ice-cream cone | Mostly manual + E2E: slow, flaky, failures localize nowhere (Cohn 2009; Fowler 2012) | Pyramid: many fast unit tests, some integration, few E2E |
| Tolerated flakiness | Retry culture drowns real signal: ~16% of Google's 4.2M tests showed flakiness; 84% of pass→fail transitions were flakes, not bugs (Micco 2016) | Quarantine immediately; fix or delete; attack root causes (sleeps, shared state, time) |
| `sleep()`-based async tests | Timing assumptions are a flakiness factory | Await conditions/events with deadlines |
| Order-dependent tests | Pass alone, fail in suite — or worse, the reverse | Isolate state per test; randomize order in CI |
| Tests that cannot fail | Missing assertions, swallowed exceptions, `assert true` | Mutation-test or hand-break the code to prove the test notices |
| Snapshot-everything | Giant snapshots get approved reflexively; churn without meaning | Snapshot small, intention-revealing outputs only |
| Testing private internals | Refactors break tests with zero behavior change; implementation calcifies | Test through public behavior and contracts |
| Permanent `@skip` | Skipped tests rot into false confidence | Skip only with a ticket and expiry — or delete |
| Fix without regression test | An unverified fix; the bug returns unnoticed | Write the red test that reproduces the bug before fixing |
| Everything mocked, prod never rehearsed | Config, migrations, and infra first exercised in production | Staging parity for the risky layer; post-deploy smoke tests; 77% of production failures reproduce in a unit test — write those (Yuan 2014) |

## 6. Debugging

*Suite mapping: `systematic-debugging`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Guess-and-patch | Changing code before understanding buries the root cause under symptom patches | Reproduce first; hypothesize; change one thing; verify |
| Shotgun debugging | Many simultaneous changes — when it "works," you don't know why | One variable at a time; log what you tried |
| "The compiler/platform is broken" | It's your code, overwhelmingly ("select isn't broken"; Hunt & Thomas 1999) | Suspect your own code until proven otherwise |
| No minimal reproduction | Debugging inside the full system with fifty free variables | Shrink to the smallest failing case; bisect (`git bisect`) |
| Skimming the error | First line read, stack trace ignored — yet in 84% of failures every triggering event was already in the logs (Yuan 2014) | Read the whole error and the logs before theorizing |
| Deploying a "likely fix" unreproduced | You learn nothing; it recurs at a worse time | Invest in reproduction, or add targeted telemetry to catch it live |
| Heisenbug denial | Debugger/print changes timing; "works now" concludes nothing | Suspect concurrency/UB; race detectors and sanitizers |
| Debugging prod by trial deploys | Each guess is an outage-grade change; Knight's improvised revert spread the defect to all 8 servers (SEC 2013) | Reproduce in a safe environment; if prod-only, use flags, canaries, and observability |

## 7. Code review & collaboration

*Suite mapping: `code-review`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Rubber-stamp LGTM | Approval without reading catches nothing and teaches nothing | Real review: ≤400 LOC per session, ≤500 LOC/hour, ≤60–90 min (Cohen 2006) |
| Monster PRs | Defect-finding ability collapses past ~400 changed lines (Cohen 2006) | Slice PRs to one reviewable concern |
| Nitpick-only review | Style comments while the architecture rots — bikeshedding at review time | Automate style with linters/formatters; humans review design, correctness, security |
| Reviewing the diff without context | No issue link, never ran the code; semantic problems invisible | PR states why and how it was verified; check out and run risky changes |
| "Fix in a follow-up," no ticket | Later equals never (LeBlanc's law; Martin 2008) | Block on it, or file the ticket before approving |
| Review as status contest | Feedback withheld or weaponized; authors hide work | Blameless, artifact-focused comments; the "Ego Effect" — code improves just because it will be read (Cohen 2006) |
| Self-merge of risky solo work | Unreviewed changes reach main because no second human exists | Self-review after a break, or a second-model/agent review pass |
| Scope expansion in review | "While you're here…" balloons the PR mid-flight | New asks become new tickets and new PRs |

## 8. Version control & integration

*Suite mapping: `executing-plans`, `finishing-work`, `using-git-worktrees`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Long-lived branches | Integration pain deferred is integration pain multiplied; small batches and trunk-based flow correlate with elite delivery performance (DORA/Accelerate 2018) | Short-lived branches merged to main frequently |
| Giant mixed commits | Refactor + feature + formatting in one commit: unreviewable, unbisectable, unrevertable | Atomic commits, one intent each — the log is a recovery map (this repo's workflow rule) |
| Messages like "fix" / "wip" | The log can no longer answer "what changed and why" | Imperative summary; the why in the body |
| Secrets committed | History is forever; rotation is the only remedy — suite-enforced rule #2 | Secret managers, pre-commit scanning, `.gitignore` first |
| Force-push to shared branches | Destroys teammates' work and the audit trail — suite-enforced rule #3 | Force-push only unshared branches, `--force-with-lease` |
| `--no-verify` as habit | Hooks encode the team's floor; bypassing normalizes a broken main — suite-enforced rule #3 | Fix the failure; if the hook is wrong, fix the hook in its own PR |
| Green + green = assumed green | Two passing branches can merge into a failing main (semantic conflict) | CI runs on the merge result (merge queue, or re-test after rebase) |
| Editing lint config to pass CI | Moves the goalposts instead of the ball — suite-enforced rule #1 | Fix the code; config changes are separate, reviewed PRs |
| Binaries in git | Repo bloat compounds forever | LFS or artifact storage |

## 9. Security

*Suite mapping: `security-baseline`*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Security as a final phase | End-stage audits find architectural flaws when they're most expensive; "Insecure Design" earned its own OWASP category (OWASP 2021→2025) | Threat-model during design; shift left |
| String-built queries/commands | Injection remains a top risk class decade after decade (OWASP 2025) | Parameterized queries, argument arrays; no shell interpolation of user input |
| Missing object-level authorization | Broken Access Control is OWASP #1 in both 2021 and 2025 (A01) | Deny by default; authorize every object access server-side; test per role |
| Trusting the client | Client-side validation and hidden fields are attacker-controlled | Revalidate everything server-side |
| Hardcoded secrets | Keys in code, logs, or URLs leak with every copy — suite-enforced rule #2 | Secret manager, rotation, automated scanning |
| Default/debug configuration in prod | Misconfiguration is OWASP #2 in 2025 (A02): default creds, open buckets, permissive CORS | Hardened baselines; config as reviewed code; environment parity |
| Known vulns left unpatched | Equifax ran a Struts version ~2 months after the fix existed; ~147M people exposed (GAO 2018) | Dependency scanning plus a severity-tied patch SLA |
| Unvetted supply chain | New OWASP A03:2025, Software Supply Chain Failures; the xz backdoor nearly shipped to every major distro via a socially-engineered lone maintainer (2024); an 11-line package takedown broke npm (left-pad 2016) | Lockfiles, pinning, provenance/signing, minimal dependencies, review what you add |
| Overprivileged credentials | Any compromise inherits the full blast radius | Least privilege; scoped, short-lived credentials |
| Obscurity as the only layer | Hidden endpoints survive exactly until enumeration (Kerckhoffs 1883) | Assume the design is known; secrecy lives only in keys |
| Sensitive data in logs | PII and tokens exfiltrate through the log pipeline | Redact at the logging boundary; classify log fields |
| DIY auth and crypto | Password storage, sessions, and JWT handling fail in subtle, known ways | Standard frameworks, memory-hard hashes (argon2/bcrypt), vetted libraries |

## 10. Deployment & release

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Manual deploy steps | Humans forget servers: Knight updated 7 of 8, lost $440M+ in 45 minutes (SEC 2013) | Scripted, idempotent, verified deploys; drift detection |
| No staged rollout | Global instant blast radius: CrowdStrike pushed a content update fleet-wide at once — ~8.5M machines down (CrowdStrike 2024); Cloudflare's WAF rule went global in seconds (Cloudflare 2019) | Canary → rings → fleet, with automatic rollback on health regression |
| Config/data updates exempt from rigor | Both CrowdStrike's channel file and Cloudflare's regex skipped binary-grade validation and staging | Same pipeline for config, flags, and data as for code: staged, validated, revertible |
| No rehearsed rollback | Knight had no documented back-out; the improvised one amplified the failure (SEC 2013) | Rehearsed rollback; expand→migrate→contract for schema changes (Fowler, ParallelChange) |
| Schema and code deployed in lockstep | Order dependency guarantees downtime in one direction | Code tolerates both schemas; migrate, then flip |
| Works-in-staging syndrome | Snowflake prod drifts from staging in config, data shape, and scale | Infra as code; immutable images (cattle, not pets; Bias 2012); config in the environment (12-Factor; Wiggins 2011) |
| Done = CI green | Nobody watches the actual rollout; the suite's `verification-before-completion` exists for this | Post-deploy smoke tests, health checks, and metric watch through the rollout window |
| Deploying when nobody can respond | Friday 17:55 releases meet empty on-call rosters | Deploy when owners are present and traffic is observable — or make rollback truly one-click first |
| Big-bang releases | Months of changes land at once; cause isolation becomes impossible; speed and stability correlate — they are not a trade-off (Accelerate 2018) | Small, frequent releases behind flags |
| Flags without lifecycle | Stale flags recombine into untested states; a repurposed flag fired Knight's dead code (SEC 2013) | Flag registry with owner and expiry; delete after full rollout |

## 11. Operations, observability & incident response

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Observability after the outage | You cannot debug what you cannot see; "what changed?" dominates MTTR | Logs, metrics, traces from day one; instrument before you need it |
| Alerting on causes, not symptoms | 500 CPU alerts, zero "users can't check out"; fatigue drowns real pages | Alert on user-visible symptoms against SLOs; causes belong on dashboards (SRE 2016) |
| No error budget | Reliability becomes unbounded, or velocity has no brake | SLOs with error budgets arbitrate feature-vs-stability (SRE 2016) |
| Untested backups | GitLab 2017: all five backup/replication mechanisms failed or weren't configured; pg_dump had been failing silently into an empty S3 bucket | A backup exists only when restore is drilled; alert on backup-job failure; assign ownership |
| No runbooks, hero culture | Recovery depends on one tired person at 3 a.m. — GitLab's operator was exactly that; the postmortem blamed systems, not him | Runbooks per alert; rotation; pairing on risky prod work; guardrails over vigilance |
| Blame culture | Punished honesty hides the information you need; cover-ups extend outages | Blameless postmortems focused on systems (Allspaw 2012; SRE 2016) |
| Single-root-cause thinking | Complex systems fail through multiple latent conditions aligning (Cook 1998); CrowdStrike's own RCA lists six findings | Contributing-factors analysis; fix the class, not the instance |
| Ignoring your own alarms | Knight's systems sent 97 warning emails before the market opened; nobody acted (SEC 2013) | Every alert is actionable or deleted; unowned alerts are noise debt |
| Toil accumulation | Manual repetitive ops eat capacity and add error surface | Automate toil; cap it (SRE 2016) |
| Vanity dashboards | Measuring what's easy, not what indicates user pain | Few golden signals: latency, traffic, errors, saturation (SRE 2016) |
| Monitoring on the monitored system | AWS's status dashboard ran on S3 during the S3 outage (2017); Facebook's outage locked engineers out of the tools needed to fix it (2021) | Out-of-band monitoring and break-glass access paths |

## 12. Maintenance & evolution

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Broken windows tolerated | Visible neglect licenses more neglect (Hunt & Thomas 1999) | Fix small rot on contact, within task scope |
| Dependency freeze | "Don't touch it" ends in a forced big-bang upgrade or an unpatched CVE (Equifax) | Small regular upgrades on a cadence; automated update PRs gated by CI |
| Floating versions | Builds change under you; one unpublished 11-line package broke npm's ecosystem (left-pad 2016) | Lockfiles and pinning *with* a deliberate update process — freeze and float both fail |
| Rewrite instead of strangle | Big-bang rewrites mean years of no features plus rediscovered bugs (Spolsky 2000) | Strangler fig: route traffic incrementally to the new path (Fowler 2004) |
| "Nobody depends on that" | With enough users, every observable behavior is depended on (Hyrum's law) | Deprecation policy: announce, measure usage, migrate, then remove |
| Docs drift | Wrong docs are worse than no docs | Docs live beside code and change in the same PR; prefer executable docs (tests, examples) |
| Debt unmanaged or moralized | Ignored debt compounds; "all debt is bad" blocks pragmatic trade-offs | Classify deliberate vs inadvertent (Fowler 2009); pay down along hot paths |
| TODO graveyards | Comments as a bug tracker nobody queries | TODOs carry ticket IDs or get deleted |
| Knowledge silos | The theory of the program lives in heads and leaves with them (Naur 1985) | Rotation, pairing, design docs; track bus factor as a risk |
| Software treated as finished | Systems degrade as their environment changes (Lehman 1980) | Budget standing capacity for evolution; declining quality is a choice |

## 13. AI-assisted development

*Suite mapping: the entire suite — process over capability*

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Merging generated code unread | You own what you merge; 90% of practitioners use AI daily, yet ~30% report little or no trust in its output (DORA 2025) | Review AI diffs like a junior engineer's PR |
| Vibe-coding production systems | Prompt-until-it-runs skips design, tests, review; AI amplifies whatever process exists — including a bad one (DORA 2025) | Same pipeline: design → plan → TDD → review |
| Installing hallucinated dependencies | ~19.7% of package suggestions across 16 models didn't exist; 43% of hallucinated names recur on every rerun, so attackers pre-register them — "slopsquatting" (Spracklen 2025) | Verify registry and provenance before installing; allowlists; lockfiles |
| Agent grades its own homework | Models edit tests or linter configs so their code "passes" — this suite hook-blocks exactly that | Immutable acceptance criteria; verification as a separate step or agent |
| Secrets in prompts | Credentials leave your trust boundary and persist in logs/context | Redact before prompting; scoped test credentials |
| Oversized agent diffs | 2,000-line generated PRs meet the same ≤400-LOC review physics (Cohen 2006); one upstream suite reports ~94% rejection of low-quality AI PRs (superpowers maintainer) | Constrain task size; land small verified slices |
| Prompt-and-pray debugging | Re-asking "fix it" without a reproduction is shotgun debugging at machine speed | Reproduce first; hand the model the failing test, not the symptom |
| Context-free generation | The model invents conventions instead of following the codebase's | Require it to read before writing; feed standards (CLAUDE.md, skills) |
| AI throughput without stability work | DORA 2025: AI now improves throughput but still *increases* delivery instability | Pair adoption with small batches, strong version control, fast rollback |

## 14. Cross-cutting laws (why these mistakes recur)

| Law | Statement | Bites you when |
|---|---|---|
| Goodhart's law | When a measure becomes a target, it ceases to be a good measure | Coverage %, velocity points, LOC quotas |
| Hyrum's law | With enough users, all observable behavior will be depended on | "Harmless" behavior changes; deprecations |
| Conway's law (1968) | Systems copy the communication structure of the org that builds them | Architecture that fights the org chart loses |
| Gall's law (1975) | Working complex systems evolve from working simple ones | Greenfield mega-designs |
| Brooks's law (1975) | Adding people to a late project makes it later | Staffing as schedule rescue |
| Second-system effect (1975) | The successor to a successful system is the most dangerous one | v2 rewrites |
| Kernighan's law (1974) | Debugging is twice as hard as writing; maximally clever code is undebuggable by you | Cleverness as a virtue |
| Knuth (1974) | Premature optimization is the root of all evil — about 97% of the time | Micro-tuning before profiling; also misquoted to excuse ignoring the critical 3% |
| Chesterton's fence (1929) | Don't remove what you don't understand | Deleting "useless" guards and configs |
| Planning fallacy (1979) | People systematically underestimate their own tasks | Estimates from intention, not history |
| Parkinson's law of triviality (1957) | Attention flows to the trivial and comprehensible | Bikeshed reviews and meetings |
| LeBlanc's law | Later equals never | "Fix in a follow-up" |

---

## Appendix A: incidents — the anti-patterns that caused them

| Incident | Year | What happened | Anti-patterns it proves |
|---|---|---|---|
| Therac-25 | 1985–87 | Radiation-therapy machine overdosed patients fatally: race conditions in code reused from models whose hardware interlocks had been removed; incident reports dismissed | Removing guards you don't understand; concurrency untested; blame-the-operator response (Leveson & Turner 1993) |
| Ariane 5 Flight 501 | 1996 | Self-destructed ~37s after launch: 64-bit float→16-bit int overflow in alignment code reused from Ariane 4 and useless after liftoff; primary and backup failed identically | Reuse without revalidating assumptions; dead code running; identical redundancy is not redundancy (Lions 1996) |
| Mars Climate Orbiter | 1999 | ≈$327M mission lost: ground software output thruster impulse in pound-force·s; flight software expected N·s | Unvalidated interface contracts; units as bare numbers (NASA MIB 1999) |
| Knight Capital | 2012 | $440M+ lost in 45 min (SEC: $460M pre-tax): deploy reached 7 of 8 servers; repurposed flag activated 8-year-dead code; 97 warning emails unread; improvised rollback spread the defect to all 8 | Manual deploys; dead code; flag reuse; ignored alarms; unrehearsed rollback (SEC 2013) |
| Heartbleed | 2014 | Missing bounds check in OpenSSL's heartbeat leaked server memory internet-wide (CVE-2014-0160) | Critical dependency chronically under-resourced; new protocol feature without adversarial tests |
| left-pad | 2016 | Author unpublished an 11-line npm package; builds broke across the ecosystem | Transitive-dependency fragility; trivial dependencies; no pinning strategy |
| GitLab database loss | 2017 | Tired engineer ran `rm -rf` on the primary, not the secondary; ~300GB → 4.5GB; **all five** backup/replication mechanisms failed or weren't set up; recovered from a 6-hour-old staging snapshot | Untested backups; silent job failure; no ownership; fatigue + prod access (GitLab 2017) |
| AWS S3 outage | 2017 | Playbook typo removed too much index capacity in us-east-1; subsystems hadn't been restarted in years; the status dashboard itself depended on S3 | Runbook commands without blast-radius limits; untested cold paths; monitoring on the monitored system (AWS 2017) |
| Equifax | 2017 | Struts CVE-2017-5638 exploited ~2 months after the patch existed; ~147M people; an expired inspection certificate had blinded egress monitoring for months | Patch latency; asset-inventory gaps; decayed security tooling (GAO 2018) |
| Cloudflare WAF outage | 2019 | A WAF regex with catastrophic backtracking deployed globally in seconds; CPU exhaustion across the edge; an earlier refactor had removed the CPU-limit protection | Config exempt from staged rollout; missing resource guards; latent protection removed (Cloudflare 2019) |
| SolarWinds SUNBURST | 2020 | Build pipeline compromised; signed malicious updates shipped to up to ~18,000 customers | Build/supply-chain integrity as an afterthought (CISA 2020) |
| Facebook outage | 2021 | Maintenance command withdrew the backbone; the audit tool meant to block it had a bug; DNS withdrew routes; internal tools and badge readers were on the same infrastructure — ~6h global outage | No out-of-band access; recovery tools inside the failure domain (Meta 2021) |
| Log4Shell | 2021 | JNDI-lookup feature in log4j2 turned every logged user string into potential RCE (CVE-2021-44228) | Feature richness inside a trust boundary; logging untrusted input; ubiquitous transitive dependency |
| CrowdStrike Channel File 291 | 2024 | Sensor's Content Validator accepted 21 fields, the Interpreter read 20 → out-of-bounds read; a wildcard 21st field masked it through every test stage; content updates had no staged rollout, unlike sensor binaries; ~8.5M Windows machines crashed | Validator/consumer contract mismatch; test data shaped like fixtures, not production; config bypassing binary-grade rigor (CrowdStrike 2024) |
| xz-utils backdoor (near miss) | 2024 | Multi-year social engineering earned co-maintainership of a core compression library; a backdoor targeting sshd shipped in release tarballs; caught pre-GA by an engineer investigating ~500ms ssh latency (CVE-2024-3094) | Single-maintainer critical dependencies; pressure-driven trust grants; release artifacts diverging from source (Freund 2024) |

## Appendix B: sources

### Re-verified 2026-07-11 (web)

- Yuan et al., *Simple Testing Can Prevent Most Critical Failures*, OSDI 2014 — 92% / 58% / 77% / 84% figures. usenix.org/conference/osdi14/technical-sessions/presentation/yuan
- Cohen / SmartBear, *Code Review at Cisco Systems* (2006) — 200–400 LOC, ≤500 LOC/hr, 60–90 min, Ego Effect. smartbear.com/learn/code-review/best-practices-for-peer-code-review/
- Micco, *Flaky Tests at Google and How We Mitigate Them*, Google Testing Blog (2016) — 1.5% of runs, ~16% of 4.2M tests, 84% of transitions
- OWASP Top 10:2025 — A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures (new), Mishandling of Exceptional Conditions (new). owasp.org/Top10/2025/
- DORA, *State of AI-assisted Software Development* (2025) — amplifier thesis; 90% adoption; ~30% low trust; throughput up, instability up. dora.dev/dora-report-2025/
- SEC, *In the Matter of Knight Capital Americas LLC*, cease-and-desist order (2013) — deployment, Power Peg, 97 emails, $460M pre-tax
- GitLab, *Postmortem of database outage of January 31* (2017) — five failed backup mechanisms, silent pg_dump failure, ownership. about.gitlab.com
- CrowdStrike, *External Technical Root Cause Analysis — Channel File 291* (2024) — 21-vs-20 mismatch, wildcard masking, staged-rollout finding
- Spracklen et al., *We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs*, USENIX Security 2025 — 19.7% average, 43% repeatability
- xz backdoor, CVE-2024-3094 (2024) — discovery by Andres Freund; multi-year social engineering (Wikipedia: "XZ Utils backdoor"; Elastic Security Labs "500ms to midnight")

### Canonical sources, cited from the literature (not re-fetched)

- Allspaw, *Blameless PostMortems and a Just Culture*, Etsy (2012)
- Beck, *Test-Driven Development: By Example* (2003)
- Beyer et al., *Site Reliability Engineering* (2016) — SLOs, error budgets, toil, symptom alerting. sre.google
- Bias, "pets vs cattle" framing (2012)
- Brooks, *The Mythical Man-Month* (1975) — Brooks's law, second-system effect
- Chesterton, *The Thing* (1929) — the fence
- Cohn, *Succeeding with Agile* (2009); Fowler, *TestPyramid* bliki (2012)
- Conway, *How Do Committees Invent?* (1968)
- Cook, *How Complex Systems Fail* (1998)
- Foote & Yoder, *Big Ball of Mud* (1997)
- Forsgren, Humble, Kim, *Accelerate* (2018) — small batches; speed and stability correlate
- Fowler, *Refactoring* (1999); *StranglerFigApplication* (2004); *TechnicalDebtQuadrant* (2009); *ParallelChange* bliki. martinfowler.com
- Gall, *Systemantics* (1975)
- GAO, *Equifax breach report* GAO-18-559 (2018)
- Hoare, *Null References: The Billion Dollar Mistake*, QCon (2009)
- Hunt & Thomas, *The Pragmatic Programmer* (1999) — tracer bullets, broken windows, "select isn't broken"
- Hyrum's law — hyrumslaw.com; Winters et al., *Software Engineering at Google* (2020)
- Kahneman, *Thinking, Fast and Slow* (2011); Kahneman & Tversky, planning fallacy (1979)
- Kerckhoffs, *La cryptographie militaire* (1883)
- Kernighan & Plauger, *The Elements of Programming Style* (1974) — Kernighan's law
- King, *Parse, don't validate* (2019)
- Knuth, *Structured Programming with go to Statements*, ACM Computing Surveys (1974)
- Lehman, laws of software evolution (1980)
- Leveson & Turner, *An Investigation of the Therac-25 Accidents*, IEEE Computer (1993)
- Lions et al., *Ariane 5 Flight 501 Failure* inquiry report (1996)
- Martin, *Clean Code* (2008) — LeBlanc's law
- McConnell, *Software Estimation* (2006) — estimate vs target vs commitment
- McKinley, *Choose Boring Technology* (2015)
- Metz, *The Wrong Abstraction* (2016)
- Meyer, *Object-Oriented Software Construction* (1988) — command–query separation
- NASA, *Mars Climate Orbiter Mishap Investigation Board Phase I Report* (1999)
- Naur, *Programming as Theory Building* (1985)
- Nygard, *Release It!* (2007)
- Ousterhout, *A Philosophy of Software Design* (2018)
- Parkinson, law of triviality (1957); popularized as "bikeshedding" by Kamp (1999)
- Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules* (1972)
- Raymond & Moen, *How To Ask Questions the Smart Way* (2001) — XY problem
- RFC 9413, *Maintaining Robust Protocols* (2023) — limits of Postel's principle
- Spolsky, *Things You Should Never Do, Part I* (2000); *The Law of Leaky Abstractions* (2002)
- Wiggins, *The Twelve-Factor App* (2011). 12factor.net
- Incident postmortems: AWS S3 service disruption message (2017); Cloudflare outage report by Graham-Cumming (2019); Meta outage engineering post (2021); CISA SUNBURST advisories (2020)
