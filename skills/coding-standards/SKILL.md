---
name: coding-standards
description: >-
  Use whenever writing or reviewing production code, in any language, on every
  implementation step.
---

# Coding Standards

## Core principles

1. **Readability over cleverness** — optimize for the reader later. Simple
   ternaries are fine; implicit coercion tricks and dense functional pipelines
   that obscure intent are not.
2. **Stateless over stateful** — derive output from inputs. Push state to
   explicit, named stores (DB, cache, queue, object store). No hidden globals,
   no mutable module-level state.
3. **Declarative over imperative** — express the desired state or outcome, not
   the steps. Prefer configuration, schemas, and rules over procedural
   scripts. Imperative only when control flow genuinely matters.
4. **Immutability over mutability** — prefer `final` / `const` / `readonly` /
   frozen records. Mutate by producing a new value, not patching in place.
5. **Lazy initialization, eager validation** — initialize expensive resources
   on first use; validate configuration eagerly at startup (health-check /
   readiness probe).
6. **Templating for configuration** — prefer templating (Jinja) over
   duplication or string concatenation. Keep logic out of templates.
7. **Smallest sufficient abstraction** — inline simple one-off logic local to
   one call site. Add helpers only when reused, domain-significant,
   independently tested, or clearly better for readability. Three similar
   lines beat a premature abstraction.

## Error handling — at the boundary, not everywhere

- Do NOT guard library-native failures. Let missing keys, invalid indexes,
  bad types, and provider errors raise naturally unless handling adds
  project-specific context.
- Catch and log ONCE at a high layer (workflow/job/request boundary) where
  full context exists. Catch earlier only to recover, translate to a domain
  error, or add context the boundary cannot know.
- Never add error handling for scenarios that cannot happen. Validate at
  system boundaries (user input, external APIs); trust internal code.
- **Resilient attribute collection**: when gathering best-effort attributes,
  pre-initialize each to its fallback, run in priority order, and build the
  result in both success and error branches from whatever was captured.

## Logging

- Structured logs (with correlation/trace IDs where possible) at every
  boundary: request in, downstream call out, response out, error caught.
- No `print` / `console.log` in production code — ever.
- Never log secrets or PII.

## Size and shape

- Functions: ideally 20–40 lines, 3–5 parameters.
- Modules: ideally 3–5 files/classes each.
- Commits: one small feature or 1–3 related functions; message 5–20 words.

## Comments

- **No comments explaining WHAT code does** — names do that.
- Comment only when the WHY is non-obvious: hidden constraint, workaround for
  a specific bug, behavior that would surprise a reader.

## Python specifics

- PEP 8, 120-character lines.
- Type hints required on all functions and parameters (optional for
  constructors); strongly preferred on variables.
- Prefer `@property` / `@cached_property` for declarative, immutable,
  lazy-init access.
- `@dataclass(frozen=True)` with immutable field types: `Sequence`/`tuple`
  instead of `list`, `Mapping` instead of `dict`.
- Imports at top of module; `if TYPE_CHECKING:` for type-only or optional
  dependencies.

## Review posture

- Never fabricate. Cite evidence for claims.
- Concrete recommendations with pros/cons; push back when the code (or user)
  is wrong. Argue a defensible position; no filler praise.
- Ask before assuming on ambiguous, high-stakes changes — architecture shifts
  or adding a library always get a question first.
