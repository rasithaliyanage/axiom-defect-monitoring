# Automated Board Defect Inspection System

An internal, AI-native application for electronics board defect inspection. The system presents
inspection context, defect reporting, and operational summaries through a user interface that is
generated at runtime by an AI model under strict architectural control.

## Current status

Phase 0 — engineering foundation only. This repository contains documentation, specifications, and
contracts. No application code exists yet. Do not assume any runtime, dependency, or build system is
in place.

The first implementation scenario is deliberately small: a single landing page rendered through
controlled Generative UI.

## The central architectural idea

The AI model does not write code. It returns a structured UI specification — a JSON document that
selects and arranges components from a fixed, approved registry and supplies user-facing text. The
application validates that specification and renders it only through pre-built React components.

This means a model failure degrades into a rejected specification and a deterministic fallback page,
never into executed code, arbitrary markup, or an unauthorised data access path.

## Runtimes

The system is organised into three runtimes with explicit boundaries.

UI Runtime — React and TypeScript. Hosts the controlled Generative UI renderer and the component
registry. Renders validated specifications. Never receives or evaluates code from the model.

Domain Runtime — FastAPI and Python. Owns board inspection, image ingest metadata, and defect
reporting. Assembles the grounded context that constrains generation. The only component permitted
to read domain data.

AI Runtime — Model gateway and UI generation model. Converts grounded context into a structured UI
specification, validates it, repairs or rejects it. Has no database access, no filesystem access to
image repositories, and no command execution capability.

See `docs/architecture.md` for the full topology and trust boundaries.

## Document map

Each document has one job. Read the one that matches your question.

| Question | Document |
| --- | --- |
| Why does this system exist, and what must it achieve for the business? | `docs/business-problem.md` |
| How is the system structured, and where are the trust boundaries? | `docs/architecture.md` |
| What exactly must be built, and how will we know it is correct? | `specs/spec.md` |
| What may the model do, what must it never do, and what shape is its output? | `specs/model-contracts.md` |
| What is the validated output schema, in machine-readable form? | `specs/ui-spec.schema.json` |
| How do we verify deterministic software behaviour? | `tests/README.md` |
| How do we measure non-deterministic model behaviour? | `evals/README.md` |
| How should Claude Code work in this repository? | `CLAUDE.md` |

## Tests and evaluations are different things

Deterministic tests live in `tests/`. They call no model, produce identical results on every run, and
gate every change. They answer: does the validator reject an unapproved component, and does the
renderer refuse to render one?

AI evaluations live in `evals/`. They call the model, produce scored and variable results, and gate
contract or prompt changes. They answer: how often does the model return a valid, grounded, in-policy
specification?

A passing test suite does not imply acceptable model behaviour. An acceptable eval score does not
imply correct software. Both are required.

## Scope boundaries for this phase

Not in scope, and not to be built: physical camera integration, edge image processing, real-time PLC
or MES signal handling, automated defect classification models, human review override workflows, and
production infrastructure.

Authentication is out of scope. This is an internal application and the initial implementation
relies on existing network-level access control. No authentication subsystem is to be created.

## Next task

The next implementation task is stated at the end of this file's companion, `specs/spec.md`, under
Acceptance criteria. It is intentionally the smallest useful increment. Do not begin work beyond it
without agreement.
