# Inventory: skills/code-review/references/reviewer-prompt.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "Use this prompt only to dispatch an isolated reviewer." | "Use this prompt only to dispatch an isolated reviewer; inline review uses the skill's \"Report format\" section and claims no fresh context." | |
| R2 | "For inline review, use the skill's \"Report format\" section without claiming a fresh context." | merged into R1 | |
| R3 | "Fill every `<field>`; the isolated reviewer gets nothing else." | "Fill every `<field>`; the isolated reviewer gets nothing else." | |
| R4 | Fenced block starting `You are reviewing a change you did not write, in a fresh context. You` | "(same fenced block, byte for byte)" | |

Counts (checker): 153 -> 152 words (0% cut), 20 -> 20 nonblank lines.
Reason: E12 allows only the three lines before the fenced block to change; the fenced prompt is the dispatch payload and stays byte for byte, and the three lines are distinct dispatcher instructions.
