---
name: review-uispec
description: Review a change that touches the UI specification contract — schema, component vocabulary, props, actions, validator, registry or renderer — against the authoritative sources. Use when a change adds or alters a component, prop, action or schema rule, or when asked whether a UISpec change is safe.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# review-uispec

Review a UI specification change against the documents and code that actually define the contract,
and report findings with the authority for each one.

**This skill is read-only.** It reports; it does not edit the specification, the schema or the
renderer. A finding is an input to a decision someone else makes.

## Governed by

`.claude/rules/runtime-boundaries.md` states the boundaries this review is checking. Read it first.

## The authorities, and what each one settles

Never answer from this file. Open the source and cite it.

| Question | Authority |
|---|---|
| Is this structurally legal? | `specs/schemas/ui-spec.schema.json` — the loaded schema. `specs/ui-spec.schema.json` carries `"deprecated": true` and is never merged |
| Is this component or prop approved, and what rejection code applies? | `specs/model-contracts.md` |
| What must the system do, and which VR covers it? | `specs/spec.md` |
| What is actually enforced? | `services/domain/validator.py` — `UISpecValidator.validate(spec, context)`, four gates |
| What can actually render? | `apps/ui/src/renderer/registry.ts`, `renderUISpec.tsx`, `types.ts` |
| How does approved input reach the renderer? | `apps/ui/src/renderer/approved.ts`, and `apps/ui/README.md` |
| Is it covered? | `tests/validator/`, `apps/ui/test/` |

When two disagree, that disagreement **is** the finding. Say which you trust and why — generally the
executing code over the prose, and say so explicitly rather than quietly picking one.

## What to check

**Vocabulary and props.** Every component name approved; every prop approved for that component with
an approved value; no prop invented to carry something the contract has no slot for. The registry is
exhaustive by construction, so a new component that compiles but is absent from
`specs/model-contracts.md` is a contract gap, not a feature.

**Actions.** Every action identifier is in the approved list. `Hero.primaryAction` is an identifier
with no label prop — labels come from `GroundedContext.actions[].label` via `options.actionLabels`.
A change that invents a label, URL, route or destination has crossed a boundary.

**Grounding.** Every referenced metric, alert, defect category and capability exists in the grounded
context. Displayed values match the context exactly — not rounded, reformatted or recomputed
(`specs/spec.md` VR-4).

**Validation is not bypassed.** Nothing reaches the renderer without `VALID`. No debug flag, no
environment variable, no test-only escape importable from `src/`. The branded `ApprovedUISpec` is
still unforgeable: the symbol unexported, no `approve(raw)` factory, no cast into the type.

**No arbitrary resolution.** One registry, own-property lookup. No second lookup path, no fallback
resolution, no dynamic import keyed on specification data.

**No model-derived value becomes behaviour.** No spec value becomes a tag name, module path, URL,
style string, event handler or spread property. Heading levels branch explicitly; they are never a
computed tag name.

**Structural limits.** Block count, nesting depth, item and row counts, string and total-text
limits — Gate 1 concerns, defined in the schema and summarised in `specs/spec.md`.

**Text policy.** No markup, URL, code-like content, and no decision language. Nothing may state or
imply that a board passes, fails, is approved or is conforming (`specs/spec.md` VR-8, BR-3).

**Tests and evals.** A contract change must touch `specs/model-contracts.md`,
`specs/schemas/ui-spec.schema.json`, `tests/` **and** `evals/` in the same change, per `CLAUDE.md`.
A change missing any of the four is incomplete — report that as a finding, with the missing ones
named.

## Reporting

Per finding: what, where (`file:line`), which authority settles it, and what would detect a
regression. Rank by whether it can reach a user.

Separate what you **verified by executing** from what you **read**. The validator passing is
evidence; the documentation saying a control exists is not. Do not assert runtime safety on the
strength of prose — if you did not run the test, say so.

If nothing is wrong, say that plainly and say what you checked. An empty finding list with no
coverage statement is indistinguishable from not having looked.

## Out of scope

Do not redesign the contract. Do not edit the specification, schema or renderer "while you are in
there" — a review that quietly changes its subject cannot be reviewed itself. Do not widen the
vocabulary to make a change fit: a component or identifier the contract does not have is a decision
for whoever owns the contract.
