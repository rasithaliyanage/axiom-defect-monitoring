# Task 2 — document review and proposed clarifications

The Documents folder was searched for the missing contract definitions, including extracted text from all seven Word documents and all four PDFs, and the Markdown architecture, foundation, workflow, backlog, and implementation material. The current repository contract remains the landing-page contract in `../specs/model-contracts.md`.

## Clarifications supported by the documents

| Source | What it establishes | Application to this task |
|---|---|---|
| `Customer_Onboarding_Task_2_Beginner_Guide_Updated.docx.pdf`, pages 3–6 | Task 2 translates an existing contract; component props must be constrained; approved actions come from the contract's action table. | Do not infer a complete property catalogue or board-specific action table from tutorial examples. |
| Same guide, pages 11–12 | Close objects to undeclared properties; reject executable component types; nonempty-string clarification; runtime checks cover total nodes, serialized size, and context equality. | Closed objects and nonempty strings are suitable clarification principles. Exact field definitions still need to be stated for this repository. |
| Same guide, page 12 | Onboarding Hero children are CTA/Text; generated_for uses ContextPayload; ProgressIndicator has a current/steps relationship. | These are explicitly onboarding-contract details. The board contract has no children/generated_for/steps/current definition, and its ProgressIndicator example uses ref. Do not copy these fields into it. |
| `Customer_Onboarding_Task_1_Beginner_Guide.docx`, sections 6 and 9–10 | The nine tutorial component names and an onboarding action example. | Supports the shared component vocabulary, but start_onboarding is not a board inspection action. No board navigation table is supplied. |
| `03 - Customer_Onboarding_Generative_UI_First_Implementation_Beginner_Guide.docx`, sections 3–4 | Illustrative onboarding landing-page JSON, with hero, feature grid, and start_onboarding CTA. | Provides the learning pattern; it is not the current board response structure. |
| `02-AI_Native_Engineering_Architecture_Beginner_Guide.docx.pdf`, section 10 | States that the exact schema will be designed later. | The example is not a complete schema definition. |
| `AI_NATIVE_GENERATIVE_UI_FIRST_IMPLEMENTATION.md`, section 9 and Appendix A | Proposes an inspector review view and a different component catalogue, including BoardSummary, ImageCompare, and ConfidenceBadge; explicitly excludes ProgressIndicator. | Conflicts with the currently directed landing-page slice. Importing this catalogue would redesign the contract and violate the same Task 2 prompt. |
| `AI_NATIVE_TASK_1_PROJECT_FOUNDATION.md`, document reference table | Identifies model-contracts.md and ui-contract.md as intended engineering artifacts. | Does not supply the missing nine-component property definitions. |
| `Proposed Project Structure - Board Defect Inspection (AI-Native)-Vinod.pdf`, sections 3 and 6 | Describes locations and ownership of UI contracts and schemas. | Defines responsibility and file organization, not component props or action identifiers. |
| `Business Requirements Document.docx`, sections 13–17, 24, 27–32 | Defines business intentions while leaving taxonomy, thresholds, reporting details, and review policy subject to confirmation. | These values cannot resolve presentation field definitions or become approved action enums. |

## Concrete engineering proposal requiring confirmation

The following would resolve the remaining ambiguities with minimal additions. These are **proposed interpretations**, not definitions found verbatim in the documents, and have not been applied to the model contract or a schema.

1. **Normal response:** require view and components as already specified. Keep context optional because it is not marked required; if present, require role and restrict it to operator, inspector, or manager. Use view = landing and 1–12 top-level components. The role requiredness and exhaustive enum are proposed clarifications.
2. **Refusal response:** require exactly view = landing, refusal = insufficient_context, and components = []; do not permit context or other fields. This promotes the documented refusal example to the exhaustive v1 refusal definition.
3. **Component envelope:** type is required; props and ref remain optional as the existing shared contract states. If present, ref is a nonempty string. Its membership in available keys is a runtime check. Do not invent a static key catalogue or restrict ref to only the three components used in examples.
4. **Closed fields:** additionalProperties is false for every response, context, component, and props object. Components have only type, props, and ref. No generic children field is introduced.
5. **Strings:** use nonempty strings, following the updated guide's clarification. Do not invent maximum lengths; retain the current contract's explicit deferral of those bounds. This does not imply a whitespace-only string is semantically acceptable; no whitespace rule is currently defined.
6. **Component-specific props:** use the table below. All listed properties remain optional; the current contract does not make any component prop required. An omitted or empty props object is allowed. Requiring nonempty component content would be a separate contract change.
7. **FeatureGrid:** if props.items is present, it is an array containing only FeatureCard components. Empty arrays are allowed and no maximum is invented. No other nested containers are added. This makes the example's child type explicit while leaving undefined cardinality limits unbounded.
8. **CTA:** keep props.label only. No action, URL, handler, or route field is accepted, because no approved board action identifier exists in the documents. This means the schema authorizes no model-selected action. It does not establish working navigation; that remains undefined and must not be presented as implemented. If working model-selected navigation is required now, an action table is still needed instead of this option.
9. **Version recording:** keep model-version recording as an application responsibility; do not add an output field absent from the contract.

| Component type | Proposed allowed props | Basis and limit |
|---|---|---|
| Hero | title, subtitle: nonempty strings | Existing board example; treat these as exhaustive v1 fields. |
| Heading | text: nonempty string | Existing board example. |
| Text | text: nonempty string | Engineering interpretation of the approved Text component and the contract's reference to props.text; no explicit Text example exists. |
| FeatureCard | title: nonempty string | Existing board example. |
| FeatureGrid | items: array of FeatureCard | Existing board example, clarified as the permitted child type. |
| CTA | label: nonempty string | Existing board example; no action table or action field. |
| Alert | none (props may only be an empty object) | Board example uses ref; no props fields are defined. |
| InfoPanel | none (props may only be an empty object) | Board example uses ref; no props fields are defined. |
| ProgressIndicator | none (props may only be an empty object) | Board example uses ref; steps/current are not imported. |

This proposal intentionally does not claim to be a complete production UI design. It is a precise, minimal formalisation option for the currently documented v1 examples and optional-property contract. It preserves the existing valid and refusal examples, admits all nine types, and supplies no board decisions or new business capabilities.

## Rerun result

The same Task 2 prompt was reconsidered against these additional sources. It still cannot be completed from existing definitions alone: it forbids inventing missing contract rules and changing the model contract. No schema was generated and no schema validation was claimed.

The next step is to confirm or amend the concrete proposal above, then record the accepted clarifications in the model contract and generate `specs/schemas/ui-spec.schema.json`. This is an explicit contract clarification step, not a business-taxonomy or threshold decision.
