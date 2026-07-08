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

## Examples

**Stateless + immutable + lazy-init:**

```python
# ❌ mutable module state, eager connection, hidden global
_cache = {}
client = boto3.client("s3")          # connects at import time

def get_user(user_id):
    if user_id not in _cache:
        _cache[user_id] = client.get_object(...)
    return _cache[user_id]

# ✅ frozen config, lazy resource, output derived from inputs
@dataclass(frozen=True)
class UserStore:
    bucket: str

    @cached_property
    def _client(self) -> "S3Client":   # created on first use
        return boto3.client("s3")

    def get_user(self, user_id: str) -> User:
        return User.from_json(self._client.get_object(Bucket=self.bucket, Key=user_id))
```

**Boundary error handling:**

```python
# ❌ guarding a library-native failure, swallowing context
try:
    value = payload["amount"]
except KeyError:
    value = None  # silent None propagates a corrupt state downstream

# ✅ let it raise; catch once at the job boundary with full context
def handle_request(payload: Mapping[str, Any]) -> Result:   # boundary
    try:
        return process(payload)          # inner code does NOT try/except
    except Exception:
        logger.exception("request failed", extra={"trace_id": payload.get("trace_id")})
        raise
```

**Comments:**

```python
# ❌ increment retry counter                    (restates the code)
retries += 1

# ✅ provider throttles bursts >5 rps; spacing calls avoids 429 storms   (the WHY)
time.sleep(0.2)
```

## Review posture

- Never fabricate. Cite evidence for claims.
- Concrete recommendations with pros/cons; push back when the code (or user)
  is wrong. Argue a defensible position; no filler praise.
- Ask before assuming on ambiguous, high-stakes changes — architecture shifts
  or adding a library always get a question first.
