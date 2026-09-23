# Task 2 execution findings

Status: prerequisite review completed; schema creation blocked by incomplete contract definitions.

Follow-up: the Documents-folder review and a concrete minimal clarification proposal are recorded in `BOARD_DEFECT_INSPECTION_TASK_2_CLARIFICATIONS.md`. The additional sources resolve validation principles but do not supply a complete board landing-page property catalogue or CTA action table. The proposal distinguishes source-backed rules from engineering interpretations; it has not been applied.

Executed the preparation and ambiguity review in `BOARD_DEFECT_INSPECTION_TASK_2_PROMPT.md`. Read `CLAUDE.md`, `docs/business-problem.md`, `docs/architecture.md`, `specs/spec.md`, `specs/model-contracts.md`, and `Documents/Business Requirements Document.docx` (including table contents).

The prompt states: “If required component properties, CTA actions, refusal rules, or constraints are undefined, report the exact contract clarification needed before completing the schema. Do not create a permissive substitute or present an incomplete schema as complete.” It also prohibits changing the model contract in this task.

Accordingly, `specs/schemas/ui-spec.schema.json` was not created. A schema accepting unrestricted component properties would not satisfy this task; closing properties based solely on examples would invent a contract.

## Required engineering clarifications

Sources below are relative to the project root. Engineering owns these definitions; they do not require inventing the BRD's unresolved business values.

| Source | Finding and effect | Exact clarification required |
|---|---|---|
| `specs/model-contracts.md` sections 2–3 | `view` and `components` are explicitly required; `context` and `context.role` are not. Role values occur in an Example column. | State whether context and role are required in a normal response and whether operator/inspector/manager are the complete role enum. |
| `specs/model-contracts.md` sections 3 and 6 | Nine component types are approved, but there is no complete property catalogue. The generic props object is described as optional and component-specific. | For each component, define every allowed prop, its type, requiredness, and whether props may be omitted or empty. Also specify which components permit or require ref and whether props/ref may coexist. |
| `specs/model-contracts.md` section 3, valid example | CTA has only props.label. No action property or action table is defined. | Specify whether CTA is label-only in this slice or has an action. If it has an action, define its exact property location, requiredness, approved identifiers, and any action-specific properties. No board-state mutation is permitted in this slice. |
| `specs/model-contracts.md` section 3, FeatureGrid example | props.items contains FeatureCard examples, without an authoritative child-type restriction or array bounds. | Define allowed item types, requiredness of items, whether empty items are allowed, and bounds if intended. State whether other components may contain children; no Hero/InfoPanel children are currently defined. |
| `specs/model-contracts.md` section 3, refusal shape | The example uses refusal: insufficient_context and components: [], conflicting with the normal minimum of one unless treated as a separate branch. | Confirm the exhaustive refusal reasons, required/allowed refusal fields, whether context is permitted, and that components must be empty. A separate response branch can then preserve the documented refusal. |
| `specs/model-contracts.md` section 8 | Per-component text length bounds are expressly open. Nonempty-string policy is absent. | Decide whether each string has a minimum/maximum length or is intentionally unbounded in v1. Deferral can be documented explicitly; no numeric defaults will be invented. |
| `specs/model-contracts.md` section 3 | ref is a string key, with example metrics and alerts but no key grammar or static catalogue. | State any static reference syntax and per-component restrictions, or explicitly leave availability membership to runtime validation. The example keys must not become an exhaustive enum by inference. |
| `specs/model-contracts.md` section 3 | Closed-object validation requires a complete field definition at each level. | Confirm exhaustive top-level/context/component/props/nested fields so additionalProperties restrictions neither permit unsupported capabilities nor reject intended properties. |

The component catalogue must cover Hero, Heading, Text, FeatureCard, FeatureGrid, CTA, Alert, InfoPanel, and ProgressIndicator. The examples show Hero title/subtitle, Heading text, FeatureCard title, FeatureGrid items, and CTA label. They show ref for InfoPanel, Alert, and ProgressIndicator. Text has no component example. These observations are evidence of intended usage, not a replacement for complete definitions.

## Rules already sufficiently explicit

- Draft 2020-12 and target path `specs/schemas/ui-spec.schema.json` are required by the executed prompt.
- Normal output has view equal to landing and 1–12 top-level components.
- Each component requires type, using the nine case-sensitive v1 names above.
- Model output is structured data, and displayed inspection values are resolved by the Domain Runtime.
- Arbitrary components such as run_query, execute_shell_command, and DispositionControl are outside this slice.
- A refusal is an expected outcome; the application later renders fallback.
- Customer-onboarding identifiers, meta.generated_for, campaign/locale, and ProgressIndicator steps/current are not defined in this board contract and cannot be imported from the tutorial.

## Business and architecture review

The BRD describes a future inspection system with detection, confidence, PASS/FAIL/REVIEW, evidence/history, review, and authorized overrides (FR-001 through FR-012). `specs/spec.md` sections 3 and 8 deliberately narrow the current slice to a read-only landing page with no quality verdict. This difference is a scope boundary, not permission to add board decision fields to UISpec.

The BRD's sections 5, 13–14, 17, and 32 leave KPI targets, taxonomy, severity classification, performance values, and example business rules subject to confirmation. These remain outside this schema task. Quality owns taxonomy and thresholds; Manufacturing owns throughput and operational fallback; Quality/Compliance owns retention. None is needed to define the current UI property catalogue.

`docs/architecture.md` section 9 records a future direction toward an inspector review panel. The current explicit landing-page contract remains the target of Task 2; no new review components were introduced.

Two enforcement statements also need careful interpretation in later work:

- The contract attributes rejection of arbitrary markup/code to schema validation. Ordinary string validation cannot prove user-facing text is safe or semantically correct. A controlled renderer must treat it as text; model evaluations address invented capabilities and implied verdicts.
- `docs/architecture.md` section 5 broadly says rejection renders fallback, whereas `specs/spec.md` section 5 specifically says an unavailable data reference omits that component and logs the issue. This distinction concerns later runtime behaviour and does not justify inventing a static reference catalogue.

## Deferred responsibilities

- Global node counting and serialized byte size; the defined top-level maximum of 12 does not cap a nested tree. No global numerical budgets are currently specified.
- Exact input-context matching and per-request available-key membership.
- Data resolution, missing-reference handling, and fallback rendering.
- Cross-field checks not conveniently represented in the schema; steps/current is not currently a board-contract field pair.
- Authorization, audit recording, model-version recording, and inspection business correctness.
- Model evaluations for invented taxonomy/capabilities and implied quality verdicts in generated text.

## Changes and checks

Created only this findings report during this execution. The prompt and source contracts were not changed. No application code, dependencies, runtime validator, tests, renderer, or model integration was added.

Completed source review, component-vocabulary comparison, response-shape review, CTA-definition review, and BRD/slice alignment review. JSON parsing, Draft 2020-12 meta-schema validation, and schema coverage checks were not run because there is no completed schema artifact to validate.

Next required input: explicit engineering definitions for the gaps above, recorded in the model contract through a separately authorized contract update. Task 2 can then translate those definitions and validate the resulting schema without redesigning the contract.
