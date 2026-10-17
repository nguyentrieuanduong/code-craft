# Inventory: skills/verification-before-completion/SKILL.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "**Claiming without verifying is lying, even when the claim turns out true.**" | "**Claiming without verifying is lying, even when the claim turns out true.**" | |
| R2 | "1. **Identify** the command that would prove the claim." | "1. **Identify** the command that would prove the claim." | |
| R3 | "2. **Run it fresh** — complete, not partial, not from memory of an earlier run." | "2. **Run it fresh** — complete, not partial (cross-module breakage is what full suites catch), not from memory of an earlier run (code changed since)." | |
| R4 | "3. **Read the full output** — not just the exit code, not just the last line." | "3. **Read the full output** — not just the exit code (suites can pass with 0 tests collected; read the counts), not just the last line." | |
| R5 | "4. **Confirm output matches the claim.**" | "4. **Confirm output matches the claim.**" | |
| R6 | "5. Only then, make the claim — and show the evidence." | "5. Only then, make the claim — and show the evidence." | |
| R7 | "Skip any step and the claim is unsupported. Do not make it." | "Skip any step and the claim is unsupported. Do not make it." | |
| R8 | "&#124; \"Tests pass\" &#124; Full suite run, output read, 0 failures counted &#124;" | "&#124; \"Tests pass\" &#124; Full suite run, output read, 0 failures counted &#124;" | |
| R9 | "&#124; \"It builds\" &#124; Build command run to completion, exit 0 seen &#124;" | "&#124; \"It builds\" &#124; Build command run to completion, exit 0 seen &#124;" | |
| R10 | "&#124; \"Linter is clean\" &#124; Lint command run, zero warnings in output &#124;" | "&#124; \"Linter is clean\" &#124; Lint command run, zero warnings in output &#124;" | |
| R11 | "&#124; \"Bug is fixed\" &#124; Reproducing test run: failed before, passes now &#124;" | "&#124; \"Bug is fixed\" &#124; Reproducing test run: failed before, passes now &#124;" | |
| R12 | "&#124; \"Feature works\" &#124; Feature exercised end-to-end (run the app, hit the endpoint, open the UI) &#124;" | "&#124; \"Feature works\" &#124; Feature exercised end-to-end (run the app, hit the endpoint, open the UI) &#124;" | |
| R13 | "If you are about to write any of these in a success statement, stop — you have not verified:" | "If you are about to write any of these in a success statement, stop — you have not verified:" | |
| R14 | "> \"should work\" · \"probably passes\" · \"seems fine\" · \"I'm confident\" · > \"ought to\" · \"likely\" · any satisfaction expressed without a command run" | "> \"should work\" · \"probably passes\" · \"seems fine\" · \"I'm confident\" · > \"ought to\" · \"likely\" · any satisfaction expressed without a command run" | |
| R15 | "State uncertainty directly instead: \"I have not run X yet\" is honest; \"it should work\" is not." | "State uncertainty directly instead: \"I have not run X yet\" is honest; \"it should work\" is not." | |
| R16 | "Run every phase. Any failure = NOT READY; fix and rerun from the failed phase." | "Run every phase. Any failure = NOT READY; fix and rerun from the failed phase." | |
| R17 | "- [ ] **Build** — project's build command, exit 0" | "- [ ] **Build** — project's build command, exit 0" | |
| R18 | "- [ ] **Types** — type-checker (`tsc --noEmit`, `mypy`, ...) clean" | "- [ ] **Types** — type-checker (`tsc --noEmit`, `mypy`, ...) clean" | |
| R19 | "- [ ] **Lint** — zero errors; report remaining warnings honestly" | "- [ ] **Lint** — zero errors; report remaining warnings honestly" | |
| R20 | "- [ ] **Tests** — full suite with coverage; happy path AND worst cases present" | "- [ ] **Tests** — full suite with coverage; happy path AND worst cases present" | |
| R21 | "- [ ] **Security scan** — no hardcoded secrets/keys, no debug prints/console.log, security-baseline rules hold" | "- [ ] **Security scan** — no hardcoded secrets/keys, no debug prints/console.log, security-baseline rules hold" | |
| R22 | "- [ ] **Diff review** — read `git diff` in full: leftover debug code? missing boundary error handling? accidental file? scope creep?" | "- [ ] **Diff review** — read `git diff` in full: leftover debug code? missing boundary error handling? accidental file? scope creep?" | |
| R23 | "Report the result per phase with the actual numbers (tests run/passed, warnings count), not adjectives." | "Report the result per phase with the actual numbers (tests run/passed, warnings count), not adjectives." | |
| R24 | "&#124; \"I ran the tests earlier\" &#124; Code changed since. Earlier runs prove nothing about now. &#124;" | merged into R3 | |
| R25 | "&#124; \"Only this file changed, partial test run is enough\" &#124; Cross-module breakage is exactly what full suites catch. &#124;" | merged into R3 | |
| R26 | "&#124; \"The change is trivial, verification is overkill\" &#124; Trivial changes cause outages precisely because nobody verifies them. &#124;" | "&#124; \"The change is trivial, verification is overkill\" &#124; Trivial changes cause outages precisely because nobody verifies them. &#124;" | |
| R27 | "&#124; \"Exit code 0 means it passed\" &#124; Suites can pass with 0 tests collected. Read the counts. &#124;" | merged into R4 | |

Counts (checker): 474 -> 438 words (7% cut), 49 -> 48 nonblank lines.
Reason: E11 keeps the five-step gate, the claim table, the whole red-flag list, and all six loop phases; three table rows restated gate steps 2 and 3 and now sit there as parenthetical counters, which is all the overlap the file has.
