# Claude Code engineering instructions

This file governs how Claude Code works in this repository. It is not business documentation and not
a specification. Business requirements live in `docs/business-problem.md`, the system specification in
`specs/spec.md`, and the model contract in `specs/model-contracts.md`.

## Project identity

AI-Based Automated Board Defect Inspection System. Internal application. AI-native and model-driven:
the runtime user interface is produced by an AI model that emits a structured specification, which the
application validates and renders through a fixed component registry.

Current phase: Phase 0, engineering foundation. Documentation and contracts only. No application code
exists. Do not scaffold a build system, install dependencies, or create source files unless the task
explicitly asks for that increment.

## Non-negotiable rules

These rules are architectural, not stylistic. Do not relax them for convenience, and do not implement
a change that violates one — raise the conflict instead.

1. The model never produces executable content. No React, no HTML, no JavaScript, no CSS, no SQL, no
   shell. Model output is a UI specification conforming to `specs/ui-spec.schema.json` and nothing else.
2. The component registry is the only render path. A component that is not registered cannot appear on
   screen. Never introduce a dynamic render escape: no `eval`, no `new Function`, no
   `dangerouslySetInnerHTML`, no dynamic import driven by model output, no string-to-component lookup
   outside the registry.
3. Every model output passes validation before it reaches the renderer. Validation failure results in
   one bounded repair attempt and then the deterministic fallback specification. Never render
   unvalidated output, and never bypass validation with a debug flag that ships.
4. The model reads no data directly. It receives only the grounded context assembled by the Domain
   Runtime. It has no database connection, no image repository access, and no tool that executes
   commands.
5. The model makes no quality decisions. It must not state or imply that a board passes, fails, is
   approved, is rejected, is safe to ship, or is conforming. Pass and fail determinations belong to
   qualified humans and to systems outside this scope.
6. The model invents nothing. Defect categories, metrics, alerts, capabilities, and actions must come
   from identifiers present in the grounded context. An identifier not in the context is a validation
   failure, not a creative liberty.
7. No authentication subsystem. Internal application, network-level access control, this phase only.
   Do not add login pages, token issuance, session management, or user tables.

## Repository layout

Present today:

```
CLAUDE.md                    this file
README.md                    orientation and document map
docs/                        business requirements and architecture
specs/                       system specification, model contract, output schema
tests/                       deterministic tests (strategy documented, suites to come)
evals/                       AI evaluations and case sets
.claude/                     Claude Code configuration for this project
```

Planned, to be created only when the corresponding increment is authorised:

```
apps/ui/                     UI Runtime — React, TypeScript, renderer, component registry
services/domain/             Domain Runtime — FastAPI, board inspection, ingest metadata, reporting
services/domain/ai/          AI Runtime — model gateway, prompt assembly, validation pipeline
```

The AI Runtime begins life as a bounded module inside the Domain Runtime rather than a separate
deployable. The boundary is enforced by interface and dependency direction, not by process isolation.
Do not promote it to its own service without an architecture decision recorded in
`docs/architecture.md`.

## Working method

Specification precedes implementation. If a task requires behaviour that `specs/spec.md` does not
describe, update the specification in the same change and say so.

Contract changes are wide changes. Any modification to the component vocabulary, component props, the
grounded context shape, or the UI specification schema requires all four of the following in one
change, or the change is incomplete:

1. `specs/model-contracts.md` updated.
2. `specs/ui-spec.schema.json` updated.
3. Deterministic tests added or amended under `tests/`.
4. Eval cases added or amended under `evals/`.

Requirements are traceable. Business requirements are numbered `BR-n`, functional requirements `FR-n`,
validation requirements `VR-n`, and architecture decisions `AD-n`. Cite the identifier you are
satisfying in commit messages and pull request descriptions.

Scope is the deliverable. Implement the increment asked for, complete it fully, and stop. Do not
speculatively add caching, feature flags, message queues, retry frameworks, metrics backends, or
abstraction layers for requirements that do not yet exist.

## Conventions

TypeScript. Strict mode on. No `any`. Model-derived data is typed as `unknown` until it has passed
validation, and the validator is the only place that narrows it. Component props are explicit
interfaces. Registry entries are typed so that an unregistered component name fails to compile.

Python. Type hints throughout. Pydantic models for every request, response, grounded context, and
validated specification. No untyped dictionaries crossing a runtime boundary.

Validation. One validation pipeline, one place. Rejections carry a stable machine-readable code from
the list in `specs/model-contracts.md`. Never silently drop an invalid block without recording the
rejection.

Logging. Log the grounded context identifier, the raw model output, the validation outcome, and every
rejection code. This log is the evidence base for evals and for incident review. Do not log image
content or anything that could identify a customer board serial beyond what the domain layer already
exposes.

Text on screen. All user-facing wording is either model-generated within the text policy or a fixed
string in the fallback specification. Do not hard-code business copy inside renderer components.

## Terminology

UI specification — the validated JSON document describing a page as approved components and text.

Component registry — the fixed mapping from an approved component name to its React implementation.

Grounded context — the structured, domain-sourced input that bounds what the model may reference.

Controlled Generative UI — generation of layout and copy within a closed vocabulary, as distinct from
generating code.

Deterministic test — a repeatable pass or fail check with no model in the loop. Lives in `tests/`.

AI evaluation — a scored measurement of model behaviour across a case set. Lives in `evals/`.

## Out of scope for this phase

Physical camera integration. Edge image processing. Real-time PLC or MES signal handling. Automated
defect classification models. Human review override workflows. Production infrastructure,
provisioning, and deployment automation. Authentication and authorisation subsystems.

If a task appears to require one of these, stop and say so rather than building a partial version.
