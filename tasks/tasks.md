# Tasks

Derived from `plans/implementation-plan.md`. One task per reviewable increment.

Each task states: objective, specification reference, dependencies, acceptance criteria, tests, eval
requirements, and security considerations. A task is not started until the preceding one is
reviewed.

---

## Completed

| ID | Objective | Result |
|---|---|---|
| TASK-001 | Project foundation | Documentation and contracts |
| TASK-002 | UI specification schema | `specs/schemas/ui-spec.schema.json` |
| TASK-003 | Validation pipeline, Gates 1–4 | 170 tests passing |
| TASK-004 | Controlled UISpec renderer | 56 tests passing, typecheck clean |
| TASK-005 | Deterministic fallback specification | 8 tests; valid against any context |
| TASK-006A | Explicit presentation request seam | 24 tests; `ContextPayload` with page, view, locale |

---

## TASK-005 — Deterministic fallback specification

**Status:** DONE (2026-10-06). `tests/fixtures/ui-spec/fallback.{spec,context}.json`, proven valid against an empty context, its own context and unrelated populated contexts. Not yet wired into a repair loop — that remains TASK-006.

**Objective.** A fixed UI specification, valid under the schema and all four gates, rendered
whenever validation fails or generation is unavailable.

**Specification reference.** `specs/spec.md` FR-05; `CLAUDE.md` non-negotiable rule 3.

**Dependencies.** None. The renderer and validator both exist.

**Acceptance criteria.**
- The fallback passes the schema and all four validation gates — asserted, not assumed
- It references no metric, alert, defect category or capability, so it is valid against any context
- It renders through the existing registry with no new component
- The landing page renders with the AI Runtime entirely absent

**Tests.** Fallback validity against an empty grounded context; renderer output for the fallback;
failure paths — invalid specification, unavailable generator, timeout — each resolving to it.

**Eval requirements.** None. The fallback is fixed content with no model in the loop.

**Security considerations.** Fixed strings only. Per `CLAUDE.md`, the fallback is the one place
business copy may be hard-coded; it must still contain no decision language.

**Why this is next.** `CLAUDE.md` rule 3 requires a fallback and none exists, so the codebase does
not currently satisfy its own non-negotiable rules. It is also the smallest remaining increment and
adds no dependency.

---

## TASK-006 — Model gateway with bounded repair

**Status:** Not started. Depends on TASK-005.

**Objective.** `services/domain/ai/` invokes the model, pins the version, attempts exactly one
repair on validation failure, and then returns the fallback.

**Specification reference.** `specs/spec.md` FR-01, FR-06; `CLAUDE.md` rule 3.

**Acceptance criteria.** Exactly one repair attempt occurs; the second failure yields the fallback;
transport failures produce the fallback with no repair attempt; every generation records context
identifier, raw output, outcome, rejection codes and model version.

**Tests.** Stub gateway asserting call counts; each failure mode resolving to the fallback.

**Eval requirements.** First task where evals become meaningful — capability honesty, verdict
neutrality, refusal behaviour and vocabulary adherence, per `evals/README.md`.

**Security considerations.** First increment where a model is invoked. The gateway is the only
egress point; it receives grounded context and returns text. No tools, no data access.

---

## Not yet broken down

TASK-007 grounded context assembly, TASK-008 domain API surface, and TASK-009 inspector review
panel. Each is described in `plans/implementation-plan.md`; they are not detailed here because the
preceding tasks may change their shape.

TASK-009 changes the approved component vocabulary and is therefore a contract change requiring all
four artefacts listed in `CLAUDE.md`.
