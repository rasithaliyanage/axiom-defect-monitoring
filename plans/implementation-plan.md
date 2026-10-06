# Implementation plan

Incremental vertical slices. Each completes fully and stops for review before the next begins.

## Completed

| Task | Delivered | Verification |
|---|---|---|
| **1** Foundation | `CLAUDE.md`, `README.md`, `docs/`, `specs/`, `tests/`, `evals/`, `.claude/` | Documentation only |
| **2** UI specification schema | `specs/schemas/ui-spec.schema.json` — nine components, closed props, five actions | Draft 2020-12 meta-validation |
| **3** Validation pipeline | `services/domain/{validator,validation_models,text_policy}.py` — Gates 1–4, stable rejection codes | 170 deterministic tests |
| **4** Controlled renderer | `apps/ui/` — component registry, renderer, nine components, DOM safety | 56 tests, strict typecheck |

Gate numbering: these are validation pipeline gates, not the inspection QG-1…QG-6. See
`docs/quality-gates.md`.

## Next candidates, not yet authorised

Ordered so that each is small, independently reviewable, and depends only on what precedes it.

**A. Fallback specification.** A fixed, deterministic UI specification rendered when validation
fails or the model is unavailable. Required by `specs/spec.md` FR-05 and by `CLAUDE.md` rule 3.
Depends on nothing new. Smallest remaining increment, and it closes a rule the code does not yet
satisfy.

**B. Model gateway with bounded repair.** `services/domain/ai/` — invocation, version pinning,
exactly one repair attempt, then fallback. Depends on A. First increment where a model is called.

**C. Grounded context assembly.** The Domain Runtime builds context from domain data rather than
fixtures, and resolves data references for the renderer. Depends on B.

**D. Domain API surface.** Read-only endpoints for inspection records, ingest metadata and defect
reporting, per `specs/spec.md` FR-08. Depends on C.

**E. Inspector review panel.** The role-aware surface over a recorded fixture in
`simulators/capture/`. Requires a vocabulary change — board summary, image comparison, defect
overlay, confidence indicator — and is therefore a contract change requiring all four artefacts in
`CLAUDE.md` "Contract changes are wide changes".

## Sequencing constraints

The deterministic evidence and audit path must exist before any automatic physical action is
enabled. Nothing in A–E takes an action on a board.

Authentication arrives with the first increment that can submit a disposition — not before, and not
after. See `docs/security.md`.

`policies/` must be populated by Quality before any threshold-dependent behaviour is built. B and
onwards do not depend on it; enforcement of BR-002 does.

## Out of scope for this phase

Camera integration, edge image processing, PLC/MES signalling, defect classification models, review
override workflows, and deployment infrastructure. See `CLAUDE.md`.
