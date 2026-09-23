# UI Specification Schema Validation Report

## Created artifact

**File**: `specs/schemas/ui-spec.schema.json`

**Standard**: JSON Schema Draft 2020-12

**Purpose**: Machine-checkable formalization of the UISpec model contract from `specs/model-contracts.md`, implementing Gate 1 structural validation.

---

## Validation results

### 1. Schema syntax and structure

✅ JSON is syntactically valid per JSON Schema Draft 2020-12

✅ Top-level structure complete:
- `specVersion` (required, const "1.0")
- `page` (required, const "landing")
- `contextId` (required, string)
- `blocks` (required, array 1–12 items)

✅ All top-level properties have `additionalProperties: false`

### 2. Component vocabulary completeness

All nine approved components are represented as discriminated unions with named block definitions:

✅ `Hero` — with required `title` and optional `eyebrow`, `subtitle`, `primaryAction`
✅ `Heading` — with required `level` (2 or 3) and `text`
✅ `Text` — with required `text` and optional `tone`
✅ `FeatureGrid` — with required `columns` (2 or 3) and `items` array (2–6 FeatureCard entries)
✅ `FeatureCard` — with required `title`, `body` and optional `icon`, `capabilityId`
✅ `CTA` — with required `label`, `action` and optional `variant`
✅ `Alert` — with required `severity`, `title`, `body` and optional `defectCategoryId`, `alertId`
✅ `InfoPanel` — with required `title` and `rows` (1–8 InfoPanelRow entries)
✅ `ProgressIndicator` — with required `metricId`, `label`, `value` and optional `caption`

### 3. Approved identifiers and enums

**CTA actions** — all five approved actions present:
- `view-inspection-queue`
- `view-defect-reports`
- `view-ingest-activity`
- `open-documentation`
- `contact-support`

**Defect categories** — all six approved categories present:
- `solder-bridge`
- `missing-component`
- `misaligned-component`
- `insufficient-solder`
- `foreign-material`
- `surface-scratch`

**Icon values** (FeatureCard):
- `inspection`, `defect`, `report`, `image`, `trend`

**Alert severity** (Alert, InfoPanel rows not constrained here):
- `info`, `warning`, `critical`

**Text tone** (Text):
- `default`, `muted`

**Variant** (CTA):
- `primary`, `secondary`

**Heading level** (Heading):
- `2`, `3`

**FeatureGrid columns**:
- `2`, `3`

### 4. Structural limits

✅ Block count: 1–12 (spec.md: "at most 12 top-level blocks")
✅ FeatureGrid items: 2–6 (spec.md: "at most 6 items in a FeatureGrid")
✅ InfoPanel rows: 1–8 (spec.md: "at most 8 rows in an InfoPanel")
✅ Nesting depth: exactly two (FeatureGrid containing FeatureCard), enforced by schema structure

### 5. String length constraints

All character limits from model-contracts.md are enforced:

- `HeroProps.eyebrow`: ≤ 40
- `HeroProps.title`: ≤ 80
- `HeroProps.subtitle`: ≤ 200
- `HeadingProps.text`: ≤ 80
- `TextProps.text`: ≤ 500
- `FeatureCardProps.title`: ≤ 60
- `FeatureCardProps.body`: ≤ 240
- `CtaProps.label`: ≤ 40
- `AlertProps.title`: ≤ 80
- `AlertProps.body`: ≤ 300
- `InfoPanelProps.title`: ≤ 60
- `InfoPanelRow.label`: ≤ 40
- `ProgressIndicatorProps.label`: ≤ 40
- `ProgressIndicatorProps.caption`: ≤ 120

### 6. Arbitrary component type prevention

✅ Block discriminator uses `oneOf` with nine explicit component cases
✅ Each case specifies `component` with `const` matching exactly one approved name
✅ No fallback, wildcard, or additional block types allowed by schema
✅ An unapproved component name will fail validation

### 7. Example validation

The valid output example from model-contracts.md (Appendix) passes structural validation:
- specVersion: "1.0" ✅
- page: "landing" ✅
- contextId present ✅
- blocks: 4 blocks (within 1–12) ✅
- block types: Hero, Alert, InfoPanel, CTA (all registered) ✅
- alert defectCategoryId: "solder-bridge" (registered) ✅
- CTA action: "view-defect-reports" (registered) ✅
- InfoPanel rows: 2 rows (within 1–8) ✅

---

## Contract ambiguities and schema notes

### Ambiguity 1: Total text limit (4000 characters)

**Contract state**: Spec.md defines a system-wide 4000-character total-text limit across all blocks.

**Schema capability**: JSON Schema cannot express cross-field aggregation or sums. There is no way to constrain "all string fields summed ≤ 4000".

**Resolution**: This limit must be validated at runtime during Gate 1 (structural validation). The schema enforces individual string limits; the validator enforces the aggregate.

**Impact**: Medium. The schema alone cannot guarantee compliance. The validator is responsible.

---

### Ambiguity 2: Metric value format and exact-match copying

**Contract state**: InfoPanel rows must display metric values that match the context Metric.value exactly, character for character. ProgressIndicator.value must be the numeric form of a context metric whose unit is "%".

**Schema capability**: The schema can require `value` to be a string (InfoPanel) or number (ProgressIndicator) with length/range limits. It cannot validate that the value matches context data or that units are present in the context.

**Resolution**: These checks must be performed at runtime during Gate 3 (grounding validation). The schema ensures type correctness and bounds; the validator ensures grounding.

**Impact**: High. Metric value matching is a critical control (prevents fabrication). It is not schema-expressible; it is a runtime responsibility.

---

### Ambiguity 3: Identifier existence in grounded context

**Contract state**: All identifier references—`primaryAction`, `capabilityId`, `defectCategoryId`, `alertId`, `metricId`—must exist in the corresponding collection in the grounded context. The schema hardcodes approved action and defect category enums, but these are also validated for presence in the request context.

**Schema capability**: The schema can enumerate approved actions and defect categories (closed vocabularies). It cannot validate that an identifier exists in a runtime-supplied context object.

**Resolution**: Enum values (actions, categories) are validated by the schema. Existence in the request's context is validated at runtime during Gate 3 (grounding). Metric/capability/alert IDs are opaque strings in the schema; their existence is a runtime check.

**Impact**: Medium to high depending on component. Defect category and action presence are partially schema-checked (value set); complete grounding is runtime-checked.

---

### Ambiguity 4: ProgressIndicator metric unit constraint

**Contract state**: ProgressIndicator.value must be 0–100 and must equal the numeric form of a context Metric whose unit is "%".

**Schema capability**: The schema enforces the 0–100 range and that value is a number. It cannot express the dependency on a metric's unit field.

**Resolution**: The unit coupling (metric must have unit "%") must be validated at runtime during Gate 3 (grounding). The schema ensures type and range.

**Impact**: Medium. The schema prevents out-of-range values; the validator must confirm the metric has unit "%".

---

### Ambiguity 5: Text policy and decision language (Gate 4)

**Contract state**: Text fields must not contain markup, URLs, emails, code-like content, or decision language (pass/fail/approved/rejected, etc.).

**Schema capability**: JSON Schema has no built-in text policy engine. Individual string length is enforced; content validation is not.

**Resolution**: All text policy checks are runtime validations during Gate 4 (policy). The schema enforces structure and bounds.

**Impact**: High. Text policy is critical for safety (BR-3). It is entirely a runtime responsibility.

---

### Ambiguity 6: FeatureCard placement (top-level vs. nested)

**Contract state**: FeatureCard may appear as a top-level block or as a child inside FeatureGrid, but never elsewhere.

**Schema capability**: The discriminated union in Block allows FeatureCardBlock as a top-level alternative. FeatureGrid contains FeatureCardProps (not FeatureCardBlock) as items, so nesting is structurally distinct.

**Resolution**: The schema achieves this through structure: top-level blocks use Block discriminator (which includes FeatureCardBlock); FeatureGrid.items directly reference FeatureCardProps, not Block. The schema prevents FeatureCard nesting anywhere else.

**Impact**: Low. The schema correctly expresses the constraint.

---

### Ambiguity 7: contextId matching

**Contract state**: UISpec.contextId must equal the contextId of the request's grounded context.

**Schema capability**: The schema can require contextId to be a non-empty string. It cannot validate equality with an external context object.

**Resolution**: Exact matching is validated at runtime during Gate 3 (grounding validation).

**Impact**: Medium. This is a critical control (prevents stale or mismatched contexts). It is runtime-validated.

---

## Gate assignment summary

The schema implements **Gate 1 (structural validation)** comprehensively:
- JSON parsing ✅
- Schema conformance ✅
- specVersion recognition ✅
- Block count, nesting depth, string length ✅
- Component name validation ✅
- Action and defect category enum validation ✅

Gates 2–4 are performed at runtime:

- **Gate 2 (registry)**: Component prop validation beyond enum values (type, unknown props). Partially in schema for enum fields.
- **Gate 3 (grounding)**: Metric/alert/capability/action existence, metric value matching, contextId matching, identifier validation.
- **Gate 4 (policy)**: Text length beyond schema bounds, markup/URL/code/decision-language detection.

---

## Schema coverage matrix

| Requirement | Schema | Runtime |
|--|--|--|
| JSON syntax | ✅ | — |
| specVersion validation | ✅ | — |
| page validation | ✅ | — |
| Block count (1–12) | ✅ | — |
| Component names (9 approved) | ✅ | — |
| Nesting depth (≤ 2) | ✅ | — |
| String length constraints | ✅ | — |
| Action enum (5 approved) | ✅ | Gate 3 existence |
| Defect category enum (6 approved) | ✅ | Gate 3 existence |
| Metric/alert/capability/action existence | — | ✅ Gate 3 |
| Metric value exact matching | — | ✅ Gate 3 |
| contextId matching | — | ✅ Gate 3 |
| Total text limit (4000 chars) | — | ✅ Gate 1 aggregate |
| Text policy (no markup/URLs/code) | — | ✅ Gate 4 |
| Decision language detection | — | ✅ Gate 4 |
| ProgressIndicator unit coupling | — | ✅ Gate 3 |

---

## Conclusion

The schema is **syntactically valid**, **complete in component coverage**, and **correctly enforces all schema-expressible constraints**. It prevents arbitrary components, enforces closure of the vocabulary, and provides a clear, type-safe structure for Gate 1 validation.

Seven contract ambiguities were identified—all are inherent to the boundary between static schema validation and runtime semantic validation. All are documented in the schema's `description` fields and do not represent schema defects; they represent the correct division of labour between structural and semantic gates.

**No schema redesign is required.** The schema accurately formalizes the structural portion of the contract. Runtime validators will enforce Gate 3 (grounding) and Gate 4 (policy) constraints using the rejection codes defined in model-contracts.md.
