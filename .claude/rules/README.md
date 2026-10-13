# Rules

Project rules and constraints for Claude Code, kept separate from `CLAUDE.md` so that individual
rules can be referenced, versioned and reviewed on their own.

**Status:** four rules. `CLAUDE.md` still carries the seven non-negotiable architectural rules
inline; these files are focused behavioural guidance that says how to act on them, and they cite
`CLAUDE.md` rather than restating it.

## The files

| File | Controls |
|---|---|
| [`runtime-boundaries.md`](runtime-boundaries.md) | Keeping the validate-then-render path intact: one registry, no forged provenance, no model-derived value becoming behaviour, and what to do when a change needs a boundary moved |
| [`business-data-integrity.md`](business-data-integrity.md) | Board-inspection specific. No invented figures, categories or capabilities; figures traceable to a source; the system reports, a qualified person decides |
| [`testing.md`](testing.md) | Read tests before changing code, run what the change touched, never soften a test to pass, never report a result that was not executed |
| [`security.md`](security.md) | No dynamic execution path, model output stays data, errors stay sanitized, no secrets, no silent bypass, no partial version of a deferred control |

## What a rule is, and is not

`CLAUDE.md` states it plainly: guidance and context, **not a security boundary**. A rule written
here is documentation with the same standing. Anything that must be technically enforced belongs in
schema validation, the component registry, `.claude/hooks/`, or tests — not in prose.

That distinction is the whole point of this directory, so it is worth laying out in full:

| | Answers | Lives in | Binds |
|---|---|---|---|
| **CLAUDE.md** | What should Claude Code know about this project? | repository root | by being read |
| **Rules** | What focused behaviours should Claude Code follow consistently? | here | by being read |
| **Specification** | What is the system required to do? | `specs/`, `docs/` | by review |
| **Runtime validation** | What does the application actually enforce? | `services/domain/validator.py`, the registry, the schema | by executing |
| **Tests** | What do we verify automatically? | `tests/`, `apps/ui/test/` | by failing |

Only the bottom two rows stop anything. A rule that matters enough to be mechanical should become a
test or a hook; until it does, it is a statement of intent that a reviewer still has to check.

## When to add a file here

Split a rule out when it needs detail that would bloat `CLAUDE.md`, or when it applies to one area
rather than the whole repository. Keep each file focused — a rule nobody finishes reading guides
nothing.
