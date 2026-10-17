# Inventory: skills/systematic-debugging/SKILL.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "**IRON LAW: NO FIXES BEFORE PHASE 1 IS COMPLETE.**" | "**IRON LAW: NO FIXES BEFORE PHASE 1 IS COMPLETE.**" | |
| R2 | "A fix proposed before the root cause is understood is a guess. Guesses that happen to work hide the real defect until it returns, worse." | "A fix proposed before the root cause is understood is a guess; a guess that happens to work hides the real defect until it returns, worse." | |
| R3 | "- **Read the error. All of it.** Stack traces, log lines, exit codes. The answer is usually in text you skimmed." | "- **Read the error. All of it.** Stack traces, log lines, exit codes. The answer is usually in text you skimmed." | |
| R4 | "- **Reproduce consistently.** Find the minimal trigger. If you cannot reproduce it, you cannot verify a fix." | "- **Reproduce consistently.** Find the minimal trigger. If you cannot reproduce it, you cannot verify a fix." | |
| R5 | "- **Check recent changes.** `git diff`, `git log` — what changed around when it broke?" | "- **Check recent changes.** `git diff`, `git log` — what changed around when it broke?" | |
| R6 | "- **Trace the data flow.** Follow the actual values from input to failure point. Read the code that runs, not the code you assume runs." | "- **Trace the data flow.** Follow the actual values from input to failure point. Read the code that runs, not the code you assume runs." | |
| R7 | "- Find a working example of the same pattern elsewhere in the codebase." | "- Find a working example of the same pattern elsewhere in the codebase." | |
| R8 | "- Diff the broken case against the working one — line by line if needed." | "- Diff the broken case against the working one — line by line if needed." | |
| R9 | "- Understand every dependency the failing path touches." | "- Understand every dependency the failing path touches." | |
| R10 | "- Form ONE specific hypothesis: \"X fails because Y causes Z.\"" | "- Form ONE specific hypothesis: \"X fails because Y causes Z.\"" | |
| R11 | "- Test it with the smallest possible probe — a log line, a REPL call, an isolated snippet. Change ONE variable at a time." | "- Test it with the smallest possible probe — a log line, a REPL call, an isolated snippet. Change ONE variable at a time." | |
| R12 | "- Hypothesis wrong? Back to Phase 1 with the new information. Do not stack a second guess on a failed one." | "- Hypothesis wrong? Back to Phase 1 with the new information. Do not stack a second guess on a failed one." | |
| R13 | "- In multi-component systems, add diagnostic instrumentation at each boundary (request in / response out) before touching any component's logic." | "- In multi-component systems, add diagnostic instrumentation at each boundary (request in / response out) before touching any component's logic." | |
| R14 | "- Write a failing test that reproduces the bug (per test-driven-development)." | "- Write a failing test that reproduces the bug (per test-driven-development)." | |
| R15 | "- Implement the single fix the hypothesis points to." | "- Implement the single fix the hypothesis points to." | |
| R16 | "- Run the full suite. Verify the reproducing test passes AND nothing else broke." | "- Run the full suite. Verify the reproducing test passes AND nothing else broke." | |
| R17 | "- Only then invoke verification-before-completion and claim it's fixed." | "- Only then invoke verification-before-completion and claim it's fixed." | |
| R18 | "If three fixes have failed: **stop fixing.** Three failed fixes mean the mental model is wrong — question the architecture and your assumptions before attempt four. State plainly to the user what you know, what you've ruled out, and what you now suspect." | "If three fixes have failed: **stop fixing.** The mental model is wrong — question the architecture and your assumptions before attempt four. State plainly to the user what you know, what you've ruled out, and what you now suspect." | |
| R19 | "&#124; \"I see the problem, it's obviously X\" &#124; Obvious-at-a-glance diagnoses are wrong often enough to require Phase 1 anyway. &#124;" | "&#124; \"I see the problem, it's obviously X\" &#124; Obvious-at-a-glance diagnoses are wrong often enough to require Phase 1 anyway. &#124;" | |
| R20 | "&#124; \"Let me just try changing this\" &#124; Shotgun debugging destroys the evidence trail and adds new variables. &#124;" | "&#124; \"Let me just try changing this\" &#124; Shotgun debugging destroys the evidence trail and adds new variables. &#124;" | |
| R21 | "&#124; \"Adding a try/except makes the error go away\" &#124; Suppressing a symptom is not fixing a defect. Let errors surface. &#124;" | "&#124; \"Adding a try/except makes the error go away\" &#124; Suppressing a symptom is not fixing a defect. Let errors surface. &#124;" | |
| R22 | "&#124; \"It works now, I don't know why\" &#124; Then it will break later and you won't know why. Find the mechanism. &#124;" | "&#124; \"It works now, I don't know why\" &#124; Then it will break later and you won't know why. Find the mechanism. &#124;" | |
| R23 | "&#124; \"Restarting/clearing cache fixed it\" &#124; State-dependent bugs return. Identify what state and why. &#124;" | "&#124; \"Restarting/clearing cache fixed it\" &#124; State-dependent bugs return. Identify what state and why. &#124;" | |

Counts (checker): 485 -> 482 words (0% cut), 50 -> 49 nonblank lines.
Reason: the file is one IRON LAW, four phases of distinct one-line actions, the circuit breaker (kept: executing-plans is not co-loaded), and five distinct rationalizations; no rule restates another in this file.
