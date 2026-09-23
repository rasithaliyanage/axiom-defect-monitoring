# UISpec schema notes — current version 1.0

Task 3 uses `specs/schemas/ui-spec.schema.json` as structural authority. The user
confirmed that the updated version 1.0 contract supersedes the former
`view/components/type/ref` contract and its refusal example. The current schema
has closed component props, required fields and per-component bounds. It is no
longer the partial schema described in the historical notes below.

## Current structural and runtime responsibilities

- Required envelope: `specVersion: "1.0"`, `page: "landing"`, `contextId`, and
  `blocks` with 1–12 entries. Each block requires `component` and `props`.
- All nine components are represented. FeatureGrid is the only component
  nesting construct, containing 2–6 FeatureCard **props objects**, not blocks.
  InfoPanel has 1–8 metric rows. Hero and InfoPanel do not contain child blocks.
- CTA actions have the five approved enum values. Hero.primaryAction is a
  string structurally and is checked against the same action set at runtime.
- No v1 refusal shape is defined. Old refusal objects are rejected rather than
  silently converted or treated as normal pages.
- ProgressIndicator requires metricId, label and numeric value in 0–100; its
  context metric must use `%` and match numerically. InfoPanel strings are
  compared verbatim. No progress steps/current fields exist.
- Context equality, identifier membership, metric matching, total text and
  deterministic text-policy checks are implemented by the local Task 3
  validator. Read `services/domain/README.md` for exact interpretations and
  semantic limitations. Passing deterministic checks is not a semantic proof.
- The alternative `specs/ui-spec.schema.json` differs in identifier, unit and
  value bounds and is not loaded by this task. Both original schemas are
  preserved; their reconciliation remains documentation/contract follow-up.
- InfoPanelRow.value's current schema description says there is no maximum,
  but the keyword `maxLength: 256` is present. The validator follows the actual
  schema keyword. The contradiction is recorded rather than silently edited.

Task 3 verifies the selected schema against the Draft 2020-12 meta-schema and
the updated contract example. No new total-node or serialized-byte limit is
introduced. `specs/TASK-3-READINESS.md` retains the original readiness findings
and records the subsequent user decision.

## Historical review of the superseded partial schema

Everything below documents the earlier contract and must not be used as the
current v1 structural definition. Its statements about missing props, open
objects, absent action enums and old field names have been superseded.

The Draft 2020-12 schema in `ui-spec.schema.json` formalises only the defined structural subset of `../model-contracts.md`. A partial schema was explicitly authorised after the gaps below were identified. It does not amend the prose contract or establish new component capabilities.

## Represented rules

- A normal page requires `view: "landing"` and `components`, with 1–12 top-level entries.
- Every top-level component requires `type`, restricted to all nine approved names: Hero, Heading, Text, FeatureCard, FeatureGrid, CTA, Alert, InfoPanel and ProgressIndicator.
- Component `props` is an optional object and `ref` is an optional string.
- When supplied, `context` is an object and `role` is a string.
- A separate refusal branch represents the documented shape: `view: "landing"`, `refusal: "insufficient_context"`, and an empty `components` array. This accounts for the explicit refusal exception to the normal 1–12 limit.
- `additionalProperties: false` closes the page, refusal, context and component envelopes to their documented fields, as requested. The prose itself does not explicitly state an unknown-field policy. Component properties remain open because no exhaustive property sets are defined.

## Unresolved rules and representation choices

| Area | Source gap or ambiguity | Partial schema treatment |
|---|---|---|
| Component-specific properties | Section 3 gives example properties, not property definitions or exhaustive allowed sets. Text has no example; several components have only references. | Only object typing for `props`; no invented property names, required properties or component-specific reference requirements. |
| String lengths | Section 8 explicitly defers text-length bounds. No other string bounds are supplied. | No `minLength` or `maxLength`; empty strings are not excluded without a contract rule. |
| Context | `context` and `role` are not explicitly marked required. | Both remain optional; an empty context object is accepted. This is a permissive treatment of missing requiredness, not a resolved contract decision. |
| Role vocabulary | Input roles are labelled examples. | No role enum is inferred. |
| FeatureGrid children | The example has `props.items` containing FeatureCard nodes, but defines no mandatory items field, exclusive child type, or size bounds. | No child schema or items limits are inferred from the example. |
| Hero and InfoPanel containers | No child fields, permitted children or nesting rules are defined. | No container rules are invented. |
| CTA actions | No action property, enum or action table exists. The example CTA has only a label. | No action enum can be checked or encoded. Open props do not establish authorisation for any action. |
| Node count and depth | The only numeric limit is 1–12 entries in the top-level components array. No total-tree count or depth limit is defined. | Enforce only the top-level array limit. `maxItems` does not count descendants; an aggregate recursive count would need a separate approach if introduced later. |
| Refusals | Only one refusal shape and reason are documented; extensibility and optional context are unspecified. | Encode exactly the documented refusal shape. Other reasons and context on refusals remain unsupported pending clarification. |
| Reference keys | No key grammar, static key enum or length bounds are given; available keys arrive through runtime context. | String typing only. Key membership and whether a string actually names data remain outside this schema. |
| Markup, code and data values | Prose attributes structural rejection to validation, but no text syntax restrictions or complete property schemas are defined. | JSON shape alone cannot enforce these prohibitions inside open props or arbitrary strings. No speculative pattern or keyword blacklist is added. |

## Cross-document discrepancies found on rereview

The updated `CLAUDE.md` and `docs/architecture.md` do not supply the missing definitions in `specs/model-contracts.md`. The schema continues to use the model contract as the requested source of truth. The following discrepancies remain unresolved:

- **Field names:** architecture describes a block list with a `component` discriminator; the model contract defines `components` entries with `type`. The schema retains `components` and `type`.
- **Data ownership:** architecture Gate 3 and AD-7 allow the model to copy metric values from grounded context. Model-contract sections 2–3 and system requirement FR-04 allow references only and withhold metric values from the model. No metric-value fields are added to the schema.
- **Rejection and repair:** architecture permits omission of unknown blocks and one repair attempt; `CLAUDE.md` also requires repair. System requirement FR-03 and the model contract require rejection rather than interpretation, and FR-03 explicitly prohibits repair and partial rendering. A static output schema cannot settle this runtime behaviour conflict.
- **Missing validation definitions:** architecture refers to string-length, nesting-depth and text-policy limits, approved props, and rejection codes allegedly defined in the model contract. Those definitions are still absent; architecture supplies no numeric bounds or property catalogue to encode.
- **Schema location:** architecture and `CLAUDE.md` reference `specs/ui-spec.schema.json`. This task explicitly requests `specs/schemas/ui-spec.schema.json`, which remains the only schema location used here.
- **Task scope:** `CLAUDE.md` calls for coordinated contract, test and eval changes for schema changes. The explicit task limits this increment to schema formalisation and forbids proceeding to tests. No contract rewrite, tests or eval changes are included.

`Documents/BOARD_DEFECT_INSPECTION_TASK_2_CLARIFICATIONS.md` contains a proposed property catalogue, nonempty-string rules and FeatureCard-only grid children, but explicitly says these interpretations are unapplied and require confirmation. They are not treated as an amendment to the authoritative model contract. Completing the requested strict schema still requires those decisions to be recorded in that contract, including an approved CTA action definition if actions are intended.

## Enforcement limitations

The component enum has no unrestricted alternative: arbitrary types cannot appear as entries in the top-level `components` array. However, open `props` can contain arbitrary nested objects, including objects that resemble components with unknown types. Consequently this partial schema cannot guarantee registry membership throughout a component tree, child validity, valid CTA actions, or exclusion of embedded data values. Schema acceptance must not be treated as approval to render arbitrary props or nested content.

Generated claims about capabilities and quality verdicts remain evaluation concerns, as the contract states. Model-version traceability is an application responsibility; the contract defines no model-version field in UISpec, so none is added.

No validator implementation, tests, runtime dependencies or application code are part of this change. Completing the enforcement boundary requires clarified contract rules before further schema work.
