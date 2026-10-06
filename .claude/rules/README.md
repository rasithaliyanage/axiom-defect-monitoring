# Rules

Project rules and constraints for Claude Code, kept separate from `CLAUDE.md` so that individual
rules can be referenced, versioned and reviewed on their own.

**Status:** empty. `CLAUDE.md` currently carries the non-negotiable rules inline, which is
appropriate while there are seven of them.

## When to add a file here

Split a rule out when it needs detail that would bloat `CLAUDE.md`, or when it applies to one area
rather than the whole repository.

## What a rule is not

`CLAUDE.md` states it plainly: guidance and context, **not a security boundary**. A rule written
here is documentation with the same standing. Anything that must be technically enforced belongs in
schema validation, the component registry, `.claude/hooks/`, or tests — not in prose.
