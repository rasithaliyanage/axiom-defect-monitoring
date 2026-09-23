# Architecture

## Executive summary

The system is composed of three runtimes — UI, Domain, and AI — separated so that the AI model can
influence presentation while being structurally incapable of executing code, reading data, or deciding
quality outcomes. The model emits a structured UI specification; the Domain Runtime grounds and
validates it; the UI Runtime renders it exclusively through a fixed component registry.

This document describes structure and control points. Requirements live in
`docs/business-problem.md`, testable behaviour in `specs/spec.md`, and the model's input and output
contract in `specs/model-contracts.md`.

## Runtime topology

```
   Browser
      |
      | 1. request landing view
      v
+--------------------------------------------+
|  UI Runtime            React + TypeScript  |
|  - Controlled Generative UI renderer       |
|  - Component registry (closed vocabulary)  |
|  - Fallback specification                  |
+--------------------------------------------+
      |
      | 2. POST /api/v1/ui/landing-page        (no model access from the browser)
      v
+--------------------------------------------+
|  Domain Runtime        FastAPI + Python     |
|  - Board inspection                         |
|  - Image ingest metadata                    |
|  - Defect reporting                         |
|  - Grounded context assembly                |
|  - Validation pipeline (authoritative)      |
+--------------------------------------------+
      |
      | 3. grounded context + schema + vocabulary
      v
+--------------------------------------------+
|  AI Runtime                                 |
|  - Model gateway                            |
|  - UI generation model                      |
|  - Structured output only                   |
|  - No DB, no files, no commands, no tools   |
+--------------------------------------------+
```

## UI Runtime

React and TypeScript. Responsible for turning a validated UI specification into rendered output and for
nothing else of consequence.

The renderer walks the specification's block list and looks each block's `component` field up in the
component registry. The registry is a statically typed, closed map from approved component name to
React implementation. There is no dynamic resolution path, no string evaluation, and no raw HTML
injection. If a block names a component that is not in the registry, the renderer omits that block and
records a rejection; it never attempts to resolve it by any other means.

Component implementations are conventional, hand-written React. They contain layout and styling. They
do not contain business copy, because copy is either model-generated inside the text policy or supplied
by the fallback specification.

The UI Runtime also holds the fallback specification: a hand-authored, always-valid UI specification
used when generation fails. This is why an unavailable model does not produce an unavailable page.

The browser never calls the model gateway and never holds a model credential.

## Domain Runtime

FastAPI and Python. Owner of all domain truth and the only party permitted to read domain data.

Its initial business surface covers three areas. Board inspection exposes inspection records and
current queue state. Image ingest metadata exposes descriptive information about ingested board images
— identifiers, timestamps, capture source, dimensions — without exposing image content or acting as an
image service. Defect reporting exposes defect records and summary aggregates over the approved defect
categories.

The Domain Runtime performs two roles that make controlled generation possible. First, it assembles the
grounded context: the closed set of metrics, alerts, defect categories, capabilities, and actions the
model is permitted to reference. Second, it hosts the authoritative validation pipeline. Validation on
the server is what makes the guarantee real; any client-side checking is convenience, not control.

## AI Runtime

A model gateway and a UI generation model. In this phase the gateway is a bounded module inside the
Domain Runtime process (`services/domain/ai/`) rather than a separate deployable, with the boundary
enforced by interface and dependency direction. Promotion to a separate service requires a recorded
decision.

The gateway assembles the prompt from the grounded context, the approved component vocabulary, and the
UI specification schema; requests structured output constrained to that schema; and returns the parsed
result to the validation pipeline. It holds the model credential.

The gateway has no database session, no filesystem access to image repositories, and no command
execution capability. The model is given no tools. Its only output channel is the specification
document.

## Request flow

1. The browser requests the landing view from the UI Runtime.
2. The UI Runtime calls the Domain Runtime's UI generation endpoint with a presentation context
   descriptor — page identity and locale. It sends no data the model will treat as ground truth.
3. The Domain Runtime assembles the grounded context from board inspection, ingest metadata, and defect
   reporting. Every identifier the model may legitimately reference is enumerated here.
4. The gateway requests a structured UI specification from the model, constrained to the schema and the
   approved vocabulary.
5. The validation pipeline evaluates the returned specification against the gates below.
6. On failure, one bounded repair attempt is made with the rejection codes supplied back to the model.
   A second failure yields the fallback specification.
7. The Domain Runtime returns a validated specification, together with the source — generated,
   repaired, or fallback — and any rejection codes.
8. The UI Runtime renders the specification through the component registry.

## Trust boundaries and control points

There are three boundaries, and each has a control point that must not be weakened.

Browser to Domain Runtime. The browser is untrusted input. It may request a page; it may not supply
grounding data, component definitions, or prompt content.

Domain Runtime to AI Runtime. The model is untrusted output. Everything crossing back from the gateway
is `unknown` until validated. The control point is the validation pipeline, and it lives on the server
side of this boundary.

Domain Runtime to data. The model is never on this path. Data reaches the model only as grounded
context that the Domain Runtime chose to include.

## Validation pipeline

Four gates, applied in order. Each rejection carries a stable machine-readable code; the code list is
defined in `specs/model-contracts.md`.

Gate 1, structural. The output parses as JSON and conforms to `specs/ui-spec.schema.json`, including
block count, nesting depth, and string length limits.

Gate 2, registry. Every `component` value is an approved component name, and every prop is approved for
that component with an approved value.

Gate 3, grounding. Every referenced metric, alert, defect category, capability, and action identifier
exists in the grounded context supplied for this request. Displayed metric values must match the
context value exactly; the model does not compute, round, or restate figures.

Gate 4, policy. Text contains no decision language, no code-like content, no markup, and no URLs, and
stays within the text policy limits.

## Failure handling

Generation failure is an expected operating state, not an incident. Model unavailability, timeout,
malformed output, and policy rejection all resolve to the same user-visible outcome: the fallback
specification renders and the failure is recorded with its rejection codes. Repair is attempted once,
never in an unbounded loop.

## Observability

Each generation records the grounded context identifier, the raw model output, the validation outcome,
every rejection code, the specification source, and latency. This record is the evidence base for the
evaluations in `evals/` and for post-incident review. Image content is never logged.

## Architecture decisions

AD-1. The model emits a UI specification, not code. A specification can be validated against a closed
grammar before anything is rendered; generated code cannot be validated to a comparable standard. This
decision is the foundation of BR-2 and is not revisitable within this architecture.

AD-2. The component registry is closed and statically typed. A closed vocabulary converts "the model
should not render unapproved things" into "the model cannot", and static typing moves registry mistakes
from runtime to compile time.

AD-3. Validation is authoritative on the server. Client-side validation can be bypassed; the guarantee
must hold where the client cannot reach.

AD-4. The AI Runtime is a module inside the Domain Runtime for now. The boundary that matters is
logical — no data access, no execution, structured output only — and a separate process would add
operational cost without strengthening it at this size.

AD-5. A hand-authored fallback specification ships with the UI Runtime. It satisfies BR-6 with no model
dependency and doubles as a reference example of a valid specification.

AD-6. No authentication subsystem in this phase, per BR constraints. Access is controlled at the
network level. Recorded explicitly so the omission reads as a decision rather than an oversight.

AD-7. Metric values are copied, never computed, by the model. Exact-match validation against the
grounded context makes fabricated or drifted figures mechanically detectable.

## Deferred concerns

Camera integration, edge image processing, PLC and MES signalling, automated defect classification,
human review override workflows, production infrastructure, caching and rate limiting strategy,
multi-page navigation, personalisation, and internationalisation. None are designed for here; the
boundaries above are intended to remain valid when they are.
