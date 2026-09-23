```text
Proceed with the proposed next smallest task.

Formalise the UISpec model contract for the AI-Based Automated Board Defect Inspection System as a machine-checkable JSON Schema.

Create:
specs/schemas/ui-spec.schema.json

Use JSON Schema Draft 2020-12.

The schema must represent the contract currently defined in:
specs/model-contracts.md

Align with the Business Requirements Document and the current internal, read-only landing-page scope.

Do not redesign the contract or introduce new capabilities.

Before writing the schema:

1. Read:
   - CLAUDE.md
   - Documents/Business Requirements Document.docx
   - docs/business-problem.md
   - docs/architecture.md
   - specs/spec.md
   - specs/model-contracts.md

2. Identify any ambiguity or contradiction between the BRD, the current implementation scope, the prose contract, and what can be represented in JSON Schema.

3. If an ambiguity affects the schema design, document it clearly rather than silently inventing a rule.

4. If required component properties, CTA actions, refusal rules, or constraints are undefined, report the exact contract clarification needed before completing the schema. Do not create a permissive substitute or present an incomplete schema as complete.

The schema must cover:

- UISpec top-level structure
- The exact view value: "landing"
- Context structure and role constraints as defined by the contract
- Required fields
- All approved v1 component types:
  - Hero
  - Heading
  - Text
  - FeatureCard
  - FeatureGrid
  - CTA
  - Alert
  - InfoPanel
  - ProgressIndicator
- Exact case-sensitive component type names
- Component-specific properties
- String length constraints where defined
- Enum constraints where defined
- Required properties
- Additional-property restrictions
- FeatureGrid props.items and child rules
- Hero child/container rules if defined by the contract
- InfoPanel child/container rules if defined by the contract
- CTA action enum/table if defined; otherwise report the missing definition
- Data reference fields and their defined structural constraints
- The normal response components array limit of 1–12 entries
- The documented refusal response, including its empty components array
- Separation between normal and refusal response constraints
- Node-count limits where JSON Schema can express them
- Array size limits where applicable

Preserve the board inspection boundaries:

- The model composes the UI using approved components and user-facing text.
- The model supplies data reference keys; the Domain Runtime resolves actual inspection data values.
- Do not treat example metric or alert keys as an exhaustive allow-list unless explicitly defined.
- Do not add components or actions that produce, display, or imply a final PASS/FAIL or quality approval decision in this slice.
- Do not add human review, override, or board disposition capabilities.
- Do not convert the BRD's illustrative defect taxonomy, suggested severity categories, sample values, or TBD thresholds into approved schema constraints.
- Do not import customer-onboarding page identifiers, actions, or context fields.
- Do not add meta.generated_for, steps, current, or children unless defined by the board inspection contract.

Apply the updated guide's clarifications where supported by the existing contract:

- Restrict Hero children to the explicitly approved types and limits.
- Apply nonempty-string constraints where specified; report undefined constraints.
- Reject undeclared properties using additionalProperties restrictions.
- Keep exact input-context matching as a later validator responsibility.
- If ProgressIndicator defines steps/current, represent its defined static bounds and document the current < len(steps) relationship for later validation.
- Do not introduce campaign or locale fields without a contract definition.

Use JSON Schema capabilities such as:

- $schema
- $defs
- $ref
- type
- enum
- const
- required
- additionalProperties
- minLength
- maxLength
- minItems
- maxItems
- minimum / maximum where defined
- oneOf / anyOf where appropriate

Document rules that require later runtime validation, including:

- Total node count across nested components
- Serialized output size
- Cross-field relationships not conveniently expressible in JSON Schema
- Exact matching to input context
- Membership in available metric, alert, and panel keys
- Data reference resolution
- Authorization and business decision correctness

Do not claim that schema validation can detect invented capabilities or implied quality verdicts in generated text. These require later model evaluations.

Do NOT add application code yet.
Do NOT add runtime dependencies.
Do NOT build the React application.
Do NOT build the FastAPI application.
Do NOT implement the runtime validator or renderer.
Do NOT integrate a UI-generation or defect-detection model.
Do NOT create authentication.
Do NOT create camera integration or image processing.
Do NOT create PLC/MES integration.
Do NOT create review, override, or disposition workflows.
Do NOT create document processing or risk functionality.
Do NOT change the model contract or unrelated files as part of this task.

After creating the schema:

1. Validate that the schema itself is syntactically valid JSON.
2. Check Draft 2020-12 meta-schema validity using available development tooling, and report any verification limitation.
3. Check that every approved v1 component in the model contract is represented.
4. Check that every allowed CTA action is represented.
5. Check that the schema does not accidentally permit arbitrary component types or properties, including inside nested structures.
6. Check that normal and refusal responses are represented correctly.
7. Check that data references remain distinct from inspection data values.
8. Report any contract ambiguity discovered and any rules deferred to runtime validation or model evaluation.
9. Summarize exactly what was created and which checks were performed.

Stop after this task.
Do not proceed to the validator or tests until explicitly instructed.
```
