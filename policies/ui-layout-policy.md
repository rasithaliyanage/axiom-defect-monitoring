# Generative UI layout policy

- **Owner:** Quality, with Manufacturing for operator-facing surfaces
- **Status:** Partially decided. The engineering boundary exists; the business rules do not.
- **Source question:** BRD §24 "Human-in-the-Loop", §27 "Reporting", §28 "Auditability"

## What this file must eventually contain

What the model is permitted to compose, for whom, and what must always be present or absent on a
screen a quality decision will eventually be made on.

## Already decided, and enforced in engineering

These are contract, not policy, and are recorded here only so the boundary is visible from the
business side. They live in `specs/model-contracts.md` and are enforced by the validator and the
component registry.

- The model selects from a closed component vocabulary; anything outside it is rejected
- The model emits a specification, never executable content
- The model names data references; the Domain Runtime resolves every displayed value
- The model may not state or imply that a board passes, fails, or is approved
- `DispositionControl` is deliberately excluded from the v1 vocabulary

## Awaiting business decision

| Question | Owner |
|---|---|
| Which roles exist, and what may each see? Operator, inspector and manager are assumed from the BRD but not confirmed | Quality |
| Must any element always appear on a review surface — for example evidence provenance or model version? | Quality |
| May layout emphasis vary by severity, or does that risk editorialising a result? | Quality |
| What must a screen show before a disposition may be submitted? | Quality |
| Is there wording the model must never produce beyond the current decision-language rule? | Quality |
| Which surfaces are permitted on the factory floor versus the enterprise network? | Manufacturing |

## The boundary worth stating plainly

A layout can editorialise without naming a verdict. Ordering that foregrounds failures, or emphasis
that makes a marginal result read as conclusive, influences a human decision without ever using a
prohibited word.

No validator detects this — it is measurable only by evaluation. That is why `evals/` exists
alongside `tests/`, and why the second and third questions above are business decisions rather than
engineering ones.
