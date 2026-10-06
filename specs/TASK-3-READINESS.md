# Task 3 readiness review

Status: historical readiness review, followed by local Task 3 implementation. The user subsequently confirmed that version 1.0 supersedes the old refusal and ProgressIndicator requirements. The current validator uses `specs/schemas/ui-spec.schema.json`; implementation choices for diagnostics, total-text counting, numeric parsing and missing-alert rejection are recorded in `services/domain/README.md`. Deterministic policy limitations remain explicit. Neither schema nor the normative model contract was rewritten. No commit or push was made.

The remaining content records the pre-implementation findings, not a statement that the old partial schema is still the current contract. The differing schema copies and unreadable Git HEAD remain separate limitations.

## Schema-path decision, resolved after Task 4

The "Schema differences" row below asked for an explicit decision. It has been taken:
`specs/schemas/ui-spec.schema.json` is the single authority, because it is the file
`services/domain/validator.py` loads. The normative references in `CLAUDE.md`, `README.md`,
`docs/architecture.md`, `specs/spec.md` and `specs/model-contracts.md` were corrected to point at it.

`specs/ui-spec.schema.json` is retained, unloaded, and now carries `"deprecated": true` plus a
`$comment` stating that it is superseded. **The two were not merged** and neither one's constraints
were altered. The comparison table below therefore still describes real differences between the two
files; it is a record, not an open action. Git HEAD is now readable (`3810dc0`, branch `wushan`).

## Definitions now present

The updated `model-contracts.md` defines the `specVersion/page/contextId/blocks` response, nine components with exhaustive props, five actions, six defect category identifiers, GroundedContext, metric copying, percentage progress and stable rejection codes. `spec.md` defines the 4000-character total-text limit. These earlier missing definitions are no longer reported as absent.

The request names `schemas/ui-spec.schema.json` as structural authority. It closes component props and represents all nine components and five CTA actions. Hero and InfoPanel are not component containers. FeatureGrid items contain FeatureCard props directly, not component envelopes. No total-node or serialized-byte maximum has been introduced.

## Decisions required before implementation

| Issue | Current evidence | Required reconciliation |
|---|---|---|
| Refusal | The prompt requires accepting `{"view":"landing","refusal":"insufficient_context","components":[]}`. The updated contract and both schemas require a different envelope and define no refusal variant. | Confirm whether the updated contract supersedes this required valid test, or explicitly define a new refusal contract. Do not silently accept output outside the schema. |
| ProgressIndicator | The prompt requires the old `ref` form. The updated contract requires `props.metricId`, `props.label`, and numeric `props.value` matched to a percentage metric. | Confirm that the new progress contract supersedes the old prompt case. No current/steps fields are needed. |
| Schema differences | The contract references `specs/ui-spec.schema.json`; the task selects `specs/schemas/ui-spec.schema.json`. They impose different accepted values. | Align references and schemas through an explicit decision; do not combine their constraints. The task-selected file would be used for this task once conflicts are resolved. |
| Stale notes | `schemas/ui-spec.schema-notes.md` describes the former partial contract, open props and refusal branch. | Replace historical assertions with notes for the approved current contract. The earlier clarification proposal is also historical and unapplied. |
| Missing alert diagnostic | Alert identifiers must exist in context, but the rejection-code table has no condition/code for a missing alert identifier. | Define the intended stable code instead of repurposing metric/category codes. |
| Validation result | Codes exist, but the task requires an agreed result shape which no current document supplies. | Define status, diagnostic fields, paths, ordering, and whether invalid supplied context is a caller error or validation result. |
| Aggregate text | `spec.md` says 4000 characters of total text; the schema report describes summing string fields. | Specify whether IDs, enums, metadata, metric strings and numeric progress representations count, and the character-count convention. |
| Numeric metric conversion | ProgressIndicator equals the numeric form of a metric string. Accepted string formats are not specified. | Define parsing for whitespace, exponent notation, thousands separators and invalid/non-finite numbers without rounding or unit conversion. |
| Semantic policy | The updated contract requires detection of all implied verdicts and capability claims; the prompt correctly says keyword filters cannot guarantee this. | State the deterministic policy coverage and how semantic limitations affect approval. Do not claim a heuristic completely enforces unrestricted natural-language meaning. |

Concrete differences between the two schemas:

| Constraint | `specs/ui-spec.schema.json` | `specs/schemas/ui-spec.schema.json` |
|---|---|---|
| contextId maximum | 128 | 256 |
| Generic reference ID | Maximum 64; lowercase identifier pattern | Maximum 256; no equivalent pattern |
| InfoPanel value maximum | 40 | 256 |
| InfoPanel unit maximum | 12 | 32 |
| Hero primaryAction | Approved action enum | Nonempty bounded string; approval checked at runtime |
| Alert defectCategoryId | Identifier syntax; approval checked at runtime | Six-category enum |

The requested schema's InfoPanel value description also says there is no schema-level maximum while its `maxLength` is 256. This is a documentation/constraint contradiction to resolve.

## Resolved or non-blocking distinctions

- The current system specification, model contract and architecture now agree on one model repair attempt in orchestration. A pure validator can reject without mutating input or invoking a model; no repair implementation is required for Task 3.
- The updated contract expressly permits copied metric values and numeric percentage progress. This is no longer a disagreement among those updated documents, although the pasted prompt and old notes retain the previous reference-only design.
- The architecture's renderer omission behaviour belongs to Task 4. It does not authorise the Task 3 validator to remove invalid blocks and accept the remainder.
- No 30-node limit, 8 KiB limit, onboarding context fields, URL-bearing props, or URL host allow-list should be introduced.
- BRD examples and TBD manufacturing targets remain separate from the explicit identifier vocabulary in the updated model contract.

## Verification and Git state

Both schema files parse as JSON. The task-selected schema declares Draft 2020-12 and has the nine component branches and five approved CTA action values. This is a syntax/coverage inspection, not meta-schema validation or executed instance tests. No validation library was installed and no test suite was run because the readiness gate failed.

Branch reported by Git: `wushan`. HEAD resolves textually to `443221d7d7905a16e542884ec5a8f7fe4f7e56be`, but `git cat-file -t HEAD` cannot read its object and `git status --short` fails with `fatal: bad object HEAD`. Diff commands produced no output; that cannot establish a clean worktree while HEAD is unreadable. Git data has not been repaired or modified. This Git issue is separate from the contract conflicts and does not itself prohibit local file work.

The only file created by this review is this report. Existing schemas, contracts and user work are preserved. The next checkpoint is an explicit reconciliation of the prompt and current contract, followed by validator implementation and actual test results. No Task 4 work is authorised by this review.
