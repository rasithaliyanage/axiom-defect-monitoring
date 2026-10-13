# Rule: runtime boundaries

**Scope:** engineering-time guidance for Claude Code. This file changes how changes get made. It
enforces nothing at runtime — see [`README.md`](README.md).

**Authority:** `CLAUDE.md` rules 1–4 state these boundaries and `docs/architecture.md` explains why
they are shaped this way. The contract itself is `specs/schemas/ui-spec.schema.json` (the loaded
schema — `specs/ui-spec.schema.json` is deprecated and never merged), with the vocabulary, prop
rules and rejection codes in `specs/model-contracts.md` and the required behaviour in
`specs/spec.md`. Read the contract there rather than inferring it from this file; where any of them
disagrees with this one, they win and this file is wrong.

## The path that must stay intact

```
ContextPayload → Domain Runtime → UI specification → schema → validator
              → approved specification → controlled renderer → approved components → browser
```

Every arrow is a narrowing. A change that lets data skip one is not a shortcut, it is a different
architecture.

## What to do

**Leave the single render path single.** `apps/ui/src/renderer/registry.ts` holds the only map from
an approved component name to a React implementation. `hasRegisteredComponent` uses own-property
lookup deliberately, so `toString`, `constructor` and `__proto__` cannot resolve as components. Do
not add a second resolution path, a fallback lookup, or a dynamic import keyed on specification data.

**Keep validation ahead of rendering, not beside it.** `UISpecValidator.validate(spec, context)` in
`services/domain/validator.py` is the authority, applying the four gates defined in
`docs/architecture.md` and reported through the rejection codes in `specs/model-contracts.md`. A
specification reaches the renderer only after it returns `VALID`. Client-side checking is
convenience; it is never the control.

**Do not forge provenance.** `ApprovedUISpec` in `apps/ui/src/renderer/approved.ts` is branded with
a symbol that is not exported, so the handle cannot be constructed elsewhere. If you need an approved
value in new code, route it through the existing issuing function. Do not widen the brand's export,
add an `approve(raw)` escape, or cast into the type — a cast proves nothing, and the brand's whole
value is that it is unfakeable.

**Treat `ContextPayload` as data.** `services/domain/request_context.py` defines it as a frozen,
slotted dataclass over closed enums. It names *what presentation is being asked for*. Nothing in it
selects a file, builds a path, or names code to run, and no field should ever be added that does.

**Keep model-derived values inert.** A value that arrived from outside the Domain Runtime may be
displayed, compared or rejected. It may not become a module path, a component name, a URL, a property
key spread onto an element, or anything the runtime executes or navigates to.

**Preserve the API boundaries that exist.** Parameters are accepted on the read-only
`/api/v1/inspection/*` endpoints and nowhere else. `POST /api/v1/ui/landing-page` ignores query
strings entirely, because it is the one endpoint whose output feeds the renderer and caller-steered
input there is precisely what the approved-input boundary prevents. Adding a parameter to it is a
boundary change, not a feature.

**Change the contract in all four places or not at all.** The component vocabulary, component props,
the grounded context shape and the specification schema are one contract spread across
`specs/model-contracts.md`, `specs/schemas/ui-spec.schema.json`, `tests/` and `evals/`. `CLAUDE.md`
requires all four in the same change. Editing the schema alone leaves the validator agreeing with a
document nobody else follows.

## What to do when a change needs a boundary moved

Stop and say so before writing the code. Name which boundary, what the change would allow that is
currently impossible, and what would detect a regression afterwards. Then wait.

A boundary change is cheap to discuss and expensive to discover later in review. "The task implied
it" is not authorisation: the requested scope is the deliverable, and a boundary crossing is outside
any scope that did not name it.

## Things that are not yet built

No AI Runtime exists in this repository — no model gateway, no model call, no generated
specification. The specifications served today are developer-authored fixtures that passed the
validator offline.

That makes these boundaries cheap to hold now and expensive to retrofit later, which is the reason
to hold them now. Do not describe the model path as implemented, in code comments, documentation or
a report, until it is.
