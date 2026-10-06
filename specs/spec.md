# System specification

## Executive summary

This specification defines the buildable, testable behaviour of the first implementation scenario: an
Automated Board Defect Inspection landing page rendered through controlled Generative UI. It states
functional requirements, the domain API surface, validation requirements, and acceptance criteria.

Business rationale is in `docs/business-problem.md`. Structure is in `docs/architecture.md`. The
model's permitted behaviour and output shape are in `specs/model-contracts.md`, which this document
treats as normative and does not duplicate.

## Scope

In scope for this scenario: one landing page; the grounded context that bounds its generation; the
validation pipeline; the component registry with nine approved components; a fallback specification;
and a minimal read-only domain API over board inspection, image ingest metadata, and defect reporting.

Out of scope: everything listed under Out of scope in `docs/business-problem.md`, plus multi-page
routing, user preferences, and write operations on domain data.

## Definitions

UI specification — a JSON document conforming to `specs/schemas/ui-spec.schema.json` that describes a page as
an ordered list of approved component blocks with approved props.

Grounded context — the structured payload assembled by the Domain Runtime enumerating every metric,
alert, defect category, capability, and action the model may reference for a given request.

Component registry — the closed, statically typed map from approved component name to React
implementation in the UI Runtime.

Specification source — the provenance of a served specification: `generated`, `repaired`, or
`fallback`.

## Functional requirements

FR-1. The UI Runtime shall render a landing page from a validated UI specification, resolving every
block through the component registry. Satisfies BR-1.

FR-2. The component registry shall contain exactly these nine components in this phase: `Hero`,
`Heading`, `Text`, `FeatureCard`, `FeatureGrid`, `CTA`, `Alert`, `InfoPanel`, `ProgressIndicator`. A
block naming anything else shall not render. Satisfies BR-2.

FR-3. The Domain Runtime shall expose a UI generation endpoint that returns a validated UI
specification for the landing page, together with its specification source and any rejection codes.
Satisfies BR-1.

FR-4. The Domain Runtime shall assemble a grounded context for each generation request containing
inspection summary metrics, recent defect alerts, the approved defect categories, the system's declared
capabilities, and the approved actions. Satisfies BR-4.

FR-5. The AI Runtime shall request structured output constrained to the UI specification schema and
shall pass the result to validation as untrusted data. It shall not execute, interpret, or render
model output. Satisfies BR-2.

FR-6. The Domain Runtime shall validate every model output through all four gates defined in
`docs/architecture.md` before returning it. Satisfies BR-2, BR-3, BR-4.

FR-7. On validation failure the system shall attempt exactly one repair, supplying the rejection codes
to the model, and on a second failure shall return the fallback specification. Satisfies BR-6.

FR-8. On model unavailability, timeout, or transport error the system shall return the fallback
specification without a repair attempt. Satisfies BR-6.

FR-9. The Domain Runtime shall expose read-only endpoints for board inspection records, image ingest
metadata, and defect report summaries over the approved defect categories. Satisfies BR-5.

FR-10. The system shall record, for each generation, the grounded context identifier, raw model output,
validation outcome, rejection codes, specification source, and latency. Image content shall not be
recorded. Satisfies BR-2.

FR-11. The landing page shall remain informative when rendered from the fallback specification: it
shall state the system's purpose and the availability of inspection and defect reporting, without
referencing figures it does not have. Satisfies BR-6.

FR-12. The system shall not implement authentication or authorisation in this phase. Satisfies the
internal-access constraint.

## UI specification model

A specification has a `specVersion`, a `page` identifier, and an ordered `blocks` array. Each block has
a `component` name and a `props` object. Only `FeatureGrid` may contain children, and only
`FeatureCard` children, giving a maximum nesting depth of two.

Structural limits, enforced at Gate 1: at most 12 top-level blocks; at most 6 items in a `FeatureGrid`;
at most 8 rows in an `InfoPanel`; at most 4000 characters of total text; individual string limits as
given in `specs/schemas/ui-spec.schema.json`.

`specVersion` is `"1.0"` for this phase. A specification whose version the runtime does not recognise
is rejected, not coerced.

## Component registry

Prop-level contracts are normative in `specs/model-contracts.md`. Summarised here for orientation:

`Hero` — page-opening banner with eyebrow, title, subtitle, and an optional call to action.
`Heading` — section heading at level 2 or 3.
`Text` — a paragraph of body copy.
`FeatureCard` — a titled card describing one capability or one summary item.
`FeatureGrid` — a two or three column arrangement of `FeatureCard` items.
`CTA` — a labelled action button bound to an approved action identifier.
`Alert` — an informational, warning, or critical notice, optionally tied to a defect category.
`InfoPanel` — a label and value list for summary statistics drawn from context metrics.
`ProgressIndicator` — a labelled percentage bar for a context metric expressed as a percentage.

## Domain API surface

Versioned under `/api/v1`. All read-only in this phase. Request and response bodies are Pydantic
models.

`POST /api/v1/ui/landing-page` — accepts a presentation context descriptor (page identity, locale) and
returns `{ spec, source, rejections, contextId }`. The only endpoint that invokes the AI Runtime.

`GET /api/v1/inspection/summary` — current inspection summary metrics.

`GET /api/v1/inspection/queue` — current inspection queue state.

`GET /api/v1/ingest/images` — image ingest metadata records. Metadata only; no image content.

`GET /api/v1/defects/categories` — the approved defect categories.

`GET /api/v1/defects/alerts` — recent defect alerts.

`GET /api/v1/defects/summary` — defect counts aggregated by approved category.

`GET /api/v1/health` — liveness, including whether AI generation is currently available.

## Grounding context contract

The grounded context shape, its identifier semantics, and the rule that metric values are copied
verbatim rather than computed are specified in `specs/model-contracts.md`. The Domain Runtime is
responsible for ensuring the context is internally consistent and contains no identifier the system
cannot substantiate.

## Validation requirements

VR-1. A specification failing JSON parsing or schema conformance shall be rejected with `E_SCHEMA`.

VR-2. A block naming a component outside the registry shall be rejected with `E_UNKNOWN_COMPONENT`.

VR-3. A prop that is unknown for its component, of the wrong type, or outside its allowed value set
shall be rejected with `E_PROP_INVALID`.

VR-4. A referenced metric identifier absent from the grounded context, or a displayed metric value not
matching the context value exactly, shall be rejected with `E_UNGROUNDED_METRIC`.

VR-5. A defect category identifier absent from the grounded context shall be rejected with
`E_UNKNOWN_DEFECT_CATEGORY`.

VR-6. An action identifier absent from the approved action list shall be rejected with
`E_UNKNOWN_ACTION`.

VR-7. Text exceeding length limits, or containing markup, URLs, or code-like content, shall be rejected
with `E_TEXT_POLICY` or `E_CODE_LIKE_CONTENT` as applicable.

VR-8. Text asserting or implying a pass, fail, approval, rejection, certification, or fitness-to-ship
outcome shall be rejected with `E_DECISION_LANGUAGE`. Satisfies BR-3.

VR-9. A specification exceeding block, item, row, or total-text limits shall be rejected with
`E_SIZE_LIMIT`; one exceeding nesting depth, with `E_DEPTH_LIMIT`.

VR-10. Validation shall be performed by the Domain Runtime. No client-side check shall be treated as
sufficient, and no configuration available in a deployed build shall disable validation.

VR-11. Validation shall report all rejections for an output, not only the first, so that repair has
complete information.

## Fallback requirements

FR-7 and FR-8 determine when the fallback is used. The fallback specification is hand-authored, stored
with the UI Runtime, and itself valid under the schema and all four gates — this is asserted by a
deterministic test, not by inspection. It references no metric, alert, or defect category, so it cannot
become stale or ungrounded.

## Non-functional requirements

NFR-1. The landing page shall render within two seconds of the browser's request in the fallback path.

NFR-2. Generation, including one repair attempt, shall be bounded by a request timeout; exceeding it
triggers the fallback path rather than a longer wait.

NFR-3. The renderer shall contain no dynamic code execution path: no `eval`, no `new Function`, no
`dangerouslySetInnerHTML`, no model-driven dynamic import. Asserted by both a deterministic test and a
lint rule.

NFR-4. Rendered output shall use semantic headings and accessible contrast; `Alert` severity shall not
be conveyed by colour alone.

NFR-5. Model-derived values shall be typed as `unknown` in TypeScript until narrowed by the validator.

## Acceptance criteria for the landing page scenario

A1. Requesting the landing page yields a rendered page composed only of registry components.

A2. Every figure on the page matches a value in the grounded context for that request, exactly.

A3. Every alert shown names a defect category present in the grounded context.

A4. No text on the page asserts a pass, fail, or approval outcome.

A5. With the model disabled, the page still renders from the fallback specification and states the
system's purpose.

A6. A crafted model output naming an unapproved component is rejected with `E_UNKNOWN_COMPONENT` and
does not reach the renderer.

A7. A crafted model output containing a script tag, a URL, or an unapproved action identifier is
rejected with the corresponding code.

A8. A crafted model output inventing a defect category is rejected with `E_UNKNOWN_DEFECT_CATEGORY`.

A9. The fallback specification passes all four validation gates.

A10. The generation record for a request contains the context identifier, raw output, outcome,
rejection codes, source, and latency.

## Traceability

BR-1 is satisfied by FR-1, FR-3, FR-4. BR-2 by FR-2, FR-5, FR-6, FR-10, VR-1 to VR-3, VR-10, NFR-3.
BR-3 by FR-6, VR-8. BR-4 by FR-4, FR-6, VR-4 to VR-6. BR-5 by FR-9. BR-6 by FR-7, FR-8, FR-11, NFR-1,
NFR-2. BR-7 by the scope limits of this specification. The internal-access constraint by FR-12.

## Next implementation increment

The smallest useful next step is the UI specification schema and its validator, with deterministic
tests, and no model and no rendering. It proves the control mechanism before anything depends on it.
It is described at the end of the assistant's foundation summary and is not to be started
automatically.
